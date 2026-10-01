from typing import Dict, List


class RecommendationEngine:
    """
    Generates defensive safety recommendations based on
    verified security indicators.
    """

    RECOMMENDATIONS: Dict[str, List[str]] = {
        "upfront_payment": [
            "Do not make the requested payment.",
            (
                "Verify the opportunity or organisation through "
                "an official and independently verified channel."
            ),
        ],
        "credential_request": [
            "Do not share your password, OTP, PIN, or CVV.",
            (
                "Use the organisation's official website or "
                "verified support channel."
            ),
        ],
        "payment_pin_manipulation": [
            (
                "Do not enter a UPI PIN to receive money or "
                "a refund."
            ),
            (
                "Do not approve an unexpected payment or "
                "collect request."
            ),
        ],
        "sensitive_information": [
            (
                "Do not share sensitive personal or financial "
                "information."
            ),
            (
                "Verify the request through an independently "
                "verified source."
            ),
        ],
        "brand_spoofing": [
            (
                "Do not trust a URL solely because it contains "
                "a familiar brand name."
            ),
            (
                "Navigate to the organisation's official website "
                "manually."
            ),
        ],
        "suspicious_tld": [
            (
                "Treat the domain with caution and verify the "
                "official website independently."
            ),
        ],
        "non_https": [
            (
                "Avoid entering sensitive information on a "
                "non-HTTPS URL."
            ),
            (
                "Verify whether an official HTTPS version exists."
            ),
        ],
        "url_credentials": [
            (
                "Do not enter passwords, OTPs, PINs, or other "
                "credentials through this URL."
            ),
        ],
        "url_obfuscation": [
            (
                "Avoid interacting with the URL until its "
                "destination is independently verified."
            ),
        ],
        "urgency": [
            (
                "Do not make a rushed decision solely because "
                "the message creates urgency."
            ),
            (
                "Verify the request before clicking, paying, "
                "or sharing information."
            ),
        ],
        "suspicious_channel": [
            (
                "Verify the sender before moving the conversation "
                "to an external messaging platform."
            ),
        ],
        "guaranteed_earnings": [
            (
                "Be cautious of guaranteed or unusually easy "
                "financial returns."
            ),
            (
                "Verify the opportunity independently before "
                "providing money or information."
            ),
        ],
        "internship_recruitment": [
            (
                "Verify the opportunity through the organisation's "
                "official recruitment channel."
            ),
        ],
        "scholarship": [
            (
                "Verify the scholarship through the institution's "
                "official website or portal."
            ),
        ],
        "kyc_account_threat": [
            (
                "Do not share OTPs, PINs, or passwords in "
                "response to the message."
            ),
            (
                "Contact the institution using an independently "
                "verified official channel."
            ),
        ],
        "impersonation": [
            (
                "Do not rely on the claimed identity of the sender."
            ),
            (
                "Verify the communication through an official "
                "contact method."
            ),
        ],
        "fake_institutional_notice": [
            (
                "Verify the notice using the institution's "
                "official website or student portal."
            ),
        ],
    }

    @classmethod
    def generate(
        cls,
        indicators: List[Dict],
    ) -> List[str]:
        """
        Generate unique defensive recommendations.
        """
        recommendations: List[str] = []

        for indicator in indicators or []:
            signal = indicator.get("signal")

            for recommendation in cls.RECOMMENDATIONS.get(
                signal,
                [],
            ):
                if recommendation not in recommendations:
                    recommendations.append(
                        recommendation
                    )

        if not recommendations:
            recommendations.append(
                (
                    "Verify important or unexpected messages "
                    "through an independent official source."
                )
            )

        return recommendations
