"""
Database seeding script with sample data for Sibu & Sibu Jaya, Sarawak
"""
import asyncio
from datetime import datetime, timedelta, date
from sqlalchemy import select, func
from shapely.geometry import box
from geoalchemy2.shape import from_shape
import logging

from app.database import get_db_context
from app.models.db_models import (
    User, SelectedArea, EnvironmentalMetric, AreaAnalysis,
    ChatMessage, NASACache, DisasterEvent, CityPreset,
    FloodRiskLevel, PriorityLevel, SessionStatus
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample areas in Sibu & Sibu Jaya
SAMPLE_AREAS = [
    {
        "name": "Sibu Town Center",
        "bbox": {"north": 2.315, "south": 2.295, "east": 111.835, "west": 111.815},
        "city": "Sibu",
        "description": "Downtown commercial district along Rajang River"
    },
    {
        "name": "Sibu Jaya Residential",
        "bbox": {"north": 2.285, "south": 2.265, "east": 111.845, "west": 111.825},
        "city": "Sibu",
        "description": "Growing residential area with new developments"
    },
    {
        "name": "Sibu Industrial Area",
        "bbox": {"north": 2.335, "south": 2.315, "east": 111.855, "west": 111.835},
        "city": "Sibu",
        "description": "Industrial zone with palm oil processing facilities"
    },
    {
        "name": "Rajang Riverfront",
        "bbox": {"north": 2.325, "south": 2.305, "east": 111.825, "west": 111.805},
        "city": "Sibu",
        "description": "Riverside area prone to seasonal flooding"
    },
    {
        "name": "Sibu Jaya Commercial Hub",
        "bbox": {"north": 2.275, "south": 2.255, "east": 111.835, "west": 111.815},
        "city": "Sibu",
        "description": "New commercial development area"
    },
]

def create_areas(db):
    """Create sample geographic areas"""
    logger.info("Creating sample areas...")
    
    # Check if areas already exist
    count = db.query(SelectedArea).count()
    
    if count > 0:
        logger.info(f"Areas already exist ({count} found). Skipping...")
        return db.query(SelectedArea).all()
    
    # Create demo user first
    user = db.query(User).filter(User.session_id == "demo_user").first()
    if not user:
        user = User(session_id="demo_user", status=SessionStatus.ACTIVE)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    areas = []
    for area_data in SAMPLE_AREAS:
        bbox = area_data["bbox"]
        
        # Create Shapely polygon from bounding box
        polygon = box(bbox["west"], bbox["south"], bbox["east"], bbox["north"])
        
        # Calculate center point and area
        center_lat = (bbox["north"] + bbox["south"]) / 2
        center_lng = (bbox["east"] + bbox["west"]) / 2
        area_km2 = polygon.area * 111 * 111  # Rough conversion to km²
        
        area = SelectedArea(
            user_id=user.id,
            name=area_data["name"],
            geometry=from_shape(polygon, srid=4326),
            center_lat=center_lat,
            center_lng=center_lng,
            area_km2=area_km2
        )
        
        db.add(area)
        areas.append(area)
    
    db.commit()
    logger.info(f"✓ Created {len(areas)} sample areas")
    return areas

def create_analyses(db, areas):
    """Create sample analysis results"""
    logger.info("Creating sample analysis results...")
    
    # Check if analyses already exist
    count = db.query(AreaAnalysis).count()
    
    if count > 0:
        logger.info(f"Analyses already exist ({count} found). Skipping...")
        return
    
    user = db.query(User).filter(User.session_id == "demo_user").first()
    
    # Sample analysis data tailored for Sibu context
    analysis_templates = [
        {
            "heat_index": 31.5,
            "air_quality_index": 85,
            "green_coverage": 35.0,
            "flood_risk": FloodRiskLevel.MEDIUM,
            "population_estimate": 50000,
            "water_stress": 18.0,
            "analysis_text": "Sibu Town Center shows elevated urban heat island effects with temperature 2°C above rural baseline. Air quality is moderate (AQI 85) with seasonal haze concerns. Green coverage at 35% is below WHO recommendations. Flood risk is medium due to Rajang River proximity.",
            "summary": {
                "classification": "Urban commercial zone",
                "main_concerns": ["Elevated heat island", "Seasonal haze", "Flood risk"],
                "status": "Requires intervention"
            },
            "priority_level": PriorityLevel.HIGH
        },
        {
            "heat_index": 29.8,
            "air_quality_index": 68,
            "green_coverage": 52.0,
            "flood_risk": FloodRiskLevel.LOW,
            "population_estimate": 35000,
            "water_stress": 22.0,
            "analysis_text": "Sibu Jaya Residential maintains good environmental conditions with adequate green coverage (52%). Air quality is acceptable but shows increasing trend. Low flood risk makes it suitable for continued residential development.",
            "summary": {
                "classification": "Residential area with moderate density",
                "main_concerns": ["Air quality during haze season", "Growing population"],
                "status": "Generally healthy"
            },
            "priority_level": PriorityLevel.MEDIUM
        },
        {
            "heat_index": 33.2,
            "air_quality_index": 110,
            "green_coverage": 18.0,
            "flood_risk": FloodRiskLevel.MEDIUM,
            "population_estimate": 15000,
            "water_stress": 15.0,
            "analysis_text": "Industrial area shows critical environmental concerns with high heat stress (33.2°C), poor air quality (AQI 110), and minimal vegetation (18%). Immediate intervention required for worker safety and environmental compliance.",
            "summary": {
                "classification": "Industrial zone with environmental concerns",
                "main_concerns": ["Poor air quality", "High heat stress", "Low vegetation"],
                "status": "Critical intervention needed"
            },
            "priority_level": PriorityLevel.CRITICAL
        },
        {
            "heat_index": 28.5,
            "air_quality_index": 72,
            "green_coverage": 62.0,
            "flood_risk": FloodRiskLevel.HIGH,
            "population_estimate": 8000,
            "water_stress": 35.0,
            "analysis_text": "Rajang Riverfront has good environmental conditions but faces high flood risk due to seasonal water level changes. Green coverage is excellent (62%) but flood vulnerability requires careful development planning.",
            "summary": {
                "classification": "Riverfront area with high flood risk",
                "main_concerns": ["Extreme flood vulnerability", "Seasonal water level changes"],
                "status": "High risk zone"
            },
            "priority_level": PriorityLevel.HIGH
        },
        {
            "heat_index": 30.2,
            "air_quality_index": 75,
            "green_coverage": 45.0,
            "flood_risk": FloodRiskLevel.LOW,
            "population_estimate": 25000,
            "water_stress": 20.0,
            "analysis_text": "Sibu Jaya Commercial Hub shows moderate environmental conditions suitable for development. Air quality is acceptable, flood risk is low, and green coverage provides good foundation for sustainable growth.",
            "summary": {
                "classification": "Emerging commercial hub",
                "main_concerns": ["Rapid development pressure", "Infrastructure strain"],
                "status": "Moderate concern"
            },
            "priority_level": PriorityLevel.MEDIUM
        },
    ]
    
    for i, area in enumerate(areas):
        template = analysis_templates[i] if i < len(analysis_templates) else analysis_templates[0]
        
        analysis = AreaAnalysis(
            user_id=user.id,
            area_id=area.id,
            analysis_text=template["analysis_text"],
            summary=template["summary"],
            priority_level=template["priority_level"],
            ai_model="deepseek-chat-v3.1",
            processing_time_ms=2500
        )
        
        db.add(analysis)
    
    db.commit()
    logger.info(f"✓ Created {len(areas)} sample analyses")

def create_metrics(db, areas):
    """Create sample environmental metrics"""
    logger.info("Creating sample environmental metrics...")
    
    # Check if metrics already exist
    count = db.query(EnvironmentalMetric).count()
    
    if count > 0:
        logger.info(f"Metrics already exist ({count} found). Skipping...")
        return
    
    # Create metrics for each area
    metrics_data = [
        {"area_idx": 0, "heat": 31.5, "aqi": 85, "green": 35.0, "flood": FloodRiskLevel.MEDIUM, "pop": 50000},
        {"area_idx": 1, "heat": 29.8, "aqi": 68, "green": 52.0, "flood": FloodRiskLevel.LOW, "pop": 35000},
        {"area_idx": 2, "heat": 33.2, "aqi": 110, "green": 18.0, "flood": FloodRiskLevel.MEDIUM, "pop": 15000},
        {"area_idx": 3, "heat": 28.5, "aqi": 72, "green": 62.0, "flood": FloodRiskLevel.HIGH, "pop": 8000},
        {"area_idx": 4, "heat": 30.2, "aqi": 75, "green": 45.0, "flood": FloodRiskLevel.LOW, "pop": 25000},
    ]
    
    for metric_data in metrics_data:
        if metric_data["area_idx"] < len(areas):
            area = areas[metric_data["area_idx"]]
            
            metric = EnvironmentalMetric(
                area_id=area.id,
                heat_index=metric_data["heat"],
                air_quality_index=metric_data["aqi"],
                green_coverage=metric_data["green"],
                flood_risk=metric_data["flood"],
                population_estimate=metric_data["pop"],
                water_stress=15.0 + (metric_data["area_idx"] * 5),
                humidity=75.0 + (metric_data["area_idx"] * 2),
                wind_speed=3.5,
                precipitation=150.0,
                building_count=metric_data["pop"] // 50,  # Rough estimate
                data_source="NASA_POWER",
                recorded_at=datetime.utcnow()
            )
            
            db.add(metric)
    
    db.commit()
    logger.info(f"✓ Created {len(metrics_data)} environmental metrics")

def create_sample_chats(db, areas):
    """Create sample chat conversations"""
    logger.info("Creating sample chat history...")
    
    # Check if chats already exist
    count = db.query(ChatMessage).count()
    
    if count > 0:
        logger.info(f"Chats already exist ({count} found). Skipping...")
        return
    
    user = db.query(User).filter(User.session_id == "demo_user").first()
    
    sample_chats = [
        {
            "role": "user",
            "content": "What are the main environmental concerns in Sibu Town Center?",
            "area_context": {"area_id": areas[0].id, "area_name": areas[0].name}
        },
        {
            "role": "assistant",
            "content": "Based on the analysis of Sibu Town Center, there are three main environmental concerns: 1) Elevated urban heat island effect (31.5°C, which is 2°C above rural baseline), 2) Moderate air quality issues (AQI 85) especially during haze season from August to October, and 3) Flood risk (Medium level) due to proximity to Rajang River. The area also has limited tree canopy at only 35%, which is below the WHO recommended 20-30% minimum for urban areas.",
            "ai_model": "deepseek-chat-v3.1",
            "tokens_used": 150
        },
        {
            "role": "user",
            "content": "Where should we build a new park in Sibu Jaya?",
            "area_context": {"area_id": areas[1].id, "area_name": areas[1].name}
        },
        {
            "role": "assistant",
            "content": "I recommend focusing on the northeastern section of Sibu Jaya Residential for several reasons: 1) It currently has the lowest vegetation coverage in the area, 2) It experiences higher land surface temperatures compared to other parts, 3) It's within walking distance (500m) of high-density residential blocks serving approximately 5,000 residents, and 4) There are suitable vacant lots totaling 1.8 hectares that are available for development. Building a park here could reduce local temperatures by 1-2°C and improve air quality for the surrounding community.",
            "ai_model": "deepseek-chat-v3.1",
            "tokens_used": 180
        },
    ]
    
    for chat_data in sample_chats:
        chat = ChatMessage(
            user_id=user.id,
            role=chat_data["role"],
            content=chat_data["content"],
            area_context=chat_data.get("area_context"),
            ai_model=chat_data.get("ai_model"),
            tokens_used=chat_data.get("tokens_used"),
            created_at=datetime.utcnow()
        )
        db.add(chat)
    
    db.commit()
    logger.info(f"✓ Created {len(sample_chats)} sample chat messages")

def create_cache_sample(db):
    """Create sample NASA API cache entries"""
    logger.info("Creating sample NASA data cache...")
    
    # Check if cache already exists
    count = db.query(NASACache).count()
    
    if count > 0:
        logger.info(f"Cache entries already exist ({count} found). Skipping...")
        return
    
    sample_cache = NASACache(
        api_endpoint="imagery",
        cache_key="imagery_2.30_111.82_0.1",
        latitude=2.30,
        longitude=111.82,
        response_data={
            "url": "https://api.nasa.gov/planetary/earth/imagery",
            "date": "2024-12-01",
            "cloud_score": 0.15,
            "note": "Sample cached NASA imagery data for Sibu"
        },
        expires_at=datetime.utcnow() + timedelta(hours=24),
        hit_count=0,
        last_accessed=datetime.utcnow()
    )
    
    db.add(sample_cache)
    db.commit()
    logger.info("✓ Created sample cache entry")

def seed_database():
    """Main seeding function"""
    logger.info("="*60)
    logger.info("Starting database seeding for EchoSphere")
    logger.info("="*60)
    
    with get_db_context() as db:
        try:
            # Create areas first (needed for foreign keys)
            areas = create_areas(db)
            
            if not areas:
                # Areas already exist, fetch them for other operations
                areas = db.query(SelectedArea).all()
            
            # Create related data
            create_analyses(db, areas)
            create_metrics(db, areas)
            create_sample_chats(db, areas)
            create_cache_sample(db)
            
            logger.info("="*60)
            logger.info("✓ Database seeding completed successfully!")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"✗ Seeding failed: {e}")
            db.rollback()
            raise

def clear_all_data():
    """Clear all data from database (for testing)"""
    logger.warning("="*60)
    logger.warning("CLEARING ALL DATA FROM DATABASE")
    logger.warning("="*60)
    
    with get_db_context() as db:
        try:
            # Delete in reverse order of foreign keys
            db.query(ChatMessage).delete()
            db.query(EnvironmentalMetric).delete()
            db.query(AreaAnalysis).delete()
            db.query(NASACache).delete()
            db.query(DisasterEvent).delete()
            db.query(SelectedArea).delete()
            db.query(User).delete()
            
            db.commit()
            logger.warning("✓ All data cleared successfully")
            
        except Exception as e:
            logger.error(f"✗ Clear failed: {e}")
            db.rollback()
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument("--clear", action="store_true", help="Clear all data before seeding")
    args = parser.parse_args()
    
    if args.clear:
        clear_all_data()
    
    seed_database()
