from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models import DetectedEvidence, ScanRecord


def normalize_risk_level(value: Optional[str]) -> str:
    """
    Convert display-style risk levels such as 'HIGH RISK'
    into database-friendly values such as 'HIGH_RISK'.
    """
    if not value:
        return "SAFE"

    return str(value).strip().upper().replace(" ", "_")


def make_input_preview(value: str) -> str:
    """
    Store a compact one-line preview for history listings.
    """
    cleaned = " ".join(value.strip().split())

    if len(cleaned) <= 255:
        return cleaned

    return cleaned[:252] + "..."


def extract_category(result: Dict[str, Any]) -> Optional[str]:
    category = result.get("category")

    if not isinstance(category, dict):
        return None

    return category.get("category")


def save_scan(
    db: Session,
    input_text: str,
    result: Dict[str, Any],
    processing_time_ms: float,
) -> ScanRecord:
    """
    Persist one completed analysis together with rule evidence
    and ML feature attributions.
    """

    risk = result.get("risk") or {}

    record = ScanRecord(
        scan_type=str(result.get("input_type", "unknown")),
        input_preview=make_input_preview(input_text),
        risk_level=normalize_risk_level(
            risk.get("risk_level")
        ),
        risk_score=float(
            risk.get("risk_score", 0.0)
        ),
        threat_category=extract_category(result),
        processing_time_ms=float(processing_time_ms),
    )

    db.add(record)
    db.flush()

    indicators = result.get("indicators") or []

    for indicator in indicators:
        if not isinstance(indicator, dict):
            continue

        evidence = DetectedEvidence(
            scan_id=record.id,
            evidence_type="rule_match",
            signal_name=str(
                indicator.get("signal", "unknown")
            ),
            verbatim_quote=indicator.get("matched_text"),
            character_offset_start=indicator.get("start"),
            character_offset_end=indicator.get("end"),
            feature_weight=None,
            severity=indicator.get("severity"),
        )

        db.add(evidence)

    risk_drivers = result.get("ml_risk_drivers") or []
    legitimacy_drivers = result.get("ml_legitimacy_drivers") or []

    for driver in [*risk_drivers, *legitimacy_drivers]:
        if not isinstance(driver, dict):
            continue

        feature = str(
            driver.get("feature", "unknown")
        )

        contribution = driver.get("contribution")

        evidence = DetectedEvidence(
            scan_id=record.id,
            evidence_type="ml_attribution",
            signal_name=feature,
            verbatim_quote=None,
            character_offset_start=None,
            character_offset_end=None,
            feature_weight=(
                float(contribution)
                if contribution is not None
                else None
            ),
            severity=None,
        )

        db.add(evidence)

    db.commit()
    db.refresh(record)

    return record
