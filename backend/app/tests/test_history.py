from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_history_endpoint():
    response = client.post(
        "/api/v1/analyze/message",
        json={
            "message": (
                "Congratulations! You have been selected "
                "for a remote internship. Pay Rs. 1999 "
                "registration fee immediately."
            )
        },
    )

    assert response.status_code == 200

    scan = response.json()

    assert scan["history_saved"] is True
    assert isinstance(scan["scan_id"], int)

    history_response = client.get(
        "/api/v1/history"
    )

    assert history_response.status_code == 200

    data = history_response.json()

    assert "items" in data
    assert "total" in data

    assert data["total"] >= 1

    matching = [
        item
        for item in data["items"]
        if item["id"] == scan["scan_id"]
    ]

    assert len(matching) == 1


def test_history_risk_filter():
    response = client.post(
        "/api/v1/analyze/url",
        json={
            "url": (
                "http://internsha1a-stipend.xyz/"
                "verify?token=123"
            )
        },
    )

    assert response.status_code == 200

    history_response = client.get(
        "/api/v1/history",
        params={
            "risk_level": "HIGH_RISK",
        },
    )

    assert history_response.status_code == 200

    data = history_response.json()

    for item in data["items"]:
        assert item["risk_level"] == "HIGH_RISK"


def test_history_detail():
    response = client.post(
        "/api/v1/analyze/message",
        json={
            "message": (
                "Reminder: Database Systems lecture slides "
                "are available on Classroom."
            )
        },
    )

    assert response.status_code == 200

    scan_id = response.json()["scan_id"]

    detail_response = client.get(
        f"/api/v1/history/{scan_id}"
    )

    assert detail_response.status_code == 200

    data = detail_response.json()

    assert data["id"] == scan_id
    assert "evidence" in data


def test_history_missing_record():
    response = client.get(
        "/api/v1/history/999999999"
    )

    assert response.status_code == 404


def test_stats_endpoint():
    response = client.get(
        "/api/v1/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_scans" in data
    assert "safe_scans" in data
    assert "low_risk_scans" in data
    assert "suspicious_scans" in data
    assert "high_risk_scans" in data
    assert "risk_distribution" in data
    assert "category_distribution" in data
    assert "average_risk_score" in data

    assert data["total_scans"] >= 0
