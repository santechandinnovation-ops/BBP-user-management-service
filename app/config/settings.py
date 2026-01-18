from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    DATABASE_HOST: str
    DATABASE_PORT: int = 6543
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    PORT: int = 8000

    class Config:
        case_sensitive = True

def get_settings() -> Settings:
    return Settings(
        DATABASE_HOST=os.getenv("DATABASE_HOST", ""),
        DATABASE_PORT=int(os.getenv("DATABASE_PORT", "6543")),
        DATABASE_NAME=os.getenv("DATABASE_NAME", "postgres"),
        DATABASE_USER=os.getenv("DATABASE_USER", ""),
        DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD", ""),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", ""),
        JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
        JWT_EXPIRATION_HOURS=int(os.getenv("JWT_EXPIRATION_HOURS", "24")),
        PORT=int(os.getenv("PORT", "8000"))
    )

settings = get_settings()
