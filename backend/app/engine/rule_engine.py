import re
from typing import Any, Dict, List


class RuleEngine:
    """
    Deterministic security rule engine for ScamShield.

    Rules identify concrete security signals from the actual
    input. They do not replace the ML model and do not invent
    predictions.

    Every message rule returns the exact matched text and its
    character positions.
    """

    MESSAGE_RULES = [
        {
            "signal": "upfront_payment",
            "patterns": [
                r"\bregistration fee\b",
                r"\bprocessing fee\b",
                r"\bsecurity deposit\b",
                r"\brefundable deposit\b",
                r"\bpay\b.{0,50}\bfee\b",
                r"\bpay\b.{0,50}\bdeposit\b",
                r"\bdeposit\b.{0,50}\bto confirm\b",
                r"\bpay\b.{0,50}\bto confirm\b",
            ],
            "severity": "high",
            "description": (
                "An upfront payment or deposit is being requested."
            ),
        },
        {
            "signal": "urgency",
            "patterns": [
                r"\bimmediately\b",
                r"\burgent\b",
                r"\bact now\b",
                r"\btoday only\b",
                r"\bfinal warning\b",
                r"\bexpires today\b",
                r"\bwithin \d+ hours?\b",
                r"\blast chance\b",
                r"\bdo it now\b",
            ],
            "severity": "medium",
            "description": (
                "The message uses pressure or urgency to "
                "encourage immediate action."
            ),
        },
        {
            "signal": "credential_request",
            "patterns": [
                r"\bpassword\b",
                r"\botp\b",
                r"\bone[- ]time password\b",
                r"\bupi pin\b",
                r"\bpin\b",
                r"\bcvv\b",
            ],
            "severity": "high",
            "description": (
                "The message requests sensitive authentication "
                "information."
            ),
        },
        {
            "signal": "sensitive_information",
            "patterns": [
                r"\bbank details\b",
                r"\bbank account\b",
                r"\baccount number\b",
                r"\baadhaar\b",
                r"\bpan\b",
                r"\bcard number\b",
                r"\bdate of birth\b",
            ],
            "severity": "high",
            "description": (
                "The message requests sensitive personal or "
                "financial information."
            ),
        },
        {
            "signal": "suspicious_channel",
            "patterns": [
                r"\bcontact\b.{0,40}\btelegram\b",
                r"\bmessage\b.{0,40}\btelegram\b",
                r"\bmove\b.{0,40}\btelegram\b",
                r"\bcontact\b.{0,40}\bwhatsapp\b",
                r"\bmessage\b.{0,40}\bwhatsapp\b",
                r"\bmove\b.{0,40}\bwhatsapp\b",
            ],
            "severity": "medium",
            "description": (
                "The message redirects the user to an external "
                "communication channel."
            ),
        },
        {
            "signal": "guaranteed_earnings",
            "patterns": [
                r"\bguaranteed income\b",
                r"\bguaranteed earnings\b",
                r"\beasy money\b",
                r"\binstant reward\b",
                r"\bguaranteed prize\b",
                r"\bguaranteed stipend\b",
                r"\bear[n]? \b\d+%?\b",
                r"\bearn\b.{0,30}\bper day\b",
            ],
            "severity": "medium",
            "description": (
                "The message promises unusually easy or "
                "guaranteed financial benefit."
            ),
        },
        {
            "signal": "internship_recruitment",
            "patterns": [
                r"\binternship\b",
                r"\bintern\b",
                r"\bjob offer\b",
                r"\brecruitment\b",
                r"\brecruiting\b",
                r"\bselected\b.{0,50}\bposition\b",
                r"\bselected\b.{0,50}\bjob\b",
            ],
            "severity": "low",
            "description": (
                "The message contains internship or "
                "recruitment-related language."
            ),
        },
        {
            "signal": "scholarship",
            "patterns": [
                r"\bscholarship\b",
                r"\bstudent grant\b",
                r"\beducation grant\b",
                r"\bfinancial aid\b",
            ],
            "severity": "low",
            "description": (
                "The message contains scholarship or student-grant "
                "language."
            ),
        },
        {
            "signal": "kyc_account_threat",
            "patterns": [
                r"\baccount will be blocked\b",
                r"\baccount will be suspended\b",
                r"\baccount suspension\b",
                r"\bkyc\b.{0,40}\bexpired\b",
                r"\bkyc\b.{0,40}\bupdate\b",
                r"\bverify your account\b",
                r"\bsim\b.{0,30}\bblocked\b",
                r"\baccount\b.{0,30}\bblocked\b",
            ],
            "severity": "high",
            "description": (
                "The message uses an account, KYC, SIM, or service "
                "suspension threat."
            ),
        },
        {
            "signal": "payment_pin_manipulation",
            "patterns": [
                r"\bupi pin\b",
                r"\benter\b.{0,40}\bpin\b.{0,40}\brefund\b",
                r"\benter\b.{0,40}\bpin\b.{0,40}\breceive\b",
                r"\bscan\b.{0,40}\bqr\b.{0,40}\breceive\b",
                r"\bscan\b.{0,40}\bqr\b.{0,40}\brefund\b",
                r"\bcollect request\b",
                r"\bapprove\b.{0,40}\bpayment\b",
            ],
            "severity": "high",
            "description": (
                "The message contains a potentially dangerous "
                "payment instruction."
            ),
        },
        {
            "signal": "impersonation",
            "patterns": [
                r"\bthis is\b.{0,30}\bbank\b",
                r"\bthis is\b.{0,30}\bpolice\b",
                r"\bthis is\b.{0,30}\bgovernment\b",
                r"\bcollege administration\b",
                r"\buniversity administration\b",
                r"\bofficial notice\b",
                r"\bauthority\b.{0,30}\bverify\b",
            ],
            "severity": "medium",
            "description": (
                "The message contains language suggesting possible "
                "impersonation of an authority or institution."
            ),
        },
        {
            "signal": "fake_institutional_notice",
            "patterns": [
                r"\bexam\b.{0,60}\bcancelled\b",
                r"\bfee payment\b.{0,60}\bimmediately\b",
                r"\bcollege notice\b",
                r"\buniversity notice\b",
                r"\bsubmit\b.{0,50}\bpersonal details\b",
                r"\bmandatory\b.{0,50}\bverification\b",
            ],
            "severity": "medium",
            "description": (
                "The message resembles an urgent institutional "
                "notice that may require independent verification."
            ),
        },
    ]

    URL_RULES = [
        {
            "signal": "ip_based_url",
            "feature": "is_ip",
            "condition": lambda value: value == 1.0,
            "severity": "high",
            "description": (
                "The URL uses an IP address instead of a normal domain."
            ),
        },
        {
            "signal": "non_https",
            "feature": "is_https",
            "condition": lambda value: value == 0.0,
            "severity": "medium",
            "description": (
                "The URL does not use HTTPS."
            ),
        },
        {
            "signal": "suspicious_tld",
            "feature": "has_suspicious_tld",
            "condition": lambda value: value == 1.0,
            "severity": "medium",
            "description": (
                "The URL uses a TLD marked as suspicious by "
                "ScamShield's configured heuristics."
            ),
        },
        {
            "signal": "sensitive_url_tokens",
            "feature": "sensitive_token_count",
            "condition": lambda value: value >= 1.0,
            "severity": "medium",
            "description": (
                "The URL contains security-sensitive tokens such as "
                "login, verify, banking, or UPI."
            ),
        },
        {
            "signal": "url_credentials",
            "feature": "has_credentials",
            "condition": lambda value: value == 1.0,
            "severity": "high",
            "description": (
                "The URL contains credential-style URL syntax."
            ),
        },
        {
            "signal": "url_obfuscation",
            "feature": "has_hex_encoding",
            "condition": lambda value: value == 1.0,
            "severity": "medium",
            "description": (
                "The URL contains percent-encoded characters "
                "that may indicate obfuscation."
            ),
        },
        {
            "signal": "brand_spoofing",
            "feature": "brand_spoofing_score",
            "condition": lambda value: value == 1.0,
            "severity": "high",
            "description": (
                "The configured brand-spoofing heuristic detected "
                "a possible impersonation pattern."
            ),
        },
    ]

    def analyze_message(
        self,
        text: str,
    ) -> List[Dict[str, Any]]:
        """
        Analyze message text and return grounded rule evidence.
        """
        if not isinstance(text, str):
            raise TypeError("Message must be a string.")

        if not text.strip():
            raise ValueError("Message cannot be empty.")

        evidence: List[Dict[str, Any]] = []

        for rule in self.MESSAGE_RULES:
            for pattern in rule["patterns"]:
                matches = re.finditer(
                    pattern,
                    text,
                    flags=re.IGNORECASE,
                )

                for match in matches:
                    evidence.append(
                        {
                            "signal": rule["signal"],
                            "severity": rule["severity"],
                            "description": rule["description"],
                            "matched_text": match.group(0),
                            "start": match.start(),
                            "end": match.end(),
                            "source": "rule",
                        }
                    )

        return self._deduplicate_evidence(evidence)

    def analyze_url_features(
        self,
        features: Dict[str, float],
    ) -> List[Dict[str, Any]]:
        """
        Analyze extracted URL features and return grounded evidence.
        """
        if not isinstance(features, dict):
            raise TypeError(
                "URL features must be a dictionary."
            )

        evidence: List[Dict[str, Any]] = []

        for rule in self.URL_RULES:
            feature = rule["feature"]

            if feature not in features:
                continue

            value = features[feature]

            if rule["condition"](value):
                evidence.append(
                    {
                        "signal": rule["signal"],
                        "severity": rule["severity"],
                        "description": rule["description"],
                        "feature": feature,
                        "value": value,
                        "source": "rule",
                    }
                )

        return self._deduplicate_evidence(evidence)

    @staticmethod
    def _deduplicate_evidence(
        evidence: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Remove exact duplicate evidence while preserving
        separate pieces of supporting evidence.
        """
        seen = set()
        result = []

        for item in evidence:
            key = (
                item.get("signal"),
                item.get("matched_text"),
                item.get("start"),
                item.get("end"),
                item.get("feature"),
                item.get("value"),
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result
