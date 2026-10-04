from __future__ import annotations

import time
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.db.schemas import ScanResponse
from app.engine.decision_engine import ScamShieldDecisionEngine
from app.services.ocr_service import OCRService
from app.services.scan_service import save_scan


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


# MacPorts installation path on the Intel macOS development machine.
# Keeping this explicit makes pytesseract work even when the backend
# process does not inherit /opt/local/bin in its PATH.
TESSERACT_PATH = "/opt/local/bin/tesseract"


def _configure_tesseract() -> None:
    """
    Configure pytesseract to use the MacPorts Tesseract binary.
    """
    try:
        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    except Exception as exc:
        raise RuntimeError(
            "Unable to configure the Tesseract OCR engine."
        ) from exc


def _merge_indicators(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Merge evidence from the OCR-extracted message and URLs.

    Duplicate indicators are removed using their signal, text,
    feature, and value fields.
    """

    merged: List[Dict[str, Any]] = []
    seen = set()

    for result in results:
        indicators = result.get("indicators") or []

        for indicator in indicators:
            if not isinstance(indicator, dict):
                continue

            key = (
                indicator.get("signal"),
                indicator.get("matched_text"),
                indicator.get("start"),
                indicator.get("end"),
                indicator.get("feature"),
                indicator.get("value"),
            )

            if key in seen:
                continue

            seen.add(key)
            merged.append(indicator)

    return merged


def _merge_drivers(
    results: List[Dict[str, Any]],
    key: str,
) -> List[Dict[str, Any]]:
    """
    Merge ML drivers from multiple analyses while removing duplicates.
    """

    merged: List[Dict[str, Any]] = []
    seen = set()

    for result in results:
        drivers = result.get(key) or []

        for driver in drivers:
            if not isinstance(driver, dict):
                continue

            driver_key = (
                driver.get("feature"),
                driver.get("direction"),
            )

            if driver_key in seen:
                continue

            seen.add(driver_key)
            merged.append(driver)

    return merged


def _merge_recommendations(
    results: List[Dict[str, Any]],
) -> List[str]:
    """
    Combine recommendations while preserving their order.
    """

    merged: List[str] = []
    seen = set()

    for result in results:
        recommendations = result.get(
            "recommendations"
        ) or []

        for recommendation in recommendations:
            if not isinstance(recommendation, str):
                continue

            recommendation = recommendation.strip()

            if not recommendation:
                continue

            key = recommendation.lower()

            if key in seen:
                continue

            seen.add(key)
            merged.append(recommendation)

    return merged


def _aggregate_results(
    ocr_text: str,
    url_results: List[Dict[str, Any]],
    message_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build one unified screenshot result.

    The strongest detected risk across the extracted message
    and every extracted URL determines the final prediction/risk.

    This is deliberately not screenshot-example matching:
    every screenshot is processed from its actual OCR text
    and any actual URLs discovered inside it.
    """

    all_results = [message_result] + url_results

    highest_result = max(
        all_results,
        key=lambda item: float(
            (item.get("risk") or {}).get(
                "risk_score",
                0.0,
            )
        ),
    )

    highest_risk = highest_result.get("risk") or {}

    indicators = _merge_indicators(
        all_results
    )

    risk_drivers = _merge_drivers(
        all_results,
        "ml_risk_drivers",
    )

    legitimacy_drivers = _merge_drivers(
        all_results,
        "ml_legitimacy_drivers",
    )

    recommendations = _merge_recommendations(
        all_results
    )

    # Use the strongest model-estimated scam probability
    # across the OCR message and extracted URLs.
    scam_probability = max(
        float(
            (
                result.get(
                    "model_estimated_probabilities"
                )
                or {}
            ).get(
                "scam",
                0.0,
            )
        )
        for result in all_results
    )

    legitimate_probability = max(
        0.0,
        min(
            1.0,
            1.0 - scam_probability,
        ),
    )

    prediction = (
        "scam"
        if scam_probability >= 0.5
        else "legitimate"
    )

    risk = dict(highest_risk)

    risk["model_estimated_scam_probability"] = round(
        scam_probability,
        6,
    )

    risk["base_score"] = round(
        scam_probability * 100.0,
        2,
    )

    # Keep the strongest risk score from the existing RiskEngine.
    risk["risk_score"] = float(
        highest_risk.get(
            "risk_score",
            0.0,
        )
    )

    risk["rule_bonus"] = round(
        float(
            highest_risk.get(
                "rule_bonus",
                0.0,
            )
        ),
        2,
    )

    risk["risk_level"] = highest_risk.get(
        "risk_level",
        "SAFE",
    )

    risk["critical_signal_triggered"] = any(
        bool(
            (
                result.get("risk") or {}
            ).get(
                "critical_signal_triggered",
                False,
            )
        )
        for result in all_results
    )

    critical_signals = []

    for result in all_results:
        result_risk = result.get("risk") or {}

        for signal in result_risk.get(
            "critical_signals",
            [],
        ):
            if signal not in critical_signals:
                critical_signals.append(signal)

    risk["critical_signals"] = critical_signals

    unique_signals = []

    for indicator in indicators:
        signal = indicator.get("signal")

        if signal and signal not in unique_signals:
            unique_signals.append(signal)

    risk["unique_signals"] = unique_signals

    # Prefer the category from the strongest result.
    category = highest_result.get(
        "category"
    )

    if not isinstance(category, dict):
        category = {
            "category": None,
            "source": None,
            "confidence": None,
        }

    result: Dict[str, Any] = {
        "input_type": "screenshot",
        "prediction": prediction,
        "model_estimated_probabilities": {
            "scam": round(
                scam_probability,
                6,
            ),
            "legitimate": round(
                legitimate_probability,
                6,
            ),
        },
        "risk": risk,
        "category": category,
        "indicators": indicators,
        "ml_risk_drivers": risk_drivers,
        "ml_legitimacy_drivers": legitimacy_drivers,
        "recommendations": recommendations,
        "ocr_text": ocr_text,
        "extracted_urls": [
            url_result.get(
                "url"
            )
            for url_result in url_results
            if url_result.get("url")
        ],
        "screenshot_pipeline": {
            "ocr_completed": True,
            "urls_detected": len(url_results),
            "message_analyzed": True,
        },
    }

    return result


@router.post(
    "/screenshot",
    response_model=ScanResponse,
    summary="Analyze a screenshot using OCR",
)
async def analyze_screenshot(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Analyze an uploaded screenshot through the complete
    ScamShield OCR pipeline.

    Pipeline:

        SCREENSHOT
            ↓
        OCR
            ↓
        MESSAGE ANALYSIS
            ↓
        URL EXTRACTION
            ↓
        URL ANALYSIS
            ↓
        UNIFIED RESULT
            ↓
        HISTORY
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A screenshot file is required.",
        )

    content_type = (
        file.content_type
        or ""
    ).lower()

    if not content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only image files are accepted.",
        )

    try:
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded screenshot is empty.",
            )

        _configure_tesseract()

        start_time = time.perf_counter()

        ocr_text = (
            OCRService.extract_text_from_bytes(
                image_bytes
            )
        )

        extracted_urls = (
            OCRService.extract_urls(
                ocr_text
            )
        )

        decision_engine = (
            ScamShieldDecisionEngine()
        )

        message_result = (
            decision_engine.analyze_message(
                ocr_text
            )
        )

        url_results: List[
            Dict[str, Any]
        ] = []

        for url in extracted_urls:
            url_result = (
                decision_engine.analyze_url(
                    url
                )
            )

            url_results.append(
                url_result
            )

        result = _aggregate_results(
            ocr_text=ocr_text,
            url_results=url_results,
            message_result=message_result,
        )

        processing_time_ms = (
            time.perf_counter()
            - start_time
        ) * 1000.0

        result["processing_time_ms"] = round(
            processing_time_ms,
            2,
        )

        # Save the OCR text as the history preview source.
        record = save_scan(
            db=db,
            input_text=ocr_text,
            result=result,
            processing_time_ms=processing_time_ms,
        )

        result["scan_id"] = record.id
        result["history_saved"] = True

        return result

    except HTTPException:
        raise

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Screenshot analysis failed: "
                f"{str(exc)}"
            ),
        ) from exc
