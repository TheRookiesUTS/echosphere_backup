"""
Area analysis models for storing analysis results
Contains environmental metrics and AI-generated insights
"""
from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from typing import Dict, List, Any, Optional
from app.models.base import Base, TimestampMixin, generate_uuid


class AreaAnalysis(Base, TimestampMixin):
    """
    Analysis results for geographic areas
    
    Stores comprehensive environmental metrics and AI-generated insights
    for each analyzed area. Uses JSON columns for flexible data storage
    to accommodate evolving analysis requirements.
    
    Attributes:
        id: Unique identifier (UUID v4)
        area_id: Foreign key to Area
        heat_stress_celsius: Temperature in Celsius
        air_quality_aqi: Air Quality Index (0-500 scale)
        water_stress_percent: Water stress percentage (0-100)
        green_coverage_percent: Green space coverage (0-100)
        population_density: People per square kilometer
        flood_risk_score: Flood risk on 0-10 scale
        analysis_summary: Structured JSON analysis
        ai_recommendations: Array of AI recommendations
        risk_factors: Identified risk factors
        opportunities: Development opportunities
        data_sources: APIs/datasets used
    """
    __tablename__ = "area_analysis"
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Unique analysis identifier (UUID)"
    )
    area_id = Column(
        String(36), 
        ForeignKey("areas.id", ondelete="CASCADE"), 
        nullable=False,
        comment="Reference to analyzed area"
    )
    
    # Core environmental metrics
    heat_stress_celsius = Column(
        Float, 
        nullable=True,
        comment="Temperature in Celsius (heat stress indicator)"
    )
    air_quality_aqi = Column(
        Integer, 
        nullable=True,
        comment="Air Quality Index (0-500, higher is worse)"
    )
    water_stress_percent = Column(
        Float, 
        nullable=True,
        comment="Water stress percentage (0-100)"
    )
    green_coverage_percent = Column(
        Float, 
        nullable=True,
        comment="Green space coverage percentage (0-100)"
    )
    population_density = Column(
        Float, 
        nullable=True,
        comment="People per square kilometer"
    )
    flood_risk_score = Column(
        Float, 
        nullable=True,
        comment="Flood risk score (0-10, higher is worse)"
    )
    
    # AI-generated insights (JSON for flexibility and space efficiency)
    analysis_summary = Column(
        JSON, 
        nullable=True,
        comment="Structured analysis summary (JSON)"
    )
    ai_recommendations = Column(
        JSON, 
        nullable=True,
        comment="Array of AI-generated recommendations (JSON)"
    )
    risk_factors = Column(
        JSON, 
        nullable=True,
        comment="Identified risk factors (JSON array)"
    )
    opportunities = Column(
        JSON, 
        nullable=True,
        comment="Development opportunities (JSON array)"
    )
    
    # Data provenance
    data_sources = Column(
        JSON, 
        nullable=True,
        comment="APIs/datasets used (e.g., ['NASA_POWER', 'MODIS'])"
    )
    
    # Relationships
    area = relationship("Area", back_populates="analyses")
    
    # Indexes for common queries
    __table_args__ = (
        # Index for finding analyses by area and time
        Index('idx_analysis_area_time', 'area_id', 'created_at'),
        # Index for filtering by risk levels
        Index('idx_analysis_risks', 'flood_risk_score', 'heat_stress_celsius'),
    )
    
    def __repr__(self) -> str:
        return (
            f"<AreaAnalysis(id={self.id}, area={self.area_id}, "
            f"aqi={self.air_quality_aqi}, heat={self.heat_stress_celsius})>"
        )
    
    @property
    def is_high_risk(self) -> bool:
        """
        Check if area has high risk based on multiple factors
        
        Returns:
            bool: True if any critical thresholds are exceeded
        """
        return any([
            self.heat_stress_celsius and self.heat_stress_celsius > 35,
            self.air_quality_aqi and self.air_quality_aqi > 150,
            self.flood_risk_score and self.flood_risk_score > 7,
            self.green_coverage_percent and self.green_coverage_percent < 15
        ])
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert analysis to dictionary for JSON serialization
        
        Returns:
            dict: Analysis data as dictionary
        """
        return {
            "id": self.id,
            "area_id": self.area_id,
            "metrics": {
                "heat_stress_celsius": self.heat_stress_celsius,
                "air_quality_aqi": self.air_quality_aqi,
                "water_stress_percent": self.water_stress_percent,
                "green_coverage_percent": self.green_coverage_percent,
                "population_density": self.population_density,
                "flood_risk_score": self.flood_risk_score,
            },
            "analysis_summary": self.analysis_summary,
            "ai_recommendations": self.ai_recommendations,
            "risk_factors": self.risk_factors,
            "opportunities": self.opportunities,
            "data_sources": self.data_sources,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_high_risk": self.is_high_risk
        }

