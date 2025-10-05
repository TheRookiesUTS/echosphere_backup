"""
AI service using DeepSeek V3.1 via OpenRouter
Handles chat and area analysis with urban planning expertise
"""
from openai import OpenAI
from typing import List, Dict, Optional
from app.config import settings
from app.models.schemas import AreaData, AreaAnalysisSummary
import logging

logger = logging.getLogger(__name__)


# System prompt for urban planning expertise
URBAN_PLANNER_SYSTEM_PROMPT = """You are an expert urban planning consultant specializing in climate resilience and sustainable city development. Your expertise includes:

- Environmental data analysis (heat islands, air quality, flood risk, green infrastructure)
- Climate adaptation and mitigation strategies
- Sustainable urban development and smart growth
- Green infrastructure planning and design
- Disaster risk reduction and resilience building
- Data-driven policy recommendations

You provide actionable, practical recommendations based on real environmental data. You understand:
- Urban heat island effects and cooling strategies
- Air quality management and pollution control
- Flood risk assessment and mitigation
- Green space optimization and ecosystem services
- Population density and urban form impacts

Your responses are:
- Evidence-based and data-driven
- Practical and actionable
- Context-aware (considering local conditions)
- Focused on sustainable, resilient solutions
- Clear and accessible to city planners and decision-makers

When analyzing data, you consider multiple factors: environmental metrics, population impacts, infrastructure needs, and long-term sustainability goals."""


class AIService:
    """AI service for chat and analysis using DeepSeek"""
    
    def __init__(self):
        # Debug: Log API key (first 20 chars only for security)
        api_key_preview = settings.openrouter_api_key[:20] + "..." if len(settings.openrouter_api_key) > 20 else settings.openrouter_api_key
        logger.info(f"Initializing AIService with API key: {api_key_preview}")
        logger.info(f"Base URL: {settings.openrouter_base_url}")
        logger.info(f"Model: {settings.deepseek_model}")
        
        # Optional headers for OpenRouter
        default_headers = {}
        if settings.site_url:
            default_headers["HTTP-Referer"] = settings.site_url
        if settings.site_name:
            default_headers["X-Title"] = settings.site_name
        
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
            default_headers=default_headers
        )
        self.model = settings.deepseek_model
    
    async def chat(
        self,
        message: str,
        chat_history: List[Dict[str, str]] = None,
        area_data: Optional[AreaData] = None
    ) -> str:
        """
        Chat with AI assistant with optional area context
        """
        if chat_history is None:
            chat_history = []
        
        # Build messages array
        messages = [{"role": "system", "content": URBAN_PLANNER_SYSTEM_PROMPT}]
        
        # Add area context if provided
        if area_data:
            context = self._build_area_context(area_data)
            messages.append({
                "role": "system",
                "content": f"Current Context: The user has selected a specific area with the following characteristics:\n{context}"
            })
        
        # Add chat history
        messages.extend(chat_history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            # Call DeepSeek via OpenRouter
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            ai_response = response.choices[0].message.content
            logger.info(f"AI chat completed successfully")
            return ai_response
        
        except Exception as e:
            logger.error(f"Error in AI chat: {str(e)}")
            return f"I apologize, but I'm having trouble processing your request right now. Please try again. (Error: {str(e)})"
    
    async def analyze_area(self, area_data: AreaData) -> Dict[str, any]:
        """
        Comprehensive area analysis with structured output
        """
        analysis_prompt = self._build_analysis_prompt(area_data)
        
        messages = [
            {"role": "system", "content": URBAN_PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )
            
            analysis_text = response.choices[0].message.content
            
            # Extract structured summary
            summary = self._extract_summary(area_data, analysis_text)
            
            logger.info("Area analysis completed successfully")
            return {
                "analysis": analysis_text,
                "summary": summary
            }
        
        except Exception as e:
            logger.error(f"Error in area analysis: {str(e)}")
            return {
                "analysis": f"Analysis temporarily unavailable. Error: {str(e)}",
                "summary": {
                    "issues": ["Unable to analyze at this time"],
                    "recommendations": ["Please try again later"],
                    "priorityLevel": "Unknown"
                }
            }
    
    async def chat_with_earth_data(
        self,
        message: str,
        chat_history: List[Dict[str, str]] = None,
        earth_data: Dict = None,
        coordinates: Dict = None
    ) -> str:
        """
        Chat with AI assistant with comprehensive Earth Data context
        """
        if chat_history is None:
            chat_history = []
        
        # Build messages array
        messages = [{"role": "system", "content": URBAN_PLANNER_SYSTEM_PROMPT}]
        
        # Add Earth Data context if provided
        if earth_data and coordinates:
            context = self._build_earth_data_context(earth_data, coordinates)
            messages.append({
                "role": "system", 
                "content": f"LOCATION CONTEXT: The user is asking about a specific location at coordinates {coordinates['lat']}, {coordinates['lng']}. Here is the comprehensive Earth observation data for this area:\n\n{context}\n\nUse this real environmental data to provide accurate, location-specific urban planning insights and recommendations."
            })
        
        # Add chat history
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Get AI response
        try:
            # Call DeepSeek via OpenRouter
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            ai_response = response.choices[0].message.content
            logger.info(f"AI chat with Earth Data completed successfully")
            return ai_response
        
        except Exception as e:
            logger.error(f"Error in AI chat with Earth Data: {str(e)}")
            return f"I apologize, but I'm having trouble processing your request right now. Please try again. (Error: {str(e)})"
    
    def _build_earth_data_context(self, earth_data: Dict, coordinates: Dict) -> str:
        """Build comprehensive Earth Data context string for AI"""
        data = earth_data.get("data", {})
        sources = earth_data.get("sources", {})
        
        context = f"""
**LOCATION**: {coordinates['lat']:.4f}, {coordinates['lng']:.4f}

**CLIMATE CONDITIONS:**
- Temperature: {data.get('climate', {}).get('temperature', {}).get('current', 'N/A')}°C (Average: {data.get('climate', {}).get('temperature', {}).get('average', 'N/A')}°C)
- Precipitation: {data.get('climate', {}).get('precipitation', {}).get('monthly_avg', 'N/A')}mm/month ({data.get('climate', {}).get('precipitation', {}).get('annual', 'N/A')}mm/year)
- Humidity: {data.get('climate', {}).get('humidity', {}).get('current', 'N/A')}%
- Wind Speed: {data.get('climate', {}).get('wind', {}).get('speed', 'N/A')} m/s
- Climate Zone: {data.get('climate', {}).get('climate_zone', 'Unknown')}

**VEGETATION & GREEN INFRASTRUCTURE:**
- Green Coverage: {data.get('vegetation', {}).get('green_coverage', 'N/A')}%
- Vegetation Index (NDVI): {data.get('vegetation', {}).get('vegetation_index', 'N/A')}
- Vegetation Type: {data.get('vegetation', {}).get('vegetation_type', 'Unknown')}
- Forest Cover: {data.get('vegetation', {}).get('forest_cover', 'N/A')}%
- Urban Green Space: {data.get('vegetation', {}).get('urban_green_space', 'N/A')}%

**WATER RESOURCES & RISK:**
- Water Stress Index: {data.get('water', {}).get('water_stress_index', 'N/A')}%
- Groundwater Level: {data.get('water', {}).get('groundwater_level', 'N/A')}%
- Surface Water: {data.get('water', {}).get('surface_water', 'N/A')}%
- Drought Risk: {data.get('water', {}).get('drought_risk', 'Unknown')}

**FLOOD RISK ASSESSMENT:**
- Flood Risk Level: {data.get('flood_risk', {}).get('flood_risk', 'Unknown')}
- Flood Probability: {data.get('flood_risk', {}).get('flood_probability', 'N/A')}%
- Elevation: {data.get('flood_risk', {}).get('elevation', 'N/A')}m
- Distance to Water: {data.get('flood_risk', {}).get('distance_to_water', 'N/A')}km

**POPULATION & URBAN METRICS:**
- Total Population: {data.get('population', {}).get('total_population', 'N/A'):,} residents
- Population Density: {data.get('population', {}).get('population_density', 'N/A')} people/km²
- Urban Percentage: {data.get('population', {}).get('urban_percentage', 'N/A')}%
- Area Size: {data.get('population', {}).get('area_km2', 'N/A')} km²

**DATA SOURCES:**
- Climate: {sources.get('climate', 'Unknown')}
- Vegetation: {sources.get('vegetation', 'Unknown')}
- Water: {sources.get('water', 'Unknown')}
- Flood Risk: {sources.get('flood_risk', 'Unknown')}
- Population: {sources.get('population', 'Unknown')}
"""
        return context.strip()
    
    def _build_area_context(self, area_data: AreaData) -> str:
        """Build readable area context string"""
        context = f"""
Area Size: {area_data.area} km²
Population: {area_data.population:,} residents
Heat Index: {area_data.heatIndex}°C
Air Quality: {area_data.airQuality} AQI
Green Coverage: {area_data.greenCoverage}%
Water Stress: {area_data.waterStress}%
Flood Risk: {area_data.floodRisk}
Buildings: {area_data.buildings if area_data.buildings else 'Unknown'}
"""
        return context.strip()
    
    def _build_analysis_prompt(self, area_data: AreaData) -> str:
        """Build comprehensive analysis prompt"""
        return f"""Please provide a comprehensive urban resilience analysis for the following area:

**Area Characteristics:**
- Size: {area_data.area} km²
- Population: {area_data.population:,} residents
- Buildings: {area_data.buildings if area_data.buildings else 'Unknown'}

**Environmental Metrics:**
- Heat Index: {area_data.heatIndex}°C
- Air Quality Index (AQI): {area_data.airQuality}
- Green Coverage: {area_data.greenCoverage}%
- Water Stress Level: {area_data.waterStress}%
- Flood Risk: {area_data.floodRisk}

**Analysis Requirements:**
1. Identify the top environmental and resilience challenges
2. Assess the severity of each issue (consider thresholds: Heat >32°C is high, AQI >100 is unhealthy, Green <25% is low)
3. Provide specific, actionable recommendations with priority levels
4. Consider the population impact and vulnerability
5. Suggest both immediate interventions and long-term strategies
6. Focus on nature-based solutions where appropriate

Please structure your analysis clearly with sections for: Key Issues, Risk Assessment, Recommendations, and Priority Actions."""
    
    def _extract_summary(self, area_data: AreaData, analysis_text: str) -> AreaAnalysisSummary:
        """Extract structured summary from analysis"""
        issues = []
        recommendations = []
        priority_level = "Medium"
        
        # Analyze based on thresholds
        if area_data.heatIndex > 32:
            issues.append("High heat stress detected")
            recommendations.append("Implement cooling strategies: green roofs, tree planting, cool pavements")
        
        if area_data.airQuality > 100:
            issues.append("Poor air quality (unhealthy levels)")
            recommendations.append("Create green barriers, reduce traffic emissions, improve ventilation")
        
        if area_data.greenCoverage < 25:
            issues.append("Low green space coverage")
            recommendations.append("Increase urban green infrastructure and parks")
        
        if area_data.waterStress and area_data.waterStress > 60:
            issues.append("High water stress")
            recommendations.append("Improve water management and conservation")
        
        if area_data.floodRisk in ["High", "Very High"]:
            issues.append("Significant flood risk")
            recommendations.append("Implement flood mitigation: permeable surfaces, retention systems")
        
        # Determine priority level
        critical_count = sum([
            area_data.heatIndex > 35,
            area_data.airQuality > 150,
            area_data.floodRisk == "Very High",
            area_data.greenCoverage < 15
        ])
        
        if critical_count >= 2:
            priority_level = "Critical"
        elif len(issues) >= 3:
            priority_level = "High"
        elif len(issues) >= 1:
            priority_level = "Medium"
        else:
            priority_level = "Low"
        
        return AreaAnalysisSummary(
            issues=issues if issues else ["No major issues detected"],
            recommendations=recommendations if recommendations else ["Continue monitoring environmental metrics"],
            priorityLevel=priority_level
        )


# Global AI service instance
ai_service = AIService()

