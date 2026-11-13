from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import User, OTPChallenge
from ..schemas import RegisterRequest, VerifyRequest
from ..security import hash_password, hash_otp, create_access_token
from ..services.otp_service import create_challenge, dispatch_demo

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(409, "Email already registered")
    user = User(name=payload.name, email=payload.email, phone=payload.phone,
                password_hash=hash_password(payload.password), skills=payload.skills,
                experience=payload.experience, qualification=payload.qualification, is_active=False)
    db.add(user)
    await db.flush()
    try:
        code, values = create_challenge(payload.email, payload.channel.lower())
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    db.add(OTPChallenge(**values))
    await db.commit()
    dispatch_demo(payload.channel.lower(), payload.email, code)
    return {"message": "Registration staged. OTP generated; check server console in demo mode.",
            "email": payload.email, "channel": payload.channel.lower()}

@router.post("/verify-2fa")
async def verify_2fa(payload: VerifyRequest, db: AsyncSession = Depends(get_db)):
    challenge = await db.scalar(select(OTPChallenge).where(
        OTPChallenge.email == payload.email, OTPChallenge.channel == payload.channel.lower(),
        OTPChallenge.verified == False).order_by(OTPChallenge.id.desc()))
    if not challenge or challenge.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP challenge missing or expired")
    if challenge.otp_hash != hash_otp(payload.otp):
        raise HTTPException(400, "Invalid OTP")
    challenge.verified = True
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = True
    await db.commit()
    return {"message": "Account verified", "access_token": create_access_token(user.email),
            "token_type": "bearer", "redirect_url": "/dashboard/student"}
