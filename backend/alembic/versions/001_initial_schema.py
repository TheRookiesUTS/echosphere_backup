"""Initial database schema with PostGIS support

Revision ID: 001
Revises: 
Create Date: 2025-10-04

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
    
    # Create enum types
    # Create ENUM types only if they don't exist
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'floodrisklevel') THEN
                CREATE TYPE floodrisklevel AS ENUM ('Very Low', 'Low', 'Medium', 'High', 'Very High');
            END IF;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'prioritylevel') THEN
                CREATE TYPE prioritylevel AS ENUM ('Low', 'Medium', 'High', 'Critical');
            END IF;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sessionstatus') THEN
                CREATE TYPE sessionstatus AS ENUM ('active', 'inactive', 'expired');
            END IF;
        END $$;
    """)
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_active', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('status', postgresql.ENUM('active', 'inactive', 'expired', name='sessionstatus'), nullable=True),
        sa.Column('preferences', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_session_id', 'users', ['session_id'], unique=True)
    
    # Selected areas table
    op.create_table(
        'selected_areas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('center_lat', sa.Float(), nullable=False),
        sa.Column('center_lng', sa.Float(), nullable=False),
        sa.Column('area_km2', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_selected_areas_center', 'selected_areas', ['center_lat', 'center_lng'])
    op.create_index('idx_selected_areas_geometry', 'selected_areas', ['geometry'], postgresql_using='gist')
    op.create_index('ix_selected_areas_id', 'selected_areas', ['id'])
    
    # Environmental metrics table
    op.create_table(
        'environmental_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('area_id', sa.Integer(), nullable=False),
        sa.Column('heat_index', sa.Float(), nullable=False),
        sa.Column('air_quality_index', sa.Integer(), nullable=False),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('wind_speed', sa.Float(), nullable=True),
        sa.Column('precipitation', sa.Float(), nullable=True),
        sa.Column('green_coverage', sa.Float(), nullable=False),
        sa.Column('water_stress', sa.Float(), nullable=True),
        sa.Column('flood_risk', postgresql.ENUM('Very Low', 'Low', 'Medium', 'High', 'Very High', name='floodrisklevel'), nullable=False),
        sa.Column('population_estimate', sa.Integer(), nullable=True),
        sa.Column('building_count', sa.Integer(), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('data_source', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['area_id'], ['selected_areas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_env_metrics_area_time', 'environmental_metrics', ['area_id', 'recorded_at'])
    op.create_index('ix_environmental_metrics_id', 'environmental_metrics', ['id'])
    
    # Area analyses table
    op.create_table(
        'area_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('area_id', sa.Integer(), nullable=False),
        sa.Column('analysis_text', sa.Text(), nullable=False),
        sa.Column('summary', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('priority_level', postgresql.ENUM('Low', 'Medium', 'High', 'Critical', name='prioritylevel'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('ai_model', sa.String(length=100), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['area_id'], ['selected_areas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_area_analyses_area_time', 'area_analyses', ['area_id', 'created_at'])
    op.create_index('idx_area_analyses_user_time', 'area_analyses', ['user_id', 'created_at'])
    op.create_index('ix_area_analyses_id', 'area_analyses', ['id'])
    
    # Chat messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('area_context', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('ai_model', sa.String(length=100), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_chat_messages_role', 'chat_messages', ['role'])
    op.create_index('idx_chat_messages_user_time', 'chat_messages', ['user_id', 'created_at'])
    op.create_index('ix_chat_messages_id', 'chat_messages', ['id'])
    
    # NASA cache table
    op.create_table(
        'nasa_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('api_endpoint', sa.String(length=255), nullable=False),
        sa.Column('cache_key', sa.String(length=500), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('response_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('hit_count', sa.Integer(), nullable=True),
        sa.Column('last_accessed', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_nasa_cache_endpoint_key', 'nasa_cache', ['api_endpoint', 'cache_key'])
    op.create_index('idx_nasa_cache_expires', 'nasa_cache', ['expires_at'])
    op.create_index('idx_nasa_cache_location', 'nasa_cache', ['latitude', 'longitude'])
    op.create_index('ix_nasa_cache_cache_key', 'nasa_cache', ['cache_key'], unique=True)
    op.create_index('ix_nasa_cache_id', 'nasa_cache', ['id'])
    
    # Disaster events table
    op.create_table(
        'disaster_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('eonet_id', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('raw_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_disaster_events_geometry', 'disaster_events', ['geometry'], postgresql_using='gist')
    op.create_index('idx_disaster_events_location', 'disaster_events', ['latitude', 'longitude'])
    op.create_index('idx_disaster_events_status', 'disaster_events', ['status'])
    op.create_index('idx_disaster_events_type', 'disaster_events', ['event_type'])
    op.create_index('ix_disaster_events_eonet_id', 'disaster_events', ['eonet_id'], unique=True)
    op.create_index('ix_disaster_events_id', 'disaster_events', ['id'])
    
    # City presets table
    op.create_table(
        'city_presets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=False),
        sa.Column('center_lat', sa.Float(), nullable=False),
        sa.Column('center_lng', sa.Float(), nullable=False),
        sa.Column('zoom_level', sa.Integer(), nullable=True),
        sa.Column('bounds', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('population', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_city_presets_active', 'city_presets', ['is_active'])
    op.create_index('idx_city_presets_location', 'city_presets', ['center_lat', 'center_lng'])
    op.create_index('ix_city_presets_id', 'city_presets', ['id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('city_presets')
    op.drop_table('disaster_events')
    op.drop_table('nasa_cache')
    op.drop_table('chat_messages')
    op.drop_table('area_analyses')
    op.drop_table('environmental_metrics')
    op.drop_table('selected_areas')
    op.drop_table('users')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS sessionstatus;')
    op.execute('DROP TYPE IF EXISTS prioritylevel;')
    op.execute('DROP TYPE IF EXISTS floodrisklevel;')

