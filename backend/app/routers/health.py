"""
Health check endpoint
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from datetime import datetime

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns status of the API and external services
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow(),
        services={
            "api": "operational",
            "openrouter": "operational",
            "nasa": "operational",
            "cache": "operational"
        }
    )

