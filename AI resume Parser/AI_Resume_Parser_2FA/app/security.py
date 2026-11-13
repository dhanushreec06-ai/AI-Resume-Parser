import os, secrets, hashlib
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_DEMO_SECRET_BEFORE_DEPLOYMENT")
JWT_ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def new_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def create_access_token(email: str) -> str:
    payload = {"sub": email, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
