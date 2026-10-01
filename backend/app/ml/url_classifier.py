import json
import os
from typing import Any, Dict, List, Optional

import joblib
import numpy as np

from app.ml.preprocessor import (
    extract_url_features,
    load_trusted_brands,
)


class URLRiskClassifier:
    """
    Explainable URL risk classifier using:

    StandardScaler + Logistic Regression

    The classifier:
    - loads trained artifacts once
    - returns model-estimated probabilities
    - exposes raw and standardized URL features
    - calculates exact feature contributions
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
            artifacts_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "artifacts",
            )

        self.artifacts_dir = artifacts_dir

        self.scaler = None
        self.model = None
        self.metadata = None
        self.trusted_brands = []

        self.is_loaded = False

        self._load_trusted_brands()
        self.load_artifacts()

    def _load_trusted_brands(self) -> None:
        """Load the configurable trusted-brand list."""
        try:
            self.trusted_brands = load_trusted_brands()
        except Exception:
            self.trusted_brands = []

    def load_artifacts(self) -> bool:
        """Load the Phase 2 scaler, model and optional metadata."""
        scaler_path = os.path.join(
            self.artifacts_dir,
            "url_scaler.joblib",
        )

        model_path = os.path.join(
            self.artifacts_dir,
            "url_model.joblib",
        )

        metadata_path = os.path.join(
            self.artifacts_dir,
            "metadata.json",
        )

        self.is_loaded = False

        if not os.path.exists(scaler_path):
            return False

        if not os.path.exists(model_path):
            return False

        try:
            self.scaler = joblib.load(scaler_path)
            self.model = joblib.load(model_path)

            if os.path.exists(metadata_path):
                with open(
                    metadata_path,
                    "r",
                    encoding="utf-8",
                ) as file:
                    self.metadata = json.load(file)

            self.is_loaded = True
            return True

        except Exception:
            self.scaler = None
            self.model = None
            self.metadata = None
            self.is_loaded = False
            return False

    def _validate_url(self, url: str) -> str:
        """Validate and normalize the input URL."""
        if not isinstance(url, str):
            raise TypeError("URL must be a string.")

        cleaned = url.strip()

        if not cleaned:
            raise ValueError("URL cannot be empty.")

        return cleaned

    def _get_feature_vector(
        self,
        url: str,
    ) -> tuple[Dict[str, float], np.ndarray]:
        """Extract raw URL features and return a model-ready vector."""
        validated_url = self._validate_url(url)

        raw_features = extract_url_features(
            validated_url,
            self.trusted_brands,
        )

        vector = np.array(
            [
                raw_features[key]
                for key in self.FEATURE_KEYS
            ],
            dtype=float,
        ).reshape(1, -1)

        return raw_features, vector

    def _get_scaled_features(
        self,
        url: str,
    ) -> tuple[Dict[str, float], np.ndarray]:
        """Return raw and standardized URL feature values."""
        raw_features, vector = self._get_feature_vector(url)

        if self.scaler is None:
            raise RuntimeError("URL scaler is not loaded.")

        scaled = self.scaler.transform(vector)[0]

        return raw_features, scaled

    def predict(self, url: str) -> str:
        """Return the model-predicted class."""
        if not self.is_loaded:
            raise RuntimeError(
                "URL model artifacts are not loaded. "
                "Run train_models.py first."
            )

        _, vector = self._get_feature_vector(url)
        scaled = self.scaler.transform(vector)

        prediction = self.model.predict(scaled)[0]

        return str(prediction)

    def predict_proba(
        self,
        url: str,
    ) -> Dict[str, float]:
        """
        Return model-estimated class probabilities.

        No probability-calibration procedure was applied during Phase 2.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "URL model artifacts are not loaded. "
                "Run train_models.py first."
            )

        _, vector = self._get_feature_vector(url)
        scaled = self.scaler.transform(vector)

        probabilities = self.model.predict_proba(scaled)[0]
        classes = self.model.classes_

        result: Dict[str, float] = {}

        for index, class_name in enumerate(classes):
            result[str(class_name)] = float(
                probabilities[index]
            )

        return result

    def get_feature_contributions(
        self,
        url: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Calculate exact feature contributions.

        contribution = standardized_feature_value
                      * Logistic Regression coefficient

        Positive contribution means movement toward the model's
        positive class. The result is converted to a scam-oriented
        interpretation using the actual model class ordering.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "URL model artifacts are not loaded."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        raw_features, scaled = self._get_scaled_features(url)

        if not hasattr(self.model, "coef_"):
            raise RuntimeError(
                "The loaded URL model does not expose coefficients."
            )

        coefficients = self.model.coef_[0]
        classes = list(self.model.classes_)

        # LogisticRegression's coef_[0] points toward classes_[1].
        # Convert contributions so positive means "toward scam".
        if len(classes) != 2:
            raise RuntimeError(
                "URL risk model must be binary."
            )

        scam_class_position = classes.index("scam")

        if scam_class_position == 1:
            scam_direction = 1.0
        else:
            scam_direction = -1.0

        contributions: List[Dict[str, Any]] = []

        for index, key in enumerate(self.FEATURE_KEYS):
            standardized_value = float(scaled[index])
            coefficient = float(coefficients[index])

            raw_contribution = (
                standardized_value * coefficient
            )

            scam_contribution = (
                raw_contribution * scam_direction
            )

            contributions.append(
                {
                    "feature": key,
                    "raw_value": round(
                        float(raw_features[key]),
                        6,
                    ),
                    "standardized_value": round(
                        standardized_value,
                        6,
                    ),
                    "model_coefficient": round(
                        coefficient,
                        6,
                    ),
                    "contribution": round(
                        scam_contribution,
                        6,
                    ),
                }
            )

        positive_drivers = sorted(
            [
                item
                for item in contributions
                if item["contribution"] > 0
            ],
            key=lambda item: item["contribution"],
            reverse=True,
        )[:top_k]

        negative_drivers = sorted(
            [
                item
                for item in contributions
                if item["contribution"] < 0
            ],
            key=lambda item: item["contribution"],
        )[:top_k]

        return {
            "raw_features": raw_features,
            "positive_drivers": positive_drivers,
            "negative_drivers": negative_drivers,
        }

    def analyze(
        self,
        url: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Return a complete URL analysis result.

        This phase provides:
        - model prediction
        - model-estimated probabilities
        - raw URL features
        - explainable model contributions

        Deterministic safety rules and final risk tiers belong
        to the later Risk & Explanation Engine phase.
        """
        validated_url = self._validate_url(url)

        probabilities = self.predict_proba(validated_url)
        prediction = self.predict(validated_url)

        contributions = self.get_feature_contributions(
            validated_url,
            top_k=top_k,
        )

        return {
            "url": validated_url,
            "prediction": prediction,
            "scam_probability": round(
                probabilities.get("scam", 0.0),
                6,
            ),
            "legitimate_probability": round(
                probabilities.get("legitimate", 0.0),
                6,
            ),
            "raw_features": contributions["raw_features"],
            "positive_drivers": contributions[
                "positive_drivers"
            ],
            "negative_drivers": contributions[
                "negative_drivers"
            ],
        }
