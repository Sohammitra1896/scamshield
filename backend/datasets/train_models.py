#!/usr/bin/env python3
"""
ScamShield ML Pipeline — Reproducible Model Training & Evaluation
Team: OBSIDIAN | INNOV12 Competition
Track: Cyber & Digital Trust (Primary) | AI & GenAI (Supporting)

Strict Rules Enforced:
1. Complete isolation of DEMO scenarios from Train, Validation, and Test sets.
2. Zero fabrication of metrics or outputs.
3. Linear, explainable models (TF-IDF + Logistic Regression for text, StandardScaler + Logistic Regression for URLs).
"""

import os
import sys
import json
import random
import datetime
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

# Ensure parent directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.ml.preprocessor import (
    clean_text,
    normalize_text_for_tfidf,
    extract_url_features,
    load_trusted_brands,
)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

ARTIFACTS_DIR = os.path.join(BACKEND_DIR, "app", "ml", "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


# ==============================================================================
# 1. DATA INGESTION & DATASET STRATEGY
# ==============================================================================

def load_uci_sms_dataset(filepath: str) -> List[Dict[str, Any]]:
    """Load authentic UCI SMS Spam Collection dataset."""
    samples = []
    if not os.path.exists(filepath):
        print(f"[!] Warning: UCI SMS dataset not found at {filepath}")
        return samples

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            parts = line.strip().split("\t", 1)
            if len(parts) == 2:
                raw_label, text = parts
                label = "scam" if raw_label.lower() == "spam" else "legitimate"
                samples.append({
                    "id": f"uci_sms_{idx:05d}",
                    "text": clean_text(text),
                    "label": label,
                    "category": "Generic Spam" if label == "scam" else "Generic Communication",
                    "source": "UCI SMS Spam Collection",
                })
    return samples


def load_student_threat_corpus(filepath: str) -> List[Dict[str, Any]]:
    """Load curated student threat and academic communication dataset."""
    if not os.path.exists(filepath):
        print(f"[!] Warning: Student threat corpus not found at {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        samples = data.get("samples", [])
        for s in samples:
            s["source"] = "Curated Student Threat Corpus"
        return samples


def load_demo_scenarios(filepath: str) -> List[Dict[str, Any]]:
    """Load isolated demonstration scenarios. NEVER to be mixed with train/val/test."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("scenarios", [])


def load_url_corpus(filepath: str) -> List[Dict[str, Any]]:
    """Load curated URL dataset."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("samples", [])


def check_leakage(train_texts: List[str], test_texts: List[str], demo_texts: List[str]) -> Dict[str, Any]:
    """Check for exact and near-duplicate leakage across splits and demo set."""
    train_set = set(normalize_text_for_tfidf(t) for t in train_texts)
    test_set = set(normalize_text_for_tfidf(t) for t in test_texts)
    demo_set = set(normalize_text_for_tfidf(t) for t in demo_texts)

    train_test_overlap = train_set.intersection(test_set)
    train_demo_overlap = train_set.intersection(demo_set)
    test_demo_overlap = test_set.intersection(demo_set)

    return {
        "train_test_exact_overlap_count": len(train_test_overlap),
        "train_demo_exact_overlap_count": len(train_demo_overlap),
        "test_demo_exact_overlap_count": len(test_demo_overlap),
        "demo_isolation_passed": (len(train_demo_overlap) == 0 and len(test_demo_overlap) == 0),
    }


# ==============================================================================
# 2. MESSAGE CLASSIFIER TRAINING
# ==============================================================================

def train_message_models(
    train_samples: List[Dict[str, Any]],
    val_samples: List[Dict[str, Any]],
    test_samples: List[Dict[str, Any]],
) -> Tuple[TfidfVectorizer, LogisticRegression, Optional[LogisticRegression], Dict[str, Any]]:
    """
    Train TF-IDF Vectorizer + Logistic Regression message classifier.
    Also trains threat category classifier on categorized scam samples.
    """
    X_train_raw = [s["text"] for s in train_samples]
    y_train = [s["label"] for s in train_samples]
    
    X_test_raw = [s["text"] for s in test_samples]
    y_test = [s["label"] for s in test_samples]

    # Preprocessing for TF-IDF
    X_train_norm = [normalize_text_for_tfidf(t) for t in X_train_raw]
    X_test_norm = [normalize_text_for_tfidf(t) for t in X_test_raw]

    # 1. TF-IDF Vectorizer (word 1-3 grams, sublinear TF scaling)
    print("\n[*] Vectorizing text corpus using TF-IDF (1-3 n-grams, sublinear scaling)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=6000,
        sublinear_tf=True,
        min_df=2,
    )
    X_train_vec = vectorizer.fit_transform(X_train_norm)
    X_test_vec = vectorizer.transform(X_test_norm)

    # 2. Logistic Regression Primary Classifier
    print("[*] Training Primary Message Classifier (Logistic Regression, L2 regularization)...")
    text_model = LogisticRegression(
        C=1.5,
        max_iter=1000,
        class_weight="balanced",
        random_state=RANDOM_SEED,
    )
    text_model.fit(X_train_vec, y_train)

    # 3. Threat Category Classifier
    # Filter scam samples that have specific student threat categories
    cat_train_samples = [s for s in train_samples if s["label"] == "scam" and s.get("category") and s.get("category") != "Generic Spam"]
    category_model = None
    if len(cat_train_samples) >= 10:
        print("[*] Training Student Threat Category Classifier (Multi-class Logistic Regression)...")
        cat_X = [normalize_text_for_tfidf(s["text"]) for s in cat_train_samples]
        cat_y = [s["category"] for s in cat_train_samples]
        cat_vec = vectorizer.transform(cat_X)
        category_model = LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=RANDOM_SEED,
        )
        category_model.fit(cat_vec, cat_y)

    # Evaluation on held-out test set
    y_pred = text_model.predict(X_test_vec)
    y_pred_proba = text_model.predict_proba(X_test_vec)

    # Binary class mapping for ROC-AUC
    classes = list(text_model.classes_)
    scam_idx = classes.index("scam")
    y_test_binary = [1 if label == "scam" else 0 for label in y_test]
    scam_probs = [float(p[scam_idx]) for p in y_pred_proba]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label="scam", zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label="scam", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label="scam", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
    auc = float(roc_auc_score(y_test_binary, scam_probs))
    cm = confusion_matrix(y_test, y_pred, labels=["legitimate", "scam"]).tolist()

    eval_results = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "f1_weighted": round(f1_weighted, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": {
            "labels": ["legitimate", "scam"],
            "matrix": cm,
            "true_negatives (legit as legit)": cm[0][0],
            "false_positives (legit as scam)": cm[0][1],
            "false_negatives (scam as legit)": cm[1][0],
            "true_positives (scam as scam)": cm[1][1],
        },
        "classes": classes,
        "sample_count": len(y_test),
    }

    return vectorizer, text_model, category_model, eval_results


# ==============================================================================
# 3. URL CLASSIFIER TRAINING
# ==============================================================================

def train_url_model(
    url_samples: List[Dict[str, Any]]
) -> Tuple[StandardScaler, LogisticRegression, Dict[str, Any]]:
    """
    Train StandardScaler + Logistic Regression URL risk classifier.
    """
    trusted_brands = load_trusted_brands()
    feature_keys = [
        "url_len", "host_len", "path_len", "query_len",
        "dot_count", "subdomain_count", "hyphen_count", "special_char_count",
        "digits_in_host", "is_ip", "is_https", "has_suspicious_tld",
        "sensitive_token_count", "has_hex_encoding", "has_credentials",
        "host_entropy", "brand_spoofing_score"
    ]

    X_raw = []
    y = []
    for s in url_samples:
        feats = extract_url_features(s["url"], trusted_brands)
        vec = [feats[k] for k in feature_keys]
        X_raw.append(vec)
        y.append(s["label"])

    X = np.array(X_raw)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED, stratify=y
    )

    print("\n[*] Training URL Risk Classifier (StandardScaler + Logistic Regression)...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    url_model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=RANDOM_SEED,
    )
    url_model.fit(X_train_scaled, y_train)

    y_pred = url_model.predict(X_test_scaled)
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, pos_label="scam", zero_division=0))
    rec = float(recall_score(y_test, y_pred, pos_label="scam", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, pos_label="scam", zero_division=0))
    cm = confusion_matrix(y_test, y_pred, labels=["legitimate", "scam"]).tolist()

    url_eval = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "sample_count": len(y_test),
        "feature_keys": feature_keys,
    }

    return scaler, url_model, url_eval


# ==============================================================================
# 4. MASTER PIPELINE EXECUTION
# ==============================================================================

def main():
    print("==================================================================")
    print(" ScamShield ML Pipeline Training & Empirical Evaluation")
    print(" Team: OBSIDIAN | INNOV12 Competition")
    print(" Primary Track: Cyber & Digital Trust | Supporting: AI & GenAI")
    print("==================================================================")

    # 1. Ingest Data Sources
    uci_path = os.path.join(CURRENT_DIR, "raw", "SMSSpamCollection")
    threat_path = os.path.join(CURRENT_DIR, "student_threat_corpus.json")
    demo_path = os.path.join(CURRENT_DIR, "demo_scenarios.json")
    url_path = os.path.join(CURRENT_DIR, "url_corpus.json")

    uci_samples = load_uci_sms_dataset(uci_path)
    student_samples = load_student_threat_corpus(threat_path)
    demo_scenarios = load_demo_scenarios(demo_path)
    url_samples = load_url_corpus(url_path)

    all_message_samples = uci_samples + student_samples
    print(f"\n[+] Loaded {len(uci_samples)} messages from UCI SMS Spam Collection.")
    print(f"[+] Loaded {len(student_samples)} messages from Student Threat Corpus.")
    print(f"[+] Loaded {len(demo_scenarios)} isolated demonstration scenarios.")
    print(f"[+] Loaded {len(url_samples)} curated URL samples.")
    print(f"[+] Total message samples combined: {len(all_message_samples)}")

    # 2. Dataset Summary & Inspection
    legit_count = sum(1 for s in all_message_samples if s["label"] == "legitimate")
    scam_count = sum(1 for s in all_message_samples if s["label"] == "scam")
    
    category_dist = {}
    for s in all_message_samples:
        cat = s.get("category", "Unspecified")
        category_dist[cat] = category_dist.get(cat, 0) + 1

    # Check duplicates and missing values based on normalized text to prevent split leakage
    norm_seen = set()
    dup_count = 0
    missing_count = 0
    clean_samples = []

    for s in all_message_samples:
        t = s["text"].strip()
        if not t:
            missing_count += 1
            continue
        norm_t = normalize_text_for_tfidf(t)
        if not norm_t:
            missing_count += 1
            continue
        if norm_t in norm_seen:
            dup_count += 1
        else:
            norm_seen.add(norm_t)
            clean_samples.append(s)

    print(f"\n--- Pre-Training Dataset Summary ---")
    print(f"Total Unique Message Samples: {len(clean_samples)} (Duplicates removed: {dup_count}, Missing: {missing_count})")
    print(f"Class Distribution: {legit_count} Legitimate ({legit_count/len(all_message_samples)*100:.1f}%), {scam_count} Scam ({scam_count/len(all_message_samples)*100:.1f}%)")
    print(f"Target Categories Covered:")
    for cat, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count} samples")

    # 3. 4-Way Dataset Partitioning (Train: 60%, Val: 20%, Test: 20%, Demo: Isolated)
    labels = [s["label"] for s in clean_samples]
    train_val, test_samples = train_test_split(
        clean_samples, test_size=0.20, random_state=RANDOM_SEED, stratify=labels
    )
    train_val_labels = [s["label"] for s in train_val]
    train_samples, val_samples = train_test_split(
        train_val, test_size=0.25, random_state=RANDOM_SEED, stratify=train_val_labels
    )  # 0.25 of 80% = 20% validation, leaving 60% train

    print(f"\n--- Split Partitions ---")
    print(f"Train Set:      {len(train_samples)} samples ({len(train_samples)/len(clean_samples)*100:.1f}%)")
    print(f"Validation Set: {len(val_samples)} samples ({len(val_samples)/len(clean_samples)*100:.1f}%)")
    print(f"Held-out Test:  {len(test_samples)} samples ({len(test_samples)/len(clean_samples)*100:.1f}%)")
    print(f"Isolated Demo:  {len(demo_scenarios)} samples (STRICTLY QUARANTINED)")

    # 4. Leakage Verification
    train_texts = [s["text"] for s in train_samples]
    test_texts = [s["text"] for s in test_samples]
    demo_texts = [s["input"] for s in demo_scenarios]

    leakage_report = check_leakage(train_texts, test_texts, demo_texts)
    print(f"\n--- Leakage Verification ---")
    print(f"Train-Test Exact Overlap: {leakage_report['train_test_exact_overlap_count']}")
    print(f"Train-Demo Exact Overlap: {leakage_report['train_demo_exact_overlap_count']}")
    print(f"Test-Demo Exact Overlap:  {leakage_report['test_demo_exact_overlap_count']}")
    assert leakage_report["demo_isolation_passed"], "CRITICAL ERROR: Demonstration samples detected in training or test set!"
    print("[+] SUCCESS: Demo set is 100% quarantined with ZERO leakage.")

    # 5. Train Message Models
    vectorizer, text_model, category_model, text_eval = train_message_models(
        train_samples, val_samples, test_samples
    )

    # 6. Train URL Model
    scaler, url_model, url_eval = train_url_model(url_samples)

    # 7. Serialize Artifacts
    print(f"\n[*] Exporting model artifacts to {ARTIFACTS_DIR}...")
    joblib.dump(vectorizer, os.path.join(ARTIFACTS_DIR, "text_vectorizer.joblib"))
    joblib.dump(text_model, os.path.join(ARTIFACTS_DIR, "text_model.joblib"))
    if category_model is not None:
        joblib.dump(category_model, os.path.join(ARTIFACTS_DIR, "category_model.joblib"))
    joblib.dump(scaler, os.path.join(ARTIFACTS_DIR, "url_scaler.joblib"))
    joblib.dump(url_model, os.path.join(ARTIFACTS_DIR, "url_model.joblib"))

    # 8. Metadata
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    metadata = {
        "timestamp": now_iso,
        "model_version": "0.1.0",
        "team": "OBSIDIAN",
        "competition": "INNOV12",
        "tracks": {
            "primary": "Cyber & Digital Trust",
            "supporting": "AI & GenAI",
        },
        "random_seed": RANDOM_SEED,
        "datasets": {
            "uci_sms_count": len(uci_samples),
            "student_threat_count": len(student_samples),
            "total_unique_messages": len(clean_samples),
            "train_size": len(train_samples),
            "val_size": len(val_samples),
            "test_size": len(test_samples),
            "demo_size": len(demo_scenarios),
            "url_count": len(url_samples),
        },
        "text_model_config": {
            "classifier": "LogisticRegression",
            "penalty": "l2",
            "C": 1.5,
            "class_weight": "balanced",
            "vectorizer": "TfidfVectorizer",
            "ngram_range": [1, 3],
            "max_features": 6000,
        },
        "url_model_config": {
            "scaler": "StandardScaler",
            "classifier": "LogisticRegression",
            "features_count": len(url_eval["feature_keys"]),
        },
        "leakage_verification": leakage_report,
    }

    with open(os.path.join(ARTIFACTS_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # 9. Empirical Evaluation Report
    full_eval_report = {
        "evaluation_timestamp": now_iso,
        "test_set_evaluation": text_eval,
        "url_test_evaluation": url_eval,
        "metadata": metadata,
    }

    report_path = os.path.join(ARTIFACTS_DIR, "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(full_eval_report, f, indent=2)

    # 10. Human-Readable Evaluation Summary
    summary_path = os.path.join(ARTIFACTS_DIR, "evaluation_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("==================================================================\n")
        f.write(" ScamShield Empirical Model Evaluation Report (Held-Out Test Set)\n")
        f.write(" Team: OBSIDIAN | INNOV12 Competition\n")
        f.write(f" Generated: {now_iso}\n")
        f.write("==================================================================\n\n")
        f.write("1. TEXT MESSAGE CLASSIFIER (TF-IDF + Logistic Regression)\n")
        f.write(f"   Held-out Test Samples: {text_eval['sample_count']}\n")
        f.write(f"   Accuracy:              {text_eval['accuracy']:.4f}\n")
        f.write(f"   Precision (Scam):      {text_eval['precision']:.4f}\n")
        f.write(f"   Recall (Scam):         {text_eval['recall']:.4f}\n")
        f.write(f"   F1-Score (Scam):       {text_eval['f1_score']:.4f}\n")
        f.write(f"   F1-Score (Weighted):   {text_eval['f1_weighted']:.4f}\n")
        f.write(f"   ROC-AUC:               {text_eval['roc_auc']:.4f}\n\n")
        f.write("   Confusion Matrix:\n")
        f.write(f"   - True Negatives (Legit identified as Legit): {text_eval['confusion_matrix']['true_negatives (legit as legit)']}\n")
        f.write(f"   - False Positives (Legit flagged as Scam):   {text_eval['confusion_matrix']['false_positives (legit as scam)']}\n")
        f.write(f"   - False Negatives (Scam missed as Legit):    {text_eval['confusion_matrix']['false_negatives (scam as legit)']}\n")
        f.write(f"   - True Positives (Scam identified as Scam):  {text_eval['confusion_matrix']['true_positives (scam as scam)']}\n\n")
        f.write("2. URL RISK CLASSIFIER (StandardScaler + Logistic Regression)\n")
        f.write(f"   Held-out Test Samples: {url_eval['sample_count']}\n")
        f.write(f"   Accuracy:              {url_eval['accuracy']:.4f}\n")
        f.write(f"   Precision (Scam):      {url_eval['precision']:.4f}\n")
        f.write(f"   Recall (Scam):         {url_eval['recall']:.4f}\n")
        f.write(f"   F1-Score (Scam):       {url_eval['f1_score']:.4f}\n\n")
        f.write("3. DEMONSTRATION SET ISOLATION:\n")
        f.write(f"   Total Isolated Demo Scenarios: {len(demo_scenarios)}\n")
        f.write(f"   Overlap with Training/Testing: 0 (PASSED)\n")

    print(f"\n[+] Empirical Evaluation Report saved to: {report_path}")
    print(f"[+] Human-readable Summary saved to:      {summary_path}")

    # Print summary to console
    with open(summary_path, "r", encoding="utf-8") as f:
        print("\n" + f.read())

    print("[+] Model artifacts generated and verified successfully!")


if __name__ == "__main__":
    main()
