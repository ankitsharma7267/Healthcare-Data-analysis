# HealthPulse Analytics

**Healthcare Data Analytics & Intelligent Disease Prediction Platform**

HealthPulse is an academic full-stack healthcare analytics project. The repository is migrating from its original Streamlit prototype to a React + Flask architecture while preserving the existing Python/scikit-learn disease-model work.

> **Safety boundary:** The current dashboard uses illustrative sample metrics and public academic datasets. It is not connected to a hospital, must not receive identifiable patient information, and is not a medical device. Model outputs are not diagnoses or validated individual clinical risk estimates.

## Technology

| Layer | Stack |
|---|---|
| Frontend | React, Vite, Framer Motion, Recharts, Lucide |
| Backend | Python, Flask, Flask REST API |
| Database | SQLAlchemy; SQLite for local tests, PostgreSQL for deployment |
| Authentication | JWT bearer access tokens, Argon2id password hashing |
| Protection | Server-side role checks, rate limits, CORS allowlist, security headers |
| Analytics / ML | Pandas, NumPy, Scikit-learn, Plotly (legacy Streamlit prototype) |
| Testing | Pytest; Vitest to be added with frontend tests |

## Repository layout

```text
.
├── app.py, train_models.py, prepare_data.py   # Original Streamlit + ML prototype
├── data/                                       # Public academic datasets
├── models/                                     # Existing trained model artifacts
├── notebooks/                                  # EDA / model-building notebook
├── backend/
│   ├── app/
│   │   ├── auth/                               # Registration, login, logout, profile
│   │   ├── api/                                # Versioned API endpoints
│   │   ├── models.py                           # User, revoked token, audit event
│   │   ├── security.py                         # Live database role checks
│   │   └── ...
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── src/
    │   ├── App.jsx                             # Responsive animated dashboard + sign-in
    │   ├── api.js                              # In-memory bearer token API client
    │   └── styles.css
    └── package.json
```

## Run locally (Windows PowerShell)

### 1. Backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`. Generate separate random secrets:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(48))"
```

Use one generated value for `SECRET_KEY` and a different value for `JWT_SECRET_KEY`. Keep `.env` private and out of Git. The default local database is SQLite; for shared or deployed environments, configure PostgreSQL in `DATABASE_URL`.

Initialize local tables and start the API:

```powershell
py -c "from app import create_app; from app.extensions import db; app=create_app(); ctx=app.app_context(); ctx.push(); db.create_all(); ctx.pop()"
py run.py
```

API health check: http://127.0.0.1:5000/api/health

### 2. Create an account and assign an administrator role

Public registration always creates an **analyst** account; clients cannot choose privileged roles.

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/v1/auth/register -ContentType "application/json" -Body '{"email":"admin@example.com","password":"Use-A-Unique-Long-Password"}'
```

Promote the account from a trusted local/server shell (requires database access):

```powershell
flask --app run.py promote-user admin@example.com --role admin
```

Then sign in through the React page. Never expose this role-change operation as a public registration option.

### 3. Frontend

Open a second PowerShell terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

Optional API URL override: create `frontend/.env.local` with `VITE_API_BASE_URL=http://127.0.0.1:5000/api/v1`.

## API endpoints

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/v1/auth/register` | Public; analyst role only |
| POST | `/api/v1/auth/login` | Public; rate-limited |
| GET | `/api/v1/auth/me` | Authenticated |
| POST | `/api/v1/auth/logout` | Authenticated; revokes current token |
| GET | `/api/v1/overview` | Authenticated roles |
| GET | `/api/v1/admin/audit-events` | Admin only |
| GET | `/api/health` | Public health check |

Bearer tokens are held in frontend memory, not localStorage. They expire after 15 minutes by default; re-authentication is required after expiry or page refresh. Logout adds the token identifier to the revocation table. Role and account status are checked against the database for protected role-gated routes.

## Run backend tests

From the `backend` directory with its virtual environment active:

```powershell
pytest -q
```

Tests cover registration, Argon2 password hashing, login, authenticated access, logout/revocation, privilege escalation prevention, and analyst denial on the admin audit endpoint.

## Security notes and remaining production work

The implemented controls are an educational baseline, not a production security certification. Before real users or health data are introduced, complete and independently review: TLS/HSTS at the deployment edge, managed secrets, PostgreSQL migrations and backups, durable shared rate-limit storage (for example Redis), token refresh/session lifecycle, account recovery and MFA, CSP and frontend XSS review, dependency scanning, authorization tests for every resource, audit retention/monitoring, incident response, privacy impact assessment, and applicable legal/compliance review. Read [SECURITY.md](SECURITY.md).

## Machine-learning migration

The original Streamlit prototype and trained models remain during migration. Before serving predictions from Flask, refactor preprocessing into Scikit-learn Pipelines fitted inside each cross-validation fold, verify dataset provenance and target definitions, evaluate class-specific metrics and calibration, and add model/version tracking. Do not load user-supplied pickle files.

## Future scope

- Patient and doctor workflows with record-level authorization
- Disease trend analytics and cohort filters
- Explainable AI (e.g. SHAP) and model monitoring
- Model performance, calibration and fairness reporting
- Secure PDF/CSV report generation
- HL7 FHIR interoperability and ABDM integration only after appropriate approvals and conformance work
- PostgreSQL-backed multi-tenant deployment, observability and disaster recovery
