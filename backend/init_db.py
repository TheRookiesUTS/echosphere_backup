#!/usr/bin/env python3
"""
Database initialization and seeding script for EchoSphere
Run this to set up your database with initial data
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db, check_db_connection, check_postgis, get_db_context
from app.crud import create_city_preset
from app.models.db_models import CityPreset
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# City Presets Data for Sibu & Major Malaysian Cities
# ============================================================================

CITY_PRESETS = [
    {
        "name": "Sibu",
        "country": "Malaysia",
        "center_lat": 2.3,
        "center_lng": 111.82,
        "zoom_level": 13,
        "bounds": {
            "north": 2.35,
            "south": 2.25,
            "east": 111.87,
            "west": 111.77
        },
        "population": 247995,
        "description": "Sibu, Sarawak - Gateway to the Heart of Borneo. Focus area for EchoSphere urban resilience analysis."
    },
    {
        "name": "Sibu Jaya",
        "country": "Malaysia",
        "center_lat": 2.27,
        "center_lng": 111.85,
        "zoom_level": 14,
        "bounds": {
            "north": 2.29,
            "south": 2.25,
            "east": 111.87,
            "west": 111.83
        },
        "population": 50000,
        "description": "Sibu Jaya - Satellite township of Sibu with modern urban development."
    },
    {
        "name": "Kuching",
        "country": "Malaysia",
        "center_lat": 1.5535,
        "center_lng": 110.3593,
        "zoom_level": 12,
        "bounds": {
            "north": 1.6,
            "south": 1.5,
            "east": 110.4,
            "west": 110.3
        },
        "population": 570000,
        "description": "Kuching - Capital of Sarawak, known as the Cat City."
    },
    {
        "name": "Kuala Lumpur",
        "country": "Malaysia",
        "center_lat": 3.1390,
        "center_lng": 101.6869,
        "zoom_level": 12,
        "bounds": {
            "north": 3.25,
            "south": 3.02,
            "east": 101.77,
            "west": 101.60
        },
        "population": 1800000,
        "description": "Kuala Lumpur - Capital city of Malaysia, major urban center."
    },
    {
        "name": "George Town",
        "country": "Malaysia",
        "center_lat": 5.4164,
        "center_lng": 100.3327,
        "zoom_level": 13,
        "bounds": {
            "north": 5.47,
            "south": 5.36,
            "east": 100.38,
            "west": 100.28
        },
        "population": 708000,
        "description": "George Town, Penang - UNESCO World Heritage City."
    },
    {
        "name": "Johor Bahru",
        "country": "Malaysia",
        "center_lat": 1.4927,
        "center_lng": 103.7414,
        "zoom_level": 12,
        "bounds": {
            "north": 1.55,
            "south": 1.43,
            "east": 103.8,
            "west": 103.68
        },
        "population": 1700000,
        "description": "Johor Bahru - Southern gateway to Malaysia."
    },
    {
        "name": "Kota Kinabalu",
        "country": "Malaysia",
        "center_lat": 5.9804,
        "center_lng": 116.0735,
        "zoom_level": 12,
        "bounds": {
            "north": 6.03,
            "south": 5.93,
            "east": 116.12,
            "west": 116.02
        },
        "population": 500000,
        "description": "Kota Kinabalu - Capital of Sabah, coastal city with Mount Kinabalu backdrop."
    },
    {
        "name": "Miri",
        "country": "Malaysia",
        "center_lat": 4.3996,
        "center_lng": 113.9914,
        "zoom_level": 12,
        "bounds": {
            "north": 4.45,
            "south": 4.35,
            "east": 114.04,
            "west": 113.94
        },
        "population": 350000,
        "description": "Miri, Sarawak - Oil and gas hub, gateway to national parks."
    }
]


def seed_city_presets():
    """Seed database with Malaysian city presets"""
    logger.info("🌆 Seeding city presets...")
    
    with get_db_context() as db:
        # Check if cities already exist
        existing_count = db.query(CityPreset).count()
        if existing_count > 0:
            logger.info(f"   ℹ️  Found {existing_count} existing city presets")
            response = input("   Clear existing cities and reseed? (y/N): ")
            if response.lower() == 'y':
                db.query(CityPreset).delete()
                db.commit()
                logger.info("   🗑️  Cleared existing city presets")
            else:
                logger.info("   ⏭️  Skipping city seeding")
                return
        
        # Add cities
        for city_data in CITY_PRESETS:
            try:
                city = create_city_preset(db, **city_data)
                logger.info(f"   ✅ Added: {city.name}, {city.country}")
            except Exception as e:
                logger.error(f"   ❌ Failed to add {city_data['name']}: {e}")
        
        logger.info(f"✅ Seeded {len(CITY_PRESETS)} city presets")


def verify_database():
    """Verify database setup"""
    logger.info("🔍 Verifying database setup...")
    
    with get_db_context() as db:
        # Check tables exist
        from app.models.db_models import User, SelectedArea, CityPreset
        
        try:
            users = db.query(User).count()
            areas = db.query(SelectedArea).count()
            cities = db.query(CityPreset).count()
            
            logger.info(f"   📊 Database contents:")
            logger.info(f"      - Users: {users}")
            logger.info(f"      - Selected Areas: {areas}")
            logger.info(f"      - City Presets: {cities}")
            
            return True
        except Exception as e:
            logger.error(f"   ❌ Verification failed: {e}")
            return False


def main():
    """Main initialization script"""
    logger.info("=" * 60)
    logger.info("🚀 EchoSphere Database Initialization")
    logger.info("=" * 60)
    
    # Check database connection
    logger.info("\n1️⃣  Checking database connection...")
    if not check_db_connection():
        logger.error("❌ Cannot connect to database. Please check your configuration.")
        logger.error("   Make sure PostgreSQL is running and DATABASE_URL is set.")
        sys.exit(1)
    
    # Check PostGIS
    logger.info("\n2️⃣  Checking PostGIS extension...")
    if not check_postgis():
        logger.warning("⚠️  PostGIS not available. Attempting to enable...")
        # The init_db function will try to enable PostGIS
    
    # Initialize database (create tables)
    logger.info("\n3️⃣  Creating database tables...")
    try:
        # Ask if user wants to drop existing tables
        response = input("   Drop existing tables and recreate? (y/N): ")
        drop_all = response.lower() == 'y'
        
        init_db(drop_all=drop_all)
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        sys.exit(1)
    
    # Seed data
    logger.info("\n4️⃣  Seeding initial data...")
    try:
        seed_city_presets()
    except Exception as e:
        logger.error(f"❌ Failed to seed data: {e}")
        sys.exit(1)
    
    # Verify setup
    logger.info("\n5️⃣  Verifying database setup...")
    if verify_database():
        logger.info("✅ Database verification passed!")
    else:
        logger.warning("⚠️  Database verification had issues")
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("✅ DATABASE INITIALIZATION COMPLETE!")
    logger.info("=" * 60)
    logger.info("\n📝 Next steps:")
    logger.info("   1. Start your backend server: python backend/main.py")
    logger.info("   2. Test the API: http://localhost:8000/docs")
    logger.info("   3. Check database health: http://localhost:8000/api/health")
    logger.info("\n🔧 Useful commands:")
    logger.info("   - Run migrations: alembic upgrade head")
    logger.info("   - Create migration: alembic revision --autogenerate -m 'message'")
    logger.info("   - Check migrations: alembic current")
    logger.info("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Initialization cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

