# 🚀 EchoSphere Database Usage Examples

Practical examples for using the database layer in your application.

---

## 📋 Table of Contents

1. [FastAPI Integration](#fastapi-integration)
2. [Common Queries](#common-queries)
3. [Geospatial Operations](#geospatial-operations)
4. [Caching NASA Data](#caching-nasa-data)
5. [Chat History Management](#chat-history-management)
6. [Analytics & Statistics](#analytics--statistics)

---

## 🔌 FastAPI Integration

### Basic Endpoint with Database

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_or_create_user, save_chat_message

router = APIRouter(prefix="/api", tags=["example"])

@router.post("/chat-example")
async def chat_example(
    message: str,
    session_id: str,
    db: Session = Depends(get_db)
):
    # Get or create user
    user = get_or_create_user(db, session_id)
    
    # Save message
    chat_msg = save_chat_message(
        db, 
        user_id=user.id,
        role="user",
        content=message
    )
    
    return {
        "user_id": user.id,
        "message_id": chat_msg.id,
        "saved_at": chat_msg.created_at
    }
```

### Health Check with Database Status

```python
from fastapi import APIRouter
from app.database import get_db_health

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
async def health_check():
    db_health = get_db_health()
    
    return {
        "status": "ok",
        "database": db_health["database"],
        "postgis": db_health["postgis"],
        "details": db_health["details"]
    }
```

---

## 📝 Common Queries

### 1. User Management

```python
from app.crud import get_or_create_user, update_user_preferences
from app.database import get_db_context

# Get or create user by session ID
with get_db_context() as db:
    user = get_or_create_user(db, session_id="abc123")
    print(f"User ID: {user.id}")
    
    # Update preferences
    user = update_user_preferences(
        db, 
        user_id=user.id,
        preferences={
            "theme": "dark",
            "default_city": "Sibu",
            "units": "metric"
        }
    )
```

### 2. Save Area Selection

```python
from app.crud import create_selected_area
from app.database import get_db_context

# Create a selected area (polygon)
with get_db_context() as db:
    # WKT format: POLYGON((lng lat, lng lat, ...))
    geometry_wkt = "POLYGON((111.80 2.28, 111.84 2.28, 111.84 2.32, 111.80 2.32, 111.80 2.28))"
    
    area = create_selected_area(
        db,
        user_id=1,
        geometry_wkt=geometry_wkt,
        center_lat=2.30,
        center_lng=111.82,
        area_km2=12.5,
        name="Downtown Sibu"
    )
    
    print(f"Area ID: {area.id}")
```

### 3. Save Environmental Metrics

```python
from app.crud import save_environmental_metrics
from app.models.db_models import FloodRiskLevel
from app.database import get_db_context

with get_db_context() as db:
    metrics = save_environmental_metrics(
        db,
        area_id=1,
        heat_index=33.5,
        air_quality_index=85,
        green_coverage=32.0,
        flood_risk=FloodRiskLevel.MEDIUM,
        population_estimate=50000,
        water_stress=45.0,
        humidity=78.0,
        wind_speed=2.5,
        data_source="NASA_POWER"
    )
    
    print(f"Metrics saved: {metrics.id}")
```

### 4. Get Time Series Data

```python
from app.crud import get_metrics_time_series
from app.database import get_db_context

with get_db_context() as db:
    # Get last 30 days of metrics
    metrics_list = get_metrics_time_series(db, area_id=1, days=30)
    
    # Extract heat index trend
    heat_trend = [m.heat_index for m in metrics_list]
    dates = [m.recorded_at for m in metrics_list]
    
    print(f"Heat trend: {heat_trend}")
```

### 5. Save Analysis Results

```python
from app.crud import save_area_analysis
from app.models.db_models import PriorityLevel
from app.database import get_db_context

with get_db_context() as db:
    analysis = save_area_analysis(
        db,
        user_id=1,
        area_id=1,
        analysis_text="## Analysis Results\n\nHigh heat stress detected...",
        summary={
            "issues": ["High heat stress", "Low green coverage"],
            "recommendations": ["Plant more trees", "Create cooling centers"],
            "priorityLevel": "High"
        },
        priority_level=PriorityLevel.HIGH,
        ai_model="deepseek-chat-v3.1",
        processing_time_ms=1250
    )
    
    print(f"Analysis ID: {analysis.id}")
```

---

## 🗺️ Geospatial Operations

### 1. Find Nearby Areas

```python
from app.crud import find_nearby_areas
from app.database import get_db_context

# Find areas within 10km of Sibu
with get_db_context() as db:
    nearby = find_nearby_areas(
        db,
        lat=2.30,
        lng=111.82,
        radius_km=10
    )
    
    for area in nearby:
        print(f"Area: {area.name}, Distance: ~{area.area_km2} km²")
```

### 2. Get Area as GeoJSON

```python
from app.crud import get_area_with_geometry_json
from app.database import get_db_context

with get_db_context() as db:
    area_geojson = get_area_with_geometry_json(db, area_id=1)
    
    # Returns:
    # {
    #   "id": 1,
    #   "name": "Downtown Sibu",
    #   "center_lat": 2.30,
    #   "center_lng": 111.82,
    #   "area_km2": 12.5,
    #   "geometry": {
    #     "type": "Polygon",
    #     "coordinates": [[[lng, lat], ...]]
    #   }
    # }
```

### 3. Find Nearby Disasters

```python
from app.crud import get_nearby_disasters
from app.database import get_db_context

with get_db_context() as db:
    disasters = get_nearby_disasters(
        db,
        lat=2.30,
        lng=111.82,
        radius_km=500,
        event_types=["Wildfires", "Floods", "Severe Storms"]
    )
    
    for event in disasters:
        print(f"Event: {event.title} ({event.event_type})")
        print(f"Status: {event.status}")
```

### 4. Direct PostGIS Query

```python
from app.database import get_db_context
from sqlalchemy import text

with get_db_context() as db:
    # Calculate distance between two points
    result = db.execute(text("""
        SELECT ST_Distance(
            ST_GeographyFromText('SRID=4326;POINT(111.82 2.30)'),
            ST_GeographyFromText('SRID=4326;POINT(111.85 2.35)')
        ) / 1000 as distance_km
    """))
    
    distance = result.fetchone()[0]
    print(f"Distance: {distance:.2f} km")
```

---

## 💾 Caching NASA Data

### 1. Save to Cache

```python
from app.crud import save_nasa_cache
from app.database import get_db_context

with get_db_context() as db:
    cache_entry = save_nasa_cache(
        db,
        api_endpoint="imagery",
        cache_key="imagery_2.30_111.82_0.1",
        response_data={
            "url": "https://...",
            "date": "2024-10-01",
            "cloud_score": 15
        },
        ttl_seconds=3600,  # 1 hour
        latitude=2.30,
        longitude=111.82
    )
    
    print(f"Cached: {cache_entry.id}")
```

### 2. Retrieve from Cache

```python
from app.crud import get_nasa_cache
from app.database import get_db_context

with get_db_context() as db:
    cache_key = "imagery_2.30_111.82_0.1"
    cached = get_nasa_cache(db, cache_key)
    
    if cached:
        print(f"Cache HIT! Hits: {cached.hit_count}")
        print(f"Data: {cached.response_data}")
    else:
        print("Cache MISS - fetch from API")
```

### 3. Cleanup Expired Cache

```python
from app.database import cleanup_expired_cache

# Remove expired entries
deleted = cleanup_expired_cache()
print(f"Deleted {deleted} expired cache entries")
```

---

## 💬 Chat History Management

### 1. Save Chat Messages

```python
from app.crud import save_chat_message
from app.database import get_db_context

with get_db_context() as db:
    # User message
    save_chat_message(
        db,
        user_id=1,
        role="user",
        content="What are the main climate risks in Sibu?",
        area_context={"area_id": 1, "city": "Sibu"}
    )
    
    # Assistant response
    save_chat_message(
        db,
        user_id=1,
        role="assistant",
        content="Based on the analysis, the main risks are...",
        ai_model="deepseek-chat-v3.1",
        tokens_used=350
    )
```

### 2. Retrieve Chat History

```python
from app.crud import get_chat_history_formatted
from app.database import get_db_context

with get_db_context() as db:
    # Get last 20 messages formatted for AI
    history = get_chat_history_formatted(db, user_id=1, limit=20)
    
    # Returns:
    # [
    #   {"role": "user", "content": "..."},
    #   {"role": "assistant", "content": "..."},
    #   ...
    # ]
```

---

## 📊 Analytics & Statistics

### 1. User Statistics

```python
from app.crud import get_user_statistics
from app.database import get_db_context

with get_db_context() as db:
    stats = get_user_statistics(db, user_id=1)
    
    print(f"Total areas analyzed: {stats['total_areas']}")
    print(f"Total analyses: {stats['total_analyses']}")
    print(f"Total messages: {stats['total_messages']}")
```

### 2. Cache Performance

```python
from app.crud import get_cache_statistics
from app.database import get_db_context

with get_db_context() as db:
    cache_stats = get_cache_statistics(db)
    
    print(f"Total cache entries: {cache_stats['total_entries']}")
    print(f"Total cache hits: {cache_stats['total_hits']}")
    
    for endpoint in cache_stats['endpoints']:
        print(f"  {endpoint['endpoint']}: {endpoint['hits']} hits")
```

### 3. High Risk Areas

```python
from app.crud import get_high_risk_areas
from app.database import get_db_context

with get_db_context() as db:
    high_risk = get_high_risk_areas(db, user_id=1)
    
    for item in high_risk:
        area = item['area']
        metrics = item['metrics']
        risks = item['risk_factors']
        
        print(f"Area: {area.name}")
        print(f"Risks: {', '.join(risks)}")
```

### 4. Critical Analyses

```python
from app.crud import get_critical_analyses
from app.database import get_db_context

with get_db_context() as db:
    critical = get_critical_analyses(db, user_id=1)
    
    print(f"Found {len(critical)} critical priority analyses")
    for analysis in critical:
        print(f"  - Area ID: {analysis.area_id}")
        print(f"    Priority: {analysis.priority_level}")
```

---

## 🔄 Full Workflow Example

```python
from app.database import get_db_context
from app.crud import (
    get_or_create_user,
    create_selected_area,
    save_environmental_metrics,
    save_area_analysis,
    save_chat_message
)
from app.models.db_models import FloodRiskLevel, PriorityLevel

# Complete workflow: User selects area → Analyze → Save results → Chat
with get_db_context() as db:
    # 1. Get/create user
    user = get_or_create_user(db, session_id="demo_session_123")
    
    # 2. Create selected area
    area = create_selected_area(
        db,
        user_id=user.id,
        geometry_wkt="POLYGON((111.80 2.28, 111.84 2.28, 111.84 2.32, 111.80 2.32, 111.80 2.28))",
        center_lat=2.30,
        center_lng=111.82,
        area_km2=12.5,
        name="Test Area - Sibu"
    )
    
    # 3. Save environmental metrics
    metrics = save_environmental_metrics(
        db,
        area_id=area.id,
        heat_index=34.0,
        air_quality_index=105,
        green_coverage=22.0,
        flood_risk=FloodRiskLevel.HIGH,
        population_estimate=45000
    )
    
    # 4. Save analysis results
    analysis = save_area_analysis(
        db,
        user_id=user.id,
        area_id=area.id,
        analysis_text="## Critical Analysis\n\nHigh heat and air quality issues...",
        summary={
            "issues": ["High heat", "Poor air quality", "Low green coverage"],
            "recommendations": ["Urban cooling", "Green infrastructure"],
            "priorityLevel": "Critical"
        },
        priority_level=PriorityLevel.CRITICAL
    )
    
    # 5. Save chat interaction
    save_chat_message(
        db,
        user_id=user.id,
        role="user",
        content="What should we prioritize?",
        area_context={"area_id": area.id}
    )
    
    save_chat_message(
        db,
        user_id=user.id,
        role="assistant",
        content="Priority 1: Urban cooling strategies...",
        ai_model="deepseek-chat-v3.1"
    )
    
    print("✅ Complete workflow saved!")
    print(f"   User: {user.session_id}")
    print(f"   Area: {area.name}")
    print(f"   Analysis Priority: {analysis.priority_level}")
```

---

## 🧹 Maintenance Tasks

### Run Daily Cleanup (Background Job)

```python
from app.database import cleanup_expired_cache, cleanup_old_chat_messages
import schedule
import time

def daily_cleanup():
    """Run daily maintenance tasks"""
    print("🧹 Running daily cleanup...")
    
    # Cleanup expired cache (free up storage)
    deleted_cache = cleanup_expired_cache()
    print(f"   Deleted {deleted_cache} expired cache entries")
    
    # Cleanup old chat messages (retain last 30 days)
    deleted_chats = cleanup_old_chat_messages(days=30)
    print(f"   Deleted {deleted_chats} old chat messages")
    
    print("✅ Cleanup complete")

# Schedule for 2 AM daily
schedule.every().day.at("02:00").do(daily_cleanup)

# Or run immediately
if __name__ == "__main__":
    daily_cleanup()
    
    # Keep running for scheduled tasks
    # while True:
    #     schedule.run_pending()
    #     time.sleep(3600)  # Check every hour
```

---

## 🔍 Advanced Queries

### Complex Geospatial Analysis

```python
from app.database import get_db_context
from sqlalchemy import text

with get_db_context() as db:
    # Find areas within 20km of a point, with high heat index
    result = db.execute(text("""
        SELECT 
            sa.id,
            sa.name,
            em.heat_index,
            ST_Distance(
                ST_GeographyFromText('SRID=4326;POINT(111.82 2.30)'),
                ST_GeographyFromText(ST_AsText(sa.geometry))
            ) / 1000 as distance_km
        FROM selected_areas sa
        JOIN environmental_metrics em ON sa.id = em.area_id
        WHERE ST_DWithin(
            ST_GeographyFromText('SRID=4326;POINT(111.82 2.30)'),
            ST_GeographyFromText(ST_AsText(sa.geometry)),
            20000  -- 20km in meters
        )
        AND em.heat_index > 32
        ORDER BY em.heat_index DESC
    """))
    
    for row in result:
        print(f"{row.name}: {row.heat_index}°C, {row.distance_km:.1f}km away")
```

---

## 📚 Additional Resources

- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [PostGIS Functions](https://postgis.net/docs/reference.html)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

Need more examples? Check `backend/app/crud.py` for all available functions!

