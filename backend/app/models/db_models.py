"""
Database models for EchoSphere - Urban Resilience Digital Twin
PostgreSQL + PostGIS schema for geospatial urban planning data
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean, 
    ForeignKey, JSON, Index, Enum as SQLEnum
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from datetime import datetime
import enum

Base = declarative_base()


# ============================================================================
# Enums
# ============================================================================

class FloodRiskLevel(str, enum.Enum):
    """Flood risk classification"""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"


class PriorityLevel(str, enum.Enum):
    """Analysis priority classification"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SessionStatus(str, enum.Enum):
    """User session status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


# ============================================================================
# User & Session Management
# ============================================================================

class User(Base):
    """User/session tracking for personalized experiences"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(SQLEnum(SessionStatus, create_type=False, native_enum=False), default=SessionStatus.ACTIVE)
    preferences = Column(JSON, default={})  # User preferences (theme, default city, etc.)
    
    # Relationships
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    area_analyses = relationship("AreaAnalysis", back_populates="user", cascade="all, delete-orphan")
    selected_areas = relationship("SelectedArea", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, session_id={self.session_id})>"


# ============================================================================
# Geospatial Data
# ============================================================================

class SelectedArea(Base):
    """User-selected geographical areas with boundaries"""
    __tablename__ = "selected_areas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=True)  # Optional area name
    
    # Geospatial data (PostGIS)
    geometry = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    area_km2 = Column(Float, nullable=False)  # Area in square kilometers
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="selected_areas")
    analyses = relationship("AreaAnalysis", back_populates="area", cascade="all, delete-orphan")
    metrics = relationship("EnvironmentalMetric", back_populates="area", cascade="all, delete-orphan")
    
    # Spatial index for fast queries
    __table_args__ = (
        Index('idx_selected_areas_geometry', 'geometry', postgresql_using='gist'),
        Index('idx_selected_areas_center', 'center_lat', 'center_lng'),
    )
    
    def __repr__(self):
        return f"<SelectedArea(id={self.id}, area={self.area_km2} km²)>"


# ============================================================================
# Environmental Metrics
# ============================================================================

class EnvironmentalMetric(Base):
    """Time-series environmental data for selected areas"""
    __tablename__ = "environmental_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("selected_areas.id", ondelete="CASCADE"), nullable=False)
    
    # Climate metrics
    heat_index = Column(Float, nullable=False)  # Temperature in °C
    air_quality_index = Column(Integer, nullable=False)  # AQI value
    humidity = Column(Float, nullable=True)  # Percentage
    wind_speed = Column(Float, nullable=True)  # m/s
    precipitation = Column(Float, nullable=True)  # mm
    
    # Urban metrics
    green_coverage = Column(Float, nullable=False)  # Percentage
    water_stress = Column(Float, nullable=True)  # Percentage
    flood_risk = Column(SQLEnum(FloodRiskLevel, create_type=False, native_enum=False), nullable=False)
    
    # Population & infrastructure
    population_estimate = Column(Integer, nullable=True)
    building_count = Column(Integer, nullable=True)
    
    # Timestamp
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    data_source = Column(String(100), nullable=True)  # e.g., "NASA_POWER", "Manual"
    
    # Relationships
    area = relationship("SelectedArea", back_populates="metrics")
    
    __table_args__ = (
        Index('idx_env_metrics_area_time', 'area_id', 'recorded_at'),
    )
    
    def __repr__(self):
        return f"<EnvironmentalMetric(area_id={self.area_id}, heat={self.heat_index}°C)>"


# ============================================================================
# Area Analysis Results
# ============================================================================

class AreaAnalysis(Base):
    """AI-generated analysis results for selected areas"""
    __tablename__ = "area_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    area_id = Column(Integer, ForeignKey("selected_areas.id", ondelete="CASCADE"), nullable=False)
    
    # Analysis content
    analysis_text = Column(Text, nullable=False)  # Full markdown analysis
    summary = Column(JSON, nullable=False)  # Structured summary with issues/recommendations
    priority_level = Column(SQLEnum(PriorityLevel, create_type=False, native_enum=False), nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_model = Column(String(100), default="deepseek-chat-v3.1")  # Track which model generated it
    processing_time_ms = Column(Integer, nullable=True)  # Performance tracking
    
    # Relationships
    user = relationship("User", back_populates="area_analyses")
    area = relationship("SelectedArea", back_populates="analyses")
    
    __table_args__ = (
        Index('idx_area_analyses_user_time', 'user_id', 'created_at'),
        Index('idx_area_analyses_area_time', 'area_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<AreaAnalysis(id={self.id}, priority={self.priority_level})>"


# ============================================================================
# Chat Conversation History
# ============================================================================

class ChatMessage(Base):
    """Chat conversation history with AI assistant"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    
    # Context
    area_context = Column(JSON, nullable=True)  # Area data if message relates to specific area
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_model = Column(String(100), nullable=True)  # Only for assistant messages
    tokens_used = Column(Integer, nullable=True)  # Track API usage
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")
    
    __table_args__ = (
        Index('idx_chat_messages_user_time', 'user_id', 'created_at'),
        Index('idx_chat_messages_role', 'role'),
    )
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role={self.role})>"


# ============================================================================
# NASA API Cache
# ============================================================================

class NASACache(Base):
    """Cache for NASA API responses to avoid rate limits"""
    __tablename__ = "nasa_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Cache key components
    api_endpoint = Column(String(255), nullable=False)  # e.g., "imagery", "eonet", "power"
    cache_key = Column(String(500), unique=True, nullable=False, index=True)  # Full cache key
    
    # Geographic context (for spatial queries)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Cached data
    response_data = Column(JSON, nullable=False)  # Full API response
    status_code = Column(Integer, default=200)
    
    # Cache management
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    hit_count = Column(Integer, default=0)  # Track cache usage
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_nasa_cache_endpoint_key', 'api_endpoint', 'cache_key'),
        Index('idx_nasa_cache_expires', 'expires_at'),
        Index('idx_nasa_cache_location', 'latitude', 'longitude'),
    )
    
    def __repr__(self):
        return f"<NASACache(endpoint={self.api_endpoint}, hits={self.hit_count})>"


# ============================================================================
# Disaster Events (from NASA EONET)
# ============================================================================

class DisasterEvent(Base):
    """Natural disaster events from NASA EONET API"""
    __tablename__ = "disaster_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # EONET data
    eonet_id = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(100), nullable=False)  # e.g., "Wildfires", "Floods", "Storms"
    
    # Location (can have multiple points, store first one)
    geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status & timing
    status = Column(String(50), default="open")  # open, closed
    event_date = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    source_url = Column(String(500), nullable=True)
    raw_data = Column(JSON, nullable=True)  # Full EONET response
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_disaster_events_type', 'event_type'),
        Index('idx_disaster_events_status', 'status'),
        Index('idx_disaster_events_geometry', 'geometry', postgresql_using='gist'),
        Index('idx_disaster_events_location', 'latitude', 'longitude'),
    )
    
    def __repr__(self):
        return f"<DisasterEvent(id={self.id}, type={self.event_type}, title={self.title})>"


# ============================================================================
# City Presets (for quick access to pre-configured cities)
# ============================================================================

class CityPreset(Base):
    """Pre-configured city data for quick access"""
    __tablename__ = "city_presets"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # City info
    name = Column(String(255), nullable=False, unique=True)
    country = Column(String(100), nullable=False)
    
    # Location
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    zoom_level = Column(Integer, default=12)
    
    # Bounding box
    bounds = Column(JSON, nullable=False)  # {north, south, east, west}
    
    # Metadata
    population = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_city_presets_location', 'center_lat', 'center_lng'),
        Index('idx_city_presets_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<CityPreset(name={self.name}, country={self.country})>"

