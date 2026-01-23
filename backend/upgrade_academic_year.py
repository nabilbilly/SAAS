import logging
from sqlalchemy import text, inspect
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upgrade():
    inspector = inspect(engine)
    table_name = "academicyears"
    
    # Check if table exists, if not maybe it's singular
    if not inspector.has_table(table_name):
        logger.warning(f"Table {table_name} not found. Checking for 'academicyear'...")
        if inspector.has_table("academicyear"):
            table_name = "academicyear"
        else:
            logger.error(f"Could not find table for AcademicYear model.")
            return

    columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    with engine.connect() as conn:
        conn.begin()
        try:
            if "start_date" not in columns:
                logger.info(f"Adding start_date to {table_name}")
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN start_date DATE"))
            
            if "end_date" not in columns:
                logger.info(f"Adding end_date to {table_name}")
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN end_date DATE"))
                
            conn.commit()
            logger.info("Upgrade complete.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Upgrade failed: {e}")

if __name__ == "__main__":
    upgrade()
