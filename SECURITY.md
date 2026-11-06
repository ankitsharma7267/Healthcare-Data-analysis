# Security Plan — HealthPulse Analytics

## Current implementation status

This repository is an academic Streamlit machine-learning demonstration. The current application must not be used with identifiable patient records or as a clinical decision system.

The initial HealthPulse redesign branch introduces a visual design system and clarifies that model outputs are educational estimates. It does **not** yet implement production authentication, authorization, or compliance controls.

## Required controls before handling personal data

- Authentication with password hashing (Argon2id or scrypt; never plaintext).
- Server-side role and permission checks on every protected operation.
- Short-lived sessions, secure cookies where supported, logout invalidation, and CSRF protection for state-changing requests.
- Least-privilege database credentials and parameterized SQL.
- Input validation, output encoding, upload restrictions, and safe error handling.
- Audit events for sign-in, access to sensitive records, exports, and administrative changes. Never log passwords, tokens, or clinical values.
- Encryption in transit (TLS) and appropriate encryption at rest with managed keys.
- Secrets supplied through environment/secret management, never committed to Git.
- Backups with restore testing, retention limits, and access controls.
- Data minimization, purpose limitation, retention/deletion workflows, and anonymization or aggregation for analytics.
- Dependency scanning, security testing, and incident response procedures.

## Machine-learning safety

- Treat model artifacts as trusted build outputs only. Do not load user-supplied pickle/joblib files.
- Fit preprocessing inside cross-validation pipelines to avoid data leakage.
- Evaluate class-specific precision, recall, F1, ROC-AUC, calibration, and confidence intervals; do not report accuracy alone.
- Keep a held-out test set untouched until final evaluation.
- Display dataset provenance, limitations, and the fact that model probability is not an individual's clinical risk.
- A qualified clinical and regulatory review is required before any real-world clinical use.

## Role model proposal

| Role | Intended access |
|---|---|
| Administrator | User and configuration management; audited administrative access |
| Clinician | Only assigned/authorized patient records |
| Analyst | Aggregated or de-identified datasets |
| Reception | Appointment and registration fields needed for the task |

## Compliance note

A checklist or academic prototype does not establish legal compliance. Any deployment processing personal or health data requires a jurisdiction-specific privacy, security, contractual, and legal assessment, including applicable Indian data-protection requirements.
