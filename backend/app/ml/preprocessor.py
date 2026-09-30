import re
import math
import json
import os
from urllib.parse import urlparse
from typing import Dict, Any, List


# Regex patterns for normalization
URL_REGEX = re.compile(r'https?://[^\s]+|www\.[^\s]+', re.IGNORECASE)
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b[6-9]\d{9}\b')
UPI_REGEX = re.compile(r'[a-zA-Z0-9._-]+@[a-zA-Z]{3,}', re.IGNORECASE)
CURRENCY_REGEX = re.compile(r'(?:Rs\.?|INR|₹|\$|USD)\s*\d+(?:,\d+)*(?:\.\d+)?|\b\d+\s*(?:INR|rupees|stipend)\b', re.IGNORECASE)
IP_REGEX = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

# Suspicious TLDs commonly seen in short-lived phishing campaigns
SUSPICIOUS_TLDS = {
    '.xyz', '.top', '.buzz', '.club', '.site', '.online', '.vip', 
    '.cf', '.cc', '.click', '.biz', '.live', '.info', '.work', '.rest'
}

# Sensitive tokens commonly exploited in phishing paths/queries
SENSITIVE_TOKENS = [
    'login', 'verify', 'secure', 'bank', 'account', 'update', 'kyc', 
    'upi', 'free', 'reward', 'stipend', 'bonus', 'claim', 'refund', 'password'
]


def clean_text(text: str) -> str:
    """
    Standard text normalization preserving fraud indicators.
    Normalizes whitespace and standardizes common tokens.
    """
    if not text or not isinstance(text, str):
        return ""

    t = text.strip()
    # Normalize excessive whitespace
    t = re.sub(r'\s+', ' ', t)
    return t


def normalize_text_for_tfidf(text: str) -> str:
    """
    Token-friendly normalization for TF-IDF vectorizer.
    Preserves text while softening punctuation and numbers.
    """
    if not text:
        return ""
    
    t = text.lower()
    # Replace URLs, emails, currencies with semantic tokens
    t = URL_REGEX.sub(' __url__ ', t)
    t = EMAIL_REGEX.sub(' __email__ ', t)
    t = UPI_REGEX.sub(' __upi__ ', t)
    t = CURRENCY_REGEX.sub(' __money__ ', t)
    t = PHONE_REGEX.sub(' __phone__ ', t)
    # Remove non-alphanumeric except underscore tokens
    t = re.sub(r'[^a-z0-9_ ]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob if p > 0])


def load_trusted_brands(config_path: str = None) -> List[Dict[str, Any]]:
    """Load configurable trusted brands list."""
    if config_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "trusted_brands.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("brands", [])
        except Exception:
            return []
    return []


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute standard Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def extract_url_features(url: str, trusted_brands: List[Dict[str, Any]] = None) -> Dict[str, float]:
    """
    Extract 16 explainable lexical, structural, and security features from a URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        parsed = urlparse(url)
    except Exception:
        parsed = urlparse('http://invalid.url')

    hostname = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    full_url = url.lower()

    # 1. Structural Lengths
    url_len = len(full_url)
    host_len = len(hostname)
    path_len = len(path)
    query_len = len(query)

    # 2. Character Counts & Structural Punctuation
    dot_count = hostname.count('.')
    subdomain_count = max(0, dot_count - 1)
    hyphen_count = hostname.count('-')
    at_symbol_count = full_url.count('@')
    special_char_count = sum(full_url.count(c) for c in ['?', '=', '&', '%', '_', '~', ';'])
    digits_in_host = sum(c.isdigit() for c in hostname)

    # 3. Security Signals
    is_ip = 1.0 if IP_REGEX.match(hostname) else 0.0
    is_https = 1.0 if parsed.scheme == 'https' else 0.0

    # 4. Suspicious TLD Indicator
    has_suspicious_tld = 0.0
    for tld in SUSPICIOUS_TLDS:
        if hostname.endswith(tld):
            has_suspicious_tld = 1.0
            break

    # 5. Sensitive Token Density
    sensitive_token_count = 0.0
    combined_path_query = (path + ' ' + query).lower()
    for token in SENSITIVE_TOKENS:
        if token in combined_path_query or token in hostname:
            sensitive_token_count += 1.0

    # 6. Obfuscation indicators
    has_hex_encoding = 1.0 if '%' in full_url else 0.0
    has_credentials = 1.0 if at_symbol_count > 0 else 0.0

    # 7. Entropy
    host_entropy = calculate_entropy(hostname)

    # 8. Brand Spoofing Check (Configurable)
    brand_spoofing_score = 0.0
    if trusted_brands:
        host_tokens = [tok for tok in re.split(r'[\.\-]+', hostname) if tok]
        # Check against each brand keyword
        for b in trusted_brands:
            canonical_domains = b.get("canonical_domains", [])
            # If it is exact canonical domain, not a spoof
            if any(hostname == cd or hostname.endswith('.' + cd) for cd in canonical_domains):
                continue
            
            # Check keywords against domain tokens
            for kw in b.get("keywords", []):
                for tok in host_tokens:
                    if kw in tok and tok not in canonical_domains:
                        brand_spoofing_score = 1.0
                        break
                    # Levenshtein distance check (1 or 2 edits away, e.g. internsha1a vs internshala)
                    if len(tok) >= 4 and abs(len(tok) - len(kw)) <= 2:
                        dist = levenshtein_distance(tok, kw)
                        if 1 <= dist <= 2:
                            brand_spoofing_score = 1.0
                            break
                if brand_spoofing_score > 0:
                    break

    return {
        "url_len": float(url_len),
        "host_len": float(host_len),
        "path_len": float(path_len),
        "query_len": float(query_len),
        "dot_count": float(dot_count),
        "subdomain_count": float(subdomain_count),
        "hyphen_count": float(hyphen_count),
        "special_char_count": float(special_char_count),
        "digits_in_host": float(digits_in_host),
        "is_ip": is_ip,
        "is_https": is_https,
        "has_suspicious_tld": has_suspicious_tld,
        "sensitive_token_count": sensitive_token_count,
        "has_hex_encoding": has_hex_encoding,
        "has_credentials": has_credentials,
        "host_entropy": host_entropy,
        "brand_spoofing_score": brand_spoofing_score,
    }
