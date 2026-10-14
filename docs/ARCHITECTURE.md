# Architecture

```text
React + Vite frontend
        |
        | HTTP
        v
FastAPI REST API
        |
        | OAuth 2.0
        v
Google Drive API
        |
        +--> Search advising-plan documents
        +--> Preview selected Google Doc
        +--> Export selected plan as PDF / DOCX
```

## Main routes

- `GET /authorize` — begins local Google OAuth flow
- `GET /oauth2callback` — stores the local OAuth token
- `GET /search?query=...` — searches Google Docs
- `GET /preview?file_id=...` — streams a PDF preview
- `GET /generate?file_id=...&format=pdf|docx` — exports the selected plan

## Security notes

- OAuth client credentials and tokens are intentionally excluded from Git.
- The project is intended as a local portfolio/demo application, not a production deployment.
- Use only synthetic/demo student data in screenshots or public demonstrations.
