"""
Metrics time-series models for historical tracking
Stores environmental metrics over time for trend analysis
"""
from sqlalchemy import Column, String, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from typing import Dict, Any
from datetime import date
from app.models.base import Base, TimestampMixin, generate_uuid


class MetricsTimeSeries(Base, TimestampMixin):
    """
    Historical metrics for trend analysis
    
    Stores environmental metrics as time-series data for analyzing
    trends over time. Each record represents a single metric value
    for a specific area on a specific date. Optimized for time-series
    queries with composite indexes.
    
    Attributes:
        id: Unique identifier (UUID v4)
        area_id: Foreign key to Area
        metric_type: Type of metric (heat, aqi, water, green, etc.)
        metric_value: Numeric value of the metric
        unit: Unit of measurement (celsius, aqi, percent, etc.)
        date_recorded: Date when metric was recorded
        data_source: Source of the data (NASA POWER, MODIS, etc.)
    """
    __tablename__ = "metrics_timeseries"
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Unique metric entry identifier (UUID)"
    )
    area_id = Column(
        String(36), 
        ForeignKey("areas.id", ondelete="CASCADE"), 
        nullable=False,
        comment="Reference to area being measured"
    )
    
    # Metric identification
    metric_type = Column(
        String(50), 
        nullable=False,
        comment="Metric type (heat, aqi, water_stress, green_coverage, etc.)"
    )
    metric_value = Column(
        Float, 
        nullable=False,
        comment="Numeric metric value"
    )
    unit = Column(
        String(20), 
        nullable=True,
        comment="Unit of measurement (celsius, aqi, percent, etc.)"
    )
    
    # Time dimension
    date_recorded = Column(
        Date, 
        nullable=False,
        comment="Date when metric was recorded"
    )
    
    # Data provenance
    data_source = Column(
        String(50), 
        nullable=True,
        comment="Data source (NASA POWER, MODIS, manual, etc.)"
    )
    
    # Relationships
    area = relationship("Area", back_populates="metrics")
    
    # Composite indexes for efficient time-series queries
    __table_args__ = (
        # Primary index for time-series queries (most common)
        Index(
            'idx_metrics_time', 
            'area_id', 
            'metric_type', 
            'date_recorded'
        ),
        # Index for data source queries
        Index('idx_metrics_source', 'data_source', 'date_recorded'),
        # Index for metric type queries across areas
        Index('idx_metrics_type', 'metric_type', 'date_recorded'),
    )
    
    def __repr__(self) -> str:
        return (
            f"<MetricsTimeSeries(type={self.metric_type}, "
            f"value={self.metric_value}{self.unit or ''}, "
            f"date={self.date_recorded})>"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metric to dictionary for JSON serialization
        
        Returns:
            dict: Metric data as dictionary
        """
        return {
            "id": self.id,
            "area_id": self.area_id,
            "metric_type": self.metric_type,
            "metric_value": self.metric_value,
            "unit": self.unit,
            "date_recorded": self.date_recorded.isoformat() if self.date_recorded else None,
            "data_source": self.data_source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    @property
    def formatted_value(self) -> str:
        """
        Get formatted metric value with unit
        
        Returns:
            str: Formatted value (e.g., "32.5°C", "95 AQI")
        """
        if self.unit == "celsius":
            return f"{self.metric_value}°C"
        elif self.unit == "aqi":
            return f"{int(self.metric_value)} AQI"
        elif self.unit == "percent":
            return f"{self.metric_value}%"
        elif self.unit:
            return f"{self.metric_value} {self.unit}"
        else:
            return str(self.metric_value)


class MetricType:
    """
    Constants for common metric types
    Ensures consistency across the application
    """
    HEAT_STRESS = "heat_stress"
    AIR_QUALITY = "air_quality"
    WATER_STRESS = "water_stress"
    GREEN_COVERAGE = "green_coverage"
    FLOOD_RISK = "flood_risk"
    POPULATION_DENSITY = "population_density"
    PRECIPITATION = "precipitation"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    
    # All valid metric types
    ALL = [
        HEAT_STRESS,
        AIR_QUALITY,
        WATER_STRESS,
        GREEN_COVERAGE,
        FLOOD_RISK,
        POPULATION_DENSITY,
        PRECIPITATION,
        HUMIDITY,
        WIND_SPEED,
    ]
    
    # Units for each metric type
    UNITS = {
        HEAT_STRESS: "celsius",
        AIR_QUALITY: "aqi",
        WATER_STRESS: "percent",
        GREEN_COVERAGE: "percent",
        FLOOD_RISK: "score",
        POPULATION_DENSITY: "per_km2",
        PRECIPITATION: "mm",
        HUMIDITY: "percent",
        WIND_SPEED: "m/s",
    }

