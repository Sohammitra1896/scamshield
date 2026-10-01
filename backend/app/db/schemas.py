from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
    critical_signals: List[str] = []
    unique_signals: List[str] = []


class CategorySchema(BaseModel):
    category: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = None


class FeatureDriverSchema(BaseModel):
    feature: str
    contribution: float
    direction: str


class ScanResponse(BaseModel):
    input_type: str
    prediction: str

    model_estimated_probabilities: Dict[str, float]

    risk: RiskSchema

    category: CategorySchema

    indicators: List[IndicatorSchema] = []

    ml_risk_drivers: List[FeatureDriverSchema] = []

    ml_legitimacy_drivers: List[FeatureDriverSchema] = []

    # The recommendation engine currently returns plain defensive
    # recommendation strings, so the API schema must reflect that.
    recommendations: List[str] = []


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
