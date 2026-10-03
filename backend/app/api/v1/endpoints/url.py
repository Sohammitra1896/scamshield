import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.db.schemas import (
    AnalyzeURLRequest,
    ScanResponse,
)
from app.engine.decision_engine import ScamShieldDecisionEngine
from app.services.scan_service import save_scan


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


@router.post(
    "/url",
    response_model=ScanResponse,
    summary="Analyze a URL",
)
def analyze_url(
    request: AnalyzeURLRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze a URL and persist the completed scan.
    """

    try:
        engine = ScamShieldDecisionEngine()

        start_time = time.perf_counter()

        result = engine.analyze_url(
            request.url
        )

        processing_time_ms = (
            time.perf_counter() - start_time
        ) * 1000.0

        record = save_scan(
            db=db,
            input_text=request.url,
            result=result,
            processing_time_ms=processing_time_ms,
        )

        response = dict(result)

        response["scan_id"] = record.id
        response["processing_time_ms"] = round(
            processing_time_ms,
            3,
        )
        response["history_saved"] = True

        return response

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"URL analysis failed: {exc}",
        ) from exc
