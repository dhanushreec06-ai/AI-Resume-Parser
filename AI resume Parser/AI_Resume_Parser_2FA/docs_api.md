# API quick reference

All endpoints are prefixed as shown. Interactive schemas are available at `/docs`.

## Resume parsing
`POST /api/v1/resume/parse` — multipart form field `file` (PDF/DOCX).

## Register
`POST /api/v1/auth/register` JSON:
```json
{"name":"Jane Doe","email":"jane@example.com","phone":"+911234567890","password":"strong-password","skills":["Python","SQL"],"channel":"email"}
```

## Verify
`POST /api/v1/auth/verify-2fa` JSON:
```json
{"email":"jane@example.com","channel":"email","otp":"123456"}
```
OTP is printed in the server terminal in demo mode.

## Profile
Send `Authorization: Bearer <access_token>` to `GET` or `PATCH /api/v1/profile`.
