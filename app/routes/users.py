from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from app.models.user import UserResponse
from app.config.database import db
from app.utils.security import get_user_id_from_token
from app.utils.exceptions import (
    TokenExpiredException, InvalidTokenException,
    UserNotFoundException
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile", response_model=UserResponse)
async def get_profile(authorization: Optional[str] = Header(None)):
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={"success": False, "error": "Unauthorized", "message": "Missing or invalid authorization header"}
            )

        token = authorization.replace("Bearer ", "")
        user_id = get_user_id_from_token(token)

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, username, email, registration_date, last_login
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )
            user = cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail={"success": False, "error": "Not Found", "message": "User not found"}
                )

            return UserResponse(
                userId=user['user_id'],
                username=user['username'],
                email=user['email'],
                registrationDate=user['registration_date'],
                lastLogin=user['last_login']
            )

    except HTTPException:
        raise
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
