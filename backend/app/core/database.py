import logging

from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.config import settings


logger = logging.getLogger("scamshield.database")


Base = declarative_base()

active_db_type = "unknown"
engine = None
SessionLocal = None
_tables_initialized = False


def init_db_engine():
    """
    Select PostgreSQL as the primary database and fall back to SQLite
    when PostgreSQL is unavailable.
    """
    global active_db_type, engine, SessionLocal

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

        logger.info(
            "Successfully connected to primary PostgreSQL database."
        )

    except Exception as exc:
        logger.warning(
            "Primary PostgreSQL connection failed (%s). "
            "Falling back to SQLite: %s",
            str(exc),
            settings.SQLITE_FALLBACK_URL,
        )

        sqlite_engine = create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False},
        )

        engine = sqlite_engine
        active_db_type = "sqlite"

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return engine


init_db_engine()


def create_tables():
    """
    Create all SQLAlchemy tables for the active database.

    Importing models inside this function avoids a circular import during
    initial database module loading.
    """
    global _tables_initialized

    if engine is None:
        init_db_engine()

    if _tables_initialized:
        return

    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    _tables_initialized = True

    logger.info(
        "Database tables initialized using %s.",
        active_db_type,
    )


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.
    """
    if SessionLocal is None:
        init_db_engine()

    create_tables()

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_db_status() -> dict:
    """
    Return the active database status without raising exceptions.
    """
    try:
        if engine is None:
            init_db_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "active_engine": active_db_type,
            "fallback_active": active_db_type == "sqlite",
        }

    except Exception as err:
        return {
            "status": "error",
            "error": str(err),
            "active_engine": active_db_type,
            "fallback_active": active_db_type == "sqlite",
        }
