"""Initial schema with new models

Revision ID: 002
Revises: 001
Create Date: 2025-10-05

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS extension (if not already enabled)
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    
    # Drop old tables if they exist (for migration from old schema)
    op.drop_table('city_presets', if_exists=True)
    op.drop_table('disaster_events', if_exists=True)
    op.drop_table('nasa_cache', if_exists=True)
    op.drop_table('chat_messages', if_exists=True)
    op.drop_table('area_analyses', if_exists=True)
    op.drop_table('environmental_metrics', if_exists=True)
    op.drop_table('selected_areas', if_exists=True)
    op.drop_table('users', if_exists=True)
    
    # Drop old enum types
    op.execute('DROP TYPE IF EXISTS sessionstatus;')
    op.execute('DROP TYPE IF EXISTS prioritylevel;')
    op.execute('DROP TYPE IF EXISTS floodrisklevel;')
    
    # Create areas table (new model structure)
    op.create_table('areas',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('bbox_geometry', Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('center_lat', sa.Float(), nullable=False),
        sa.Column('center_lon', sa.Float(), nullable=False),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), default='Malaysia'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    
    # Create spatial index on bbox_geometry
    op.execute('CREATE INDEX idx_areas_geometry ON areas USING GIST (bbox_geometry);')
    op.execute('CREATE INDEX idx_areas_location ON areas (city, country);')
    op.execute('CREATE INDEX idx_areas_center ON areas (center_lat, center_lon);')
    
    # Create area_analysis table
    op.create_table('area_analysis',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('area_id', sa.String(36), nullable=False),
        sa.Column('heat_stress_celsius', sa.Float(), nullable=True),
        sa.Column('air_quality_aqi', sa.Integer(), nullable=True),
        sa.Column('water_stress_percent', sa.Float(), nullable=True),
        sa.Column('green_coverage_percent', sa.Float(), nullable=True),
        sa.Column('population_density', sa.Float(), nullable=True),
        sa.Column('flood_risk_score', sa.Float(), nullable=True),
        sa.Column('analysis_summary', sa.JSON(), nullable=True),
        sa.Column('ai_recommendations', sa.JSON(), nullable=True),
        sa.Column('risk_factors', sa.JSON(), nullable=True),
        sa.Column('opportunities', sa.JSON(), nullable=True),
        sa.Column('data_sources', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['area_id'], ['areas.id'], ondelete='CASCADE'),
    )
    op.execute('CREATE INDEX idx_analysis_area_time ON area_analysis (area_id, created_at);')
    op.execute('CREATE INDEX idx_analysis_risks ON area_analysis (flood_risk_score, heat_stress_celsius);')
    
    # Create nasa_data_cache table
    op.create_table('nasa_data_cache',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('api_source', sa.String(50), nullable=False),
        sa.Column('request_params', sa.JSON(), nullable=False),
        sa.Column('response_data', sa.JSON(), nullable=False),
        sa.Column('bbox_geometry', Geometry(geometry_type='POLYGON', srid=4326), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_valid', sa.Boolean(), default=True),
    )
    op.execute('CREATE INDEX idx_cache_lookup ON nasa_data_cache (api_source, is_valid);')
    op.execute('CREATE INDEX idx_cache_expiry ON nasa_data_cache (expires_at, is_valid);')
    op.execute('CREATE INDEX idx_cache_geometry ON nasa_data_cache USING GIST (bbox_geometry);')
    
    # Create chat_history table
    op.create_table('chat_history',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(100), nullable=False),
        sa.Column('area_id', sa.String(36), nullable=True),
        sa.Column('user_message', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('context_data', sa.JSON(), nullable=True),
        sa.Column('model_used', sa.String(50), default='deepseek/deepseek-chat'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['area_id'], ['areas.id'], ondelete='CASCADE'),
    )
    op.execute('CREATE INDEX idx_session_time ON chat_history (session_id, created_at);')
    op.execute('CREATE INDEX idx_chat_area ON chat_history (area_id, created_at);')
    
    # Create metrics_timeseries table
    op.create_table('metrics_timeseries',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('area_id', sa.String(36), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(20), nullable=True),
        sa.Column('date_recorded', sa.Date(), nullable=False),
        sa.Column('data_source', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['area_id'], ['areas.id'], ondelete='CASCADE'),
    )
    op.execute('CREATE INDEX idx_metrics_time ON metrics_timeseries (area_id, metric_type, date_recorded);')
    op.execute('CREATE INDEX idx_metrics_source ON metrics_timeseries (data_source, date_recorded);')
    op.execute('CREATE INDEX idx_metrics_type ON metrics_timeseries (metric_type, date_recorded);')


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('metrics_timeseries')
    op.drop_table('chat_history')
    op.drop_table('nasa_data_cache')
    op.drop_table('area_analysis')
    op.drop_table('areas')
    
    # Optionally drop PostGIS extension (be careful in production!)
    # op.execute('DROP EXTENSION IF EXISTS postgis;')
