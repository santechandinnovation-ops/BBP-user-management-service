from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.config.database import db

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    try:
        with db.get_cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return {
            "status": "healthy",
            "service": "User Management Service",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "service": "User Management Service",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "disconnected",
                "error": str(e)
            }
        )
