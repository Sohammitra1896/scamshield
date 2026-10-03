from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


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

    scan_id: Optional[int] = None
    processing_time_ms: Optional[float] = None
    history_saved: bool = False


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
    items: List[HistoryRecordSchema]
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
