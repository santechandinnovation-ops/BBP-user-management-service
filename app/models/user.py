from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    userId: str
    username: str
    email: str
    registrationDate: Optional[datetime] = None
    lastLogin: Optional[datetime] = None

class TokenResponse(BaseModel):
    success: bool = True
    token: str
    user: dict

class RegisterResponse(BaseModel):
    success: bool = True
    userId: str
    message: str = "Registration successful"

class LogoutResponse(BaseModel):
    success: bool = True
    message: str = "Logout successful"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str
