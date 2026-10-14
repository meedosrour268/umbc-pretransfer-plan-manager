"""FastAPI backend for the UMBC Pre-Transfer Plan Manager portfolio project."""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from services.export_service import EXPORT_MIME_TYPES, export_google_doc

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="UMBC Pre-Transfer Plan Manager API", version="1.0.0")

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
]

CREDENTIALS_FILE = BASE_DIR / os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = BASE_DIR / os.getenv("GOOGLE_TOKEN_FILE", "token.json")
TARGET_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "").strip()
OAUTH_REDIRECT_URI = os.getenv(
    "OAUTH_REDIRECT_URI", "http://localhost:8000/oauth2callback"
)


def _save_token(creds: Credentials) -> None:
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")


def get_drive_service():
    """Return an authenticated Google Drive service."""
    if not TOKEN_FILE.exists():
        raise HTTPException(
            status_code=401,
            detail="Google OAuth is not configured. Visit /authorize first.",
        )

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_token(creds)

    if not creds.valid:
        raise HTTPException(status_code=401, detail="Google OAuth token is invalid.")

    return build("drive", "v3", credentials=creds, cache_discovery=False)


@app.get("/authorize", include_in_schema=False)
def authorize_user():
    """Start the local Google OAuth flow."""
    if not CREDENTIALS_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="credentials.json is missing. See README setup instructions.",
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        scopes=SCOPES,
        redirect_uri=OAUTH_REDIRECT_URI,
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    app.state.oauth_flow = flow
    app.state.oauth_state = state
    return RedirectResponse(auth_url)


@app.get("/oauth2callback", include_in_schema=False)
def oauth2callback(code: str, state: str | None = None):
    """Complete OAuth and persist a local token.json file."""
    flow = getattr(app.state, "oauth_flow", None)
    expected_state = getattr(app.state, "oauth_state", None)
    if flow is None:
        raise HTTPException(status_code=400, detail="OAuth flow has not been started.")
    if state and expected_state and state != expected_state:
        raise HTTPException(status_code=400, detail="OAuth state mismatch.")

    flow.fetch_token(code=code)
    _save_token(flow.credentials)
    return RedirectResponse("http://localhost:5173/?oauth=success")


@app.get("/search")
def search_files(query: str = Query(min_length=1, max_length=100)):
    """Search Google Docs by name, optionally restricted to one Drive folder."""
    service = get_drive_service()
    safe_query = query.replace("'", "\\'")

    clauses = [
        f"name contains '{safe_query}'",
        "mimeType = 'application/vnd.google-apps.document'",
        "trashed = false",
    ]
    if TARGET_FOLDER_ID:
        clauses.append(f"'{TARGET_FOLDER_ID}' in parents")

    try:
        results = (
            service.files()
            .list(
                q=" and ".join(clauses),
                pageSize=25,
                orderBy="modifiedTime desc",
                fields="files(id,name,modifiedTime,webViewLink)",
            )
            .execute()
        )
        return results.get("files", [])
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Google Drive search failed.") from exc


@app.get("/generate")
def generate(file_id: str, format: Literal["pdf", "docx"] = "pdf"):
    """Export a selected Google Doc as PDF or DOCX."""
    service = get_drive_service()
    try:
        file_bytes = export_google_doc(file_id, service, format)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Document export failed.") from exc

    return StreamingResponse(
        iter([file_bytes]),
        media_type=EXPORT_MIME_TYPES[format],
        headers={"Content-Disposition": f'attachment; filename="student-plan.{format}"'},
    )


@app.get("/preview")
def preview_doc(file_id: str):
    """Stream a selected Google Doc as PDF."""
    service = get_drive_service()
    try:
        pdf_bytes = export_google_doc(file_id, service, "pdf")
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Document preview failed.") from exc

    return StreamingResponse(iter([pdf_bytes]), media_type="application/pdf")


@app.get("/")
def home():
    return {"status": "ok", "service": "UMBC Pre-Transfer Plan Manager API"}
