# 📊 EchoSphere Database Models Guide

Complete guide to SQLAlchemy models with PostGIS support, optimized for Render's 1GB free tier.

---

## 📋 Table of Contents

1. [Model Overview](#model-overview)
2. [Model Descriptions](#model-descriptions)
3. [Usage Examples](#usage-examples)
4. [Database Optimization](#database-optimization)
5. [Maintenance](#maintenance)

---

## 🗂️ Model Overview

### Model Structure

```
backend/app/models/
├── base.py           # Base classes and mixins
├── area.py           # Geographic areas (PostGIS polygons)
├── analysis.py       # Analysis results and metrics
├── cache.py          # NASA API response caching
├── chat.py           # AI conversation history
├── metrics.py        # Time-series metrics
├── __init__.py       # Model exports and utilities
└── MODEL_GUIDE.md    # This file
```

### Database Schema

```
┌─────────────────┐
│     areas       │  (PostGIS polygons)
└────────┬────────┘
         │
         ├───────> area_analysis (metrics & AI insights)
         ├───────> chat_history (AI conversations)
         └───────> metrics_timeseries (historical data)

nasa_data_cache (independent caching)
```

### Key Features

- ✅ **PostGIS Support**: Full geospatial capabilities
- ✅ **JSON Columns**: Flexible data storage
- ✅ **Cascade Deletes**: Automatic cleanup
- ✅ **Composite Indexes**: Optimized queries
- ✅ **Type Hints**: Full type safety
- ✅ **UUID Primary Keys**: Better distribution
- ✅ **Automatic Timestamps**: created_at, updated_at
- ✅ **1GB Optimized**: Designed for Render free tier

---

## 📚 Model Descriptions

### 1. **Area** (`area.py`)

Stores user-selected geographic areas for analysis.

**Key Fields:**
- `id` (UUID): Unique identifier
- `name` (String): Area name (e.g., "Downtown Sibu")
- `bbox_geometry` (PostGIS Polygon): Area boundary (SRID 4326)
- `center_lat`, `center_lon` (Float): Center coordinates
- `city`, `country` (String): Location metadata

**Relationships:**
- `analyses` → Many AreaAnalysis records
- `chat_history` → Many ChatHistory records
- `metrics` → Many MetricsTimeSeries records

**Indexes:**
- GIST index on `bbox_geometry` (spatial queries)
- Index on `(city, country)` (location searches)
- Index on `(center_lat, center_lon)` (nearby searches)

**Example:**
```python
from app.models import Area
from geoalchemy2.shape import to_shape
from shapely.geometry import box

# Create area with bounding box
area = Area(
    name="Sibu Downtown",
    bbox_geometry=f"SRID=4326;{box(111.80, 2.28, 111.84, 2.32).wkt}",
    center_lat=2.30,
    center_lon=111.82,
    city="Sibu",
    country="Malaysia"
)
```

---

### 2. **AreaAnalysis** (`analysis.py`)

Stores comprehensive analysis results for areas.

**Key Fields:**
- `id` (UUID): Unique identifier
- `area_id` (UUID FK): Reference to Area
- `heat_stress_celsius` (Float): Temperature
- `air_quality_aqi` (Integer): Air quality index
- `water_stress_percent` (Float): Water stress
- `green_coverage_percent` (Float): Green space
- `flood_risk_score` (Float): Flood risk (0-10)
- `analysis_summary` (JSON): Structured analysis
- `ai_recommendations` (JSON): AI suggestions
- `risk_factors` (JSON): Identified risks
- `opportunities` (JSON): Development opportunities

**Properties:**
- `is_high_risk`: Boolean indicating critical thresholds
- `to_dict()`: Convert to dictionary

**Indexes:**
- Index on `(area_id, created_at)` (time-series)
- Index on `(flood_risk_score, heat_stress_celsius)` (risk queries)

**Example:**
```python
from app.models import AreaAnalysis

analysis = AreaAnalysis(
    area_id=area.id,
    heat_stress_celsius=34.5,
    air_quality_aqi=95,
    green_coverage_percent=28.0,
    flood_risk_score=6.5,
    analysis_summary={
        "overall_risk": "medium",
        "priority_actions": ["increase green space", "improve drainage"]
    },
    ai_recommendations=[
        "Plant 500 trees in central district",
        "Install permeable pavements"
    ],
    risk_factors=["high heat", "low green coverage"],
    data_sources=["NASA_POWER", "MODIS"]
)

# Check if high risk
if analysis.is_high_risk:
    print("⚠️ High risk area!")
```

---

### 3. **NASADataCache** (`cache.py`)

Caches NASA API responses to reduce API calls.

**Key Fields:**
- `id` (UUID): Unique identifier
- `api_source` (String): API name (POWER, MODIS, EONET, FIRMS)
- `request_params` (JSON): Request parameters (cache key)
- `response_data` (JSON): Cached response
- `bbox_geometry` (PostGIS Polygon): Spatial extent (optional)
- `fetched_at` (DateTime): Fetch timestamp
- `expires_at` (DateTime): Expiration timestamp
- `is_valid` (Boolean): Validity flag

**Properties:**
- `is_expired`: Check if expired
- `time_until_expiry`: Time remaining
- `invalidate()`: Mark as invalid
- `extend_expiry(hours)`: Extend expiration

**Indexes:**
- Index on `(api_source, is_valid)` with JSONB ops
- Index on `(expires_at, is_valid)` (cleanup)
- GIST index on `bbox_geometry` (spatial)

**Example:**
```python
from app.models import NASADataCache
from datetime import datetime, timedelta

# Cache NASA POWER data
cache = NASADataCache(
    api_source="POWER",
    request_params={
        "lat": 2.30,
        "lon": 111.82,
        "parameters": ["T2M", "PRECTOTCORR"],
        "start": "20240101",
        "end": "20240131"
    },
    response_data={
        "properties": {
            "parameter": {
                "T2M": {
                    "20240115": 32.5,
                    # ... more dates
                }
            }
        }
    },
    expires_at=datetime.utcnow() + timedelta(hours=24)
)

# Check cache
if not cache.is_expired:
    data = cache.response_data
```

---

### 4. **ChatHistory** (`chat.py`)

Stores AI chatbot conversations.

**Key Fields:**
- `id` (UUID): Unique identifier
- `session_id` (String): Session identifier
- `area_id` (UUID FK): Related area (optional)
- `user_message` (Text): User's message
- `ai_response` (Text): AI's response
- `context_data` (JSON): Additional context
- `model_used` (String): AI model name

**Methods:**
- `to_dict(include_context)`: Convert to dictionary
- `format_for_ai(messages)`: Format for AI consumption

**Indexes:**
- Index on `(session_id, created_at)` (session queries)
- Index on `(area_id, created_at)` (area-specific chats)

**Example:**
```python
from app.models import ChatHistory

# Save conversation
chat = ChatHistory(
    session_id="user_123_20241004",
    area_id=area.id,
    user_message="What are the main climate risks in Sibu?",
    ai_response="Based on the analysis, Sibu faces three main climate risks: ...",
    context_data={
        "metrics": {
            "heat_stress": 34.5,
            "aqi": 95,
            "green_coverage": 28.0
        }
    },
    model_used="deepseek/deepseek-chat"
)

# Format for AI
history = await session.execute(
    select(ChatHistory)
    .where(ChatHistory.session_id == "user_123_20241004")
    .order_by(ChatHistory.created_at)
    .limit(10)
)
formatted = ChatHistory.format_for_ai(history.scalars().all())
```

---

### 5. **MetricsTimeSeries** (`metrics.py`)

Stores historical metrics for trend analysis.

**Key Fields:**
- `id` (UUID): Unique identifier
- `area_id` (UUID FK): Reference to Area
- `metric_type` (String): Metric name (heat_stress, air_quality, etc.)
- `metric_value` (Float): Metric value
- `unit` (String): Unit of measurement
- `date_recorded` (Date): Date of measurement
- `data_source` (String): Data source

**Properties:**
- `formatted_value`: Formatted string with unit
- `to_dict()`: Convert to dictionary

**Constants:**
- `MetricType.HEAT_STRESS`, `MetricType.AIR_QUALITY`, etc.
- `MetricType.UNITS`: Unit mappings

**Indexes:**
- Index on `(area_id, metric_type, date_recorded)` (time-series)
- Index on `(data_source, date_recorded)` (source queries)
- Index on `(metric_type, date_recorded)` (type queries)

**Example:**
```python
from app.models import MetricsTimeSeries, MetricType
from datetime import date

# Record daily metric
metric = MetricsTimeSeries(
    area_id=area.id,
    metric_type=MetricType.HEAT_STRESS,
    metric_value=34.5,
    unit=MetricType.UNITS[MetricType.HEAT_STRESS],  # "celsius"
    date_recorded=date.today(),
    data_source="NASA_POWER"
)

# Get formatted value
print(metric.formatted_value)  # "34.5°C"
```

---

## 💻 Usage Examples

### Basic CRUD Operations

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Area, AreaAnalysis

async def create_area_with_analysis(session: AsyncSession):
    """Create area and analysis"""
    
    # Create area
    area = Area(
        name="Sibu Downtown",
        bbox_geometry="SRID=4326;POLYGON((111.80 2.28, 111.84 2.28, 111.84 2.32, 111.80 2.32, 111.80 2.28))",
        center_lat=2.30,
        center_lon=111.82,
        city="Sibu",
        country="Malaysia"
    )
    session.add(area)
    await session.flush()  # Get area.id
    
    # Create analysis
    analysis = AreaAnalysis(
        area_id=area.id,
        heat_stress_celsius=34.5,
        air_quality_aqi=95,
        green_coverage_percent=28.0,
        flood_risk_score=6.5
    )
    session.add(analysis)
    
    await session.commit()
    return area, analysis


async def get_area_with_latest_analysis(session: AsyncSession, area_id: str):
    """Get area with most recent analysis"""
    
    result = await session.execute(
        select(Area)
        .where(Area.id == area_id)
        .options(
            selectinload(Area.analyses).order_by(AreaAnalysis.created_at.desc())
        )
    )
    area = result.scalar_one_or_none()
    
    if area and area.analyses:
        latest_analysis = area.analyses[0]
        return area, latest_analysis
    
    return area, None
```

### Spatial Queries

```python
from geoalchemy2.functions import ST_DWithin, ST_GeographyFromText

async def find_areas_near_point(
    session: AsyncSession,
    lat: float,
    lon: float,
    radius_km: float = 10
):
    """Find areas within radius of point"""
    
    point = f"SRID=4326;POINT({lon} {lat})"
    
    result = await session.execute(
        select(Area).where(
            ST_DWithin(
                ST_GeographyFromText(Area.bbox_geometry),
                ST_GeographyFromText(point),
                radius_km * 1000  # Convert to meters
            )
        )
    )
    
    return result.scalars().all()
```

### Cache Management

```python
from datetime import datetime, timedelta
from app.models import NASADataCache

async def get_or_fetch_nasa_data(
    session: AsyncSession,
    api_source: str,
    params: dict
):
    """Get cached data or fetch from NASA"""
    
    # Check cache
    result = await session.execute(
        select(NASADataCache).where(
            NASADataCache.api_source == api_source,
            NASADataCache.request_params == params,
            NASADataCache.is_valid == True,
            NASADataCache.expires_at > datetime.utcnow()
        )
    )
    cache = result.scalar_one_or_none()
    
    if cache:
        return cache.response_data, True  # From cache
    
    # Fetch from NASA (implement your fetch logic)
    data = await fetch_from_nasa(api_source, params)
    
    # Cache the result
    cache = NASADataCache(
        api_source=api_source,
        request_params=params,
        response_data=data,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    session.add(cache)
    await session.commit()
    
    return data, False  # Freshly fetched
```

### Time-Series Analysis

```python
from datetime import date, timedelta
from app.models import MetricsTimeSeries, MetricType

async def get_metric_trend(
    session: AsyncSession,
    area_id: str,
    metric_type: str,
    days: int = 30
):
    """Get metric trend for last N days"""
    
    cutoff_date = date.today() - timedelta(days=days)
    
    result = await session.execute(
        select(MetricsTimeSeries)
        .where(
            MetricsTimeSeries.area_id == area_id,
            MetricsTimeSeries.metric_type == metric_type,
            MetricsTimeSeries.date_recorded >= cutoff_date
        )
        .order_by(MetricsTimeSeries.date_recorded)
    )
    
    metrics = result.scalars().all()
    
    return {
        "dates": [m.date_recorded.isoformat() for m in metrics],
        "values": [m.metric_value for m in metrics],
        "unit": metrics[0].unit if metrics else None
    }
```

---

## ⚡ Database Optimization

### For Render's 1GB Free Tier

**1. Use JSON Columns Efficiently**
```python
# Good: Structured, compact
analysis.analysis_summary = {
    "risk": "medium",
    "score": 6.5,
    "factors": ["heat", "low_green"]
}

# Avoid: Large, redundant data
analysis.analysis_summary = {
    "full_report": "very long text...",  # Use separate field
    "duplicate_metrics": {...}  # Already in other columns
}
```

**2. Regular Cleanup**
```python
from app.models import cleanup_old_data

# Run weekly/monthly
stats = await cleanup_old_data(
    session,
    days_to_keep=90,  # Keep 3 months
    dry_run=False
)
print(f"Deleted {stats['total_deleted']} old records")
```

**3. Monitor Database Size**
```python
from app.models import get_database_size_estimate

stats = await get_database_size_estimate(session)
print(f"Database size: {stats['database_size']}")
print(f"Total records: {stats['total_records']}")
```

**4. Efficient Queries**
```python
# Good: Use lazy loading for large collections
area = await session.get(Area, area_id)
analyses = await session.execute(
    select(AreaAnalysis)
    .where(AreaAnalysis.area_id == area_id)
    .limit(10)
)

# Avoid: Eager loading everything
area = await session.execute(
    select(Area)
    .options(selectinload(Area.analyses))  # Could load thousands
)
```

---

## 🧹 Maintenance

### Regular Maintenance Tasks

**Daily:** Clean expired cache
```bash
python -c "
from app.database import AsyncSessionLocal
from app.models import cleanup_old_data
import asyncio

async def cleanup():
    async with AsyncSessionLocal() as session:
        stats = await cleanup_old_data(session, days_to_keep=7)
        print(f'Cleaned {stats[\"cache_expired\"]} expired cache entries')

asyncio.run(cleanup())
"
```

**Weekly:** Full cleanup
```bash
python -c "
from app.database import AsyncSessionLocal
from app.models import cleanup_old_data, get_database_size_estimate
import asyncio

async def maintenance():
    async with AsyncSessionLocal() as session:
        # Cleanup
        stats = await cleanup_old_data(session, days_to_keep=90)
        print(f'Total deleted: {stats[\"total_deleted\"]}')
        
        # Check size
        size_stats = await get_database_size_estimate(session)
        print(f'Database size: {size_stats[\"database_size\"]}')

asyncio.run(maintenance())
"
```

**Monthly:** Database analysis
```sql
-- Run in psql
VACUUM ANALYZE;
REINDEX DATABASE echosphere_db;
```

---

## 🔗 Related Documentation

- **[DATABASE_README.md](../../DATABASE_README.md)** - Complete database guide
- **[USAGE_EXAMPLES.md](../../USAGE_EXAMPLES.md)** - More code examples
- **[database.py](../database.py)** - Database configuration
- **[crud.py](../crud.py)** - CRUD operations

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍

**Database**: PostgreSQL 15 + PostGIS 3.3  
**Optimization**: 1GB free tier (Render.com)  
**Focus Area**: Sibu, Sarawak, Malaysia

