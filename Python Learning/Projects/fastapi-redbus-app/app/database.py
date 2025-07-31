from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv 
from urllib.parse import quote_plus
import os
import logging

# Setup basic logger
logger = logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv()

# Declare the Base class for ORM models
Base = declarative_base()

# Fetch DB configuration from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))  # Encode special characters in password
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# You can switch between these two for local or env config
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
try:
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    # Create a session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine and session created successfully.")
except Exception as e:
    logger.error(f"Failed to create engine or session: {e}")
    raise

def get_db():
    """
    Dependency function to get DB session for request lifecycle.
    Ensures session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")
