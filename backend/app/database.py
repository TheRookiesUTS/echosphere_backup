"""
Database configuration and session management
SQLAlchemy + PostgreSQL + PostGIS setup
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
import logging
import os

from app.models.db_models import Base

logger = logging.getLogger(__name__)


# ============================================================================
# Database Configuration
# ============================================================================

def get_database_url() -> str:
    """
    Get database URL from environment variables
    Supports both local development and Render.com deployment
    """
    # Try Render.com DATABASE_URL first (for production)
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Render provides postgres:// but SQLAlchemy needs postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        logger.info("Using DATABASE_URL from environment (Render/production)")
        return database_url
    
    # Fall back to individual components (for local development)
    db_user = os.getenv("DB_USER", "echosphere")
    db_password = os.getenv("DB_PASSWORD", "echosphere_dev")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "echosphere_db")
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    logger.info(f"Using local database: {db_host}:{db_port}/{db_name}")
    return database_url


# ============================================================================
# Engine Configuration
# ============================================================================

def create_db_engine(database_url: str = None):
    """
    Create SQLAlchemy engine with optimized settings for Render.com free tier
    """
    if database_url is None:
        database_url = get_database_url()
    
    # Determine if we're on Render (production) or local
    is_production = "DATABASE_URL" in os.environ
    
    engine_kwargs = {
        "echo": not is_production,  # Log SQL in development only
        "future": True,  # Use SQLAlchemy 2.0 style
    }
    
    if is_production:
        # Render.com free tier optimization
        engine_kwargs.update({
            "pool_size": 5,  # Limited connections on free tier
            "max_overflow": 2,
            "pool_pre_ping": True,  # Check connection health before using
            "pool_recycle": 300,  # Recycle connections every 5 minutes
            "connect_args": {
                "connect_timeout": 10,
                "options": "-c timezone=utc"
            }
        })
        logger.info("🚀 Production engine configuration (Render.com)")
    else:
        # Local development - more permissive
        engine_kwargs.update({
            "pool_size": 10,
            "max_overflow": 5,
            "pool_pre_ping": True,
        })
        logger.info("💻 Development engine configuration (local)")
    
    engine = create_engine(database_url, **engine_kwargs)
    
    # Enable PostGIS extension on connection
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        """Ensure PostGIS is available"""
        with dbapi_conn.cursor() as cursor:
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
                dbapi_conn.commit()
            except Exception as e:
                logger.warning(f"PostGIS extension check: {e}")
    
    return engine


# ============================================================================
# Session Management
# ============================================================================

# Global engine and session factory
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for non-FastAPI usage
    Usage: 
        with get_db_context() as db:
            # use db
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================================================
# Database Initialization
# ============================================================================

def init_db(drop_all: bool = False):
    """
    Initialize database tables
    
    Args:
        drop_all: If True, drop all tables first (DESTRUCTIVE!)
    """
    logger.info("🔧 Initializing database...")
    
    try:
        if drop_all:
            logger.warning("⚠️  Dropping all tables...")
            Base.metadata.drop_all(bind=engine)
        
        logger.info("📊 Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database initialized successfully!")
        return True
    
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def check_db_connection() -> bool:
    """
    Check if database connection is working
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Database connection OK")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def check_postgis() -> bool:
    """
    Check if PostGIS extension is available
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(
                "SELECT PostGIS_Version();"
            ).fetchone()
            if result:
                logger.info(f"✅ PostGIS available: {result[0]}")
                return True
    except Exception as e:
        logger.error(f"❌ PostGIS not available: {e}")
        return False


# ============================================================================
# Health Check
# ============================================================================

def get_db_health() -> dict:
    """
    Get database health status for health check endpoint
    """
    health = {
        "database": "unknown",
        "postgis": "unknown",
        "details": {}
    }
    
    try:
        # Check basic connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            health["database"] = "healthy"
            
            # Check PostGIS
            try:
                result = conn.execute("SELECT PostGIS_Version();").fetchone()
                health["postgis"] = "healthy"
                health["details"]["postgis_version"] = result[0] if result else "unknown"
            except:
                health["postgis"] = "unavailable"
            
            # Get connection pool stats
            pool = engine.pool
            health["details"]["pool_size"] = pool.size()
            health["details"]["checked_out"] = pool.checkedout()
            
    except Exception as e:
        health["database"] = "unhealthy"
        health["details"]["error"] = str(e)
    
    return health


# ============================================================================
# Cleanup
# ============================================================================

def cleanup_expired_cache():
    """
    Clean up expired NASA cache entries
    Should be run periodically (e.g., via cron job or background task)
    """
    from app.models.db_models import NASACache
    from datetime import datetime
    
    try:
        with get_db_context() as db:
            deleted = db.query(NASACache).filter(
                NASACache.expires_at < datetime.utcnow()
            ).delete()
            
            if deleted > 0:
                logger.info(f"🧹 Cleaned up {deleted} expired cache entries")
            return deleted
    except Exception as e:
        logger.error(f"❌ Cache cleanup failed: {e}")
        return 0


def cleanup_old_chat_messages(days: int = 30):
    """
    Clean up old chat messages (retain last N days)
    
    Args:
        days: Number of days to retain
    """
    from app.models.db_models import ChatMessage
    from datetime import datetime, timedelta
    
    try:
        with get_db_context() as db:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            deleted = db.query(ChatMessage).filter(
                ChatMessage.created_at < cutoff_date
            ).delete()
            
            if deleted > 0:
                logger.info(f"🧹 Cleaned up {deleted} old chat messages")
            return deleted
    except Exception as e:
        logger.error(f"❌ Chat cleanup failed: {e}")
        return 0

