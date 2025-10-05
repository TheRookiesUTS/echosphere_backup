"""
Base classes and mixins for SQLAlchemy models
Provides common functionality for all database models
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func
from datetime import datetime
import uuid

Base = declarative_base()


def generate_uuid() -> str:
    """
    Generate UUID v4 as string for primary keys
    
    Returns:
        str: UUID v4 string (36 characters with hyphens)
    """
    return str(uuid.uuid4())


class TimestampMixin:
    """
    Mixin for automatic created_at and updated_at timestamps
    
    Attributes:
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when record was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when record was last updated"
    )

