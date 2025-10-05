"""
NASA API proxy endpoints
Provides secure access to NASA APIs with caching
"""
from fastapi import APIRouter, Query
from app.services.nasa_service import nasa_service
from app.models.schemas import NASAImageryResponse, EONETResponse, NASAPowerResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/nasa", tags=["nasa"])


@router.get("/imagery", response_model=NASAImageryResponse)
async def get_earth_imagery(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    dim: float = Query(0.1, description="Image dimension", ge=0.01, le=0.5)
):
    """
    Fetch NASA Earth imagery for given coordinates
    
    - **lat**: Latitude (-90 to 90)
    - **lng**: Longitude (-180 to 180)
    - **dim**: Image dimension (default: 0.1)
    """
    logger.info(f"Fetching Earth imagery for {lat}, {lng}")
    result = await nasa_service.get_earth_imagery(lat, lng, dim)
    return NASAImageryResponse(**result)


@router.get("/eonet/events", response_model=EONETResponse)
async def get_eonet_events(
    status: str = Query("open", description="Event status: open, closed, all"),
    limit: int = Query(50, description="Maximum number of events", ge=1, le=100)
):
    """
    Fetch natural disaster events from NASA EONET
    
    - **status**: Event status (open, closed, all)
    - **limit**: Maximum number of events to return (1-100)
    
    Returns real-time data about:
    - Wildfires
    - Severe storms
    - Floods
    - Volcanoes
    - Earthquakes
    - And more natural events
    """
    logger.info(f"Fetching EONET events (status={status}, limit={limit})")
    result = await nasa_service.get_eonet_events(status, limit)
    return EONETResponse(**result)


@router.get("/power/climate", response_model=NASAPowerResponse)
async def get_power_climate_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch climate and weather data from NASA POWER API
    
    - **lat**: Latitude (-90 to 90)
    - **lng**: Longitude (-180 to 180)
    
    Returns:
    - Temperature data
    - Precipitation
    - Humidity
    - Wind speed
    - And more climate parameters
    """
    logger.info(f"Fetching POWER climate data for {lat}, {lng}")
    result = await nasa_service.get_power_climate_data(lat, lng)
    return NASAPowerResponse(**result)

