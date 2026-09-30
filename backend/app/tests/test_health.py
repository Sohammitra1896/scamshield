import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "ScamShield"
    assert data["team"] == "OBSIDIAN"
    assert data["status"] == "online"


def test_health_endpoint():
    response = client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "ScamShield"
    assert data["version"] == settings.VERSION
    assert data["team"] == "OBSIDIAN"
    assert data["competition"] == "INNOV12"
    assert "Soham Mitra" in str(data["team_members"])
    assert "database" in data
    assert data["database"]["status"] == "connected"
