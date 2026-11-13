# AI-Powered Resume Parser & Multi-Channel 2FA Onboarding Pipeline

A runnable internship-task implementation based on the supplied task brief. It provides resume upload and extraction, registration staging, Argon2 password hashing, OTP verification, JWT access tokens, profile editing, and dashboard routing.

## Stack
- Python 3.11+, FastAPI, Pydantic v2
- SQLAlchemy async ORM; PostgreSQL via `asyncpg` or SQLite for quick local demo
- PDF: `pdfplumber`; DOCX: `python-docx`; regex-based field extraction
- Passlib Argon2id, PyJWT

## Run locally (fastest)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000` for the onboarding page and `/docs` for Swagger API documentation. SQLite is used by default, so no database server is required for the demo.

## PostgreSQL
Create a database named `resume_onboarding`, copy `.env.example` to `.env`, set `DATABASE_URL` to:
`postgresql+asyncpg://USER:PASSWORD@HOST:5432/resume_onboarding`
Set a strong `JWT_SECRET` and load environment variables before starting the server.

## Main endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/resume/parse` | Upload PDF/DOCX and return extracted fields |
| POST | `/api/v1/auth/register` | Validate, hash password, stage account and create OTP |
| POST | `/api/v1/auth/verify-2fa` | Verify OTP, activate account and issue JWT |
| GET | `/api/v1/profile` | View authenticated profile |
| PATCH | `/api/v1/profile` | Edit authenticated profile |
| GET | `/api/v1/dashboard` | Return dashboard routing payload |
| GET | `/health` | Health check |

## OTP demo behaviour
For all three channel choices (email, WhatsApp, browser), this project creates a one-time code, stores only its SHA-256 hash, applies a five-minute expiry, and prints the code in the server console. This is a development adapter, **not a live email/WhatsApp integration**. Production deployment must connect SMTP/email and WhatsApp Business API providers, add delivery retries/rate limits, and use a dedicated TOTP authenticator implementation if authenticator-app TOTP is required.

## Important production hardening
- Change the JWT secret and configure secrets outside source control.
- Add migrations (Alembic), rate limiting, audit logging, HTTPS, upload malware scanning, file retention controls and stronger resume validation.
- Restrict CORS to trusted origins; add role-based authorization and refresh-token/session revocation.
- Avoid returning raw extracted resume text in production responses.
- The parser uses transparent regex/keyword heuristics; validate and allow users to edit extracted fields.

## GitHub upload
Create a new repository, extract this ZIP, then upload the contents of this folder (not the ZIP itself). Do not commit `.env`, database files, passwords or real resumes.
