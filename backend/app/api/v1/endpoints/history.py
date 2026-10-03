from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.db.models import ScanRecord
from app.db.schemas import (
    HistoryRecordSchema,
    HistoryResponse,
)
from app.services.scan_service import normalize_risk_level


router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get(
    "",
    response_model=HistoryResponse,
    summary="Get scan history",
)
def get_history(
    search: Optional[str] = Query(
        default=None,
        max_length=100,
    ),
    risk_level: Optional[str] = Query(
        default=None,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    """
    Return persisted scans in newest-first order.
    Supports search, risk-level filtering and pagination.
    """

    query = db.query(ScanRecord)

    if search:
        term = f"%{search.strip()}%"

        query = query.filter(
            or_(
                ScanRecord.input_preview.ilike(term),
                ScanRecord.threat_category.ilike(term),
                ScanRecord.scan_type.ilike(term),
            )
        )

    if risk_level:
        query = query.filter(
            ScanRecord.risk_level
            == normalize_risk_level(risk_level)
        )

    total = query.count()

    records = (
        query.order_by(
            desc(ScanRecord.created_at)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = [
        HistoryRecordSchema.model_validate(record)
        for record in records
    ]

    return HistoryResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{scan_id}",
    response_model=HistoryRecordSchema,
    summary="Get one historical scan",
)
def get_history_record(
    scan_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one persisted scan with all stored evidence.
    """

    record = (
        db.query(ScanRecord)
        .filter(ScanRecord.id == scan_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Scan {scan_id} was not found.",
        )

    return HistoryRecordSchema.model_validate(
        record
    )
