import os
import subprocess

import pytest

from app.ml.url_classifier import URLRiskClassifier


@pytest.fixture(scope="module")
def classifier():
    model = URLRiskClassifier()

    assert model.is_loaded
    assert model.scaler is not None
    assert model.model is not None

    return model


def test_predict_returns_valid_class(classifier):
    url = "http://sbi-kyc-pan-update.online/banking/login.php"

    prediction = classifier.predict(url)

    assert prediction in {"scam", "legitimate"}


def test_probabilities_are_valid(classifier):
    url = "http://internsha1a-stipend.xyz/verify?token=123"

    probabilities = classifier.predict_proba(url)

    assert "scam" in probabilities
    assert "legitimate" in probabilities

    scam = probabilities["scam"]
    legitimate = probabilities["legitimate"]

    assert 0.0 <= scam <= 1.0
    assert 0.0 <= legitimate <= 1.0

    assert abs(
        (scam + legitimate) - 1.0
    ) < 1e-6


def test_prediction_matches_probability(classifier):
    url = "http://sbi-kyc-pan-update.online/banking/login.php"

    prediction = classifier.predict(url)
    probabilities = classifier.predict_proba(url)

    expected = max(
        probabilities,
        key=probabilities.get,
    )

    assert prediction == expected


def test_feature_contributions_have_expected_structure(
    classifier,
):
    url = "http://internsha1a-stipend.xyz/verify?token=123"

    result = classifier.get_feature_contributions(
        url,
        top_k=5,
    )

    assert "raw_features" in result
    assert "positive_drivers" in result
    assert "negative_drivers" in result

    assert len(result["raw_features"]) == 17

    for item in result["positive_drivers"]:
        assert "feature" in item
        assert "raw_value" in item
        assert "standardized_value" in item
        assert "model_coefficient" in item
        assert "contribution" in item

        assert item["contribution"] > 0


def test_contribution_formula(classifier):
    url = "http://internsha1a-stipend.xyz/verify?token=123"

    result = classifier.get_feature_contributions(
        url,
        top_k=17,
    )

    classes = list(classifier.model.classes_)

    scam_direction = (
        1.0 if classes.index("scam") == 1
        else -1.0
    )

    for item in (
        result["positive_drivers"]
        + result["negative_drivers"]
    ):
        expected = (
            item["standardized_value"]
            * item["model_coefficient"]
            * scam_direction
        )

        assert abs(
            item["contribution"] - expected
        ) < 1e-5


def test_known_phishing_url(classifier):
    url = "http://sbi-kyc-pan-update.online/banking/login.php"

    result = classifier.analyze(url)

    assert result["prediction"] == "scam"
    assert result["scam_probability"] > 0.5


def test_known_legitimate_url(classifier):
    url = "https://internshala.com/student/dashboard"

    result = classifier.analyze(url)

    assert result["prediction"] == "legitimate"
    assert result["legitimate_probability"] > 0.5


def test_empty_url_is_rejected(classifier):
    with pytest.raises(ValueError):
        classifier.predict("")

    with pytest.raises(ValueError):
        classifier.predict_proba("   ")

    with pytest.raises(ValueError):
        classifier.analyze("")


def test_analyze_returns_expected_structure(classifier):
    url = "https://internshala.com/student/dashboard"

    result = classifier.analyze(url)

    assert "url" in result
    assert "prediction" in result
    assert "scam_probability" in result
    assert "legitimate_probability" in result
    assert "raw_features" in result
    assert "positive_drivers" in result
    assert "negative_drivers" in result


def test_fresh_process_loads_url_classifier():
    command = [
        "backend/venv/bin/python",
        "-c",
        (
            "from app.ml.url_classifier "
            "import URLRiskClassifier; "
            "u = URLRiskClassifier(); "
            "assert u.is_loaded; "
            "r = u.analyze("
            "'https://internshala.com/student/dashboard'"
            "); "
            "assert 'scam_probability' in r; "
            "print('URL_ANALYZER_OK')"
        ),
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = "backend"

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "URL_ANALYZER_OK" in result.stdout
