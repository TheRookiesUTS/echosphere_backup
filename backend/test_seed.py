#!/usr/bin/env python3
"""
Simple test script to verify the seeding script works
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from app.db.seed import seed_database, clear_all_data
    print("✓ Seeding script imports successfully")
    
    # Test that functions exist
    assert callable(seed_database), "seed_database function not found"
    assert callable(clear_all_data), "clear_all_data function not found"
    print("✓ All required functions are available")
    
    print("\n" + "="*60)
    print("SEEDING SCRIPT READY!")
    print("="*60)
    print("Usage:")
    print("  python -m app.db.seed              # Basic seeding")
    print("  python -m app.db.seed --clear      # Clear and reseed")
    print("\nPrerequisites:")
    print("  1. Install dependencies: pip install -r requirements/database.txt")
    print("  2. Set up PostgreSQL + PostGIS")
    print("  3. Configure .env file with database credentials")
    print("  4. Run database migrations: alembic upgrade head")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nMake sure you have installed the required dependencies:")
    print("  pip install -r requirements/database.txt")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
