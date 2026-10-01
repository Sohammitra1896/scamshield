import json
import os
from typing import Any, Dict, List, Optional

import joblib
import numpy as np

from app.ml.preprocessor import normalize_text_for_tfidf


class TextMessageAnalyzer:
    """
    Explainable text scam classifier using TF-IDF + Logistic Regression.

    The analyzer:
    - loads trained artifacts once
    - returns model-estimated probabilities
    - calculates exact TF-IDF * coefficient contributions
    - optionally predicts a student threat category
    """

    def __init__(self, artifacts_dir: Optional[str] = None):
        if artifacts_dir is None:
            artifacts_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "artifacts",
            )

        self.artifacts_dir = artifacts_dir

        self.vectorizer = None
        self.model = None
        self.category_model = None
        self.metadata = None
        self.is_loaded = False

        self.load_artifacts()

    def load_artifacts(self) -> bool:
        """Load serialized Phase 2 artifacts from disk."""
        vec_path = os.path.join(
            self.artifacts_dir, "text_vectorizer.joblib"
        )
        model_path = os.path.join(
            self.artifacts_dir, "text_model.joblib"
        )
        category_path = os.path.join(
            self.artifacts_dir, "category_model.joblib"
        )
        metadata_path = os.path.join(
            self.artifacts_dir, "metadata.json"
        )

        self.is_loaded = False

        if not os.path.exists(vec_path):
            return False

        if not os.path.exists(model_path):
            return False

        try:
            self.vectorizer = joblib.load(vec_path)
            self.model = joblib.load(model_path)

            if os.path.exists(category_path):
                self.category_model = joblib.load(category_path)

            if os.path.exists(metadata_path):
                with open(metadata_path, "r", encoding="utf-8") as file:
                    self.metadata = json.load(file)

            self.is_loaded = True
            return True

        except Exception:
            self.vectorizer = None
            self.model = None
            self.category_model = None
            self.metadata = None
            self.is_loaded = False
            return False

    def _validate_text(self, text: str) -> str:
        """Validate and normalize input before inference."""
        if not isinstance(text, str):
            raise TypeError("Message must be a string.")

        cleaned = text.strip()

        if not cleaned:
            raise ValueError("Message cannot be empty.")

        return cleaned

    def _transform(self, text: str):
        """Apply the exact training-time normalization and vectorization."""
        message = self._validate_text(text)

        normalized = normalize_text_for_tfidf(message)
        vector = self.vectorizer.transform([normalized])

        return message, normalized, vector

    def predict(self, text: str) -> str:
        """
        Return the model prediction.

        Possible outputs:
        - scam
        - legitimate
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model artifacts are not loaded. "
                "Run train_models.py first."
            )

        _, _, vector = self._transform(text)

        prediction = self.model.predict(vector)[0]

        return str(prediction)

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Return model-estimated class probabilities.

        This is NOT probability-calibrated unless a separate
        calibration procedure has been applied during training.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model artifacts are not loaded. "
                "Run train_models.py first."
            )

        _, _, vector = self._transform(text)

        probabilities = self.model.predict_proba(vector)[0]
        classes = self.model.classes_

        result = {}

        for index, class_name in enumerate(classes):
            result[str(class_name)] = float(probabilities[index])

        return result

    def get_feature_contributions(
        self,
        text: str,
        top_k: int = 5,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calculate exact linear feature contributions.

        contribution = TF-IDF value * Logistic Regression coefficient
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model artifacts are not loaded."
            )

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        _, _, vector = self._transform(text)

        feature_names = self.vectorizer.get_feature_names_out()

        if not hasattr(self.model, "coef_"):
            raise RuntimeError(
                "The loaded model does not expose linear coefficients."
            )

        coefficients = self.model.coef_[0]

        sparse_vector = vector.tocoo()

        contributions = []

        for column, value in zip(
            sparse_vector.col,
            sparse_vector.data,
        ):
            feature = feature_names[column]
            tfidf_value = float(value)
            coefficient = float(coefficients[column])

            contribution = tfidf_value * coefficient

            contributions.append(
                {
                    "token": str(feature),
                    "tf_idf_value": round(tfidf_value, 6),
                    "model_coefficient": round(coefficient, 6),
                    "contribution": round(contribution, 6),
                }
            )

        positive = sorted(
            [
                item
                for item in contributions
                if item["contribution"] > 0
            ],
            key=lambda item: item["contribution"],
            reverse=True,
        )[:top_k]

        negative = sorted(
            [
                item
                for item in contributions
                if item["contribution"] < 0
            ],
            key=lambda item: item["contribution"],
        )[:top_k]

        return {
            "positive_drivers": positive,
            "negative_drivers": negative,
        }

    def predict_category(
        self,
        text: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Predict one of the student threat categories.

        This is an experimental/supporting component because
        category-specific training data is currently limited.
        """
        if not self.is_loaded:
            raise RuntimeError(
                "Model artifacts are not loaded."
            )

        if self.category_model is None:
            return None

        _, _, vector = self._transform(text)

        prediction = self.category_model.predict(vector)[0]
        probabilities = self.category_model.predict_proba(vector)[0]

        confidence = float(np.max(probabilities))

        return {
            "category": str(prediction),
            "confidence": round(confidence, 6),
        }

    def analyze(
        self,
        text: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Return a single structured message-analysis result.

        This method combines:
        - prediction
        - model-estimated probabilities
        - feature attribution
        - optional category prediction

        It does not generate safety recommendations or rule-based
        risk explanations. Those belong to later phases.
        """
        message = self._validate_text(text)

        probabilities = self.predict_proba(message)
        prediction = self.predict(message)
        contributions = self.get_feature_contributions(
            message,
            top_k=top_k,
        )
        category = self.predict_category(message)

        return {
            "prediction": prediction,
            "scam_probability": round(
                probabilities.get("scam", 0.0),
                6,
            ),
            "legitimate_probability": round(
                probabilities.get("legitimate", 0.0),
                6,
            ),
            "positive_drivers": contributions["positive_drivers"],
            "negative_drivers": contributions["negative_drivers"],
            "category": category,
        }
