# Architecture and workflow

1. Browser uploads a PDF/DOCX to `POST /api/v1/resume/parse`.
2. Parsing service extracts text and maps name, email, phone and keyword skills into JSON.
3. Registration validates the editable details with Pydantic, hashes the password with Argon2id and stores an inactive account.
4. OTP service creates a six-digit code, stores a hash with a five-minute expiry, and dispatches through a demo channel adapter.
5. Verification activates the account and returns a two-hour JWT.
6. JWT-protected profile endpoints support GET/PATCH. Dashboard endpoint returns `/dashboard/student`.

The database has `users`, `user_resumes`, and `otp_challenges` tables. Extracted metadata uses JSON-compatible columns, mapped to PostgreSQL JSONB when PostgreSQL is selected.
