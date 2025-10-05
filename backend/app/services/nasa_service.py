"""
NASA API integration service
Handles all NASA API calls with caching and error handling
"""
import httpx
from typing import Optional, Dict, Any
from app.config import settings
from app.services.cache_service import cache
import logging

logger = logging.getLogger(__name__)


class NASAService:
    """NASA API service with caching"""
    
    def __init__(self):
        self.nasa_base_url = settings.nasa_base_url
        self.eonet_base_url = settings.eonet_base_url
        self.api_key = settings.nasa_api_key
        self.cache_ttl = settings.nasa_cache_ttl
    
    async def get_earth_imagery(self, lat: float, lng: float, dim: float = 0.1) -> Dict[str, Any]:
        """
        Fetch NASA Earth imagery for given coordinates
        https://api.nasa.gov/planetary/earth/imagery
        """
        cache_key = f"nasa_imagery_{lat}_{lng}_{dim}"
        
        # Check cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for imagery at {lat}, {lng}")
            return {"data": cached_data, "cached": True, "error": None}
        
        # Make API request
        url = f"{self.nasa_base_url}/planetary/earth/imagery"
        params = {
            "lat": lat,
            "lon": lng,
            "dim": dim,
            "api_key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    # Cache the result
                    cache.set(cache_key, data, self.cache_ttl)
                    logger.info(f"Successfully fetched imagery for {lat}, {lng}")
                    return {"data": data, "cached": False, "error": None}
                else:
                    logger.warning(f"NASA API returned {response.status_code}")
                    return {"data": None, "cached": False, "error": f"API returned status {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Error fetching NASA imagery: {str(e)}")
            return {"data": None, "cached": False, "error": str(e)}
    
    async def get_eonet_events(self, status: str = "open", limit: int = 50) -> Dict[str, Any]:
        """
        Fetch natural disaster events from EONET
        https://eonet.gsfc.nasa.gov/api/v3/events
        """
        cache_key = f"eonet_events_{status}_{limit}"
        
        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("Cache hit for EONET events")
            return {"events": cached_data, "count": len(cached_data), "cached": True}
        
        # Make API request
        url = f"{self.eonet_base_url}/events"
        params = {
            "status": status,
            "limit": limit
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get("events", [])
                    
                    # Cache the result
                    cache.set(cache_key, events, self.cache_ttl)
                    logger.info(f"Successfully fetched {len(events)} EONET events")
                    return {"events": events, "count": len(events), "cached": False}
                else:
                    logger.warning(f"EONET API returned {response.status_code}")
                    return {"events": [], "count": 0, "cached": False}
        
        except Exception as e:
            logger.error(f"Error fetching EONET events: {str(e)}")
            return {"events": [], "count": 0, "cached": False}
    
    async def get_power_climate_data(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Fetch climate/weather data from NASA POWER API
        https://power.larc.nasa.gov/api/
        """
        cache_key = f"nasa_power_{lat}_{lng}"
        
        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for POWER data at {lat}, {lng}")
            return {"data": cached_data, "cached": True, "error": None}
        
        # NASA POWER API endpoint
        url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
        
        # Request parameters for recent data
        params = {
            "parameters": "T2M,PRECTOTCORR,RH2M,WS10M",  # Temperature, Precipitation, Humidity, Wind Speed
            "community": "RE",  # Renewable Energy community
            "longitude": lng,
            "latitude": lat,
            "start": "20240101",  # Recent year
            "end": "20241231",
            "format": "JSON"
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    # Cache the result
                    cache.set(cache_key, data, self.cache_ttl)
                    logger.info(f"Successfully fetched POWER data for {lat}, {lng}")
                    return {"data": data, "cached": False, "error": None}
                else:
                    logger.warning(f"POWER API returned {response.status_code}")
                    return {"data": None, "cached": False, "error": f"API returned status {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Error fetching POWER data: {str(e)}")
            return {"data": None, "cached": False, "error": str(e)}


# Global NASA service instance
nasa_service = NASAService()

