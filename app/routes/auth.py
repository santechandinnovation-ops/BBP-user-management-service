from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime
import uuid

from app.models.user import (
    UserRegister, UserLogin, TokenResponse,
    RegisterResponse, LogoutResponse
)
from app.config.database import db
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, get_user_id_from_token
)
from app.utils.exceptions import (
    UserAlreadyExistsException, InvalidCredentialsException,
    TokenExpiredException, InvalidTokenException
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(user: UserRegister):
    try:
        with db.get_cursor(commit=True) as cursor:
            cursor.execute(
                "SELECT user_id FROM users WHERE email = %s",
                (user.email,)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail={"success": False, "error": "Conflict", "message": "Email already registered"}
                )

            user_id = str(uuid.uuid4())
            password_hash = hash_password(user.password)
            registration_date = datetime.utcnow()

            cursor.execute(
                """
                INSERT INTO users (user_id, username, email, password_hash, registration_date)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, user.username, user.email, password_hash, registration_date)
            )

            return RegisterResponse(
                success=True,
                userId=user_id,
                message="Registration successful"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Internal Server Error", "message": str(e)}
        )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    try:
        if not credentials.email or not credentials.password:
            raise HTTPException(
                status_code=400,
                detail={"success": False, "error": "Bad Request", "message": "Missing email or password"}
            )

        with db.get_cursor(commit=True) as cursor:
            cursor.execute(
                "SELECT user_id, username, email, password_hash FROM users WHERE email = %s",
                (credentials.email,)
            )
            user = cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail={"success": False, "error": "Unauthorized", "message": "Invalid credentials"}
                )

            if not verify_password(credentials.password, user['password_hash']):
                raise HTTPException(
                    status_code=401,
                    detail={"success": False, "error": "Unauthorized", "message": "Invalid credentials"}
                )

            cursor.execute(
                "UPDATE users SET last_login = %s WHERE user_id = %s",
                (datetime.utcnow(), user['user_id'])
            )

            token = create_access_token({
                "user_id": user['user_id'],
                "email": user['email']
            })

            return TokenResponse(
                success=True,
                token=token,
                user={
                    "userId": user['user_id'],
                    "username": user['username'],
                    "email": user['email']
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Internal Server Error", "message": str(e)}
        )

@router.post("/logout", response_model=LogoutResponse)
async def logout(authorization: Optional[str] = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={"success": False, "error": "Unauthorized", "message": "Missing or invalid authorization header"}
            )

        token = authorization.replace("Bearer ", "")
        user_id = get_user_id_from_token(token)

        return LogoutResponse(
            success=True,
            message="Logout successful"
        )

    except (TokenExpiredException, InvalidTokenException) as e:
        raise HTTPException(
            status_code=401,
            detail={"success": False, "error": "Unauthorized", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Internal Server Error", "message": str(e)}
        )
