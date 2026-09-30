import os
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ScamShield"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Team & Competition Metadata
    TEAM_NAME: str = "OBSIDIAN"
    COMPETITION: str = "INNOV12"
    PRIMARY_TRACK: str = "Cyber & Digital Trust"
    SUPPORTING_TRACK: str = "AI & GenAI"
    TEAM_MEMBERS: List[str] = [
        "Soham Mitra — CSE, 3rd Year",
        "Khyati K Doshi — CSE (IOTCSBT), 3rd Year",
        "Srinistha Biswas — CSE (IOTCSBT), 3rd Year",
    ]

    # Database Configuration (PostgreSQL primary with SQLite fallback)
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/scamshield",
        description="Primary PostgreSQL database URL",
    )
    SQLITE_FALLBACK_URL: str = Field(
        default="sqlite:///./scamshield.db",
        description="Local fallback SQLite database URL",
    )

    # CORS Configuration
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TRUSTED_BRANDS_PATH: str = "app/config/trusted_brands.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
