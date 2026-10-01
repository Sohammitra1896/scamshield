from fastapi import APIRouter, HTTPException

from app.db.schemas import AnalyzeURLRequest, ScanResponse
from app.engine.decision_engine import ScamShieldDecisionEngine


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


@router.post(
    "/url",
    response_model=ScanResponse,
    summary="Analyze a URL",
)
def analyze_url(request: AnalyzeURLRequest):
    """
    Analyze a URL using ScamShield's URL ML classifier,
    deterministic security rules, risk engine, and explanation engine.
    """

    try:
        engine = ScamShieldDecisionEngine()

        result = engine.analyze_url(request.url)

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"URL analysis failed: {exc}",
        ) from exc
