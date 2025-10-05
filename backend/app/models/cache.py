"""
Cache models for NASA API responses
Reduces API calls and improves performance
"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean, Index
from geoalchemy2 import Geometry
from datetime import datetime, timedelta
from typing import Optional
from app.models.base import Base, generate_uuid


class NASADataCache(Base):
    """
    Cache for NASA API responses to avoid rate limits
    
    Stores API responses with expiration times. Uses JSON for flexible
    data storage and PostGIS geometry for spatial queries. Optimized
    for Render's 1GB limit with automatic expiration.
    
    Attributes:
        id: Unique identifier (UUID v4)
        api_source: NASA API identifier (POWER, MODIS, EONET, FIRMS)
        request_params: Request parameters as JSON (used for cache key)
        response_data: Cached API response data as JSON
        bbox_geometry: Optional spatial extent of cached data
        fetched_at: When data was fetched from NASA
        expires_at: When cache entry expires
        is_valid: Whether cache entry is still valid
    """
    __tablename__ = "nasa_data_cache"
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Unique cache entry identifier (UUID)"
    )
    
    # API source identifier
    api_source = Column(
        String(50), 
        nullable=False,
        comment="NASA API source (POWER, MODIS, EONET, FIRMS, etc.)"
    )
    
    # Request parameters as JSON for cache key matching
    request_params = Column(
        JSON, 
        nullable=False,
        comment="API request parameters (used for cache lookup)"
    )
    
    # Cached response data (compressed JSON)
    response_data = Column(
        JSON, 
        nullable=False,
        comment="Cached API response data"
    )
    
    # Optional spatial extent (for spatial cache queries)
    bbox_geometry = Column(
        Geometry(geometry_type='POLYGON', srid=4326),
        nullable=True,
        comment="Spatial extent of cached data (optional)"
    )
    
    # Cache metadata
    fetched_at = Column(
        DateTime(timezone=True), 
        default=datetime.utcnow, 
        nullable=False,
        comment="Timestamp when data was fetched from NASA"
    )
    expires_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        comment="Timestamp when cache entry expires"
    )
    is_valid = Column(
        Boolean, 
        default=True,
        comment="Whether cache entry is valid (can be invalidated manually)"
    )
    
    # Composite indexes for fast cache lookups
    __table_args__ = (
        # Primary cache lookup index (most common query)
        Index(
            'idx_cache_lookup', 
            'api_source', 
            'is_valid',
            postgresql_ops={'request_params': 'jsonb_path_ops'}
        ),
        # Index for expiration cleanup queries
        Index('idx_cache_expiry', 'expires_at', 'is_valid'),
        # Spatial index for geographic cache queries
        Index(
            'idx_cache_geometry', 
            'bbox_geometry', 
            postgresql_using='gist'
        ),
    )
    
    @property
    def is_expired(self) -> bool:
        """
        Check if cache entry has expired
        
        Returns:
            bool: True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_until_expiry(self) -> Optional[timedelta]:
        """
        Calculate time remaining until expiration
        
        Returns:
            timedelta: Time until expiry, or None if already expired
        """
        if self.is_expired:
            return None
        return self.expires_at - datetime.utcnow()
    
    def invalidate(self) -> None:
        """Mark cache entry as invalid"""
        self.is_valid = False
    
    def extend_expiry(self, hours: int = 24) -> None:
        """
        Extend expiration time
        
        Args:
            hours: Number of hours to extend by (default 24)
        """
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def __repr__(self) -> str:
        status = "expired" if self.is_expired else "valid"
        return (
            f"<NASADataCache(source={self.api_source}, "
            f"status={status}, expires={self.expires_at})>"
        )
    
    @classmethod
    def create_cache_key(cls, api_source: str, **params) -> str:
        """
        Generate cache key from parameters
        
        Args:
            api_source: NASA API source identifier
            **params: API request parameters
        
        Returns:
            str: Cache key for lookup
        """
        import json
        # Sort parameters for consistent keys
        sorted_params = json.dumps(params, sort_keys=True)
        return f"{api_source}:{sorted_params}"

