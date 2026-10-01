from typing import Any, Dict, List, Optional

from app.engine.category_matcher import CategoryMatcher
from app.engine.explainability import ExplainabilityEngine
from app.engine.recommendations import RecommendationEngine
from app.engine.risk_engine import RiskEngine
from app.engine.rule_engine import RuleEngine
from app.ml.text_classifier import TextMessageAnalyzer
from app.ml.url_classifier import URLRiskClassifier


class ScamShieldDecisionEngine:
    """
    Central ScamShield orchestration layer.

    Pipeline:

        DETECT
          ↓
        EXPLAIN
          ↓
        PROTECT
    """

    def __init__(
        self,
        text_analyzer: Optional[
            TextMessageAnalyzer
        ] = None,
        url_analyzer: Optional[
            URLRiskClassifier
        ] = None,
    ):
        self.text_analyzer = (
            text_analyzer
            if text_analyzer is not None
            else TextMessageAnalyzer()
        )

        self.url_analyzer = (
            url_analyzer
            if url_analyzer is not None
            else URLRiskClassifier()
        )

        self.rule_engine = RuleEngine()

    def _build_result(
        self,
        input_type: str,
        prediction: str,
        scam_probability: float,
        legitimate_probability: float,
        indicators: List[Dict[str, Any]],
        model_category: Optional[Dict[str, Any]],
        model_drivers: List[Dict[str, Any]],
        original_input: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Combine ML evidence, rule evidence, risk scoring,
        explanation, category, and recommendations.
        """
        risk = RiskEngine.calculate(
            scam_probability=scam_probability,
            indicators=indicators,
        )

        category = CategoryMatcher.match(
            indicators=indicators,
            model_category=model_category,
            scam_probability=scam_probability,
        )

        if prediction == "scam":
            selected_drivers = model_drivers
            explanation_type = "scam"
        else:
            selected_drivers = model_drivers
            explanation_type = "legitimate"

        rule_explanations = (
            ExplainabilityEngine.build_rule_explanations(
                indicators
            )
        )

        ml_explanations = (
            ExplainabilityEngine.build_ml_explanations(
                selected_drivers,
                prediction_type=explanation_type,
            )
        )

        recommendations = (
            RecommendationEngine.generate(
                indicators
            )
        )

        result: Dict[str, Any] = {
            "input_type": input_type,
            "prediction": prediction,
            "model_estimated_probabilities": {
                "scam": round(
                    scam_probability,
                    6,
                ),
                "legitimate": round(
                    legitimate_probability,
                    6,
                ),
            },
            "risk": risk,
            "category": category,
            "indicators": indicators,
            "explanations": (
                rule_explanations
                + ml_explanations
            ),
            "recommendations": recommendations,
        }

        if original_input is not None:
            if input_type == "url":
                result["url"] = original_input
            else:
                result["message"] = original_input

        return result

    def analyze_message(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Analyze a message using:
        ML + deterministic rules + risk synthesis.
        """
        if not isinstance(text, str):
            raise TypeError(
                "Message must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Message cannot be empty."
            )

        ml_result = self.text_analyzer.analyze(
            text
        )

        indicators = (
            self.rule_engine.analyze_message(
                text
            )
        )

        return self._build_result(
            input_type="message",
            prediction=ml_result["prediction"],
            scam_probability=float(
                ml_result["scam_probability"]
            ),
            legitimate_probability=float(
                ml_result["legitimate_probability"]
            ),
            indicators=indicators,
            model_category=ml_result.get(
                "category"
            ),
            model_drivers=(
                ml_result["positive_drivers"]
                if ml_result["prediction"] == "scam"
                else ml_result["negative_drivers"]
            ),
            original_input=text,
        )

    def analyze_url(
        self,
        url: str,
    ) -> Dict[str, Any]:
        """
        Analyze a URL using:
        ML + deterministic URL rules + risk synthesis.
        """
        if not isinstance(url, str):
            raise TypeError(
                "URL must be a string."
            )

        if not url.strip():
            raise ValueError(
                "URL cannot be empty."
            )

        ml_result = self.url_analyzer.analyze(
            url
        )

        indicators = (
            self.rule_engine.analyze_url_features(
                ml_result["raw_features"]
            )
        )

        return self._build_result(
            input_type="url",
            prediction=ml_result["prediction"],
            scam_probability=float(
                ml_result["scam_probability"]
            ),
            legitimate_probability=float(
                ml_result["legitimate_probability"]
            ),
            indicators=indicators,
            model_category=None,
            model_drivers=(
                ml_result["positive_drivers"]
                if ml_result["prediction"] == "scam"
                else ml_result["negative_drivers"]
            ),
            original_input=ml_result["url"],
        )

    def analyze_combined(
        self,
        message: str,
        url: str,
    ) -> Dict[str, Any]:
        """
        Analyze a message and URL together.

        This is useful when a message contains a suspicious link.
        """
        if not isinstance(message, str):
            raise TypeError(
                "Message must be a string."
            )

        if not isinstance(url, str):
            raise TypeError(
                "URL must be a string."
            )

        if not message.strip():
            raise ValueError(
                "Message cannot be empty."
            )

        if not url.strip():
            raise ValueError(
                "URL cannot be empty."
            )

        message_result = self.text_analyzer.analyze(
            message
        )

        url_result = self.url_analyzer.analyze(
            url
        )

        message_indicators = (
            self.rule_engine.analyze_message(
                message
            )
        )

        url_indicators = (
            self.rule_engine.analyze_url_features(
                url_result["raw_features"]
            )
        )

        all_indicators = (
            message_indicators
            + url_indicators
        )

        combined_probability = max(
            float(message_result["scam_probability"]),
            float(url_result["scam_probability"]),
        )

        legitimate_probability = 1.0 - combined_probability

        if (
            message_result["prediction"] == "scam"
            or url_result["prediction"] == "scam"
        ):
            prediction = "scam"

            drivers = (
                message_result["positive_drivers"]
                + url_result["positive_drivers"]
            )
        else:
            prediction = "legitimate"

            drivers = (
                message_result["negative_drivers"]
                + url_result["negative_drivers"]
            )

        category = CategoryMatcher.match(
            indicators=all_indicators,
            model_category=message_result.get(
                "category"
            ),
            scam_probability=combined_probability,
        )

        risk = RiskEngine.calculate(
            scam_probability=combined_probability,
            indicators=all_indicators,
        )

        rule_explanations = (
            ExplainabilityEngine.build_rule_explanations(
                all_indicators
            )
        )

        ml_explanations = (
            ExplainabilityEngine.build_ml_explanations(
                drivers,
                prediction_type=(
                    "scam"
                    if prediction == "scam"
                    else "legitimate"
                ),
            )
        )

        recommendations = (
            RecommendationEngine.generate(
                all_indicators
            )
        )

        return {
            "input_type": "combined",
            "prediction": prediction,
            "message": message,
            "url": url,
            "model_estimated_probabilities": {
                "scam": round(
                    combined_probability,
                    6,
                ),
                "legitimate": round(
                    legitimate_probability,
                    6,
                ),
            },
            "individual_model_probabilities": {
                "message_scam": round(
                    float(
                        message_result[
                            "scam_probability"
                        ]
                    ),
                    6,
                ),
                "url_scam": round(
                    float(
                        url_result[
                            "scam_probability"
                        ]
                    ),
                    6,
                ),
            },
            "risk": risk,
            "category": category,
            "indicators": all_indicators,
            "explanations": (
                rule_explanations
                + ml_explanations
            ),
            "recommendations": recommendations,
        }
