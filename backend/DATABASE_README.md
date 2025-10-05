# 🗄️ EchoSphere Database Layer

Complete database layer for EchoSphere urban resilience platform with PostgreSQL + PostGIS support.

---

## 🎯 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements/linux.txt
pip install -r requirements/database.txt
```

### 2. Set Up PostgreSQL

```bash
# Install PostgreSQL + PostGIS (see DATABASE_SETUP.md for your OS)

# Create database
sudo -u postgres psql
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# Enable PostGIS
psql -U echosphere -d echosphere_db
CREATE EXTENSION postgis;
\q
```

### 3. Configure Environment

Create `backend/.env`:

```env
# Database
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db

# API Keys
OPENROUTER_API_KEY=your_key_here
NASA_API_KEY=your_key_here
```

### 4. Initialize Database

```bash
cd backend
python init_db.py
```

This will:
- ✅ Create all tables
- ✅ Enable PostGIS
- ✅ Seed Malaysian city presets
- ✅ Verify setup

### 5. Start Using

```python
from app.database import get_db_context
from app.crud import get_or_create_user

with get_db_context() as db:
    user = get_or_create_user(db, session_id="test_123")
    print(f"User ID: {user.id}")
```

---

## 📁 File Structure

```
backend/
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── env.py
│   └── script.py.mako
├── alembic.ini                 # Alembic configuration
├── init_db.py                  # Database initialization script
├── app/
│   ├── database.py             # Database connection & config
│   ├── crud.py                 # CRUD operations & queries
│   ├── config.py               # Environment settings
│   └── models/
│       ├── db_models.py        # SQLAlchemy models
│       └── schemas.py          # Pydantic schemas
└── requirements/
    └── database.txt            # Database dependencies
```

---

## 🗂️ Database Schema

### Core Tables

#### **users**
Tracks user sessions and preferences.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| session_id | String | Unique session identifier |
| name | String | Optional user name |
| email | String | Optional email |
| created_at | DateTime | Creation timestamp |
| last_active | DateTime | Last activity timestamp |
| status | Enum | active, inactive, expired |
| preferences | JSON | User preferences |

#### **selected_areas**
Geospatial polygons for selected urban areas.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| name | String | Optional area name |
| **geometry** | **PostGIS Polygon** | Geospatial boundary |
| center_lat | Float | Center latitude |
| center_lng | Float | Center longitude |
| area_km2 | Float | Area in square kilometers |
| created_at | DateTime | Creation timestamp |

**Indexes**:
- GIST index on geometry (spatial queries)
- Index on center coordinates

#### **environmental_metrics**
Time-series environmental data.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| area_id | Integer | Foreign key to selected_areas |
| heat_index | Float | Temperature in °C |
| air_quality_index | Integer | AQI value |
| green_coverage | Float | Percentage |
| water_stress | Float | Percentage |
| flood_risk | Enum | Very Low to Very High |
| population_estimate | Integer | Population count |
| building_count | Integer | Number of buildings |
| recorded_at | DateTime | Measurement timestamp |

**Indexes**:
- Composite index on (area_id, recorded_at) for time-series queries

#### **area_analyses**
AI-generated analysis results.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| area_id | Integer | Foreign key to selected_areas |
| analysis_text | Text | Full markdown analysis |
| summary | JSON | Structured summary |
| priority_level | Enum | Low, Medium, High, Critical |
| ai_model | String | Model identifier |
| processing_time_ms | Integer | Performance tracking |
| created_at | DateTime | Creation timestamp |

#### **chat_messages**
Chatbot conversation history.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| role | String | 'user' or 'assistant' |
| content | Text | Message content |
| area_context | JSON | Related area data |
| ai_model | String | Model used (assistant only) |
| tokens_used | Integer | API usage tracking |
| created_at | DateTime | Timestamp |

#### **nasa_cache**
Caches NASA API responses.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| api_endpoint | String | e.g., 'imagery', 'eonet' |
| cache_key | String | Unique cache identifier |
| latitude | Float | Optional location |
| longitude | Float | Optional location |
| response_data | JSON | Cached API response |
| expires_at | DateTime | Expiration timestamp |
| hit_count | Integer | Usage tracking |

#### **disaster_events**
NASA EONET natural disaster events.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| eonet_id | String | EONET event ID |
| title | String | Event title |
| event_type | String | Wildfires, Floods, etc. |
| **geometry** | **PostGIS Point** | Event location |
| latitude | Float | Latitude |
| longitude | Float | Longitude |
| status | String | open, closed |
| event_date | DateTime | Event timestamp |
| raw_data | JSON | Full EONET data |

#### **city_presets**
Pre-configured city locations.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | City name |
| country | String | Country |
| center_lat | Float | Center latitude |
| center_lng | Float | Center longitude |
| zoom_level | Integer | Default map zoom |
| bounds | JSON | Map boundaries |
| population | Integer | Population |
| is_active | Boolean | Active status |

---

## 🔧 Common Operations

### User Management

```python
from app.crud import get_or_create_user, update_user_preferences

# Get or create user
user = get_or_create_user(db, session_id="abc123")

# Update preferences
user = update_user_preferences(db, user.id, {
    "theme": "dark",
    "default_city": "Sibu"
})
```

### Geospatial Operations

```python
from app.crud import create_selected_area, find_nearby_areas

# Create area
area = create_selected_area(
    db,
    user_id=1,
    geometry_wkt="POLYGON((111.80 2.28, 111.84 2.28, 111.84 2.32, 111.80 2.32, 111.80 2.28))",
    center_lat=2.30,
    center_lng=111.82,
    area_km2=12.5,
    name="Sibu Downtown"
)

# Find nearby areas (within 10km)
nearby = find_nearby_areas(db, lat=2.30, lng=111.82, radius_km=10)
```

### Environmental Data

```python
from app.crud import save_environmental_metrics, get_metrics_time_series
from app.models.db_models import FloodRiskLevel

# Save metrics
metrics = save_environmental_metrics(
    db,
    area_id=1,
    heat_index=33.5,
    air_quality_index=95,
    green_coverage=28.0,
    flood_risk=FloodRiskLevel.MEDIUM,
    population_estimate=50000
)

# Get time series (last 30 days)
history = get_metrics_time_series(db, area_id=1, days=30)
```

### NASA Cache

```python
from app.crud import get_nasa_cache, save_nasa_cache

# Check cache
cache_key = "imagery_2.30_111.82_0.1"
cached = get_nasa_cache(db, cache_key)

if cached:
    data = cached.response_data
else:
    # Fetch from API and cache
    data = await fetch_from_nasa_api()
    save_nasa_cache(
        db,
        api_endpoint="imagery",
        cache_key=cache_key,
        response_data=data,
        ttl_seconds=3600
    )
```

---

## 🔄 Migrations

### Create Migration

```bash
cd backend

# After modifying models in db_models.py
alembic revision --autogenerate -m "Add new field to table"

# Review generated migration in alembic/versions/
# Edit if needed

# Apply migration
alembic upgrade head
```

### Common Migration Commands

```bash
# Check current version
alembic current

# Apply all pending migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# View history
alembic history

# Reset to specific version
alembic downgrade <revision_id>
alembic upgrade <revision_id>
```

---

## 📊 Performance Optimization

### Indexes

All tables have optimized indexes:
- **Spatial indexes**: GIST indexes on geometry columns
- **Time-series indexes**: Composite indexes on (id, timestamp)
- **Foreign keys**: Automatic indexes on all foreign keys
- **Unique constraints**: Indexes on unique fields

### Connection Pooling

Optimized for Render.com free tier:
```python
# In app/database.py
pool_size=5          # Max 5 persistent connections
max_overflow=2       # Max 2 additional connections
pool_pre_ping=True   # Health check before using
pool_recycle=300     # Recycle every 5 minutes
```

### Caching Strategy

- **NASA API responses**: Cached for 1 hour (configurable)
- **Automatic cleanup**: Expired cache entries removed
- **Hit counting**: Track cache performance

---

## 🧹 Maintenance

### Daily Cleanup (Automated)

```python
from app.database import cleanup_expired_cache

# Remove expired cache entries
deleted = cleanup_expired_cache()
print(f"Deleted {deleted} expired entries")
```

### Weekly Cleanup

```python
from app.database import cleanup_old_chat_messages

# Remove messages older than 30 days
deleted = cleanup_old_chat_messages(days=30)
```

### Database Health Check

```python
from app.database import get_db_health

health = get_db_health()
print(f"Database: {health['database']}")
print(f"PostGIS: {health['postgis']}")
print(f"Pool size: {health['details']['pool_size']}")
```

---

## 📚 Documentation Files

- **`DATABASE_SETUP.md`**: Complete setup guide for all operating systems
- **`USAGE_EXAMPLES.md`**: Comprehensive code examples and queries
- **`DEPLOYMENT.md`**: Render.com deployment guide
- **`DATABASE_README.md`**: This file - overview and quick reference

---

## 🐛 Troubleshooting

### Connection Issues

```bash
# Test connection
python -c "from app.database import check_db_connection; check_db_connection()"

# Test PostGIS
python -c "from app.database import check_postgis; check_postgis()"
```

### Reset Database

```bash
# WARNING: This will delete all data!
cd backend
python init_db.py
# Choose "y" when prompted to drop tables
```

### Check Migration Status

```bash
cd backend
alembic current
alembic history
```

---

## 🔗 API Integration

### FastAPI Dependency

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/example")
async def example(db: Session = Depends(get_db)):
    # Use db for queries
    from app.crud import get_all_city_presets
    cities = get_all_city_presets(db)
    return {"cities": cities}
```

### Context Manager (Non-FastAPI)

```python
from app.database import get_db_context

with get_db_context() as db:
    # Your database operations
    pass
    # Automatically commits on success, rollbacks on error
```

---

## ✅ Verification Checklist

After setup:
- [ ] Database created
- [ ] PostGIS enabled
- [ ] Tables created (9 tables)
- [ ] City presets seeded (8 cities)
- [ ] Health check passes
- [ ] Migrations work
- [ ] Queries execute successfully

---

## 🚀 Next Steps

1. **Integrate with existing endpoints**:
   - Update chat.py to use database for history
   - Cache NASA responses in database
   - Store analysis results

2. **Add new features**:
   - User authentication
   - Area sharing/collaboration
   - Historical trend analysis
   - Export reports

3. **Deploy to production**:
   - Follow DEPLOYMENT.md
   - Set up monitoring
   - Configure backups

---

## 📞 Support

**Questions?**
- Check USAGE_EXAMPLES.md for code examples
- Review DATABASE_SETUP.md for installation help
- See DEPLOYMENT.md for Render.com deployment

**Issues?**
- Check troubleshooting section
- Review logs in Render dashboard
- Verify environment variables

---

Built for NASA Space Apps Challenge 2025 🚀🌍

Focused on Sibu & Sibu Jaya, Sarawak, Malaysia
Optimized for Render.com free tier deployment

