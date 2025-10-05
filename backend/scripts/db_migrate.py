#!/usr/bin/env python3
"""
Database migration helper script for EchoSphere
Compatible with Arch Linux and Windows 11
"""
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Tuple


def run_command(cmd: List[str], description: str, cwd: str = None) -> Tuple[bool, str, str]:
    """
    Run shell command with error handling
    
    Args:
        cmd: Command to run as list
        description: Human-readable description
        cwd: Working directory (optional)
    
    Returns:
        Tuple of (success, stdout, stderr)
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=cwd,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✓ {description} completed successfully\n")
            return True, result.stdout, result.stderr
        else:
            print(result.stderr, file=sys.stderr)
            print(f"✗ {description} failed\n", file=sys.stderr)
            return False, result.stdout, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out after 5 minutes\n", file=sys.stderr)
        return False, "", "Timeout"
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}\n", file=sys.stderr)
        return False, "", str(e)


def check_database_connection() -> bool:
    """Check if database is accessible"""
    print("Checking database connection...")
    
    # Try to connect to PostgreSQL
    success, stdout, stderr = run_command([
        "psql", "-U", "echosphere", "-d", "echosphere_db", "-c", "SELECT 1;"
    ], "Database connection test")
    
    if success:
        print("✓ Database connection successful")
        return True
    else:
        print("✗ Database connection failed")
        print("Make sure PostgreSQL is running and database exists")
        return False


def check_postgis() -> bool:
    """Check if PostGIS extension is available"""
    print("Checking PostGIS extension...")
    
    success, stdout, stderr = run_command([
        "psql", "-U", "echosphere", "-d", "echosphere_db", "-c", "SELECT PostGIS_Version();"
    ], "PostGIS version check")
    
    if success and "PostGIS" in stdout:
        print("✓ PostGIS extension available")
        return True
    else:
        print("✗ PostGIS extension not found")
        print("Run: psql -U echosphere -d echosphere_db -c 'CREATE EXTENSION postgis;'")
        return False


def run_migrations() -> bool:
    """Run Alembic migrations"""
    backend_dir = Path(__file__).parent.parent
    
    # Check if alembic is initialized
    if not (backend_dir / "alembic").exists():
        print("Error: Alembic not initialized. Run 'alembic init alembic' first.")
        return False
    
    # Set up environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir.parent / ".venv-packages")
    
    # Run migrations
    success, stdout, stderr = run_command(
        ["python", "-m", "alembic", "upgrade", "head"],
        "Apply all pending migrations",
        cwd=str(backend_dir)
    )
    
    if not success:
        print("Migration failed. Common issues:")
        print("1. Database not running: sudo systemctl start postgresql")
        print("2. Database not created: createdb -U echosphere echosphere_db")
        print("3. PostGIS not enabled: psql -U echosphere -d echosphere_db -c 'CREATE EXTENSION postgis;'")
        return False
    
    return True


def show_current_version() -> bool:
    """Show current migration version"""
    backend_dir = Path(__file__).parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir.parent / ".venv-packages")
    
    success, stdout, stderr = run_command(
        ["python", "-m", "alembic", "current"],
        "Show current migration version",
        cwd=str(backend_dir)
    )
    
    return success


def show_migration_history() -> bool:
    """Show migration history"""
    backend_dir = Path(__file__).parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir.parent / ".venv-packages")
    
    success, stdout, stderr = run_command(
        ["python", "-m", "alembic", "history", "--verbose"],
        "Show migration history",
        cwd=str(backend_dir)
    )
    
    return success


def main():
    """Main migration script"""
    print("EchoSphere Database Migration Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    backend_dir = Path(__file__).parent.parent
    if not (backend_dir / "alembic").exists():
        print("Error: Run this script from the backend directory")
        print("Expected: backend/scripts/db_migrate.py")
        sys.exit(1)
    
    print(f"Working directory: {backend_dir}")
    print(f"Python path: {backend_dir.parent / '.venv-packages'}")
    
    # Check database connection
    if not check_database_connection():
        print("\nTroubleshooting steps:")
        print("1. Start PostgreSQL: sudo systemctl start postgresql")
        print("2. Create database: createdb -U echosphere echosphere_db")
        print("3. Enable PostGIS: psql -U echosphere -d echosphere_db -c 'CREATE EXTENSION postgis;'")
        sys.exit(1)
    
    # Check PostGIS
    if not check_postgis():
        print("\nEnabling PostGIS...")
        success, stdout, stderr = run_command([
            "psql", "-U", "echosphere", "-d", "echosphere_db", "-c", "CREATE EXTENSION IF NOT EXISTS postgis;"
        ], "Enable PostGIS extension")
        
        if not success:
            print("Failed to enable PostGIS. Please run manually:")
            print("psql -U echosphere -d echosphere_db -c 'CREATE EXTENSION postgis;'")
            sys.exit(1)
    
    # Run migrations
    print("\nRunning migrations...")
    if not run_migrations():
        sys.exit(1)
    
    # Show current version
    print("\nMigration status:")
    show_current_version()
    
    print("\n" + "="*60)
    print("✓ Database migration completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
