# FINAL_PHASE2_REVIEW.md
**ScamShield — Phase 2: Data & ML Pipeline**
**Team: OBSIDIAN | INNOV12 Competition**
**Primary Track: Cyber & Digital Trust | Supporting: AI & GenAI**
**Status: CORRECTIONS APPLIED — AWAITING PHASE 3 APPROVAL**

---

## 1. Data Sources (Clearly Distinguished)

| ID | Dataset | Type | Samples | Notes |
|----|---------|------|---------|-------|
| A | **UCI SMS Spam Collection** | Public labeled benchmark | 5,574 raw | General English SMS spam/ham from circa 2011. NOT modern student-specific scams. Source: [UCI ML Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection). |
| B | **Student Threat Corpus** | Curated domain-specific | 68 | Student-specific scam/legitimate scenarios across 8 threat categories. Curated by Team OBSIDIAN for this project. |
| C | **URL Risk Corpus** | Curated URL-specific | 50 | 25 legitimate + 25 scam URLs. Used exclusively for the URL risk classifier; completely separate pipeline. |
| D | **Demonstration Scenarios** | Strictly isolated | 5 | Synthetic demo examples (DEMO-001 to DEMO-005). NEVER used for training, validation, or testing. |

> [!IMPORTANT]
> The UCI SMS Spam Collection is a **general-purpose English SMS benchmark** and should not be presented as student-scam data. The Student Threat Corpus (B) provides all domain-specific student fraud coverage.

---

## 2. Dataset Pipeline Summary

| Metric | Value |
|--------|-------|
| Total raw messages (A + B) | 5,642 |
| Duplicates removed (normalized) | 463 |
| Missing / empty after normalization | 2 |
| **Unique clean message samples** | **5,177** |
| Legitimate samples | 4,843 (85.8%) |
| Scam samples | 799 (14.2%) |
| Train set (60%) | 3,105 |
| Validation set (20%) | 1,036 |
| Held-out test set (20%) | 1,036 |
| Isolated demo scenarios | 5 (quarantined) |
| URL corpus size | 50 |
| URL test set size | 13 |

**Partitioning:** Stratified split, `random_state=42`. Class imbalance handled with `class_weight='balanced'` in the Logistic Regression primary classifier.

### Leakage Verification Results

| Check | Result |
|-------|--------|
| Train–Test exact overlap | **0** |
| Train–Demo exact overlap | **0** |
| Test–Demo exact overlap | **0** |
| Demo isolation passed | **YES** |

---

## 3. Actual Measured Metrics (Held-Out Test Set, Seed 42)

### 3a. Text Message Classifier (TF-IDF + Logistic Regression)

| Metric | Value |
|--------|-------|
| Held-out test samples | 1,036 |
| Accuracy | **0.9846** |
| Precision (Scam) | **0.9328** |
| Recall (Scam) | **0.9470** |
| F1-Score (Scam) | **0.9398** |
| F1-Score (Weighted) | **0.9846** |
| ROC-AUC | **0.9961** |

**Confusion Matrix:**

|  | Predicted Legit | Predicted Scam |
|--|----------------|----------------|
| **Actual Legit** | 895 (TN) | 9 (FP) |
| **Actual Scam** | 7 (FN) | 125 (TP) |

> [!NOTE]
> The 7 false negatives demonstrate empirically that a deterministic rule engine (Phase 5) is required as a safety floor. The linear model works well for typical patterns but can be evaded by linguistic obfuscation.

### 3b. URL Risk Classifier (StandardScaler + Logistic Regression, 17 features)

| Metric | Value |
|--------|-------|
| Held-out test samples | **13** |
| Accuracy | 1.0000 |
| Precision (Scam) | 1.0000 |
| Recall (Scam) | 1.0000 |
| F1-Score (Scam) | 1.0000 |

> [!WARNING]
> **The initial URL evaluation achieved 100% accuracy on a held-out set of 13 URLs. Due to the small evaluation set, this result has limited generalizability.** It reflects separability of the 17 lexical features on this particular small sample; it is not a reliable indicator of real-world performance. No additional public URL data was incorporated at this stage. This limitation is explicitly documented in `evaluation_summary.txt` and `metadata.json`.

---

## 4. Probability Terminology Correction

**Correction applied throughout all source files:**

All instances of "calibrated probability" have been replaced with **"model-estimated probability"**.

**Reason:** `LogisticRegression.predict_proba()` in scikit-learn returns the raw logistic sigmoid output. True probability calibration requires a procedure such as `CalibratedClassifierCV` with isotonic regression or Platt scaling. **No such calibration was applied to any model in this pipeline.**

**Files corrected:**
- `backend/app/ml/text_classifier.py` — class docstring and `predict_proba` docstring
- `backend/app/ml/url_classifier.py` — `predict_proba` docstring
- `backend/datasets/train_models.py` — metadata field `probability_terminology` added; no "calibrated" in console output
- `backend/app/ml/artifacts/metadata.json` — field `probability_terminology` set to `"model-estimated (logistic regression sigmoid output; no calibration procedure such as CalibratedClassifierCV was applied)"`
- `backend/app/ml/artifacts/evaluation_summary.txt` — Section 5 KNOWN LIMITATIONS explicitly states this

---

## 5. Category Classifier Limitation

> [!WARNING]
> **The category classifier is an experimental/supporting component only.** It must NOT be presented as highly reliable.

**Details:**
- Trained on 8 student threat categories with approximately 6–8 samples each.
- Multi-class Logistic Regression on the same TF-IDF feature space.
- Expected confidence values: ~0.30–0.45 (low, due to tiny sample sizes per class).
- **The Phase 5 rule engine must have authority to override or validate category predictions when explicit rule-based evidence is detected.**
- No additional labelled samples were fabricated to inflate category performance.

**Metadata field added to `metadata.json`:**
```
"category_model_limitation": "Experimental supporting component only. Each of the 8 student threat categories has approximately 6-8 training samples. Confidence values are expected to be low (~0.30-0.45). Category predictions must be validated or overridden by the rule engine (Phase 5) when explicit rule-based evidence is detected. Do NOT present category predictions as highly reliable."
```

---

## 6. Reproducibility Verification

Training was re-run from scratch after removing all `*.joblib`, `*.json`, and `*.txt` artifacts:

```
rm -f backend/app/ml/artifacts/*.joblib backend/app/ml/artifacts/*.json backend/app/ml/artifacts/*.txt
PYTHONPATH=backend backend/venv/bin/python backend/datasets/train_models.py
```

**Result:** All counts, splits, leakage verification results, and evaluation metrics reproduced exactly. Seed `42` is fixed in both `random.seed()` and `np.random.seed()`.

---

## 7. Test Suite Results

```
PYTHONPATH=backend backend/venv/bin/pytest backend/app/tests/ -v
```

```
11 passed, 1 warning in 6.15s
```

| Test | Result |
|------|--------|
| test_root_endpoint | PASSED |
| test_health_endpoint | PASSED |
| test_dataset_files_exist | PASSED |
| test_metadata_isolation | PASSED |
| test_text_preprocessing | PASSED |
| test_models_loaded | PASSED |
| test_predict_proba_range | PASSED |
| test_feature_attribution | PASSED |
| test_url_feature_extraction | PASSED |
| test_url_model_prediction | PASSED |
| test_fresh_process_loading | PASSED |

---

## 8. Fresh-Process Artifact Loading

Verified in an isolated Python process:

```python
from app.ml.text_classifier import TextMessageAnalyzer
from app.ml.url_classifier import URLRiskClassifier
t = TextMessageAnalyzer()
u = URLRiskClassifier()
assert t.is_loaded and u.is_loaded
```

**Output:** `ARTIFACTS_OK` — all five artifacts load cleanly.

---

## 9. Generated Artifacts

| Artifact | Purpose |
|----------|---------|
| `text_vectorizer.joblib` | TF-IDF vectorizer (1–3 n-grams, 6,000 features) |
| `text_model.joblib` | Primary scam/legitimate Logistic Regression classifier |
| `category_model.joblib` | Experimental 8-class student threat category classifier |
| `url_scaler.joblib` | StandardScaler for 17 URL lexical features |
| `url_model.joblib` | URL risk Logistic Regression classifier |
| `metadata.json` | Training metadata including all limitation fields |
| `evaluation_report.json` | Full machine-readable evaluation metrics |
| `evaluation_summary.txt` | Human-readable report with limitations, dataset sources |

---

## 10. Known Limitations Summary

| Limitation | Status |
|-----------|--------|
| Probability outputs are model-estimated, not calibrated | Documented in all files |
| Category classifier has ~6–8 samples per class | Documented; marked experimental |
| URL evaluation on only 13 test samples | Documented with explicit caveat |
| 7 false negatives in text classifier | Documented; Phase 5 rule engine required as safety floor |
| UCI dataset is general SMS spam, not student-specific | Documented; clearly distinguished from Student Corpus |

---

*Generated: 2026-10-01 | Team: OBSIDIAN | Phase 2 corrections complete.*
