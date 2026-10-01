import os
import joblib
import numpy as np
from typing import Dict, Any, List, Optional
from app.ml.preprocessor import extract_url_features, load_trusted_brands


class URLRiskClassifier:
    """
    Explainable URL Risk Classifier using StandardScaler + Logistic Regression.
    Evaluates lexical/structural security features and calculates exact feature contributions.
    """

    FEATURE_KEYS = [
        "url_len",
        "host_len",
        "path_len",
        "query_len",
        "dot_count",
        "subdomain_count",
        "hyphen_count",
        "special_char_count",
        "digits_in_host",
        "is_ip",
        "is_https",
        "has_suspicious_tld",
        "sensitive_token_count",
        "has_hex_encoding",
        "has_credentials",
        "host_entropy",
        "brand_spoofing_score",
    ]

    def __init__(self, artifacts_dir: Optional[str] = None):
        if artifacts_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            artifacts_dir = os.path.join(base_dir, "artifacts")
        
        self.artifacts_dir = artifacts_dir
        self.scaler = None
        self.model = None
        self.metadata = None
        self.is_loaded = False
        self.trusted_brands = load_trusted_brands()

        self.load_artifacts()

    def load_artifacts(self) -> bool:
        """Load serialized scaler and model artifacts from disk."""
        scaler_path = os.path.join(self.artifacts_dir, "url_scaler.joblib")
        model_path = os.path.join(self.artifacts_dir, "url_model.joblib")

        if os.path.exists(scaler_path) and os.path.exists(model_path):
            try:
                self.scaler = joblib.load(scaler_path)
                self.model = joblib.load(model_path)
                self.is_loaded = True
                return True
            except Exception:
                self.is_loaded = False
                return False
        self.is_loaded = False
        return False

    def _get_feature_vector(self, url: str) -> np.ndarray:
        feats = extract_url_features(url, self.trusted_brands)
        vec = [feats[k] for k in self.FEATURE_KEYS]
        return np.array(vec).reshape(1, -1)

    def predict(self, url: str) -> str:
        """Predict class label: 'scam' or 'legitimate'."""
        if not self.is_loaded:
            raise RuntimeError("URL model artifacts not loaded. Run train_models.py first.")
        vec = self._get_feature_vector(url)
        scaled = self.scaler.transform(vec)
        pred = self.model.predict(scaled)[0]
        return str(pred)

    def predict_proba(self, url: str) -> Dict[str, float]:
        """
        Compute model-estimated probability distribution from logistic regression sigmoid output.
        Note: No calibration procedure (e.g. CalibratedClassifierCV) was applied.
        Returns {'legitimate': float, 'scam': float}
        """
        if not self.is_loaded:
            raise RuntimeError("URL model artifacts not loaded. Run train_models.py first.")
        vec = self._get_feature_vector(url)
        scaled = self.scaler.transform(vec)
        probs = self.model.predict_proba(scaled)[0]

        classes = self.model.classes_
        result = {}
        for idx, cls in enumerate(classes):
            result[str(cls)] = float(probs[idx])
        return result

    def get_feature_contributions(self, url: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Compute mathematical contribution of each standardized feature:
        contribution_i = z_i * beta_i
        """
        if not self.is_loaded:
            raise RuntimeError("URL model artifacts not loaded.")

        raw_feats = extract_url_features(url, self.trusted_brands)
        vec = self._get_feature_vector(url)
        scaled = self.scaler.transform(vec)[0]  # shape (n_features,)
        
        coefs = self.model.coef_[0]  # shape (n_features,)
        
        contributions = []
        for i, key in enumerate(self.FEATURE_KEYS):
            z_val = float(scaled[i])
            c_val = float(coefs[i])
            contrib = float(z_val * c_val)
            contributions.append({
                "feature": key,
                "raw_value": round(float(raw_feats[key]), 3),
                "standardized_value": round(z_val, 3),
                "model_coefficient": round(c_val, 3),
                "contribution": round(contrib, 3)
            })

        sorted_contribs = sorted(contributions, key=lambda x: x["contribution"], reverse=True)
        positive_drivers = [c for c in sorted_contribs if c["contribution"] > 0][:top_k]
        negative_drivers = sorted([c for c in sorted_contribs if c["contribution"] < 0], key=lambda x: x["contribution"])[:top_k]

        return {
            "raw_features": raw_feats,
            "positive_drivers": positive_drivers,
            "negative_drivers": negative_drivers
        }
