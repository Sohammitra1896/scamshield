from fastapi import APIRouter, HTTPException

from app.db.schemas import AnalyzeMessageRequest, ScanResponse
from app.engine.decision_engine import ScamShieldDecisionEngine


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


@router.post(
    "/message",
    response_model=ScanResponse,
    summary="Analyze a message",
)
def analyze_message(request: AnalyzeMessageRequest):
    """
    Analyze message text using the ScamShield ML and rule-based
    decision pipeline.
    """

    try:
        engine = ScamShieldDecisionEngine()

        result = engine.analyze_message(request.message)

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Message analysis failed: {exc}",
        ) from exc
