from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScanRecord(Base):
    """
    Relational record for an analyzed message, URL, or screenshot.
    Full history functionality will be finalized in Phase 8.
    """
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    scan_type = Column(String(50), nullable=False, index=True)  # 'message', 'url', 'screenshot'
    input_preview = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False, index=True)  # 'SAFE', 'LOW_RISK', 'SUSPICIOUS', 'HIGH_RISK'
    risk_score = Column(Float, nullable=False)  # 0.0 to 100.0
    threat_category = Column(String(100), nullable=True)
    processing_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    evidence = relationship("DetectedEvidence", back_populates="scan_record", cascade="all, delete-orphan")


class DetectedEvidence(Base):
    """
    Individual evidence indicators tied to a scan record.
    Preserves verbatim quotes from rules or ML token weights.
    """
    __tablename__ = "detected_evidence"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scan_records.id", ondelete="CASCADE"), nullable=False)
    evidence_type = Column(String(50), nullable=False)  # 'rule_match', 'ml_attribution'
    signal_name = Column(String(100), nullable=False)
    verbatim_quote = Column(Text, nullable=True)
    character_offset_start = Column(Integer, nullable=True)
    character_offset_end = Column(Integer, nullable=True)
    feature_weight = Column(Float, nullable=True)
    severity = Column(String(50), nullable=True)

    scan_record = relationship("ScanRecord", back_populates="evidence")
