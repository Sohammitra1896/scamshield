from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.db.models import ScanRecord
from app.db.schemas import StatsResponse


router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@router.get(
    "",
    response_model=StatsResponse,
    summary="Get scan statistics",
)
def get_stats(
    db: Session = Depends(get_db),
):
    """
    Return statistics calculated directly from persisted scans.
    """

    records = (
        db.query(ScanRecord)
        .all()
    )

    total = len(records)

    risk_distribution = Counter()
    category_distribution = Counter()

    for record in records:
        risk_distribution[
            record.risk_level
        ] += 1

        if record.threat_category:
            category_distribution[
                record.threat_category
            ] += 1

    safe_count = risk_distribution.get(
        "SAFE",
        0,
    )

    low_risk_count = risk_distribution.get(
        "LOW_RISK",
        0,
    )

    suspicious_count = risk_distribution.get(
        "SUSPICIOUS",
        0,
    )

    high_risk_count = risk_distribution.get(
        "HIGH_RISK",
        0,
    )

    average_risk_score = (
        sum(
            float(record.risk_score or 0.0)
            for record in records
        )
        / total
        if total
        else 0.0
    )

    return StatsResponse(
        total_scans=total,
        safe_scans=safe_count,
        low_risk_scans=low_risk_count,
        suspicious_scans=suspicious_count,
        high_risk_scans=high_risk_count,
        risk_distribution=dict(
            risk_distribution
        ),
        category_distribution=dict(
            category_distribution
        ),
        average_risk_score=round(
            average_risk_score,
            2,
        ),
    )
