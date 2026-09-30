import os
import joblib
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from app.ml.preprocessor import normalize_text_for_tfidf


class TextMessageAnalyzer:
    """
    Explainable Text Message Classifier using TF-IDF + Calibrated Logistic Regression.
    Computes genuine probabilities and linear token feature contributions (w_i * x_i).
    """

    def __init__(self, artifacts_dir: Optional[str] = None):
        if artifacts_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            artifacts_dir = os.path.join(base_dir, "artifacts")
        
        self.artifacts_dir = artifacts_dir
        self.vectorizer = None
        self.model = None
        self.category_model = None
        self.metadata = None
        self.is_loaded = False
        
        self.load_artifacts()

    def load_artifacts(self) -> bool:
        """Load serialized model artifacts from disk."""
        vec_path = os.path.join(self.artifacts_dir, "text_vectorizer.joblib")
        model_path = os.path.join(self.artifacts_dir, "text_model.joblib")
        cat_path = os.path.join(self.artifacts_dir, "category_model.joblib")
        meta_path = os.path.join(self.artifacts_dir, "metadata.json")

        if os.path.exists(vec_path) and os.path.exists(model_path):
            try:
                self.vectorizer = joblib.load(vec_path)
                self.model = joblib.load(model_path)
                if os.path.exists(cat_path):
                    self.category_model = joblib.load(cat_path)
                if os.path.exists(meta_path):
                    import json
                    with open(meta_path, "r", encoding="utf-8") as f:
                        self.metadata = json.load(f)
                self.is_loaded = True
                return True
            except Exception as e:
                self.is_loaded = False
                return False
        self.is_loaded = False
        return False

    def predict(self, text: str) -> str:
        """Predict class label: 'scam' or 'legitimate'."""
        if not self.is_loaded:
            raise RuntimeError("Model artifacts are not loaded. Run train_models.py first.")
        norm = normalize_text_for_tfidf(text)
        vec = self.vectorizer.transform([norm])
        pred = self.model.predict(vec)[0]
        return str(pred)

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Compute genuine calibrated probability distribution.
        Returns {'legitimate': float, 'scam': float}
        """
        if not self.is_loaded:
            raise RuntimeError("Model artifacts are not loaded. Run train_models.py first.")
        norm = normalize_text_for_tfidf(text)
        vec = self.vectorizer.transform([norm])
        probs = self.model.predict_proba(vec)[0]
        
        classes = self.model.classes_
        result = {}
        for idx, cls in enumerate(classes):
            result[str(cls)] = float(probs[idx])
        return result

    def get_feature_contributions(self, text: str, top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Compute exact mathematical feature contribution for each token:
        contribution_i = x_i * beta_i
        
        Returns top positive (scam-driving) and top negative (legit-driving) terms.
        """
        if not self.is_loaded:
            raise RuntimeError("Model artifacts are not loaded.")

        norm = normalize_text_for_tfidf(text)
        vec = self.vectorizer.transform([norm])
        
        feature_names = self.vectorizer.get_feature_names_out()
        coefficients = self.model.coef_[0]  # Shape: (n_features,)
        
        # Non-zero indices in input vector
        cx = vec.tocoo()
        contributions = []
        for col, val in zip(cx.col, cx.data):
            token = feature_names[col]
            weight = float(coefficients[col])
            contrib = float(val * weight)
            contributions.append({
                "token": token,
                "tf_idf_value": round(float(val), 4),
                "model_coefficient": round(weight, 4),
                "contribution": round(contrib, 4)
            })

        # Sort by contribution
        sorted_contribs = sorted(contributions, key=lambda x: x["contribution"], reverse=True)
        
        positive_drivers = [c for c in sorted_contribs if c["contribution"] > 0][:top_k]
        negative_drivers = [c for c in sorted_contribs if c["contribution"] < 0]
        # Sort negative drivers ascending (most negative first)
        negative_drivers = sorted(negative_drivers, key=lambda x: x["contribution"])[:top_k]

        return {
            "positive_drivers": positive_drivers,
            "negative_drivers": negative_drivers,
        }

    def predict_category(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Predict threat category among the 8 student threat categories.
        """
        if self.category_model is None or not self.is_loaded:
            return None
        norm = normalize_text_for_tfidf(text)
        vec = self.vectorizer.transform([norm])
        pred = self.category_model.predict(vec)[0]
        probs = self.category_model.predict_proba(vec)[0]
        confidence = float(np.max(probs))
        
        return {
            "category": str(pred),
            "confidence": round(confidence, 4)
        }
