import os
import subprocess

import pytest

from app.ml.text_classifier import TextMessageAnalyzer


@pytest.fixture(scope="module")
def analyzer():
    model = TextMessageAnalyzer()

    assert model.is_loaded
    assert model.vectorizer is not None
    assert model.model is not None

    return model


def test_predict_returns_valid_class(analyzer):
    text = (
        "Congratulations! You have been selected for an internship. "
        "Pay Rs. 1999 registration fee immediately."
    )

    prediction = analyzer.predict(text)

    assert prediction in {"scam", "legitimate"}


def test_probabilities_are_valid(analyzer):
    text = (
        "Congratulations! You won a lottery prize. "
        "Pay the processing fee now."
    )

    probabilities = analyzer.predict_proba(text)

    assert "scam" in probabilities
    assert "legitimate" in probabilities

    scam = probabilities["scam"]
    legitimate = probabilities["legitimate"]

    assert 0.0 <= scam <= 1.0
    assert 0.0 <= legitimate <= 1.0

    assert abs((scam + legitimate) - 1.0) < 1e-6


def test_prediction_matches_highest_probability(analyzer):
    text = (
        "Congratulations! You have won a cash prize. "
        "Send your bank details immediately."
    )

    probabilities = analyzer.predict_proba(text)
    prediction = analyzer.predict(text)

    expected = max(
        probabilities,
        key=probabilities.get,
    )

    assert prediction == expected


def test_feature_contribution_structure(analyzer):
    text = (
        "Selected for internship. "
        "Pay registration fee of Rs. 1500 to confirm slot."
    )

    result = analyzer.get_feature_contributions(text, top_k=5)

    assert "positive_drivers" in result
    assert "negative_drivers" in result

    for item in result["positive_drivers"]:
        assert "token" in item
        assert "tf_idf_value" in item
        assert "model_coefficient" in item
        assert "contribution" in item

        assert item["tf_idf_value"] >= 0
        assert item["contribution"] > 0


def test_contribution_formula(analyzer):
    text = (
        "Selected for internship. "
        "Pay registration fee immediately."
    )

    result = analyzer.get_feature_contributions(text, top_k=10)

    for item in result["positive_drivers"]:
        expected = (
            item["tf_idf_value"]
            * item["model_coefficient"]
        )

        assert abs(
            item["contribution"] - expected
        ) < 1e-5


def test_legitimate_message_is_processed(analyzer):
    text = (
        "Reminder: Database Systems lecture slides "
        "and assignment 3 are available on Classroom."
    )

    result = analyzer.analyze(text)

    assert result["prediction"] in {
        "scam",
        "legitimate",
    }

    assert 0.0 <= result["scam_probability"] <= 1.0
    assert 0.0 <= result["legitimate_probability"] <= 1.0


def test_empty_message_is_rejected(analyzer):
    with pytest.raises(ValueError):
        analyzer.predict("")

    with pytest.raises(ValueError):
        analyzer.predict_proba("   ")

    with pytest.raises(ValueError):
        analyzer.analyze("")


def test_analyze_returns_expected_structure(analyzer):
    text = (
        "Urgent scholarship update. "
        "Pay processing fee today to claim your scholarship."
    )

    result = analyzer.analyze(text)

    assert "prediction" in result
    assert "scam_probability" in result
    assert "legitimate_probability" in result
    assert "positive_drivers" in result
    assert "negative_drivers" in result
    assert "category" in result


def test_fresh_process_loads_message_analyzer():
    command = [
        "backend/venv/bin/python",
        "-c",
        (
            "from app.ml.text_classifier import TextMessageAnalyzer; "
            "a = TextMessageAnalyzer(); "
            "assert a.is_loaded; "
            "r = a.analyze('Pay a registration fee now'); "
            "assert 'scam_probability' in r; "
            "print('MESSAGE_ANALYZER_OK')"
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
    assert "MESSAGE_ANALYZER_OK" in result.stdout
