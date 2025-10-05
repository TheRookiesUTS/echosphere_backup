# 🔄 Alembic Database Migrations Setup

Complete guide for setting up Alembic database migrations in EchoSphere project, compatible with Arch Linux and Windows 11.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running Migrations](#running-migrations)
5. [Common Commands](#common-commands)
6. [Troubleshooting](#troubleshooting)
7. [Cross-Platform Notes](#cross-platform-notes)

---

## ✅ Prerequisites

### Required Software

**Arch Linux:**
```bash
# Install PostgreSQL and PostGIS
sudo pacman -S postgresql postgis

# Install Python dependencies
pip install --target=../.venv-packages alembic geoalchemy2 asyncpg
```

**Windows 11:**
```bash
# Install via pip (PostgreSQL should be installed separately)
pip install --target=../.venv-packages alembic geoalchemy2 asyncpg
```

### Database Setup

**Arch Linux:**
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
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

**Windows 11:**
```powershell
# Using pgAdmin or psql
psql -U postgres
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q

# Enable PostGIS
psql -U echosphere -d echosphere_db
CREATE EXTENSION postgis;
\q
```

---

## 🔧 Installation

### 1. Initialize Alembic

```bash
cd backend

# Arch Linux / Windows (same command)
alembic init alembic
```

### 2. Install Dependencies

```bash
# Install required packages
pip install --target=../.venv-packages alembic geoalchemy2 asyncpg
```

---

## ⚙️ Configuration

### 1. Update `alembic.ini`

The configuration file is already set up with:

```ini
[alembic]
script_location = alembic
version_path_separator = os  # Cross-platform compatibility
sqlalchemy.url =  # Will be set from environment

[loggers]
keys = root,sqlalchemy,alembic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic
```

### 2. Update `alembic/env.py`

The environment script is configured for:
- ✅ Async database support
- ✅ PostGIS extension management
- ✅ Cross-platform compatibility
- ✅ Automatic model detection

### 3. Environment Variables

Create or update `backend/.env`:

```env
# Database Configuration
DB_USER=echosphere
DB_PASSWORD=echosphere_dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=echosphere_db

# API Keys
OPENROUTER_API_KEY=your_key_here
NASA_API_KEY=your_key_here
```

---

## 🚀 Running Migrations

### Method 1: Using Migration Script (Recommended)

```bash
# Arch Linux / Windows
cd backend
python scripts/db_migrate.py
```

### Method 2: Manual Commands

**Arch Linux:**
```bash
cd backend

# Set Python path
export PYTHONPATH=../.venv-packages

# Run migrations
python -m alembic upgrade head

# Check status
python -m alembic current
```

**Windows 11:**
```powershell
cd backend

# Set Python path
$env:PYTHONPATH = "..\.venv-packages"

# Run migrations
python -m alembic upgrade head

# Check status
python -m alembic current
```

### Method 3: Direct Alembic Commands

```bash
# Using the installed alembic
PYTHONPATH=../.venv-packages python -m alembic upgrade head
```

---

## 📝 Common Commands

### Migration Management

```bash
# Check current version
alembic current

# View migration history
alembic history --verbose

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Check if database is up to date
alembic check
```

### Creating New Migrations

```bash
# Auto-detect changes
alembic revision --autogenerate -m "Add new column"

# Create empty migration (manual)
alembic revision -m "Custom migration"
```

### Database Verification

```bash
# Check tables exist
psql -U echosphere -d echosphere_db -c "\dt"

# Check PostGIS
psql -U echosphere -d echosphere_db -c "SELECT PostGIS_Version();"

# Check indexes
psql -U echosphere -d echosphere_db -c "\di"
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'app'"

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Set Python path
export PYTHONPATH=../.venv-packages  # Arch Linux
$env:PYTHONPATH = "..\.venv-packages"  # Windows
```

#### Issue 2: "sqlalchemy.exc.ProgrammingError: function postgis_version() does not exist"

**Solution:**
```sql
-- Connect to database and enable PostGIS
psql -U echosphere -d echosphere_db
CREATE EXTENSION IF NOT EXISTS postgis;
\q
```

#### Issue 3: "asyncpg.exceptions.InvalidCatalogNameError: database does not exist"

**Solution:**
```bash
# Arch Linux
createdb -U echosphere echosphere_db

# Windows
psql -U postgres
CREATE DATABASE echosphere_db;
CREATE USER echosphere WITH PASSWORD 'echosphere_dev';
GRANT ALL PRIVILEGES ON DATABASE echosphere_db TO echosphere;
\q
```

#### Issue 4: "ImportError: cannot import name 'Geometry' from 'geoalchemy2'"

**Solution:**
```bash
pip install --target=../.venv-packages geoalchemy2
```

#### Issue 5: "ModuleNotFoundError: No module named 'asyncpg'"

**Solution:**
```bash
pip install --target=../.venv-packages asyncpg
```

#### Issue 6: Windows path issues with Alembic

**Solution:**
```ini
# In alembic.ini, ensure:
version_path_separator = os  # Uses os.pathsep (cross-platform)
```

#### Issue 7: Database connection refused

**Arch Linux:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start if not running
sudo systemctl start postgresql
```

**Windows:**
```powershell
# Check PostgreSQL service
Get-Service postgresql*

# Start if not running
Start-Service postgresql-x64-15
```

### Database Connection Issues

**Test connection:**
```bash
# Arch Linux / Windows
psql -U echosphere -d echosphere_db -c "SELECT 1;"
```

**If connection fails:**
1. Check PostgreSQL is running
2. Verify user exists and has permissions
3. Check database exists
4. Verify connection parameters in `.env`

### Migration Issues

**Reset migrations:**
```bash
# WARNING: This will delete all data!
psql -U echosphere -d echosphere_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic upgrade head
```

**Check migration status:**
```bash
alembic current
alembic history
```

---

## 🌍 Cross-Platform Notes

### Path Separators

- **Arch Linux**: Uses `/` for paths
- **Windows**: Uses `\` for paths
- **Solution**: Alembic configured with `version_path_separator = os` for automatic handling

### Environment Variables

**Arch Linux:**
```bash
export PYTHONPATH=../.venv-packages
```

**Windows:**
```powershell
$env:PYTHONPATH = "..\.venv-packages"
```

### Database Commands

**Arch Linux:**
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database
createdb -U echosphere echosphere_db
```

**Windows:**
```powershell
# Start PostgreSQL (if installed as service)
Start-Service postgresql-x64-15

# Create database
psql -U postgres -c "CREATE DATABASE echosphere_db;"
```

### Python Path Issues

**Arch Linux:**
```bash
# Use export
export PYTHONPATH=../.venv-packages
python -m alembic upgrade head
```

**Windows:**
```powershell
# Use environment variable
$env:PYTHONPATH = "..\.venv-packages"
python -m alembic upgrade head
```

---

## 📊 Migration Files

### Current Migrations

1. **001_initial_schema.py** - Original schema (legacy)
2. **002_initial_schema_new_models.py** - New model structure

### Migration Structure

```
backend/alembic/
├── versions/
│   ├── 001_initial_schema.py
│   └── 002_initial_schema_new_models.py
├── env.py
├── script.py.mako
└── alembic.ini
```

---

## 🔍 Verification

### After Migration

**Check tables:**
```sql
psql -U echosphere -d echosphere_db -c "\dt"
```

**Expected tables:**
- `areas`
- `area_analysis`
- `nasa_data_cache`
- `chat_history`
- `metrics_timeseries`

**Check PostGIS:**
```sql
psql -U echosphere -d echosphere_db -c "SELECT PostGIS_Version();"
```

**Check indexes:**
```sql
psql -U echosphere -d echosphere_db -c "\di"
```

---

## 🚀 Next Steps

1. **Run migrations**: `python scripts/db_migrate.py`
2. **Verify setup**: Check tables and PostGIS
3. **Test models**: Import and use new models
4. **Create new migrations**: As you modify models

---

## 📚 Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [GeoAlchemy2 Documentation](https://geoalchemy2.readthedocs.io/)

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍

**Database**: PostgreSQL 15 + PostGIS 3.3  
**Migration Tool**: Alembic 1.16+  
**Compatibility**: Arch Linux & Windows 11
