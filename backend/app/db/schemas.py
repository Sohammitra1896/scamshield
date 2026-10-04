from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AnalyzeMessageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Message text to analyze",
    )


class AnalyzeURLRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        description="URL to analyze",
    )


class IndicatorSchema(BaseModel):
    signal: str
    severity: str
    description: str
    matched_text: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    source: str


class RiskSchema(BaseModel):
    model_estimated_scam_probability: float
    base_score: float
    rule_bonus: float
    risk_score: float
    risk_level: str
    critical_signal_triggered: bool

    critical_signals: List[str] = Field(
        default_factory=list
    )

    unique_signals: List[str] = Field(
        default_factory=list
    )


class CategorySchema(BaseModel):
    category: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = None


class FeatureDriverSchema(BaseModel):
    feature: str
    contribution: float
    direction: str


class ScanResponse(BaseModel):
    # Original backend response
    input_type: str
    prediction: str

    model_estimated_probabilities: Dict[str, float]

    risk: RiskSchema

    category: Optional[CategorySchema] = None

    indicators: List[IndicatorSchema] = Field(
        default_factory=list
    )

    ml_risk_drivers: List[FeatureDriverSchema] = Field(
        default_factory=list
    )

    ml_legitimacy_drivers: List[FeatureDriverSchema] = Field(
        default_factory=list
    )

    recommendations: List[str] = Field(
        default_factory=list
    )

    # Flattened fields for Next.js frontend
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    scam_probability: Optional[float] = None
    model_scam_probability: Optional[float] = None
    threat_category: Optional[str] = None

    evidence: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    positive_drivers: List[str] = Field(
        default_factory=list
    )

    negative_drivers: List[str] = Field(
        default_factory=list
    )

    recommended_actions: List[str] = Field(
        default_factory=list
    )

    # Screenshot / OCR fields
    ocr_text: Optional[str] = None

    extracted_urls: List[str] = Field(
        default_factory=list
    )

    screenshot_pipeline: Optional[Dict[str, Any]] = None

    # Frontend compatibility
    url_analysis: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    input_preview: Optional[str] = None
    type: Optional[str] = None

    scan_id: Optional[int] = None

    processing_time_ms: Optional[float] = None

    history_saved: bool = False

    @model_validator(mode="before")
    @classmethod
    def build_frontend_fields(cls, values):
        """
        Preserve the original backend response while also exposing
        flat fields expected by the Next.js frontend.
        """

        if not isinstance(values, dict):
            return values

        risk = values.get("risk") or {}

        probabilities = (
            values.get("model_estimated_probabilities")
            or {}
        )

        category = values.get("category") or {}

        indicators = values.get("indicators") or []

        ml_risk_drivers = (
            values.get("ml_risk_drivers") or []
        )

        ml_legitimacy_drivers = (
            values.get("ml_legitimacy_drivers") or []
        )

        recommendations = (
            values.get("recommendations") or []
        )

        # Risk
        values.setdefault(
            "risk_level",
            risk.get("risk_level"),
        )

        values.setdefault(
            "risk_score",
            risk.get("risk_score"),
        )

        values.setdefault(
            "scam_probability",
            probabilities.get("scam"),
        )

        values.setdefault(
            "model_scam_probability",
            probabilities.get("scam"),
        )

        # Category
        values.setdefault(
            "threat_category",
            category.get("category"),
        )

        # Evidence
        if not values.get("evidence"):
            evidence = []

            for indicator in indicators:
                if not isinstance(indicator, dict):
                    continue

                evidence.append(
                    {
                        "label": indicator.get("signal"),
                        "text": indicator.get("matched_text"),
                        "severity": indicator.get("severity"),
                        "description": indicator.get(
                            "description"
                        ),
                    }
                )

            values["evidence"] = evidence

        # Positive ML drivers
        if not values.get("positive_drivers"):
            positive = []

            for driver in ml_risk_drivers:
                if not isinstance(driver, dict):
                    continue

                feature = driver.get("feature")
                contribution = driver.get("contribution")

                if feature:
                    if contribution is not None:
                        positive.append(
                            f"{feature} (+{float(contribution):.4f})"
                        )
                    else:
                        positive.append(str(feature))

            values["positive_drivers"] = positive

        # Legitimacy ML drivers
        if not values.get("negative_drivers"):
            negative = []

            for driver in ml_legitimacy_drivers:
                if not isinstance(driver, dict):
                    continue

                feature = driver.get("feature")
                contribution = driver.get("contribution")

                if feature:
                    if contribution is not None:
                        negative.append(
                            f"{feature} ({float(contribution):.4f})"
                        )
                    else:
                        negative.append(str(feature))

            values["negative_drivers"] = negative

        # Recommendations
        values.setdefault(
            "recommended_actions",
            recommendations,
        )

        # Generic compatibility
        values.setdefault(
            "type",
            values.get("input_type"),
        )

        return values


class HealthResponse(BaseModel):
    status: str
    project: str
    version: str
    team: str
    competition: str
    tracks: Dict[str, str]
    team_members: List[str]
    database: Dict[str, Any]
    environment: str


class ErrorResponse(BaseModel):
    detail: str


class HistoryEvidenceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    evidence_type: str
    signal_name: str
    verbatim_quote: Optional[str] = None
    character_offset_start: Optional[int] = None
    character_offset_end: Optional[int] = None
    feature_weight: Optional[float] = None
    severity: Optional[str] = None


class HistoryRecordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scan_type: str
    input_preview: str
    risk_level: str
    risk_score: float
    threat_category: Optional[str] = None
    processing_time_ms: Optional[float] = None
    created_at: datetime

    evidence: List[HistoryEvidenceSchema] = Field(
        default_factory=list
    )


class HistoryResponse(BaseModel):
    items: List[HistoryRecordSchema] = Field(
        default_factory=list
    )

    total: int
    skip: int
    limit: int


class StatsResponse(BaseModel):
    total_scans: int
    safe_scans: int
    low_risk_scans: int
    suspicious_scans: int
    high_risk_scans: int

    risk_distribution: Dict[str, int]

    category_distribution: Dict[str, int]

    average_risk_score: float
