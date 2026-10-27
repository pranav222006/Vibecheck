# Vibe Check – Website with AI Assistant

**Live site (HTTPS):** https://YOUR-APP.onrender.com  <!-- replace after deploying -->

A responsive Django site with a mood-based "Vibe Check" home page, FAQ page, error-code catalog, support tickets, health page, and a chat assistant on every page.

## Features
- 5+ pages: Home, FAQs (12, SQL), Error Codes (8 incl. custom 418 "Vibe Mismatch"), Support Tickets, Health
- AI assistant: answers from FAQ data, explains error codes, creates a ticket when it can't answer (optional LLM via `ANTHROPIC_API_KEY`)
- SQL (SQLite/Postgres): FAQs, error codes, tickets · MongoDB: chat logs and feedback
- Custom 404/500 pages with "Ask the Assistant for Help"
- `RequestLoggingMiddleware`, `/health/` (+ `?format=json`), third-party quote API with 3s timeout and local fallback
- Secrets only in environment variables (`.env.example` provided)

## Run locally
```
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # set DEBUG=True for local dev
python manage.py migrate && python manage.py seed
python manage.py runserver
```
Test 404 and 500 pages with `DEBUG=False`: `/test-404-route` and `/test-error/?code=500`.

## Deploy (Render)
Build: `bash build.sh` · Start: see `Procfile` · Set env vars from `.env.example` (MongoDB Atlas URI in `MONGODB_URI`).

## Proposed improvement
Add user accounts with saved mood history and personalised playlists, plus semantic (embedding) search so the assistant matches FAQs more accurately.
