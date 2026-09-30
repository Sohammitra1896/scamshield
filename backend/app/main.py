import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router
from app.core.database import get_db_status

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("scamshield.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown routines.
    """
    logger.info("Initializing %s v%s...", settings.PROJECT_NAME, settings.VERSION)
    logger.info("Team: %s | Competition: %s", settings.TEAM_NAME, settings.COMPETITION)
    logger.info("Tracks: %s (Primary), %s (Supporting)", settings.PRIMARY_TRACK, settings.SUPPORTING_TRACK)
    
    # Check database status on startup
    db_status = get_db_status()
    logger.info("Database status: %s (Engine: %s, Fallback: %s)", 
                db_status.get("status"), 
                db_status.get("active_engine"), 
                db_status.get("fallback_active"))
    
    yield
    
    logger.info("Shutting down %s...", settings.PROJECT_NAME)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "ScamShield is an explainable AI-powered digital safety platform designed "
        "primarily for students and young digital users.\n\n"
        "Philosophy: DETECT → EXPLAIN → PROTECT\n\n"
        "Team OBSIDIAN — INNOV12 Competition"
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS if isinstance(settings.BACKEND_CORS_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root_redirect():
    """Root redirect with basic service information."""
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_url": f"{settings.API_V1_STR}/health",
        "team": settings.TEAM_NAME,
        "competition": settings.COMPETITION,
    }
