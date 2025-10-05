# ⚡ Alembic Quick Start Guide

**EchoSphere Database Migrations - Arch Linux & Windows 11 Compatible**

---

## 🚀 3-Step Setup

### Step 1: Install Dependencies

**Arch Linux:**
```bash
cd backend
pip install --target=../.venv-packages alembic geoalchemy2 asyncpg
```

**Windows 11:**
```powershell
cd backend
pip install --target=..\.venv-packages alembic geoalchemy2 asyncpg
```

### Step 2: Test Setup

```bash
# Arch Linux / Windows
PYTHONPATH=../.venv-packages python scripts/test_migration.py
```

**Expected output:**
```
✓ All tests passed! Migration setup is ready.
```

### Step 3: Run Migrations

```bash
# Arch Linux / Windows
PYTHONPATH=../.venv-packages python scripts/db_migrate.py
```

---

## 🔧 Quick Commands

### Check Status
```bash
# Current migration version
PYTHONPATH=../.venv-packages python -m alembic current

# Migration history
PYTHONPATH=../.venv-packages python -m alembic history
```

### Run Migrations
```bash
# Apply all pending migrations
PYTHONPATH=../.venv-packages python -m alembic upgrade head

# Rollback one version
PYTHONPATH=../.venv-packages python -m alembic downgrade -1
```

### Create New Migration
```bash
# Auto-detect changes
PYTHONPATH=../.venv-packages python -m alembic revision --autogenerate -m "Description"

# Manual migration
PYTHONPATH=../.venv-packages python -m alembic revision -m "Description"
```

---

## 🐛 Quick Troubleshooting

### "ModuleNotFoundError"
```bash
# Set Python path
export PYTHONPATH=../.venv-packages  # Arch Linux
$env:PYTHONPATH = "..\.venv-packages"  # Windows
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Arch Linux
Get-Service postgresql*  # Windows

# Create database
createdb -U echosphere echosphere_db  # Arch Linux
psql -U postgres -c "CREATE DATABASE echosphere_db;"  # Windows
```

### "PostGIS extension not found"
```sql
psql -U echosphere -d echosphere_db -c "CREATE EXTENSION postgis;"
```

---

## 📊 Verify Setup

### Check Tables
```sql
psql -U echosphere -d echosphere_db -c "\dt"
```

**Expected tables:**
- `areas`
- `area_analysis`
- `nasa_data_cache`
- `chat_history`
- `metrics_timeseries`

### Check PostGIS
```sql
psql -U echosphere -d echosphere_db -c "SELECT PostGIS_Version();"
```

---

## 🎯 Next Steps

1. **Database Ready**: Tables created with PostGIS support
2. **Models Ready**: New SQLAlchemy models available
3. **Migrations Ready**: Alembic configured for future changes
4. **Cross-Platform**: Works on Arch Linux and Windows 11

---

**Built for NASA Space Apps Challenge 2025** 🚀🌍

**Database**: PostgreSQL 15 + PostGIS 3.3  
**Migration Tool**: Alembic 1.16+  
**Models**: 5 optimized tables with spatial indexes
