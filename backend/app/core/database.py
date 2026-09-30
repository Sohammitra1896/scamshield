import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

logger = logging.getLogger("scamshield.database")

Base = declarative_base()

# Determine active database engine with fallback
active_db_type = "unknown"
engine = None
SessionLocal = None


def init_db_engine():
    global active_db_type, engine, SessionLocal

    # 1. Try PostgreSQL Primary
    try:
        pg_engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3},
        )
        with pg_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine = pg_engine
        active_db_type = "postgresql"
        logger.info("Successfully connected to primary PostgreSQL database.")
    except Exception as e:
        logger.warning(
            "Primary PostgreSQL connection failed (%s). Falling back to SQLite: %s",
            str(e),
            settings.SQLITE_FALLBACK_URL,
        )
        # 2. Fallback to SQLite
        sqlite_engine = create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False},
        )
        engine = sqlite_engine
        active_db_type = "sqlite"

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine


# Initialize engine on module load
init_db_engine()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to yield database session."""
    if SessionLocal is None:
        init_db_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_status() -> dict:
    """Return current database connection status without raising exceptions."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "active_engine": active_db_type,
            "fallback_active": (active_db_type == "sqlite"),
        }
    except Exception as err:
        return {
            "status": "error",
            "error": str(err),
            "active_engine": active_db_type,
        }
