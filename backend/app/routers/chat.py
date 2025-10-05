"""
AI Chat and Analysis endpoints
Powered by DeepSeek V3.1 via OpenRouter
"""
from fastapi import APIRouter, Query
from typing import List, Dict
from app.services.ai_service import ai_service
from app.services.cache_service import cache
from app.services.earth_data_service import earth_data_service
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    AnalyzeAreaRequest,
    AnalyzeAreaResponse,
    EarthDataResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    AI-powered urban planning chatbot
    
    Features:
    - Context-aware responses
    - Urban planning expertise
    - Chat history support
    - Area-specific analysis when area is selected
    
    Request body:
    - **message**: User's message
    - **chatHistory**: Previous conversation (optional)
    - **selectedAreaData**: Selected area context (optional)
    - **sessionId**: Session identifier (optional)
    """
    logger.info(f"Chat request: session={request.sessionId}, has_area={request.selectedAreaData is not None}")
    
    # Get chat history from cache
    history = cache.get_chat_history(request.sessionId)
    
    # If chat history provided in request, use it (overrides cache)
    if request.chatHistory:
        history = [msg.dict() for msg in request.chatHistory]
    
    # Get AI response
    ai_response = await ai_service.chat(
        message=request.message,
        chat_history=history,
        area_data=request.selectedAreaData
    )
    
    # Save to chat history
    cache.save_chat_message(request.sessionId, "user", request.message)
    cache.save_chat_message(request.sessionId, "assistant", ai_response)
    
    return ChatResponse(response=ai_response)


@router.post("/chat-with-location", response_model=ChatResponse)
async def chat_with_location(
    message: str = Query(..., description="User's message"),
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lng: float = Query(..., description="Longitude", ge=-180, le=180),
    session_id: str = Query("default", description="Session identifier"),
    chat_history: List[Dict[str, str]] = None
):
    """
    AI-powered chat with Earth Data context for selected location
    
    This endpoint:
    1. Fetches comprehensive Earth Data for the selected coordinates
    2. Provides AI with real environmental data context
    3. Enables location-specific urban planning insights
    
    The AI can analyze:
    - Climate conditions (temperature, precipitation, humidity, wind)
    - Vegetation and green coverage data
    - Water stress and flood risk
    - Population density and urban metrics
    - Air quality (when available)
    """
    logger.info(f"Location-aware chat: lat={lat}, lng={lng}, session={session_id}")
    
    try:
        # Fetch comprehensive Earth Data for the location
        # Use the existing comprehensive endpoint logic
        import asyncio
        
        climate_task = earth_data_service.get_climate_data(lat, lng)
        vegetation_task = earth_data_service.get_vegetation_data(lat, lng)
        water_task = earth_data_service.get_water_data(lat, lng)
        flood_task = earth_data_service.get_flood_risk_data(lat, lng)
        population_task = earth_data_service.get_population_data(lat, lng, 5.0)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(
            climate_task, vegetation_task, water_task, flood_task, population_task,
            return_exceptions=True
        )
        
        climate_data, vegetation_data, water_data, flood_data, population_data = results
        
        # Check for any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error in comprehensive data fetch {i}: {result}")
        
        earth_data_response = {
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
            "location": {"lat": lat, "lng": lng, "radius_km": 5.0}
        }
        
        if not earth_data_response.get("success", False):
            logger.warning("Failed to fetch Earth Data, using fallback")
            earth_data_response = {
                "success": False,
                "data": {
                    "climate": {"temperature": {"current": 22.0}},
                    "vegetation": {"green_coverage": 35.0},
                    "water": {"water_stress_index": 30.0},
                    "flood_risk": {"flood_risk": "Medium"},
                    "population": {"total_population": 50000}
                },
                "sources": {
                    "climate": "Fallback data",
                    "vegetation": "Fallback data", 
                    "water": "Fallback data",
                    "flood_risk": "Fallback data",
                    "population": "Fallback data"
                }
            }
        
        # Get chat history
        history = cache.get_chat_history(session_id)
        if chat_history:
            history = chat_history
        
        # Get AI response with Earth Data context
        ai_response = await ai_service.chat_with_earth_data(
            message=message,
            chat_history=history,
            earth_data=earth_data_response,
            coordinates={"lat": lat, "lng": lng}
        )
        
        # Save to chat history
        cache.save_chat_message(session_id, "user", message)
        cache.save_chat_message(session_id, "assistant", ai_response)
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        logger.error(f"Error in location-aware chat: {e}")
        # Fallback to regular chat
        ai_response = await ai_service.chat(message, history or [])
        return ChatResponse(response=ai_response)


@router.post("/analyze-area", response_model=AnalyzeAreaResponse)
async def analyze_area(request: AnalyzeAreaRequest):
    """
    Comprehensive AI-powered area analysis
    
    Analyzes selected area and provides:
    - Environmental risk assessment
    - Identified issues and challenges
    - Actionable recommendations
    - Priority levels
    - Data-driven insights
    
    Request body:
    - **areaData**: Complete area information including:
        - Area size, population, buildings
        - Heat index, air quality, green coverage
        - Water stress, flood risk
        - Coordinates
    """
    logger.info(f"Area analysis request: area={request.areaData.area} km², pop={request.areaData.population}")
    
    # Get AI analysis
    result = await ai_service.analyze_area(request.areaData)
    
    return AnalyzeAreaResponse(
        analysis=result["analysis"],
        summary=result["summary"]
    )

