"""
Configuration management for Echosphere Backend
Loads environment variables and provides settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    
    # API Keys
    openrouter_api_key: str
    nasa_api_key: str
    open_aq_api_key: Optional[str] = None  # OpenAQ API for air quality data
    earth_data: Optional[str] = None  # NASA Earth Data API key
    
    # OpenRouter Configuration
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    deepseek_model: str = "deepseek/deepseek-chat-v3.1:free"
    
    # NASA Configuration
    nasa_base_url: str = "https://api.nasa.gov"
    eonet_base_url: str = "https://eonet.gsfc.nasa.gov/api/v3"
    earth_data_base_url: Optional[str] = None  # Will be set from EARTH_DATA env var or default
    
    # OpenAQ Configuration
    openaq_base_url: str = "https://api.openaq.org/v3"
    
    # Server Configuration
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://127.0.0.1:5500"  # Default for Live Server
    
    # Database Configuration (PostgreSQL + PostGIS)
    database_url: Optional[str] = None  # Full database URL (for Render.com)
    db_user: str = "echosphere"
    db_password: str = "echosphere_dev"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "echosphere_db"
    
    # Optional: Site info for OpenRouter
    site_url: Optional[str] = None
    site_name: Optional[str] = "Echosphere Urban Resilience"
    
    # Cache TTL (seconds)
    nasa_cache_ttl: int = 3600  # 1 hour
    
    # Database pool settings (optimized for Render.com free tier)
    db_pool_size: int = 5
    db_max_overflow: int = 2
    
    @property
    def async_database_url(self) -> str:
        """Get async database URL for SQLAlchemy"""
        if self.database_url:
            # Convert sync URL to async (asyncpg)
            return self.database_url.replace(
                "postgresql://", 
                "postgresql+asyncpg://"
            )
        else:
            # Build URL from components
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )
    
    @property
    def earth_data_url(self) -> str:
        """Get Earth Data API URL - uses EARTH_DATA env var or default"""
        return self.earth_data or "https://earthdata.nasa.gov/api"


# Global settings instance
settings = Settings()

