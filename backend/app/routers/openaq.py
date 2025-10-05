"""
OpenAQ API endpoints for real-time air quality data
Provides access to global air quality measurements
"""
from fastapi import APIRouter, Query, HTTPException
from app.services.openaq_service import openaq_service
from app.models.schemas import OpenAQResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/openaq", tags=["openaq"])


@router.get("/air-quality", response_model=OpenAQResponse)
async def get_air_quality_by_coordinates(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    radius: float = Query(1000, description="Search radius in meters", ge=100, le=10000)
):
    """
    Fetch real-time air quality data for given coordinates
    
    - **lat**: Latitude (-90 to 90)
    - **lng**: Longitude (-180 to 180)  
    - **radius**: Search radius in meters (100-10000, default: 1000)
    
    Returns real-time air quality data including:
    - Air Quality Index (AQI)
    - PM2.5, PM10, NO2, O3, SO2, CO concentrations
    - Location information
    - Data source and quality indicators
    """
    try:
        logger.info(f"Fetching air quality data for coordinates {lat}, {lng}")
        result = await openaq_service.get_air_quality_by_coordinates(lat, lng, radius)
        return OpenAQResponse(**result)
    except Exception as e:
        logger.error(f"Error fetching air quality data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch air quality data: {str(e)}")


@router.get("/air-quality/city", response_model=OpenAQResponse)
async def get_air_quality_by_city(
    city: str = Query(..., description="City name", min_length=2),
    country: str = Query(None, description="Country code (optional)")
):
    """
    Fetch real-time air quality data for a specific city
    
    - **city**: City name (required)
    - **country**: Country code (optional)
    
    Returns real-time air quality data for the specified city including:
    - Air Quality Index (AQI)
    - PM2.5, PM10, NO2, O3, SO2, CO concentrations
    - Location information
    - Data source and quality indicators
    """
    try:
        logger.info(f"Fetching air quality data for city: {city}, country: {country}")
        result = await openaq_service.get_air_quality_by_city(city, country)
        return OpenAQResponse(**result)
    except Exception as e:
        logger.error(f"Error fetching city air quality data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch city air quality data: {str(e)}")


@router.get("/health")
async def openaq_health_check():
    """
    Check OpenAQ service health and API key status
    """
    try:
        # Test API connectivity
        test_result = await openaq_service.get_air_quality_by_coordinates(2.3, 111.82)  # Sibu coordinates
        
        return {
            "status": "healthy",
            "api_key_configured": openaq_service.api_key is not None,
            "base_url": openaq_service.base_url,
            "test_result": "success" if test_result.get("data_quality") == "real" else "fallback",
            "data_source": test_result.get("source", "unknown")
        }
    except Exception as e:
        logger.error(f"OpenAQ health check failed: {e}")
        return {
            "status": "unhealthy",
            "api_key_configured": openaq_service.api_key is not None,
            "base_url": openaq_service.base_url,
            "error": str(e)
        }