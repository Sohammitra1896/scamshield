from typing import Any, Dict, List


class RiskEngine:
    """
    Transparent application-level risk synthesis.

    ML probability and application risk score are separate values.

    Base score:
        scam_probability * 100

    Rule bonuses:
        applied once per unique signal

    Critical signals:
        enforce a minimum application risk score.
    """

    SEVERITY_BONUS = {
        "high": 12,
        "medium": 7,
        "low": 3,
    }

    MAX_RULE_BONUS = 30

    CRITICAL_SIGNALS = {
        "upfront_payment",
        "credential_request",
        "payment_pin_manipulation",
        "sensitive_information",
    }

    MIN_CRITICAL_SCORE = 80.0

    THRESHOLDS = {
        "safe_max": 25.0,
        "low_risk_max": 50.0,
        "suspicious_max": 75.0,
    }

    @classmethod
    def level_from_score(
        cls,
        score: float,
    ) -> str:
        """
        Convert a 0-100 risk score into a risk level.
        """
        score = float(score)

        if not 0.0 <= score <= 100.0:
            raise ValueError(
                "Risk score must be between 0 and 100."
            )

        if score <= cls.THRESHOLDS["safe_max"]:
            return "SAFE"

        if score <= cls.THRESHOLDS["low_risk_max"]:
            return "LOW RISK"

        if score <= cls.THRESHOLDS["suspicious_max"]:
            return "SUSPICIOUS"

        return "HIGH RISK"

    @classmethod
    def _unique_signal_severities(
        cls,
        indicators: List[Dict[str, Any]],
    ) -> Dict[str, str]:
        """
        Return one severity for each unique signal.

        Multiple evidence snippets from the same signal should
        not multiply the risk bonus.
        """
        severity_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        unique: Dict[str, str] = {}

        for indicator in indicators or []:
            signal = indicator.get("signal")

            if not signal:
                continue

            severity = str(
                indicator.get("severity", "low")
            ).lower()

            if severity not in severity_rank:
                severity = "low"

            current = unique.get(signal)

            if current is None:
                unique[signal] = severity
                continue

            if (
                severity_rank[severity]
                > severity_rank[current]
            ):
                unique[signal] = severity

        return unique

    @classmethod
    def calculate(
        cls,
        scam_probability: float,
        indicators: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate application-level risk.

        The model probability is preserved.
        The risk score is a separate transparent policy score.
        """
        if not isinstance(
            scam_probability,
            (int, float),
        ):
            raise TypeError(
                "scam_probability must be numeric."
            )

        scam_probability = float(
            scam_probability
        )

        if not 0.0 <= scam_probability <= 1.0:
            raise ValueError(
                "scam_probability must be between 0 and 1."
            )

        indicators = indicators or []

        base_score = scam_probability * 100.0

        unique_signals = (
            cls._unique_signal_severities(
                indicators
            )
        )

        rule_bonus = sum(
            cls.SEVERITY_BONUS.get(
                severity,
                0,
            )
            for severity in unique_signals.values()
        )

        rule_bonus = min(
            float(rule_bonus),
            float(cls.MAX_RULE_BONUS),
        )

        risk_score = min(
            100.0,
            base_score + rule_bonus,
        )

        critical_signals = [
            signal
            for signal in unique_signals
            if signal in cls.CRITICAL_SIGNALS
        ]

        critical_signal_triggered = bool(
            critical_signals
        )

        if critical_signal_triggered:
            risk_score = max(
                risk_score,
                cls.MIN_CRITICAL_SCORE,
            )

        risk_score = round(
            risk_score,
            2,
        )

        return {
            "model_estimated_scam_probability": round(
                scam_probability,
                6,
            ),
            "base_score": round(
                base_score,
                2,
            ),
            "rule_bonus": round(
                rule_bonus,
                2,
            ),
            "risk_score": risk_score,
            "risk_level": cls.level_from_score(
                risk_score
            ),
            "critical_signal_triggered": (
                critical_signal_triggered
            ),
            "critical_signals": critical_signals,
            "unique_signals": list(
                unique_signals.keys()
            ),
        }
