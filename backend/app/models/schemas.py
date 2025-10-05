"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# Chat Models
# ============================================================================

class ChatMessage(BaseModel):
    """Individual chat message"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class AreaData(BaseModel):
    """Geospatial area data from frontend"""
    area: float = Field(..., description="Area in km²")
    center: Optional[Dict[str, float]] = Field(None, description="Center coordinates {lat, lng}")
    bounds: Optional[Dict[str, Any]] = Field(None, description="Boundary coordinates")
    heatIndex: float = Field(..., description="Heat index in °C")
    airQuality: int = Field(..., description="Air Quality Index (AQI)")
    greenCoverage: float = Field(..., description="Green coverage percentage")
    waterStress: Optional[float] = Field(None, description="Water stress percentage")
    floodRisk: str = Field(..., description="Flood risk level")
    population: int = Field(..., description="Population estimate")
    buildings: Optional[int] = Field(None, description="Number of buildings")


class ChatRequest(BaseModel):
    """Request for AI chat endpoint"""
    message: str = Field(..., description="User message", min_length=1)
    chatHistory: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation")
    selectedAreaData: Optional[AreaData] = Field(None, description="Selected area context")
    sessionId: Optional[str] = Field(default="default", description="Session identifier")


class ChatResponse(BaseModel):
    """Response from AI chat endpoint"""
    response: str = Field(..., description="AI assistant response")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyzeAreaRequest(BaseModel):
    """Request for area analysis endpoint"""
    areaData: AreaData = Field(..., description="Area data to analyze")


class AreaAnalysisSummary(BaseModel):
    """Summary of area analysis"""
    issues: List[str] = Field(..., description="Identified issues")
    recommendations: List[str] = Field(..., description="Recommendations")
    priorityLevel: str = Field(..., description="Priority level: Low, Medium, High, Critical")


class AnalyzeAreaResponse(BaseModel):
    """Response from area analysis endpoint"""
    analysis: str = Field(..., description="Full analysis report (markdown formatted)")
    summary: AreaAnalysisSummary = Field(..., description="Analysis summary")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# NASA Models
# ============================================================================

class NASAImageryResponse(BaseModel):
    """NASA Earth imagery response"""
    data: Optional[Dict[str, Any]] = Field(None, description="NASA imagery data")
    cached: bool = Field(False, description="Whether response was cached")
    error: Optional[str] = Field(None, description="Error message if any")


class EONETEvent(BaseModel):
    """EONET natural event"""
    id: str
    title: str
    description: Optional[str] = None
    categories: List[Dict[str, Any]]
    geometry: List[Dict[str, Any]]
    link: Optional[str] = None


class EONETResponse(BaseModel):
    """EONET events response"""
    events: List[Dict[str, Any]] = Field(..., description="List of natural events")
    count: int = Field(..., description="Number of events")
    cached: bool = Field(False, description="Whether response was cached")


class NASAPowerResponse(BaseModel):
    """NASA POWER climate data response"""
    data: Optional[Dict[str, Any]] = Field(None, description="Climate data")
    cached: bool = Field(False, description="Whether response was cached")
    error: Optional[str] = Field(None, description="Error message if any")


# ============================================================================
# OpenAQ Models
# ============================================================================

class AirQualityPollutants(BaseModel):
    """Air quality pollutant measurements"""
    pm25: float = Field(..., description="PM2.5 concentration")
    pm10: float = Field(..., description="PM10 concentration")
    no2: float = Field(..., description="NO2 concentration")
    o3: float = Field(..., description="O3 concentration")
    so2: float = Field(..., description="SO2 concentration")
    co: float = Field(..., description="CO concentration")


class AirQualityUnits(BaseModel):
    """Units for air quality measurements"""
    pm25: str = Field(default="µg/m³", description="PM2.5 unit")
    pm10: str = Field(default="µg/m³", description="PM10 unit")
    no2: str = Field(default="µg/m³", description="NO2 unit")
    o3: str = Field(default="µg/m³", description="O3 unit")
    so2: str = Field(default="µg/m³", description="SO2 unit")
    co: str = Field(default="mg/m³", description="CO unit")


class AirQualityLocation(BaseModel):
    """Location information for air quality data"""
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")


class OpenAQResponse(BaseModel):
    """OpenAQ air quality response"""
    aqi: int = Field(..., description="Air Quality Index (0-500)")
    pollutants: AirQualityPollutants = Field(..., description="Pollutant concentrations")
    units: AirQualityUnits = Field(..., description="Measurement units")
    location: AirQualityLocation = Field(..., description="Location data")
    timestamp: str = Field(..., description="Data timestamp")
    source: str = Field(..., description="Data source")
    data_quality: str = Field(..., description="Data quality indicator")
    api_error: Optional[str] = Field(None, description="Error message from API if any")


class EarthDataResponse(BaseModel):
    """NASA Earth Data API response"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Dict[str, Any] = Field(..., description="Earth observation data")
    source: str = Field(..., description="Data source information")
    timestamp: str = Field(..., description="Data timestamp")
    location: Dict[str, float] = Field(..., description="Location coordinates")
    error: Optional[str] = Field(None, description="Error message if any")


# ============================================================================
# Health Check
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = Field(..., description="Status of external services")


# ============================================================================
# Reporting Models
# ============================================================================

class ReportType(str, Enum):
    ENVIRONMENTAL_ISSUE = "environmental_issue"
    FLOOD_RISK = "flood_risk"
    HEAT_STRESS = "heat_stress"
    AIR_QUALITY = "air_quality"
    GREEN_SPACE = "green_space"
    URBAN_PLANNING = "urban_planning_suggestion"
    INFRASTRUCTURE = "infrastructure_issue"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReportCategory(str, Enum):
    HEAT_ISLAND = "heat_island"
    FLOODING = "flooding"
    AIR_POLLUTION = "air_pollution"
    GREEN_COVERAGE = "green_coverage"
    TRANSPORTATION = "transportation"
    WASTE_MANAGEMENT = "waste_management"
    ENERGY = "energy"
    OTHER = "other"

class ReportLocation(BaseModel):
    address: str = Field(..., description="Street address or general location description")
    latitude: Optional[float] = Field(None, description="Latitude of the reported location")
    longitude: Optional[float] = Field(None, description="Longitude of the reported location")

class ReportSubmission(BaseModel):
    reporter_name: str = Field(..., min_length=3, max_length=100, description="Name of the person submitting the report")
    reporter_email: str = Field(..., description="Email address of the reporter")
    report_type: ReportType = Field(..., description="Type of report being submitted")
    title: str = Field(..., min_length=5, max_length=200, description="Concise title for the report")
    description: str = Field(..., min_length=20, description="Detailed description of the issue or suggestion")
    severity: SeverityLevel = Field(..., description="Severity level of the reported issue")
    category: ReportCategory = Field(..., description="Category of the report")
    location: ReportLocation = Field(..., description="Location details of the report")
    date_observed: datetime = Field(..., description="Date and time when the issue was observed")
    images: List[str] = Field(default_factory=list, description="List of URLs to uploaded images")
    contact_permission: bool = Field(False, description="Permission to contact the reporter for follow-up")
    follow_up: bool = Field(False, description="Request for follow-up updates on the report")

class ReportResponse(BaseModel):
    report_id: str = Field(..., description="Unique identifier for the submitted report")
    status: str = Field(..., description="Status of the report submission")
    message: str = Field(..., description="Confirmation message")
    estimated_review_time: str = Field(..., description="Estimated time for initial review")

