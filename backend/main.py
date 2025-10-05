"""
Echosphere Backend - Urban Resilience Digital Twin
FastAPI application for NASA Space Apps Challenge

Provides:
- AI-powered urban planning assistant (DeepSeek V3.1)
- NASA API proxy for Earth observation data
- Area analysis and environmental assessment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from app.routers import chat, nasa, health, openaq, earth_data, reports
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Echosphere API",
    description="Urban Resilience Digital Twin - NASA Space Apps Challenge",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
        "*"  # Allow all for hackathon - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(nasa.router)
app.include_router(openaq.router)
app.include_router(earth_data.router)
app.include_router(reports.router)


@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("=" * 50)
    logger.info("🚀 Echosphere Backend Starting...")
    logger.info(f"📍 Backend URL: {settings.backend_url}")
    logger.info(f"🌐 Frontend URL: {settings.frontend_url}")
    logger.info(f"🤖 AI Model: {settings.deepseek_model}")
    logger.info(f"🛰️  NASA API: Configured")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("👋 Echosphere Backend Shutting Down...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Echosphere API - Urban Resilience Digital Twin",
        "status": "operational",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

