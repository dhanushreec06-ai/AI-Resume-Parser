from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ParsedResume(BaseModel):
    name: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = []
    experience: Optional[str] = None
    qualification: Optional[str] = None

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(min_length=8)
    skills: list[str] = []
    experience: Optional[str] = None
    qualification: Optional[str] = None
    channel: str = "email"

class VerifyRequest(BaseModel):
    email: EmailStr
    channel: str
    otp: str = Field(min_length=6, max_length=8)

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[list[str]] = None
    experience: Optional[str] = None
    qualification: Optional[str] = None
