from fastapi import APIRouter
from app.config import settings
from app.core.database import get_db_status
from app.db.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def get_health() -> HealthResponse:
    """
    Genuine health check endpoint providing service health and project metadata.
    """
    db_status = get_db_status()
    return HealthResponse(
        status="healthy",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        team=settings.TEAM_NAME,
        competition=settings.COMPETITION,
        tracks={
            "primary": settings.PRIMARY_TRACK,
            "supporting": settings.SUPPORTING_TRACK,
        },
        team_members=settings.TEAM_MEMBERS,
        database=db_status,
        environment=settings.ENVIRONMENT,
    )
