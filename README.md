# ScamShield

**Explainable AI-Powered Digital Safety Platform for Students & Young Digital Users**  
*DETECT → EXPLAIN → PROTECT*

---

## Competition & Team Credentials
- **Competition:** INNOV12 Undergraduate Innovation & Product Challenge
- **Primary Track:** Cyber & Digital Trust
- **Supporting Track:** AI & GenAI
- **Team Name:** OBSIDIAN
- **Team Members:**
  - **Soham Mitra** — CSE, 3rd Year
  - **Khyati K Doshi** — CSE (IOTCSBT), 3rd Year
  - **Srinistha Biswas** — CSE (IOTCSBT), 3rd Year

---

## 1. Project Purpose

ScamShield is an explainable AI safety platform designed to protect students, young developers, and campus communities against modern cyber fraud. Rather than producing opaque binary labels ("SCAM" / "NOT SCAM"), ScamShield deconstructs the threat into:
1. **DETECT:** A calibrated risk score ($0–100$) and risk tier (`SAFE`, `LOW RISK`, `SUSPICIOUS`, `HIGH RISK`).
2. **EXPLAIN:** Grounded threat indicators citing verbatim matched text snippets from the input, alongside mathematical feature attribution ($w_i \cdot x_i$) from our calibrated linear models.
3. **PROTECT:** Practical, threat-specific defensive instructions.

### Target Threat Scenarios
1. **Fake Internship Offers** (stipend without interview, upfront laptop/security deposit)
2. **Task & Part-Time Scams** (Telegram/WhatsApp tasks, YouTube video liking scams)
3. **Scholarship & Grant Frauds** (fake sanction notices, processing fee collection)
4. **Credential Phishing & Typosquatting** (lookalike college portals, brand-jacking)
5. **UPI PIN & Payment Fraud** (fake buyer QR codes, collect requests)
6. **Digital Impersonation** (CBI/Police "Digital Arrest", Courier/FedEx parcel alerts)
7. **Institutional Notice Clones** (emergency exam circulars, fake fee portals)
8. **KYC & Account Suspension** (SIM block, electricity cut threats)

---

## 2. Architecture Overview

```
                      User Input (Text / URL / Screenshot)
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
   ┌─────────────────────────────┐           ┌─────────────────────────────┐
   │    Logistic Regression      │           │     Rule & Signal Engine    │
   │      (ML Classifier)        │           │   (Deterministic Matcher)   │
   └──────────────┬──────────────┘           └──────────────┬──────────────┘
                  │                                         │
        • P(Scam | X)                              • Matched Rule IDs
        • Token weights: w_i * x_i                 • Verbatim quotes: [start, end]
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │          EVIDENCE SYNTHESIS           │
                   ├───────────────────────────────────────┤
                   │ 1. Risk Tier & Score (0-100)          │
                   │ 2. Grounded Indicators (Rule quotes)  │
                   │ 3. ML Top Attributed Tokens           │
                   │ 4. Category Classification            │
                   └───────────────────┬───────────────────┘
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │           PROTECT ADVISORY            │
                   │ Actionable safety steps tailored      │
                   │ strictly to category & verified rules │
                   └───────────────────────────────────────┘
```

- **Backend:** FastAPI (Python 3.12), Pydantic v2, SQLAlchemy 2.0.
- **Explainable ML:** TF-IDF + Logistic Regression (sublinear scaling, token feature attribution).
- **URL Engine:** 24 lexical features + Logistic Regression + Configurable brand spoofing validator (`trusted_brands.json`).
- **Database:** PostgreSQL 18.6 primary with automatic SQLite fallback (`scamshield.db`).
- **Frontend:** React + Vite + Tailwind CSS + Lucide React (Cybersecurity UI).

---

## 3. Prerequisites

- **Python:** 3.12+
- **Node.js:** v20+ (tested on Node v24)
- **Package Managers:** `pip` and `npm`
- **PostgreSQL (Optional for dev):** System automatically falls back to local SQLite if PostgreSQL is not active.
- **Tesseract OCR (Optional for screenshots):** `brew install tesseract` (macOS).

---

## 4. Setup & Installation

### Backend Setup
```bash
# 1. Create and activate virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Configure environment
cp backend/.env.example backend/.env
```

### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install
```

---

## 5. Running the Application

### Option A: One-Command Startup (Recommended)
From the root directory:
```bash
./run_dev.sh
```

### Option B: Manual Execution
**Terminal 1 — Backend:**
```bash
source backend/venv/bin/activate
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

- **Frontend Application:** `http://localhost:5173`
- **API Documentation (Swagger):** `http://127.0.0.1:8000/api/v1/docs`
- **Health Check Endpoint:** `http://127.0.0.1:8000/api/v1/health`

---

## 6. Current Development Status

- **Phase 1 (Project Foundation):** **COMPLETED & VERIFIED**
  - Monorepo structure initialized.
  - FastAPI application with lifespan management and CORS active.
  - Genuine `/api/v1/health` endpoint returning team & database status.
  - Dual-engine database architecture (PostgreSQL with SQLite fallback) ready.
  - Configurable `trusted_brands.json` implemented.
  - React + Vite + Tailwind CSS cybersecurity shell with navigation, branding, and status indicators active.
- **Phase 2 (Data and ML Pipeline):** Up next (dataset ingestion, TF-IDF + Logistic Regression training).
