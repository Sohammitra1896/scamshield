from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    project: str = Field(..., json_schema_extra={"example": "ScamShield"})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})
    team: str = Field(..., json_schema_extra={"example": "OBSIDIAN"})
    competition: str = Field(..., json_schema_extra={"example": "INNOV12"})
    tracks: Dict[str, str] = Field(
        ...,
        json_schema_extra={"example": {"primary": "Cyber & Digital Trust", "supporting": "AI & GenAI"}},
    )
    team_members: List[str]
    database: Dict[str, Any]
    environment: str
