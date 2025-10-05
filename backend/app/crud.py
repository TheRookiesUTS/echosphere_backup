"""
CRUD operations for EchoSphere database
Common queries and data access patterns
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from geoalchemy2.functions import ST_GeomFromText, ST_AsGeoJSON, ST_Distance, ST_DWithin
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from app.models.db_models import (
    User, SelectedArea, EnvironmentalMetric, AreaAnalysis,
    ChatMessage, NASACache, DisasterEvent, CityPreset,
    FloodRiskLevel, PriorityLevel, SessionStatus
)


# ============================================================================
# User Operations
# ============================================================================

def get_or_create_user(db: Session, session_id: str) -> User:
    """Get existing user by session_id or create new one"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        user = User(session_id=session_id, status=SessionStatus.ACTIVE)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update last_active timestamp
        user.last_active = datetime.utcnow()
        db.commit()
    return user


def update_user_preferences(db: Session, user_id: int, preferences: Dict[str, Any]) -> User:
    """Update user preferences"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.preferences = preferences
        db.commit()
        db.refresh(user)
    return user


# ============================================================================
# Selected Area Operations
# ============================================================================

def create_selected_area(
    db: Session,
    user_id: int,
    geometry_wkt: str,
    center_lat: float,
    center_lng: float,
    area_km2: float,
    name: Optional[str] = None
) -> SelectedArea:
    """
    Create a new selected area with PostGIS geometry
    
    Args:
        geometry_wkt: Well-Known Text representation of polygon
                     e.g., "POLYGON((lng1 lat1, lng2 lat2, ...))"
    """
    area = SelectedArea(
        user_id=user_id,
        name=name,
        geometry=geometry_wkt,
        center_lat=center_lat,
        center_lng=center_lng,
        area_km2=area_km2
    )
    db.add(area)
    db.commit()
    db.refresh(area)
    return area


def get_user_areas(db: Session, user_id: int, limit: int = 10) -> List[SelectedArea]:
    """Get user's selected areas (most recent first)"""
    return db.query(SelectedArea).filter(
        SelectedArea.user_id == user_id
    ).order_by(desc(SelectedArea.created_at)).limit(limit).all()


def get_area_with_geometry_json(db: Session, area_id: int) -> Optional[Dict[str, Any]]:
    """Get area with geometry as GeoJSON"""
    area = db.query(SelectedArea).filter(SelectedArea.id == area_id).first()
    if not area:
        return None
    
    # Convert PostGIS geometry to GeoJSON
    geojson = db.query(
        ST_AsGeoJSON(SelectedArea.geometry)
    ).filter(SelectedArea.id == area_id).scalar()
    
    return {
        "id": area.id,
        "name": area.name,
        "center_lat": area.center_lat,
        "center_lng": area.center_lng,
        "area_km2": area.area_km2,
        "geometry": json.loads(geojson) if geojson else None,
        "created_at": area.created_at.isoformat()
    }


def find_nearby_areas(
    db: Session,
    lat: float,
    lng: float,
    radius_km: float = 10
) -> List[SelectedArea]:
    """
    Find areas within radius of a point
    
    Args:
        radius_km: Search radius in kilometers
    """
    # Create point geometry
    point = f"POINT({lng} {lat})"
    
    # Query areas within distance (using ST_DWithin with geography for accurate distance)
    areas = db.query(SelectedArea).filter(
        func.ST_DWithin(
            func.ST_GeographyFromText(f'SRID=4326;{point}'),
            func.ST_GeographyFromText(func.ST_AsText(SelectedArea.geometry)),
            radius_km * 1000  # Convert km to meters
        )
    ).all()
    
    return areas


# ============================================================================
# Environmental Metrics Operations
# ============================================================================

def save_environmental_metrics(
    db: Session,
    area_id: int,
    heat_index: float,
    air_quality_index: int,
    green_coverage: float,
    flood_risk: FloodRiskLevel,
    population_estimate: Optional[int] = None,
    water_stress: Optional[float] = None,
    humidity: Optional[float] = None,
    wind_speed: Optional[float] = None,
    precipitation: Optional[float] = None,
    building_count: Optional[int] = None,
    data_source: Optional[str] = None
) -> EnvironmentalMetric:
    """Save environmental metrics for an area"""
    metric = EnvironmentalMetric(
        area_id=area_id,
        heat_index=heat_index,
        air_quality_index=air_quality_index,
        green_coverage=green_coverage,
        flood_risk=flood_risk,
        population_estimate=population_estimate,
        water_stress=water_stress,
        humidity=humidity,
        wind_speed=wind_speed,
        precipitation=precipitation,
        building_count=building_count,
        data_source=data_source
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def get_latest_metrics(db: Session, area_id: int) -> Optional[EnvironmentalMetric]:
    """Get most recent environmental metrics for an area"""
    return db.query(EnvironmentalMetric).filter(
        EnvironmentalMetric.area_id == area_id
    ).order_by(desc(EnvironmentalMetric.recorded_at)).first()


def get_metrics_time_series(
    db: Session,
    area_id: int,
    days: int = 30
) -> List[EnvironmentalMetric]:
    """Get time series of metrics for trend analysis"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    return db.query(EnvironmentalMetric).filter(
        and_(
            EnvironmentalMetric.area_id == area_id,
            EnvironmentalMetric.recorded_at >= cutoff_date
        )
    ).order_by(EnvironmentalMetric.recorded_at).all()


def get_high_risk_areas(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Get areas with high environmental risks"""
    # Join areas with their latest metrics
    results = db.query(
        SelectedArea, EnvironmentalMetric
    ).join(
        EnvironmentalMetric, SelectedArea.id == EnvironmentalMetric.area_id
    ).filter(
        and_(
            SelectedArea.user_id == user_id,
            or_(
                EnvironmentalMetric.heat_index > 32,
                EnvironmentalMetric.air_quality_index > 100,
                EnvironmentalMetric.green_coverage < 25,
                EnvironmentalMetric.flood_risk.in_([FloodRiskLevel.HIGH, FloodRiskLevel.VERY_HIGH])
            )
        )
    ).all()
    
    return [
        {
            "area": area,
            "metrics": metric,
            "risk_factors": _identify_risk_factors(metric)
        }
        for area, metric in results
    ]


def _identify_risk_factors(metric: EnvironmentalMetric) -> List[str]:
    """Helper to identify risk factors"""
    risks = []
    if metric.heat_index > 32:
        risks.append("High heat stress")
    if metric.air_quality_index > 100:
        risks.append("Poor air quality")
    if metric.green_coverage < 25:
        risks.append("Low green coverage")
    if metric.flood_risk in [FloodRiskLevel.HIGH, FloodRiskLevel.VERY_HIGH]:
        risks.append("High flood risk")
    return risks


# ============================================================================
# Area Analysis Operations
# ============================================================================

def save_area_analysis(
    db: Session,
    user_id: int,
    area_id: int,
    analysis_text: str,
    summary: Dict[str, Any],
    priority_level: PriorityLevel,
    ai_model: str = "deepseek-chat-v3.1",
    processing_time_ms: Optional[int] = None
) -> AreaAnalysis:
    """Save AI-generated area analysis"""
    analysis = AreaAnalysis(
        user_id=user_id,
        area_id=area_id,
        analysis_text=analysis_text,
        summary=summary,
        priority_level=priority_level,
        ai_model=ai_model,
        processing_time_ms=processing_time_ms
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_area_analyses(
    db: Session,
    area_id: int,
    limit: int = 5
) -> List[AreaAnalysis]:
    """Get analysis history for an area"""
    return db.query(AreaAnalysis).filter(
        AreaAnalysis.area_id == area_id
    ).order_by(desc(AreaAnalysis.created_at)).limit(limit).all()


def get_critical_analyses(db: Session, user_id: int) -> List[AreaAnalysis]:
    """Get all critical priority analyses for a user"""
    return db.query(AreaAnalysis).filter(
        and_(
            AreaAnalysis.user_id == user_id,
            AreaAnalysis.priority_level == PriorityLevel.CRITICAL
        )
    ).order_by(desc(AreaAnalysis.created_at)).all()


# ============================================================================
# Chat Message Operations
# ============================================================================

def save_chat_message(
    db: Session,
    user_id: int,
    role: str,
    content: str,
    area_context: Optional[Dict[str, Any]] = None,
    ai_model: Optional[str] = None,
    tokens_used: Optional[int] = None
) -> ChatMessage:
    """Save chat message"""
    message = ChatMessage(
        user_id=user_id,
        role=role,
        content=content,
        area_context=area_context,
        ai_model=ai_model,
        tokens_used=tokens_used
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_chat_history(
    db: Session,
    user_id: int,
    limit: int = 20
) -> List[ChatMessage]:
    """Get recent chat history"""
    return db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(desc(ChatMessage.created_at)).limit(limit).all()


def get_chat_history_formatted(db: Session, user_id: int, limit: int = 20) -> List[Dict[str, str]]:
    """Get chat history formatted for AI model"""
    messages = get_chat_history(db, user_id, limit)
    return [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(messages)  # Reverse to get chronological order
    ]


# ============================================================================
# NASA Cache Operations
# ============================================================================

def get_nasa_cache(db: Session, cache_key: str) -> Optional[NASACache]:
    """Get cached NASA API response if not expired"""
    cache_entry = db.query(NASACache).filter(
        and_(
            NASACache.cache_key == cache_key,
            NASACache.expires_at > datetime.utcnow()
        )
    ).first()
    
    if cache_entry:
        # Update hit count and last accessed
        cache_entry.hit_count += 1
        cache_entry.last_accessed = datetime.utcnow()
        db.commit()
    
    return cache_entry


def save_nasa_cache(
    db: Session,
    api_endpoint: str,
    cache_key: str,
    response_data: Dict[str, Any],
    ttl_seconds: int = 3600,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    status_code: int = 200
) -> NASACache:
    """Save NASA API response to cache"""
    expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    # Check if cache entry already exists
    existing = db.query(NASACache).filter(NASACache.cache_key == cache_key).first()
    
    if existing:
        # Update existing entry
        existing.response_data = response_data
        existing.expires_at = expires_at
        existing.last_accessed = datetime.utcnow()
        db.commit()
        return existing
    else:
        # Create new entry
        cache_entry = NASACache(
            api_endpoint=api_endpoint,
            cache_key=cache_key,
            latitude=latitude,
            longitude=longitude,
            response_data=response_data,
            status_code=status_code,
            expires_at=expires_at
        )
        db.add(cache_entry)
        db.commit()
        db.refresh(cache_entry)
        return cache_entry


def cleanup_expired_cache(db: Session) -> int:
    """Remove expired cache entries"""
    deleted = db.query(NASACache).filter(
        NASACache.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
    return deleted


# ============================================================================
# Disaster Event Operations
# ============================================================================

def save_disaster_event(
    db: Session,
    eonet_id: str,
    title: str,
    event_type: str,
    description: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    status: str = "open",
    event_date: Optional[datetime] = None,
    source_url: Optional[str] = None,
    raw_data: Optional[Dict[str, Any]] = None
) -> DisasterEvent:
    """Save or update disaster event from EONET"""
    # Check if event already exists
    existing = db.query(DisasterEvent).filter(DisasterEvent.eonet_id == eonet_id).first()
    
    if existing:
        # Update existing event
        existing.title = title
        existing.description = description
        existing.event_type = event_type
        existing.status = status
        existing.event_date = event_date
        existing.source_url = source_url
        existing.raw_data = raw_data
        existing.updated_at = datetime.utcnow()
        
        if latitude and longitude:
            existing.latitude = latitude
            existing.longitude = longitude
            existing.geometry = f"POINT({longitude} {latitude})"
        
        db.commit()
        return existing
    else:
        # Create new event
        geometry = f"POINT({longitude} {latitude})" if latitude and longitude else None
        
        event = DisasterEvent(
            eonet_id=eonet_id,
            title=title,
            description=description,
            event_type=event_type,
            geometry=geometry,
            latitude=latitude,
            longitude=longitude,
            status=status,
            event_date=event_date,
            source_url=source_url,
            raw_data=raw_data
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event


def get_nearby_disasters(
    db: Session,
    lat: float,
    lng: float,
    radius_km: float = 500,
    event_types: Optional[List[str]] = None
) -> List[DisasterEvent]:
    """Find disaster events near a location"""
    point = f"POINT({lng} {lat})"
    
    query = db.query(DisasterEvent).filter(
        func.ST_DWithin(
            func.ST_GeographyFromText(f'SRID=4326;{point}'),
            func.ST_GeographyFromText(func.ST_AsText(DisasterEvent.geometry)),
            radius_km * 1000  # Convert to meters
        ),
        DisasterEvent.status == "open"
    )
    
    if event_types:
        query = query.filter(DisasterEvent.event_type.in_(event_types))
    
    return query.order_by(desc(DisasterEvent.event_date)).all()


# ============================================================================
# City Preset Operations
# ============================================================================

def get_all_city_presets(db: Session) -> List[CityPreset]:
    """Get all active city presets"""
    return db.query(CityPreset).filter(CityPreset.is_active == True).all()


def create_city_preset(
    db: Session,
    name: str,
    country: str,
    center_lat: float,
    center_lng: float,
    bounds: Dict[str, float],
    population: Optional[int] = None,
    description: Optional[str] = None,
    zoom_level: int = 12
) -> CityPreset:
    """Create a new city preset"""
    city = CityPreset(
        name=name,
        country=country,
        center_lat=center_lat,
        center_lng=center_lng,
        zoom_level=zoom_level,
        bounds=bounds,
        population=population,
        description=description
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


# ============================================================================
# Analytics & Statistics
# ============================================================================

def get_user_statistics(db: Session, user_id: int) -> Dict[str, Any]:
    """Get user activity statistics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}
    
    areas_count = db.query(SelectedArea).filter(SelectedArea.user_id == user_id).count()
    analyses_count = db.query(AreaAnalysis).filter(AreaAnalysis.user_id == user_id).count()
    messages_count = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).count()
    
    return {
        "user_id": user_id,
        "session_id": user.session_id,
        "created_at": user.created_at.isoformat(),
        "last_active": user.last_active.isoformat(),
        "total_areas": areas_count,
        "total_analyses": analyses_count,
        "total_messages": messages_count,
        "preferences": user.preferences
    }


def get_cache_statistics(db: Session) -> Dict[str, Any]:
    """Get NASA cache performance statistics"""
    total_entries = db.query(NASACache).count()
    total_hits = db.query(func.sum(NASACache.hit_count)).scalar() or 0
    
    endpoint_stats = db.query(
        NASACache.api_endpoint,
        func.count(NASACache.id).label('count'),
        func.sum(NASACache.hit_count).label('hits')
    ).group_by(NASACache.api_endpoint).all()
    
    return {
        "total_entries": total_entries,
        "total_hits": total_hits,
        "endpoints": [
            {
                "endpoint": stat[0],
                "entries": stat[1],
                "hits": stat[2] or 0
            }
            for stat in endpoint_stats
        ]
    }

