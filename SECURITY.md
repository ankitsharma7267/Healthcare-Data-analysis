# HealthPulse Analytics — Security Notes

## Implemented in the current React + Flask foundation

- Passwords are hashed with Argon2id; plaintext passwords are never stored.
- Public account registration always assigns the least-privileged `analyst` role. It cannot grant admin or clinician access.
- JWT bearer access tokens expire after 15 minutes by default and are held in React memory rather than localStorage.
- Logout revokes the current token identifier in the database.
- Protected role-gated endpoints read the user's current role and active status from the database on each request.
- Login and registration endpoints have rate limits.
- CORS is restricted to the configured frontend origin(s).
- API responses receive `Cache-Control: no-store`; baseline browser security headers are set.
- Audit metadata records account registration, successful and failed login, and logout. It deliberately excludes passwords, tokens, and clinical payloads.
- An admin-only audit-events endpoint is available. Role promotion is restricted to a trusted server shell command.
- Backend tests cover registration, password hashing, login, authenticated requests, logout/revocation, public role-escalation prevention, and analyst denial on the admin audit endpoint.

## Important limitations

This is an academic security baseline, not a production security certification. The current app uses sample dashboard data and has no live patient records or patient-management API. Do not enter or upload identifiable patient or health information.

The frontend keeps the access token in memory. A page refresh or token expiry requires signing in again; a production refresh-token/session design still needs threat modelling and review. The default rate-limit storage is in-memory and is not suitable for multiple production workers. Use a shared Redis-backed store in a deployed environment.

## Required before real users or health data

- Serve only over HTTPS; configure HSTS at the trusted TLS-terminating edge.
- Use managed secrets and rotate credentials; never commit `.env` files.
- Use PostgreSQL migrations, least-privilege database accounts, encrypted backups, and tested restore procedures.
- Add MFA, verified account recovery, administrator lifecycle controls, and a reviewed token renewal/revocation strategy.
- Add a strict Content Security Policy, dependency scanning, frontend XSS review, secure file-upload controls if uploads are introduced, and security monitoring.
- Test object-level authorization for every patient, appointment, report, export, and model-history resource before those resources exist.
- Establish audit retention, access review, incident response, deletion/retention workflows, privacy notices, and a privacy impact assessment.
- Complete jurisdiction-specific legal, contractual, privacy, and healthcare regulatory review.

## Role model

| Role | Intended future permissions |
|---|---|
| Admin | User administration and audited configuration access |
| Clinician | Only assigned/authorized patient records |
| Analyst | Aggregated or de-identified analytics |
| Reception | Minimum registration and appointment fields required for work |

Role names do not themselves establish permission boundaries; every API operation must enforce server-side authorization and, where relevant, record-level access.

## Machine-learning safety

- Only load trusted model artifacts created by the project build pipeline; never load user-supplied pickle/joblib files.
- Fit preprocessing inside each cross-validation fold to avoid data leakage.
- Evaluate class-specific precision, recall, F1, ROC-AUC, calibration, uncertainty, and confidence intervals, not accuracy alone.
- Preserve a held-out test set for final evaluation.
- Model probabilities are not a person's clinical risk and must not be presented as diagnoses or treatment guidance.
- Clinical validation and regulatory review are required before any real-world clinical use.

## Compliance

A prototype checklist does not establish legal compliance. Any deployment processing personal or health data requires a jurisdiction-specific privacy, security, contractual, and legal assessment, including applicable Indian data-protection requirements.
