# Day 28 — OTP Register/Login System

A username + password auth system where email ownership is verified via a
one-time password (OTP), backed by n8n as the workflow/data layer and
Streamlit as the frontend.

## What it does

- **Register**: enter username, email, password → n8n emails a 6-digit OTP
  (valid 10 minutes) → enter the OTP to verify your email.
- **Login**: username + password, checked against the stored (hashed)
  password once the account is verified.
- **Forgot Password**: enter your email → n8n emails a new OTP → enter the
  OTP + a new password to reset it.
- On successful login: **"Well done, Rajeev, one more step forward towards
  the future you want."**

## Tech stack

- **Streamlit** — the form/UI, running locally
- **Python** (`requests`, `hashlib`, `python-dotenv`) — talks to n8n over
  HTTP, hashes passwords with SHA-256 before they ever leave the machine
- **n8n** (local, `localhost:5678`) — 4 webhook-triggered workflows, using
  n8n's built-in **Data Table** (no external database) as the user store,
  and the Gmail node (existing OAuth connection) to send OTP emails

## Why these choices

- **Password hashing happens in Python, not n8n** — the plaintext password
  never travels over the wire or gets stored anywhere. n8n only ever sees
  a SHA-256 hash.
- **n8n Data Table over Google Sheets** — same zero-budget requirement,
  but no extra OAuth scope needed, and it's the pattern n8n itself
  recommends for exactly this use case (persisting form/webhook data
  across runs).
- **Gmail node over `smtplib`** — the OAuth connection already existed
  from a prior project, so there's no new credential setup, and n8n
  handles the auth token refresh automatically (a plain `smtplib` +
  App Password setup would need a new Google security step).

## How to run it

### 1. Import the n8n workflows

In your local n8n editor (`localhost:5678`):

1. Create a new workflow → **⋮ menu → Import from File** → select
   `1-otp-register.json`. Repeat for `2-otp-verify.json`,
   `3-otp-login.json`, `4-otp-forgot-reset.json`.
2. In each imported workflow, open the **Gmail node(s)** and re-select
   your existing Gmail OAuth credential from the dropdown (the JSON ships
   with a placeholder credential ID that won't resolve on your instance).
3. **Activate** all four workflows (top-right toggle).
4. Confirm the `users` Data Table exists (**Overview → Data Tables**) with
   columns: `username`, `email`, `password_hash`, `verified`, `otp_code`,
   `otp_expiry`. If it doesn't exist yet, create it manually with those six
   columns before testing.

### 2. Set up the Python side

```bash
pip install streamlit requests python-dotenv
cp .env.example .env
```

`.env` should contain:
```
N8N_BASE_URL=http://localhost:5678/webhook
```

### 3. Run it

```bash
streamlit run streamlit_app.py
```

Open the local URL Streamlit prints, register with a real email you can
check, and follow the OTP prompt.

## Notes

- This is a learning project — OTP rate-limiting, brute-force lockouts,
  and stronger password hashing (bcrypt/argon2) are intentionally left out
  to keep scope tight, per the Day 28 goal.
