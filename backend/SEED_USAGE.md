# 🌱 Database Seeding Guide

Complete guide for seeding EchoSphere database with Sibu & Sibu Jaya sample data.

## 📋 Prerequisites

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements/database.txt
```

### 2. Database Setup
- PostgreSQL 15+ with PostGIS extension
- Database `echosphere_db` created
- User `echosphere` with proper permissions

### 3. Environment Configuration
Create `backend/.env`:
```env
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db
OPENROUTER_API_KEY=your_key_here
NASA_API_KEY=your_key_here
```

### 4. Run Migrations
```bash
cd backend
alembic upgrade head
```

## 🚀 Usage

### Basic Seeding
```bash
cd backend
python -m app.db.seed
```

### Clear and Reseed
```bash
cd backend
python -m app.db.seed --clear
```

### Verify Seeded Data
```bash
# Check areas
psql -U echosphere -d echosphere_db -c "SELECT name, city FROM selected_areas;"

# Check analyses
psql -U echosphere -d echosphere_db -c "SELECT COUNT(*) FROM area_analyses;"

# Check metrics
psql -U echosphere -d echosphere_db -c "SELECT COUNT(*) FROM environmental_metrics;"

# Check chat history
psql -U echosphere -d echosphere_db -c "SELECT COUNT(*) FROM chat_messages;"
```

## 📊 Sample Data Created

### 5 Geographic Areas
1. **Sibu Town Center** - Downtown commercial district
2. **Sibu Jaya Residential** - Growing residential area
3. **Sibu Industrial Area** - Industrial zone with palm oil facilities
4. **Rajang Riverfront** - Riverside area prone to flooding
5. **Sibu Jaya Commercial Hub** - New commercial development

### Analysis Results
- Environmental metrics for each area
- AI-generated analysis with priority levels
- Realistic data for Sibu's tropical climate context
- Haze season considerations (August-October)
- Flood risk assessments

### Chat History
- Sample conversations about environmental concerns
- AI responses with specific recommendations
- Context-aware responses for different areas

### NASA Cache
- Sample cached API responses
- Proper expiration handling
- Hit counting for performance tracking

## 🎯 Key Features

### Realistic Data
- **Climate Context**: Tropical Malaysian climate data
- **Haze Season**: Air quality patterns for August-October
- **Flood Risk**: Rajang River seasonal flooding
- **Urban Heat**: Heat island effects in commercial areas
- **Green Coverage**: Realistic vegetation percentages

### Sibu-Specific Context
- **Coordinates**: Accurate lat/lng for Sibu & Sibu Jaya
- **Industries**: Palm oil processing facilities
- **Infrastructure**: Commercial, residential, industrial zones
- **Environmental Issues**: Haze, flooding, heat stress

### Database Optimization
- **PostGIS Geometry**: Proper spatial polygons
- **Foreign Keys**: Correct relationships between tables
- **Indexes**: Optimized for spatial and time-series queries
- **Cascade Deletes**: Proper cleanup on data removal

## 🐛 Troubleshooting

### Import Errors
```bash
# Install missing dependencies
pip install sqlalchemy geoalchemy2 shapely psycopg2-binary
```

### Database Connection
```bash
# Test connection
python -c "from app.database import check_db_connection; check_db_connection()"
```

### PostGIS Issues
```sql
-- Enable PostGIS
psql -U echosphere -d echosphere_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### Clear All Data
```bash
# Reset everything
python -m app.db.seed --clear
```

## 📈 Expected Results

After successful seeding:
- **5 areas** in selected_areas table
- **5 analyses** in area_analyses table
- **5 metrics** in environmental_metrics table
- **4 chat messages** in chat_messages table
- **1 cache entry** in nasa_cache table
- **1 demo user** in users table

## 🔄 Integration

The seeded data integrates with:
- **Frontend**: Areas appear in map selection
- **AI Chat**: Context-aware responses using sample conversations
- **Analysis**: Pre-populated environmental assessments
- **Caching**: NASA API response examples
- **Metrics**: Historical data for trend analysis

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍

**Focus**: Sibu & Sibu Jaya, Sarawak, Malaysia
