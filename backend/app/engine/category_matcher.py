from typing import Any, Dict, List, Optional


class CategoryMatcher:
    """
    Determines ScamShield's threat category.

    Strong deterministic evidence takes priority over the
    experimental category model.

    Weak model-only classifications are intentionally rejected.
    """

    CATEGORY_NAMES = {
        "Fake Internship",
        "Fake Recruitment",
        "Scholarship Scam",
        "Phishing",
        "Payment / UPI Fraud",
        "Impersonation",
        "Fake Institutional Notice",
        "KYC / Account Scam",
    }

    @classmethod
    def match(
        cls,
        indicators: List[Dict[str, Any]],
        model_category: Optional[Dict[str, Any]] = None,
        scam_probability: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Match a threat category from verified evidence.
        """
        indicators = indicators or []

        signals = {
            item.get("signal")
            for item in indicators
            if item.get("signal")
        }

        # -----------------------------------------------------
        # 1. Fake Internship
        # -----------------------------------------------------
        # Internship-related language alone does NOT indicate
        # a scam. Require a stronger suspicious signal too.
        if (
            "internship_recruitment" in signals
            and (
                "upfront_payment" in signals
                or "credential_request" in signals
                or "suspicious_channel" in signals
                or "guaranteed_earnings" in signals
            )
        ):
            return {
                "category": "Fake Internship",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 2. Fake Recruitment
        # -----------------------------------------------------
        if (
            "internship_recruitment" in signals
            and (
                "upfront_payment" in signals
                or "suspicious_channel" in signals
                or "guaranteed_earnings" in signals
            )
        ):
            return {
                "category": "Fake Recruitment",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 3. Scholarship Scam
        # -----------------------------------------------------
        if (
            "scholarship" in signals
            and (
                "upfront_payment" in signals
                or "guaranteed_earnings" in signals
                or "sensitive_information" in signals
            )
        ):
            return {
                "category": "Scholarship Scam",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 4. Payment / UPI Fraud
        # -----------------------------------------------------
        if (
            "payment_pin_manipulation" in signals
            or (
                "upfront_payment" in signals
                and "internship_recruitment" not in signals
                and "scholarship" not in signals
            )
        ):
            return {
                "category": "Payment / UPI Fraud",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 5. KYC / Account Scam
        # -----------------------------------------------------
        if "kyc_account_threat" in signals:
            return {
                "category": "KYC / Account Scam",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 6. Fake Institutional Notice
        # -----------------------------------------------------
        if "fake_institutional_notice" in signals:
            return {
                "category": "Fake Institutional Notice",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 7. Phishing
        # -----------------------------------------------------
        if (
            "brand_spoofing" in signals
            or "credential_request" in signals
        ):
            if (
                scam_probability is None
                or scam_probability >= 0.50
            ):
                return {
                    "category": "Phishing",
                    "source": "rule",
                    "confidence": None,
                }

        # -----------------------------------------------------
        # 8. Impersonation
        # -----------------------------------------------------
        if "impersonation" in signals:
            return {
                "category": "Impersonation",
                "source": "rule",
                "confidence": None,
            }

        # -----------------------------------------------------
        # 9. Model fallback
        # -----------------------------------------------------
        # Never allow the experimental category model to
        # classify a clearly legitimate message.
        if model_category is not None:
            if scam_probability is not None:
                if scam_probability < 0.50:
                    return None

            category = model_category.get("category")
            confidence = model_category.get("confidence")

            if category not in cls.CATEGORY_NAMES:
                return None

            if confidence is None:
                return None

            confidence = float(confidence)

            # The Phase 2 category model has limited data.
            if confidence < 0.50:
                return None

            return {
                "category": category,
                "source": "model",
                "confidence": round(
                    confidence,
                    6,
                ),
            }

        return None
