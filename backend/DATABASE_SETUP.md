# 🗄️ EchoSphere Database Setup Guide

Complete guide for setting up PostgreSQL + PostGIS for EchoSphere (local development and Render.com deployment).

> **📚 For detailed step-by-step local setup instructions, see [../docs/LOCAL_DB_SETUP.md](../docs/LOCAL_DB_SETUP.md)**

---

## 📋 Table of Contents

1. [Local PostgreSQL Setup](#local-postgresql-setup)
   - [Linux](#linux-ubuntu--debian)
   - [macOS](#macos)
   - [Windows](#windows)
2. [Database Configuration](#database-configuration)
3. [Running Migrations](#running-migrations)
4. [Render.com Deployment](#rendercom-deployment)
5. [Troubleshooting](#troubleshooting)

---

## 🐧 Local PostgreSQL Setup

### Linux (Ubuntu / Debian)

```bash
# 1. Install PostgreSQL and PostGIS
sudo apt update
sudo apt install postgresql postgresql-contrib postgis postgresql-15-postgis-3

# 2. Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 3. Create database and user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# 4. Enable PostGIS extension
sudo -u postgres psql -d echosphere_db
CREATE EXTENSION postgis;
\q

# 5. Verify installation
psql -U echosphere -d echosphere_db -h localhost -c "SELECT PostGIS_Version();"
```

### macOS

#### Option 1: Homebrew (Recommended)

```bash
# 1. Install PostgreSQL with PostGIS
brew install postgresql@15 postgis

# 2. Start PostgreSQL
brew services start postgresql@15

# 3. Add PostgreSQL to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 4. Create database and user
psql postgres

# In PostgreSQL prompt:
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# 5. Enable PostGIS
psql -d echosphere_db
CREATE EXTENSION postgis;
\q

# 6. Verify
psql -U echosphere -d echosphere_db -h localhost -c "SELECT PostGIS_Version();"
```

#### Option 2: Postgres.app

1. Download **Postgres.app** from https://postgresapp.com/
2. Install and start the app
3. Click "Initialize" to create a server
4. Open terminal and run:

```bash
# Add to PATH (if not already)
echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Create database
psql postgres
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# Enable PostGIS
psql -d echosphere_db
CREATE EXTENSION postgis;
\q
```

### Windows

#### Option 1: PostgreSQL Installer (Recommended)

1. **Download PostgreSQL installer**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15.x installer

2. **Run installer**
   - Install PostgreSQL
   - Install Stack Builder when prompted
   - Use Stack Builder to install **PostGIS** extension

3. **Create database using pgAdmin 4** (installed with PostgreSQL)
   - Open pgAdmin 4
   - Connect to PostgreSQL server (default password set during install)
   - Right-click "Databases" → "Create" → "Database"
   - Name: `echosphere_db`
   - Owner: Create new user `echosphere` with password `echosphere_dev`

4. **Enable PostGIS**
   - Open SQL tool for `echosphere_db`
   - Run: `CREATE EXTENSION postgis;`

#### Option 2: Command Line (PowerShell)

```powershell
# After installing PostgreSQL

# 1. Add PostgreSQL to PATH
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"

# 2. Create database
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
ALTER DATABASE echosphere_db OWNER TO echosphere;
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# 3. Enable PostGIS
psql -U postgres -d echosphere_db
CREATE EXTENSION postgis;
\q

# 4. Verify
psql -U echosphere -d echosphere_db -h localhost -c "SELECT PostGIS_Version();"
```

---

## ⚙️ Database Configuration

### 1. Install Python Dependencies

```bash
cd backend

# Install database-specific requirements
pip install -r requirements/database.txt

# Or install all requirements
pip install --target=../.venv-packages -r requirements/linux.txt
pip install --target=../.venv-packages -r requirements/database.txt
```

### 2. Configure Environment Variables

Create or update `backend/.env`:

```env
# Database Configuration (Local Development)
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db

# For Render.com (use DATABASE_URL instead)
# DATABASE_URL will be automatically provided by Render

# API Keys (keep existing)
OPENROUTER_API_KEY=your_key_here
NASA_API_KEY=your_key_here
```

### 3. Initialize Database

```bash
cd backend

# Run initialization script (creates tables and seeds data)
python init_db.py

# You'll be prompted:
# - Drop existing tables? (y/N)
# - Clear existing cities and reseed? (y/N)
```

**What this does:**
- ✅ Checks database connection
- ✅ Enables PostGIS extension
- ✅ Creates all tables
- ✅ Seeds Malaysian city presets (Sibu, Kuala Lumpur, etc.)

---

## 🔄 Running Migrations

### Using Alembic

```bash
cd backend

# Check current migration version
alembic current

# Run all pending migrations
alembic upgrade head

# Create a new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"

# Rollback to previous version
alembic downgrade -1

# View migration history
alembic history
```

### Manual Migration (if needed)

```bash
# Apply initial schema
alembic upgrade head

# Or run init_db.py with drop_all=True
python init_db.py
```

---

## 🚀 Render.com Deployment

### 1. Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `echosphere-db`
   - **Database**: `echosphere_db`
   - **User**: `echosphere`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click "Create Database"
5. **Copy the Internal Database URL** (starts with `postgresql://`)

### 2. Enable PostGIS on Render

Render PostgreSQL includes PostGIS by default, but you need to enable it:

```sql
-- Connect to your Render database using psql or Render's shell
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify
SELECT PostGIS_Version();
```

**To connect to Render database locally:**

```bash
# Get connection string from Render dashboard
psql "postgresql://echosphere:password@hostname.render.com/echosphere_db"

# Then run:
CREATE EXTENSION IF NOT EXISTS postgis;
```

### 3. Configure Render Web Service

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r backend/requirements/linux.txt -r backend/requirements/database.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     DATABASE_URL=<your-render-postgres-internal-url>
     OPENROUTER_API_KEY=<your-key>
     NASA_API_KEY=<your-key>
     PYTHON_VERSION=3.13
     ```

### 4. Run Migrations on Render

After deployment, run migrations:

1. Open Render Shell for your web service
2. Run:
   ```bash
   cd backend
   alembic upgrade head
   python init_db.py  # Seed initial data
   ```

Or add to your `render.yaml`:

```yaml
services:
  - type: web
    name: echosphere-backend
    env: python
    buildCommand: |
      pip install -r backend/requirements/linux.txt -r backend/requirements/database.txt
      cd backend && alembic upgrade head && python init_db.py
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: echosphere-db
          property: connectionString
      - key: OPENROUTER_API_KEY
        sync: false
      - key: NASA_API_KEY
        sync: false
```

### 5. Render Free Tier Optimization

Our database configuration is already optimized for Render free tier:

```python
# In app/database.py
engine_kwargs = {
    "pool_size": 5,          # Limited connections
    "max_overflow": 2,       # Max extra connections
    "pool_pre_ping": True,   # Health checks
    "pool_recycle": 300,     # Recycle every 5 min
}
```

**Free Tier Limits:**
- ✅ 1GB storage
- ✅ 97 connections (but we use max 7)
- ✅ 30-day data retention
- ⚠️ Database sleeps after 90 days of inactivity

---

## 🐛 Troubleshooting

### Common Issues

#### "psycopg2 not installed"
```bash
pip install psycopg2-binary
# Or for production:
pip install psycopg2
```

#### "PostGIS extension not found"
```sql
-- Connect to database and run:
CREATE EXTENSION postgis;

-- If you get permission error:
-- Connect as superuser (postgres)
sudo -u postgres psql -d echosphere_db
CREATE EXTENSION postgis;
```

#### "Connection refused"
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list                # macOS

# Start if not running
sudo systemctl start postgresql   # Linux
brew services start postgresql@15 # macOS
```

#### "Role 'echosphere' does not exist"
```sql
-- Connect as postgres user and run:
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
```

#### "Database 'echosphere_db' does not exist"
```sql
-- Connect as postgres user and run:
CREATE DATABASE echosphere_db OWNER echosphere;
```

#### Alembic "Can't locate revision"
```bash
# Reset alembic
cd backend
rm -rf alembic/versions/*.py
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Verify Database Setup

```bash
cd backend

# Test connection
python -c "from app.database import check_db_connection, check_postgis; check_db_connection(); check_postgis()"

# Test API
python main.py
# Visit: http://localhost:8000/api/health
```

### Check Database Contents

```bash
# Connect to database
psql -U echosphere -d echosphere_db -h localhost

# List tables
\dt

# Check PostGIS
SELECT PostGIS_Version();

# Check city presets
SELECT name, country FROM city_presets;

# Exit
\q
```

---

## 📊 Database Schema Overview

**Tables:**
- `users` - User sessions and preferences
- `selected_areas` - Geospatial polygons (PostGIS)
- `environmental_metrics` - Time-series climate data
- `area_analyses` - AI-generated analysis results
- `chat_messages` - Chatbot conversation history
- `nasa_cache` - API response caching
- `disaster_events` - NASA EONET disaster data (PostGIS)
- `city_presets` - Pre-configured cities

**Key Features:**
- 🗺️ PostGIS for geospatial queries
- 📈 Time-series metrics for trend analysis
- 💾 Smart caching to reduce API calls
- 🔍 Spatial indexing for fast queries
- 🔄 Full migration support with Alembic

---

## 🔗 Useful Links

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Render PostgreSQL Guide](https://render.com/docs/databases)

---

## ✅ Quick Checklist

**Local Development:**
- [ ] PostgreSQL installed
- [ ] PostGIS extension enabled
- [ ] Database `echosphere_db` created
- [ ] User `echosphere` created with password
- [ ] Python dependencies installed
- [ ] `.env` file configured
- [ ] `init_db.py` run successfully
- [ ] Tables created and seeded
- [ ] Health check endpoint working

**Render Deployment:**
- [ ] PostgreSQL database created on Render
- [ ] PostGIS extension enabled
- [ ] DATABASE_URL environment variable set
- [ ] Migrations run on production
- [ ] Initial data seeded
- [ ] Health check returns "healthy"

---

Need help? Check the troubleshooting section or open an issue on GitHub!

