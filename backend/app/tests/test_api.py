from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "ScamShield"
    assert data["team"] == "OBSIDIAN"
    assert data["status"] == "online"


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["project"] == "ScamShield"


def test_message_endpoint():
    response = client.post(
        "/api/v1/analyze/message",
        json={
            "message": (
                "Congratulations! You have been selected for a remote "
                "internship. Pay Rs. 1999 registration fee immediately."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["input_type"] == "message"
    assert data["prediction"] in {"scam", "legitimate"}

    assert "model_estimated_probabilities" in data
    assert "risk" in data
    assert "category" in data
    assert "indicators" in data
    assert "ml_risk_drivers" in data
    assert "ml_legitimacy_drivers" in data
    assert "recommendations" in data

    assert data["history_saved"] is True
    assert isinstance(data["scan_id"], int)
    assert data["processing_time_ms"] >= 0

    assert 0.0 <= data["risk"]["model_estimated_scam_probability"] <= 1.0
    assert 0.0 <= data["risk"]["risk_score"] <= 100.0


def test_message_validation():
    response = client.post(
        "/api/v1/analyze/message",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_url_endpoint():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "http://internsha1a-stipend.xyz/verify?token=123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["input_type"] == "url"
    assert data["prediction"] in {"scam", "legitimate"}

    assert "model_estimated_probabilities" in data
    assert "risk" in data
    assert "category" in data
    assert "indicators" in data
    assert "recommendations" in data

    assert data["history_saved"] is True
    assert isinstance(data["scan_id"], int)
    assert data["processing_time_ms"] >= 0

    assert 0.0 <= data["risk"]["model_estimated_scam_probability"] <= 1.0
    assert 0.0 <= data["risk"]["risk_score"] <= 100.0


def test_url_validation():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": "",
        },
    )

    assert response.status_code == 422


def test_screenshot_endpoint_does_not_fabricate_results():
    response = client.post(
        "/api/v1/analyze/screenshot",
        files={
            "file": (
                "test.png",
                b"fake-image-data",
                "image/png",
            )
        },
    )

    assert response.status_code == 501

    data = response.json()

    assert "Phase 9" in data["detail"]
