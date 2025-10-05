"""
Geographic area models for spatial analysis
Stores user-selected areas with PostGIS geometry support
"""
from sqlalchemy import Column, String, Float, Text, Index
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.models.base import Base, TimestampMixin, generate_uuid


class Area(Base, TimestampMixin):
    """
    User-selected geographic areas for analysis
    
    Stores bounding boxes as PostGIS polygons for spatial queries
    and analysis. Each area represents a geographic region that users
    want to analyze for urban resilience metrics.
    
    Attributes:
        id: Unique identifier (UUID v4)
        name: Human-readable name for the area
        bbox_geometry: PostGIS polygon representing the area boundary
        center_lat: Center latitude for quick reference
        center_lon: Center longitude for quick reference
        city: City name (optional)
        country: Country name (defaults to Malaysia)
        description: Optional description
    """
    __tablename__ = "areas"
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Unique area identifier (UUID)"
    )
    name = Column(
        String(255), 
        nullable=False,
        comment="Area name (e.g., 'Downtown Sibu')"
    )
    
    # Bounding box as PostGIS polygon (SRID 4326 = WGS84)
    bbox_geometry = Column(
        Geometry(geometry_type='POLYGON', srid=4326),
        nullable=False,
        comment="Area boundary as PostGIS polygon"
    )
    
    # Center point for quick reference and sorting
    center_lat = Column(
        Float, 
        nullable=False,
        comment="Center latitude"
    )
    center_lon = Column(
        Float, 
        nullable=False,
        comment="Center longitude"
    )
    
    # Location metadata
    city = Column(
        String(100), 
        nullable=True,
        comment="City name (e.g., 'Sibu')"
    )
    country = Column(
        String(100), 
        default="Malaysia",
        comment="Country name"
    )
    
    # Optional description
    description = Column(
        Text, 
        nullable=True,
        comment="User-provided description of the area"
    )
    
    # Relationships
    analyses = relationship(
        "AreaAnalysis",
        back_populates="area",
        cascade="all, delete-orphan",
        lazy="dynamic"  # Load on demand to save memory
    )
    
    chat_history = relationship(
        "ChatHistory",
        back_populates="area",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    metrics = relationship(
        "MetricsTimeSeries",
        back_populates="area",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Indexes for performance
    __table_args__ = (
        # Spatial index (GIST) for fast geometric queries
        Index(
            'idx_areas_geometry', 
            'bbox_geometry', 
            postgresql_using='gist'
        ),
        # Index for location-based searches
        Index('idx_areas_location', 'city', 'country'),
        # Index for center coordinates (for nearby searches)
        Index('idx_areas_center', 'center_lat', 'center_lon'),
    )
    
    def __repr__(self) -> str:
        return f"<Area(id={self.id}, name={self.name}, city={self.city})>"

