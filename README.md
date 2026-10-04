# ScamShield

**Explainable AI-Powered Digital Safety Platform for Students & Young Digital Users**

**DETECT → EXPLAIN → PROTECT**

---

## Competition & Team

- **Competition:** INNOV12 Undergraduate Innovation & Product Challenge
- **Primary Track:** Cyber & Digital Trust
- **Supporting Track:** AI & GenAI
- **Team Name:** OBSIDIAN

### Team Members

| Name | Department | Year |
|---|---|---|
| Soham Mitra | CSE | 3rd Year |
| Khyati K Doshi | CSE (IOTCSBT) | 3rd Year |
| Srinistha Biswas | CSE (IOTCSBT) | 3rd Year |

**Institute:** Institute of Engineering & Management, Kolkata

---

# 1. Project Overview

ScamShield is an explainable AI-powered digital safety platform designed to help students, young developers, and digital users identify suspicious messages, URLs, and screenshots.

Instead of returning only a binary result such as **SCAM** or **LEGITIMATE**, ScamShield combines machine learning, deterministic security rules, risk assessment, explainability, and safety recommendations.

The platform follows three core principles:

### DETECT

Identify potentially suspicious or malicious digital content.

### EXPLAIN

Show the indicators and model-derived signals that contributed to the analysis.

### PROTECT

Provide practical safety recommendations based on the detected threat.

---

# 2. Problem Statement

Students and young digital users are increasingly exposed to scams involving:

- Fake internship and job offers
- Upfront registration or security fees
- Scholarship and grant fraud
- Phishing links
- Typosquatted websites
- UPI and payment fraud
- KYC and account suspension threats
- Impersonation of banks, institutions, police, and government agencies
- Fake academic or university notices
- Telegram and WhatsApp task scams

These attacks often rely on urgency, authority, impersonation, financial pressure, and requests for sensitive information.

ScamShield aims to provide a simple interface where a user can submit suspicious digital content and receive an understandable security assessment.

---

# 3. Target Threat Scenarios

ScamShield is designed around common threat scenarios such as:

1. **Fake Internship Offers**
   - Fake stipend promises
   - Upfront laptop or security deposits
   - Registration-fee scams

2. **Task and Part-Time Scams**
   - Telegram or WhatsApp recruitment
   - Fake YouTube or social-media tasks
   - Guaranteed earnings

3. **Scholarship and Grant Frauds**
   - Fake scholarship notifications
   - Processing-fee requests
   - Fake sanction messages

4. **Credential Phishing and Typosquatting**
   - Fake login pages
   - Lookalike domains
   - Credential harvesting

5. **UPI and Payment Fraud**
   - Payment manipulation
   - Fake buyer requests
   - UPI PIN-related scams

6. **Digital Impersonation**
   - Fake police or government communication
   - Courier and parcel scams
   - Institutional impersonation

7. **Fake Institutional Notices**
   - Fake exam circulars
   - Fake fee notices
   - Fake university portals

8. **KYC and Account Scams**
   - Account suspension threats
   - KYC update requests
   - SIM or banking threats

---

# 4. Core Workflow

    User Input
         │
         ├── Message
         ├── URL
         └── Screenshot
                │
                ▼
       Feature / OCR Analysis
                │
                ▼
          ML + Rule Engine
                │
                ▼
       Risk & Category Engine
                │
                ▼
           Explainability
                │
                ▼
         Recommendations
                │
                ▼
           User Decision

The product philosophy is:

**DETECT → EXPLAIN → PROTECT**

---

# 5. System Architecture

    ┌─────────────────────────────────────────────┐
    │                 Next.js UI                  │
    │                                             │
    │ Dashboard │ Analyze │ History │ Awareness   │
    │                 │ About                    │
    └──────────────────────┬──────────────────────┘
                           │
                           │ REST API
                           ▼
    ┌─────────────────────────────────────────────┐
    │                 FastAPI                     │
    ├─────────────────────────────────────────────┤
    │ Message Analysis                            │
    │ URL Analysis                                │
    │ Screenshot / OCR Analysis                   │
    │ History & Statistics                        │
    └──────────────┬──────────────────────────────┘
                   │
          ┌────────┴──────────┐
          ▼                   ▼
    ┌───────────────┐   ┌─────────────────────┐
    │ ML Classifiers│   │ Rule / Signal Engine│
    │               │   │                     │
    │ TF-IDF +      │   │ Security indicators │
    │ Logistic      │   │ and deterministic   │
    │ Regression    │   │ matching rules      │
    └───────┬───────┘   └──────────┬──────────┘
            │                      │
            └──────────┬───────────┘
                       ▼
             ┌─────────────────────┐
             │     Risk Engine     │
             │                     │
             │ Risk Score          │
             │ Risk Level          │
             │ Threat Category     │
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │ Explainability +    │
             │ Recommendations     │
             └──────────┬──────────┘
                        ▼
                  Final Result

---

# 6. Detection Pipeline

## Message Analysis

Message analysis uses:

- TF-IDF text representation
- Logistic Regression
- Text normalization
- Model feature contributions
- Rule-based security indicators

The system can identify patterns associated with:

- Payment requests
- Credential requests
- Urgency
- Impersonation
- Suspicious recruitment
- Fake institutional notices
- KYC and account threats
- Guaranteed earnings
- Internship and scholarship scams

---

## URL Analysis

URL analysis evaluates lexical and structural characteristics including:

- URL length
- Host length
- Path length
- Query length
- Dot count
- Subdomain count
- Hyphen count
- Special characters
- Digits in hostname
- IP-based hosts
- HTTPS usage
- Suspicious TLDs
- Sensitive tokens
- Hexadecimal encoding
- Credential patterns
- Host entropy
- Brand spoofing characteristics

The URL classifier combines these features with Logistic Regression.

---

## Screenshot Analysis

Screenshot analysis extracts text from uploaded images using OCR.

    Screenshot
         │
         ▼
      OCR Engine
         │
         ▼
     Extracted Text
         │
         ▼
   Message Analysis
         │
         ▼
   Risk + Explanation
         │
         ▼
    Recommendation

The system validates uploaded images before processing them and does not fabricate analysis for invalid image data.

---

# 7. Risk Assessment

ScamShield produces a risk score from **0 to 100**.

The score is mapped into risk levels such as:

- **SAFE**
- **LOW RISK**
- **SUSPICIOUS**
- **HIGH RISK**

The final assessment combines machine-learning output with deterministic security signals.

Examples of high-severity security indicators include:

- Upfront payment requests
- Credential requests
- Sensitive-information requests
- Payment or PIN manipulation

This combination helps reduce dependence on a single model signal.

---

# 8. Explainability

ScamShield is designed to provide reasoning alongside its predictions.

The analysis result can include:

- Scam probability
- Legitimate probability
- Risk score
- Risk level
- Threat category
- Positive model drivers
- Negative model drivers
- Security-rule indicators
- Matched evidence
- Safety recommendations

For message analysis, model feature attribution is derived from the relationship between TF-IDF feature values and Logistic Regression coefficients.

For URL analysis, feature contributions are derived from standardized URL features and their corresponding model coefficients.

This allows users to understand not just **what** ScamShield predicted, but also **why**.

---

# 9. Threat Categories

ScamShield can classify suspicious inputs into threat categories such as:

- Fake Internship
- Fake Recruitment
- Scholarship Scam
- Phishing
- Payment / UPI Fraud
- Impersonation
- Fake Institutional Notice
- KYC / Account Scam
- Academic Notice
- Campus Service
- Student Activity
- Placement Drive
- Administrative
- Academic Coursework
- Hostel Notice
- Campus Sports
- Banking Alert
- Internship Program
- Scholarship Information
- Health Center
- Research Assistantship

---

# 10. Recommendations

The recommendation layer converts detection results into practical safety advice.

Examples include:

- Do not transfer money
- Do not share OTPs or PINs
- Do not provide passwords or credentials
- Verify the sender independently
- Check the official domain
- Contact the institution through its official website
- Avoid clicking suspicious links
- Do not respond to urgent payment demands

Recommendations are designed to be understandable to non-technical users.

---

# 11. History & Analytics

ScamShield stores analyzed scans so users can review previous results.

The platform supports:

- Scan history
- Individual scan details
- History deletion
- Clear-all history
- Scan statistics

Stored information can include:

- Scan type
- Input preview
- Risk level
- Risk score
- Threat category
- Processing time
- Analysis evidence
- Creation timestamp

---

# 12. Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Lucide React

## Backend

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy

## Machine Learning

- Scikit-learn
- TF-IDF
- Logistic Regression
- URL feature-based classification

## OCR

- Tesseract OCR
- pytesseract

## Database

- PostgreSQL
- SQLite fallback

## Deployment

- Docker
- Render
- Vercel

---

# 13. API Endpoints

## Health

    GET /api/v1/health

## Message Analysis

    POST /api/v1/analyze/message

## URL Analysis

    POST /api/v1/analyze/url

## Screenshot Analysis

    POST /api/v1/analyze/screenshot

## History

    GET    /api/v1/history
    GET    /api/v1/history/{scan_id}
    DELETE /api/v1/history
    DELETE /api/v1/history/{scan_id}

## Statistics

    GET /api/v1/stats

---

# 14. Local Development

## Backend Setup

From the project root:

    python3 -m venv backend/venv
    source backend/venv/bin/activate

Install dependencies:

    pip install -r backend/requirements.txt

Run the backend:

    uvicorn app.main:app \
      --app-dir backend \
      --host 127.0.0.1 \
      --port 8000 \
      --reload

Backend:

    http://127.0.0.1:8000

---

# 15. Frontend Setup

From the project root:

    pnpm install

Run the frontend:

    pnpm dev

Frontend:

    http://localhost:3000

Create `.env.local` in the project root:

    NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

---

# 16. API Documentation

FastAPI provides interactive API documentation.

Swagger UI:

    http://127.0.0.1:8000/docs

Health endpoint:

    http://127.0.0.1:8000/api/v1/health

---

# 17. Database

ScamShield uses a dual database strategy.

## PostgreSQL

PostgreSQL is used as the preferred database when configured and available.

## SQLite

SQLite is used as a fallback for local development when PostgreSQL is unavailable.

This allows the application to continue operating without requiring a PostgreSQL server during development.

---

# 18. Project Structure

    ScamShield/
    │
    ├── app/
    │   └── page.tsx
    │
    ├── components/
    │   └── scamshield.tsx
    │
    ├── lib/
    │   └── api.ts
    │
    ├── public/
    │
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   ├── db/
    │   │   ├── engine/
    │   │   ├── ml/
    │   │   ├── services/
    │   │   └── tests/
    │   │
    │   ├── datasets/
    │   ├── requirements.txt
    │   └── Dockerfile
    │
    ├── frontend/
    │   └── legacy frontend
    │
    ├── package.json
    ├── next.config.mjs
    ├── .dockerignore
    └── README.md

---

# 19. Testing

Run the backend tests from the project root:

    pytest -q backend/app/tests

The test suite covers areas including:

- Root endpoint
- Health endpoint
- Message analysis
- Message validation
- URL analysis
- URL validation
- Screenshot validation
- History
- Machine-learning pipeline
- Explainability
- URL feature contributions

---

# 20. Docker Deployment

The backend includes a Docker configuration for deployment.

Build the backend image:

    docker build -f backend/Dockerfile -t scamshield-backend .

Run locally:

    docker run -p 8000:8000 scamshield-backend

The container includes the OCR dependency required for screenshot processing.

The backend listens on:

    0.0.0.0:${PORT}

---

# 21. Deployment Architecture

                       Internet
                           │
                           ▼
                  ┌─────────────────┐
                  │     Vercel      │
                  │   Next.js UI    │
                  └────────┬────────┘
                           │
                           │ HTTPS REST API
                           ▼
                  ┌─────────────────┐
                  │     Render      │
                  │ FastAPI Backend │
                  │                 │
                  │ ML Models       │
                  │ Rule Engine     │
                  │ OCR Engine      │
                  └────────┬────────┘
                           │
                           ▼
                  PostgreSQL / SQLite

---

# 22. Deployment Environment Variables

## Frontend

Set:

    NEXT_PUBLIC_API_BASE_URL=https://YOUR-BACKEND-URL

## Backend

Configure the database and any application-specific environment variables required by the deployment environment.

---

# 23. Deployment Notes

The backend is designed to run as a Docker web service.

The Docker environment installs Tesseract OCR so screenshot processing does not depend on a developer's local operating-system installation.

The frontend is a Next.js application intended for deployment as a web application.

---

# 24. Current Project Status

Implemented core capabilities include:

- Project foundation
- FastAPI backend
- Next.js frontend
- CORS configuration
- PostgreSQL / SQLite database architecture
- Message scam classification
- URL phishing classification
- Rule-based threat indicators
- Risk scoring
- Threat categorization
- Explainability
- Safety recommendations
- Scan history
- History deletion
- Statistics
- Screenshot upload handling
- OCR-based screenshot analysis
- Automated backend tests
- Docker deployment configuration

---

# 25. Product Philosophy

ScamShield follows three principles:

## DETECT

Identify potentially harmful or suspicious digital content.

## EXPLAIN

Show the evidence and signals behind the result.

## PROTECT

Give users practical next steps to reduce the chance of financial loss, credential theft, or other digital harm.

---

# 26. Key Innovation

ScamShield combines multiple layers of analysis rather than relying only on a single classification model.

The platform brings together:

    Machine Learning
          +
    Deterministic Security Rules
          +
    Risk Scoring
          +
    Explainability
          +
    OCR
          +
    Safety Recommendations

This creates a user-facing workflow that moves beyond simply saying:

> "This is a scam."

Instead, ScamShield aims to answer:

> **Why is it risky, what evidence was detected, and what should the user do next?**

---

# 27. Competition Positioning

**Competition:** INNOV12  
**Team:** OBSIDIAN  
**Primary Track:** Cyber & Digital Trust  
**Supporting Track:** AI & GenAI

ScamShield is positioned as an accessible digital-trust tool for students and young digital users who frequently encounter fraudulent recruitment, payment, academic, and phishing scenarios online.

---

# 28. Disclaimer

ScamShield is a prototype security-assistance platform developed for competition and demonstration purposes.

Detection results are probabilistic and should be treated as decision support rather than absolute proof that a communication is malicious or legitimate.

Users should independently verify important communications through trusted official channels.

---

# DETECT → EXPLAIN → PROTECT

**ScamShield — Team OBSIDIAN**
