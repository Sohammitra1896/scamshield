import os
import json
import pytest
import numpy as np

from app.ml.preprocessor import (
    clean_text,
    normalize_text_for_tfidf,
    extract_url_features,
    load_trusted_brands,
)
from app.ml.text_classifier import TextMessageAnalyzer
from app.ml.url_classifier import URLRiskClassifier


@pytest.fixture(scope="module")
def text_analyzer():
    analyzer = TextMessageAnalyzer()
    assert analyzer.is_loaded, "TextMessageAnalyzer failed to load model artifacts!"
    return analyzer


@pytest.fixture(scope="module")
def url_classifier():
    classifier = URLRiskClassifier()
    assert classifier.is_loaded, "URLRiskClassifier failed to load model artifacts!"
    return classifier


# 1. Dataset Loading Tests
def test_dataset_files_exist():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    threat_path = os.path.join(base_dir, "datasets", "student_threat_corpus.json")
    demo_path = os.path.join(base_dir, "datasets", "demo_scenarios.json")
    url_path = os.path.join(base_dir, "datasets", "url_corpus.json")

    assert os.path.exists(threat_path), "student_threat_corpus.json missing"
    assert os.path.exists(demo_path), "demo_scenarios.json missing"
    assert os.path.exists(url_path), "url_corpus.json missing"

    with open(threat_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data.get("samples", [])) > 0, "No samples in student threat corpus"

    with open(demo_path, "r", encoding="utf-8") as f:
        demo = json.load(f)
        assert len(demo.get("scenarios", [])) > 0, "No scenarios in demo dataset"


# 2 & 3. Split Isolation & No Demo/Test Overlap
def test_metadata_isolation():
    artifacts_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "artifacts"
    )
    meta_path = os.path.join(artifacts_dir, "metadata.json")
    assert os.path.exists(meta_path), "metadata.json not found in artifacts"

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    leak = meta.get("leakage_verification", {})
    assert leak.get("train_demo_exact_overlap_count") == 0, "Demo leaked into train set"
    assert leak.get("test_demo_exact_overlap_count") == 0, "Demo leaked into test set"
    assert leak.get("train_test_exact_overlap_count") == 0, "Train and test overlap detected"
    assert leak.get("demo_isolation_passed") is True, "Demo isolation check failed"


# 4. Preprocessing Tests
def test_text_preprocessing():
    raw = "Urgent: Win Rs. 50,000! Visit http://scam.xyz or call 9876543210. Pay to user@okaxis."
    norm = normalize_text_for_tfidf(raw)
    assert "__url__" in norm
    assert "__money__" in norm
    assert "__phone__" in norm
    assert "__upi__" in norm


# 5. Model Loading
def test_models_loaded(text_analyzer, url_classifier):
    assert text_analyzer.vectorizer is not None
    assert text_analyzer.model is not None
    assert url_classifier.scaler is not None
    assert url_classifier.model is not None


# 6 & 7. predict_proba() & Probability Range
def test_predict_proba_range(text_analyzer):
    sample = "You won a lottery of 1000000 rupees. Call now to claim prize."
    probs = text_analyzer.predict_proba(sample)
    
    assert "scam" in probs
    assert "legitimate" in probs
    assert 0.0 <= probs["scam"] <= 1.0
    assert 0.0 <= probs["legitimate"] <= 1.0
    assert abs((probs["scam"] + probs["legitimate"]) - 1.0) < 1e-4

    # Legitimate sample check
    legit_sample = "Reminder: The operating systems lecture is postponed to 2 PM tomorrow in Hall 3."
    legit_probs = text_analyzer.predict_proba(legit_sample)
    assert legit_probs["legitimate"] > legit_probs["scam"]


# 8. Feature Attribution
def test_feature_attribution(text_analyzer):
    text = "Selected for internship! Pay registration fee of Rs. 1500 to confirm slot."
    contribs = text_analyzer.get_feature_contributions(text, top_k=5)
    
    assert "positive_drivers" in contribs
    assert "negative_drivers" in contribs
    assert len(contribs["positive_drivers"]) > 0

    for driver in contribs["positive_drivers"]:
        assert "token" in driver
        assert "tf_idf_value" in driver
        assert "model_coefficient" in driver
        assert "contribution" in driver
        assert driver["contribution"] > 0, "Positive driver must have positive contribution"


# 9. URL Feature Extraction
def test_url_feature_extraction():
    url = "http://internsha1a-stipend.xyz/verify?token=12345"
    brands = load_trusted_brands()
    feats = extract_url_features(url, brands)
    
    assert feats["is_https"] == 0.0
    assert feats["has_suspicious_tld"] == 1.0
    assert feats["sensitive_token_count"] >= 1.0
    assert feats["brand_spoofing_score"] == 1.0  # internsha1a spoof of internshala


# 10. URL Model Prediction
def test_url_model_prediction(url_classifier):
    phishing_url = "http://sbi-kyc-pan-update.online/banking/login.php"
    legit_url = "https://internshala.com/student/dashboard"

    phish_pred = url_classifier.predict(phishing_url)
    phish_probs = url_classifier.predict_proba(phishing_url)
    assert phish_pred == "scam"
    assert phish_probs["scam"] > 0.5

    legit_pred = url_classifier.predict(legit_url)
    legit_probs = url_classifier.predict_proba(legit_url)
    assert legit_pred == "legitimate"
    assert legit_probs["legitimate"] > 0.5


# 11. Fresh Python Process Loading Test
def test_fresh_process_loading():
    import subprocess
    cmd = [
        "backend/venv/bin/python",
        "-c",
        "from app.ml.text_classifier import TextMessageAnalyzer; "
        "from app.ml.url_classifier import URLRiskClassifier; "
        "t = TextMessageAnalyzer(); u = URLRiskClassifier(); "
        "assert t.is_loaded and u.is_loaded; "
        "p = t.predict('test message'); "
        "print('LOADED_OK')"
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "backend"
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert res.returncode == 0
    assert "LOADED_OK" in res.stdout
