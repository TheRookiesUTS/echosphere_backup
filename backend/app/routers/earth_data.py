"""
NASA Earth Data API endpoints
Provides comprehensive Earth observation data for urban planning
"""
from fastapi import APIRouter, Query, HTTPException
from app.services.earth_data_service import earth_data_service
from app.models.schemas import EarthDataResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/earth-data", tags=["earth-data"])

@router.get("/climate", response_model=EarthDataResponse)
async def get_climate_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch comprehensive climate data for given coordinates
    Includes temperature, precipitation, humidity, and wind data from NASA Earth Data
    """
    logger.info(f"Fetching climate data for {lat}, {lng}")
    result = await earth_data_service.get_climate_data(lat, lng)
    return EarthDataResponse(**result)

@router.get("/vegetation", response_model=EarthDataResponse)
async def get_vegetation_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch vegetation and green coverage data
    Includes NDVI, forest cover, and urban green space metrics
    """
    logger.info(f"Fetching vegetation data for {lat}, {lng}")
    result = await earth_data_service.get_vegetation_data(lat, lng)
    return EarthDataResponse(**result)

@router.get("/water", response_model=EarthDataResponse)
async def get_water_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch water stress and hydrological data
    Includes groundwater levels, surface water, and drought risk
    """
    logger.info(f"Fetching water data for {lat}, {lng}")
    result = await earth_data_service.get_water_data(lat, lng)
    return EarthDataResponse(**result)

@router.get("/flood-risk", response_model=EarthDataResponse)
async def get_flood_risk_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180)
):
    """
    Fetch flood risk assessment data
    Includes flood probability, elevation, and distance to water bodies
    """
    logger.info(f"Fetching flood risk data for {lat}, {lng}")
    result = await earth_data_service.get_flood_risk_data(lat, lng)
    return EarthDataResponse(**result)

@router.get("/population", response_model=EarthDataResponse)
async def get_population_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    radius_km: float = Query(5.0, description="Radius in kilometers", ge=0.5, le=50.0)
):
    """
    Fetch population density data for specified area
    Includes total population, density, and urban percentage
    """
    logger.info(f"Fetching population data for {lat}, {lng} with radius {radius_km}km")
    result = await earth_data_service.get_population_data(lat, lng, radius_km)
    return EarthDataResponse(**result)

@router.get("/comprehensive", response_model=dict)
async def get_comprehensive_data(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    radius_km: float = Query(5.0, description="Radius in kilometers", ge=0.5, le=50.0)
):
    """
    Fetch comprehensive Earth observation data for urban planning
    Combines climate, vegetation, water, flood risk, and population data
    """
    logger.info(f"Fetching comprehensive Earth data for {lat}, {lng}")
    
    try:
        # Fetch all data types in parallel
        import asyncio
        
        climate_task = earth_data_service.get_climate_data(lat, lng)
        vegetation_task = earth_data_service.get_vegetation_data(lat, lng)
        water_task = earth_data_service.get_water_data(lat, lng)
        flood_task = earth_data_service.get_flood_risk_data(lat, lng)
        population_task = earth_data_service.get_population_data(lat, lng, radius_km)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(
            climate_task, vegetation_task, water_task, flood_task, population_task,
            return_exceptions=True
        )
        
        climate_data, vegetation_data, water_data, flood_data, population_data = results
        
        # Check for any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error in data fetch {i}: {result}")
        
        return {
            "success": True,
            "data": {
                "climate": climate_data.get("data", {}),
                "vegetation": vegetation_data.get("data", {}),
                "water": water_data.get("data", {}),
                "flood_risk": flood_data.get("data", {}),
                "population": population_data.get("data", {})
            },
            "sources": {
                "climate": climate_data.get("source", "Unknown"),
                "vegetation": vegetation_data.get("source", "Unknown"),
                "water": water_data.get("source", "Unknown"),
                "flood_risk": flood_data.get("source", "Unknown"),
                "population": population_data.get("source", "Unknown")
            },
            "timestamp": climate_data.get("timestamp"),
            "location": {"lat": lat, "lng": lng, "radius_km": radius_km}
        }
        
    except Exception as e:
        logger.error(f"Error fetching comprehensive data: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching comprehensive data: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for Earth Data service"""
    is_configured = bool(earth_data_service.api_key)
    
    return {
        "status": "healthy",
        "service": "Earth Data API",
        "api_key_configured": is_configured,
        "base_url": earth_data_service.base_url,
        "endpoints": [
            "/api/earth-data/climate",
            "/api/earth-data/vegetation", 
            "/api/earth-data/water",
            "/api/earth-data/flood-risk",
            "/api/earth-data/population",
            "/api/earth-data/comprehensive"
        ]
    }
