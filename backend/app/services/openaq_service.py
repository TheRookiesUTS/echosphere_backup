"""
OpenAQ API service for real-time air quality data
Provides access to global air quality measurements
"""
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Dict, List, Optional, Any
from app.config import settings

logger = logging.getLogger(__name__)

class OpenAQService:
    def __init__(self):
        self.base_url = settings.openaq_base_url
        self.api_key = settings.open_aq_api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        } if self.api_key else {}
        
        logger.info(f"OpenAQ Service initialized with base URL: {self.base_url}")
        if self.api_key:
            logger.info("OpenAQ API key configured")
        else:
            logger.warning("OpenAQ API key not configured - using public endpoints only")

    async def get_air_quality_by_coordinates(
        self, 
        lat: float, 
        lng: float, 
        radius: float = 1000
    ) -> Dict[str, Any]:
        """
        Fetch air quality data for given coordinates
        
        Args:
            lat: Latitude
            lng: Longitude  
            radius: Search radius in meters (default: 1000m)
            
        Returns:
            Dict containing air quality data
        """
        try:
            # Use requests instead of httpx for better compatibility
            params = {
                "coordinates": f"{lng},{lat}",
                "radius": radius,
                "limit": 10,
                "sort": "datetime",
                "order": "desc"
            }
            
            # Run in thread pool to maintain async compatibility
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                response = await loop.run_in_executor(
                    executor,
                    lambda: requests.get(
                        f"{self.base_url}/measurements",
                        params=params,
                        headers=self.headers,
                        timeout=10.0
                    )
                )
            
            response.raise_for_status()
            data = response.json()
            return self._process_air_quality_data(data, lat, lng)
                
        except requests.RequestException as e:
            logger.error(f"OpenAQ API error: {e}")
            logger.warning("OpenAQ API is not available - using fallback data")
            return self._get_fallback_data(lat, lng, api_error=str(e))
        except Exception as e:
            logger.error(f"Unexpected error fetching air quality: {e}")
            logger.warning("OpenAQ API is not available - using fallback data")
            return self._get_fallback_data(lat, lng, api_error=str(e))

    async def get_air_quality_by_city(self, city: str, country: str = None) -> Dict[str, Any]:
        """
        Fetch air quality data for a specific city
        
        Args:
            city: City name
            country: Country code (optional)
            
        Returns:
            Dict containing air quality data
        """
        try:
            params = {
                "city": city,
                "limit": 10,
                "sort": "datetime", 
                "order": "desc"
            }
            
            if country:
                params["country"] = country
            
            # Run in thread pool to maintain async compatibility
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                response = await loop.run_in_executor(
                    executor,
                    lambda: requests.get(
                        f"{self.base_url}/measurements",
                        params=params,
                        headers=self.headers,
                        timeout=10.0
                    )
                )
            
            response.raise_for_status()
            data = response.json()
            return self._process_city_air_quality_data(data, city)
                
        except requests.RequestException as e:
            logger.error(f"OpenAQ API error for city {city}: {e}")
            return self._get_fallback_data(0, 0, city=city, api_error=str(e))
        except Exception as e:
            logger.error(f"Unexpected error fetching city air quality: {e}")
            return self._get_fallback_data(0, 0, city=city, api_error=str(e))

    def _process_air_quality_data(self, data: Dict, lat: float, lng: float) -> Dict[str, Any]:
        """Process OpenAQ API response into standardized format"""
        try:
            results = data.get("results", [])
            if not results:
                logger.warning(f"No air quality data found for {lat}, {lng}")
                return self._get_fallback_data(lat, lng)
            
            # Group measurements by parameter
            measurements = {}
            for result in results:
                param = result.get("parameter", "").lower()
                value = result.get("value", 0)
                unit = result.get("unit", "")
                
                if param not in measurements:
                    measurements[param] = {
                        "value": value,
                        "unit": unit,
                        "count": 1
                    }
                else:
                    # Average multiple measurements
                    measurements[param]["value"] = (
                        measurements[param]["value"] * measurements[param]["count"] + value
                    ) / (measurements[param]["count"] + 1)
                    measurements[param]["count"] += 1
            
            # Calculate AQI based on PM2.5 (primary indicator)
            aqi = self._calculate_aqi(measurements)
            
            # Get latest timestamp
            latest_time = max(result.get("date", {}).get("utc", "") for result in results)
            
            return {
                "aqi": aqi,
                "pollutants": {
                    "pm25": measurements.get("pm25", {}).get("value", 0),
                    "pm10": measurements.get("pm10", {}).get("value", 0),
                    "no2": measurements.get("no2", {}).get("value", 0),
                    "o3": measurements.get("o3", {}).get("value", 0),
                    "so2": measurements.get("so2", {}).get("value", 0),
                    "co": measurements.get("co", {}).get("value", 0)
                },
                "units": {
                    "pm25": measurements.get("pm25", {}).get("unit", "µg/m³"),
                    "pm10": measurements.get("pm10", {}).get("unit", "µg/m³"),
                    "no2": measurements.get("no2", {}).get("unit", "µg/m³"),
                    "o3": measurements.get("o3", {}).get("unit", "µg/m³"),
                    "so2": measurements.get("so2", {}).get("unit", "µg/m³"),
                    "co": measurements.get("co", {}).get("unit", "mg/m³")
                },
                "location": {
                    "lat": lat,
                    "lng": lng,
                    "city": results[0].get("city", "Unknown"),
                    "country": results[0].get("country", "Unknown")
                },
                "timestamp": latest_time,
                "source": "OpenAQ",
                "data_quality": "real"
            }
            
        except Exception as e:
            logger.error(f"Error processing air quality data: {e}")
            return self._get_fallback_data(lat, lng)

    def _process_city_air_quality_data(self, data: Dict, city: str) -> Dict[str, Any]:
        """Process city-specific air quality data"""
        try:
            results = data.get("results", [])
            if not results:
                logger.warning(f"No air quality data found for city {city}")
                return self._get_fallback_data(0, 0, city=city)
            
            # Use first result for location
            first_result = results[0]
            location = first_result.get("location", {})
            coordinates = location.get("coordinates", {})
            
            return self._process_air_quality_data(data, 
                coordinates.get("latitude", 0), 
                coordinates.get("longitude", 0)
            )
            
        except Exception as e:
            logger.error(f"Error processing city air quality data: {e}")
            return self._get_fallback_data(0, 0, city=city)

    def _calculate_aqi(self, measurements: Dict) -> int:
        """Calculate Air Quality Index based on PM2.5 values"""
        try:
            pm25 = measurements.get("pm25", {}).get("value", 0)
            if pm25 <= 0:
                # Fallback to PM10 if PM2.5 not available
                pm10 = measurements.get("pm10", {}).get("value", 0)
                if pm10 > 0:
                    # Rough PM2.5 estimate from PM10 (PM2.5 ≈ 0.5 * PM10)
                    pm25 = pm10 * 0.5
            
            if pm25 <= 0:
                return 50  # Default moderate AQI
            
            # US EPA AQI calculation for PM2.5
            if pm25 <= 12.0:
                return int((50/12.0) * pm25)
            elif pm25 <= 35.4:
                return int(50 + (100-50)/(35.4-12.0) * (pm25 - 12.0))
            elif pm25 <= 55.4:
                return int(100 + (150-100)/(55.4-35.4) * (pm25 - 55.4))
            elif pm25 <= 150.4:
                return int(150 + (200-150)/(150.4-55.4) * (pm25 - 55.4))
            elif pm25 <= 250.4:
                return int(200 + (300-200)/(250.4-150.4) * (pm25 - 150.4))
            else:
                return min(500, int(300 + (500-300)/(500-250.4) * (pm25 - 250.4)))
                
        except Exception as e:
            logger.error(f"Error calculating AQI: {e}")
            return 50

    def _get_fallback_data(self, lat: float, lng: float, city: str = None, api_error: str = None) -> Dict[str, Any]:
        """Provide fallback data when OpenAQ API is unavailable"""
        logger.warning("Using fallback air quality data")
        
        # Generate more realistic fallback data based on location
        import random
        random.seed(int(lat * 1000 + lng * 1000))  # Seed based on location for consistency
        
        aqi = random.randint(45, 120)  # More realistic AQI range
        
        return {
            "aqi": aqi,
            "pollutants": {
                "pm25": round(random.uniform(15, 35), 1),
                "pm10": round(random.uniform(25, 55), 1),
                "no2": round(random.uniform(20, 50), 1),
                "o3": round(random.uniform(30, 60), 1),
                "so2": round(random.uniform(5, 25), 1),
                "co": round(random.uniform(1.5, 4.0), 1)
            },
            "units": {
                "pm25": "µg/m³",
                "pm10": "µg/m³", 
                "no2": "µg/m³",
                "o3": "µg/m³",
                "so2": "µg/m³",
                "co": "mg/m³"
            },
            "location": {
                "lat": lat,
                "lng": lng,
                "city": city or "Unknown",
                "country": "Unknown"
            },
            "timestamp": "2024-01-01T00:00:00Z",
            "source": "Fallback (OpenAQ API unavailable)",
            "data_quality": "fallback",
            "api_error": api_error
        }

# Global instance
openaq_service = OpenAQService()