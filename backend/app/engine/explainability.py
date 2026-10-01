from typing import Any, Dict, List


class ExplainabilityEngine:
    """
    Builds explanations only from actual evidence.

    Allowed sources:
    - deterministic rule matches
    - actual ML feature contributions
    """

    @staticmethod
    def build_rule_explanations(
        indicators: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Convert rule evidence into user-readable structured
        explanations.
        """
        explanations = []

        for indicator in indicators or []:
            item = {
                "type": "rule",
                "signal": indicator.get("signal"),
                "severity": indicator.get(
                    "severity"
                ),
                "description": indicator.get(
                    "description"
                ),
                "source": "rule",
            }

            if "matched_text" in indicator:
                item["evidence"] = indicator.get(
                    "matched_text"
                )
                item["start"] = indicator.get(
                    "start"
                )
                item["end"] = indicator.get(
                    "end"
                )

            if "feature" in indicator:
                item["feature"] = indicator.get(
                    "feature"
                )
                item["value"] = indicator.get(
                    "value"
                )

            explanations.append(item)

        return explanations

    @staticmethod
    def build_ml_explanations(
        drivers: List[Dict[str, Any]],
        prediction_type: str = "scam",
    ) -> List[Dict[str, Any]]:
        """
        Convert actual model feature contributions into
        structured explanations.

        prediction_type:
            scam
            legitimate
        """
        explanations = []

        if prediction_type == "scam":
            title = "Model Risk Driver"
        else:
            title = "Legitimacy Driver"

        for driver in drivers or []:
            feature = driver.get(
                "token",
                driver.get("feature"),
            )

            explanations.append(
                {
                    "type": "ml",
                    "title": title,
                    "feature": feature,
                    "contribution": driver.get(
                        "contribution"
                    ),
                    "source": "ml",
                }
            )

        return explanations
