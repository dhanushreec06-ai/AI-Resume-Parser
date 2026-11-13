import jwt, os
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import User
from ..schemas import ProfileUpdate

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])
SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_DEMO_SECRET_BEFORE_DEPLOYMENT")

async def current_user(authorization: str = Header(default=""), db: AsyncSession = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Bearer token required")
    try:
        email = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])["sub"]
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
    user = await db.scalar(select(User).where(User.email == email, User.is_active == True))
    if not user:
        raise HTTPException(401, "Active user not found")
    return user

@router.get("")
async def get_profile(user: User = Depends(current_user)):
    return {"name": user.name, "email": user.email, "phone": user.phone,
            "skills": user.skills, "experience": user.experience,
            "qualification": user.qualification, "is_active": user.is_active}

@router.patch("")
async def update_profile(payload: ProfileUpdate, user: User = Depends(current_user),
                         db: AsyncSession = Depends(get_db)):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    return {"message": "Profile updated"}
