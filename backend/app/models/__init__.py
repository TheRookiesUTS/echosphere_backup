"""
SQLAlchemy models for EchoSphere database

This module contains all database models with PostGIS support,
optimized for Render.com's 1GB free tier.

Models:
    - Area: Geographic areas for analysis
    - AreaAnalysis: Analysis results and metrics
    - NASADataCache: Cached NASA API responses
    - ChatHistory: AI conversation history
    - MetricsTimeSeries: Historical metrics for trends
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base, TimestampMixin, generate_uuid
from app.models.area import Area
from app.models.analysis import AreaAnalysis
from app.models.cache import NASADataCache
from app.models.chat import ChatHistory
from app.models.metrics import MetricsTimeSeries, MetricType

__all__ = [
    "Base",
    "TimestampMixin",
    "generate_uuid",
    "Area",
    "AreaAnalysis",
    "NASADataCache",
    "ChatHistory",
    "MetricsTimeSeries",
    "MetricType",
    "cleanup_old_data",
    "get_database_size_estimate",
]


# Cleanup utilities for production (save space on Render's 1GB limit)

async def cleanup_old_data(
    session: AsyncSession, 
    days_to_keep: int = 90,
    dry_run: bool = False
) -> dict:
    """
    Remove old data to stay under 1GB limit
    
    This function helps maintain database size by removing:
    - Expired cache entries
    - Old chat history (keeps last 100 per session)
    - Old metrics (keeps recent data only)
    
    Args:
        session: AsyncSession instance
        days_to_keep: Number of days of data to retain (default: 90)
        dry_run: If True, only count records without deleting
    
    Returns:
        dict: Statistics about cleanup operation
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    stats = {
        "cutoff_date": cutoff_date.isoformat(),
        "cache_expired": 0,
        "cache_old": 0,
        "chat_old": 0,
        "metrics_old": 0,
        "dry_run": dry_run,
    }
    
    try:
        # 1. Delete expired cache entries
        expired_cache = await session.execute(
            delete(NASADataCache).where(
                NASADataCache.expires_at < datetime.utcnow()
            ).returning(NASADataCache.id)
        )
        stats["cache_expired"] = len(expired_cache.fetchall())
        
        # 2. Delete old cache entries (beyond retention period)
        old_cache = await session.execute(
            delete(NASADataCache).where(
                NASADataCache.fetched_at < cutoff_date
            ).returning(NASADataCache.id)
        )
        stats["cache_old"] = len(old_cache.fetchall())
        
        # 3. Delete old chat history (keep recent conversations)
        # Note: This keeps last 100 messages per session automatically via limit
        old_chat = await session.execute(
            delete(ChatHistory).where(
                ChatHistory.created_at < cutoff_date
            ).returning(ChatHistory.id)
        )
        stats["chat_old"] = len(old_chat.fetchall())
        
        # 4. Delete old metrics (or consider aggregating them)
        old_metrics = await session.execute(
            delete(MetricsTimeSeries).where(
                MetricsTimeSeries.date_recorded < cutoff_date.date()
            ).returning(MetricsTimeSeries.id)
        )
        stats["metrics_old"] = len(old_metrics.fetchall())
        
        if not dry_run:
            await session.commit()
        else:
            await session.rollback()
        
        stats["total_deleted"] = (
            stats["cache_expired"] + 
            stats["cache_old"] + 
            stats["chat_old"] + 
            stats["metrics_old"]
        )
        
        return stats
        
    except Exception as e:
        await session.rollback()
        stats["error"] = str(e)
        return stats


async def get_database_size_estimate(session: AsyncSession) -> dict:
    """
    Get estimated database size and record counts
    
    Useful for monitoring database growth on Render's free tier
    to ensure we stay under the 1GB limit.
    
    Args:
        session: AsyncSession instance
    
    Returns:
        dict: Database statistics
    """
    from sqlalchemy import func, select
    
    stats = {}
    
    try:
        # Count records in each table
        stats["areas"] = await session.scalar(select(func.count(Area.id)))
        stats["analyses"] = await session.scalar(select(func.count(AreaAnalysis.id)))
        stats["cache"] = await session.scalar(select(func.count(NASADataCache.id)))
        stats["chat"] = await session.scalar(select(func.count(ChatHistory.id)))
        stats["metrics"] = await session.scalar(select(func.count(MetricsTimeSeries.id)))
        
        # Get database size (PostgreSQL-specific)
        result = await session.execute(
            "SELECT pg_size_pretty(pg_database_size(current_database())) as size"
        )
        row = result.fetchone()
        if row:
            stats["database_size"] = row[0]
        
        # Calculate total records
        stats["total_records"] = sum([
            stats["areas"],
            stats["analyses"],
            stats["cache"],
            stats["chat"],
            stats["metrics"],
        ])
        
        return stats
        
    except Exception as e:
        stats["error"] = str(e)
        return stats


def get_model_by_name(model_name: str):
    """
    Get model class by name
    
    Args:
        model_name: Name of the model (e.g., 'Area', 'AreaAnalysis')
    
    Returns:
        Model class or None if not found
    """
    models = {
        "Area": Area,
        "AreaAnalysis": AreaAnalysis,
        "NASADataCache": NASADataCache,
        "ChatHistory": ChatHistory,
        "MetricsTimeSeries": MetricsTimeSeries,
    }
    return models.get(model_name)
