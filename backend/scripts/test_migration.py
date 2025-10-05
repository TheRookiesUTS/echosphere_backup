#!/usr/bin/env python3
"""
Test script to verify Alembic migration setup
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        import alembic
        print("✓ Alembic imported successfully")
        
        import geoalchemy2
        print("✓ GeoAlchemy2 imported successfully")
        
        import asyncpg
        print("✓ AsyncPG imported successfully")
        
        # Test app imports
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from app.models.base import Base
        print("✓ Base model imported successfully")
        
        from app.models import Area, AreaAnalysis, NASADataCache, ChatHistory, MetricsTimeSeries
        print("✓ All models imported successfully")
        
        from app.config import settings
        print("✓ Settings imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_database_url():
    """Test database URL generation"""
    print("\nTesting database URL generation...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from app.config import settings
        
        url = settings.async_database_url
        print(f"✓ Database URL: {url}")
        
        if "postgresql+asyncpg://" in url:
            print("✓ Async URL format correct")
            return True
        else:
            print("✗ URL format incorrect")
            return False
            
    except Exception as e:
        print(f"✗ Error generating database URL: {e}")
        return False


def test_alembic_config():
    """Test Alembic configuration"""
    print("\nTesting Alembic configuration...")
    
    try:
        backend_dir = Path(__file__).parent.parent
        alembic_ini = backend_dir / "alembic.ini"
        env_py = backend_dir / "alembic" / "env.py"
        
        if alembic_ini.exists():
            print("✓ alembic.ini exists")
        else:
            print("✗ alembic.ini missing")
            return False
            
        if env_py.exists():
            print("✓ alembic/env.py exists")
        else:
            print("✗ alembic/env.py missing")
            return False
            
        # Check versions directory
        versions_dir = backend_dir / "alembic" / "versions"
        if versions_dir.exists():
            print("✓ versions directory exists")
            migration_files = list(versions_dir.glob("*.py"))
            print(f"✓ Found {len(migration_files)} migration files")
        else:
            print("✗ versions directory missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Error checking Alembic config: {e}")
        return False


def main():
    """Main test function"""
    print("EchoSphere Migration Setup Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Database URL Test", test_database_url),
        ("Alembic Config Test", test_alembic_config),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n✓ All tests passed! Migration setup is ready.")
        print("\nNext steps:")
        print("1. Ensure PostgreSQL is running")
        print("2. Create database: createdb -U echosphere echosphere_db")
        print("3. Enable PostGIS: psql -U echosphere -d echosphere_db -c 'CREATE EXTENSION postgis;'")
        print("4. Run migrations: python scripts/db_migrate.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
