# UMBC Pre-Transfer Plan Manager

A portfolio reconstruction of a full-stack software engineering project created to support the management of academic advising plans for prospective transfer students entering UMBC.

This portfolio version focuses on the reconstructed workflow: authenticating with Google, searching advising-plan documents, previewing a selected plan, and exporting it as PDF or Word through a React frontend and FastAPI backend.

> **Project context:** The original system was developed collaboratively as part of a software engineering course project. This repository is a cleaned portfolio reconstruction of the recovered application workflow, rather than a claim of sole authorship over the original team repository.

## Features

- React/Vite search interface for advising plans
- Python/FastAPI REST backend
- Google OAuth 2.0 authentication
- Google Drive document search
- Embedded Google Docs preview
- PDF and DOCX export
- Optional restriction to a dedicated Drive folder
- Environment-based configuration with credentials excluded from source control

## Tech stack

**Frontend:** React, React Router, Vite  
**Backend:** Python, FastAPI, Uvicorn  
**Integrations:** Google OAuth 2.0, Google Drive API

## Architecture

```text
React / Vite
     |
     | REST
     v
FastAPI
     |
     | OAuth 2.0
     v
Google Drive API
     |
     +-- Search advising plans
     +-- Preview Google Docs
     +-- Export PDF / DOCX
```

More detail: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Local setup

### 1. Backend

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
cp .env.example .env
```

Create a Google OAuth Desktop App credential in Google Cloud and place the downloaded file at:

```text
backend/credentials.json
```

Never commit that file.

Run the API:

```bash
uvicorn main:app --reload --port 8000
```

Then visit:

```text
http://localhost:8000/authorize
```

to complete Google OAuth once and create the local `token.json` file.

### 2. Frontend

In another terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## Configuration

Backend environment variables are documented in `backend/.env.example`.

If `GOOGLE_DRIVE_FOLDER_ID` is populated, searches are restricted to that Drive folder. Leaving it blank searches accessible Google Docs more broadly.

## Portfolio/demo guidance

For public screenshots or demos, use synthetic student names and a dedicated demo Drive folder. Do not expose real student records, OAuth tokens, client secrets, or personal Google account details.

## Background

The original course project explored pre-transfer advising workflows and academic-plan management. During development I worked across UI, backend integration, Google Workspace workflows, testing, documentation, and system design, This cleaned portfolio version reconstructs the recovered search, preview, and export workflow. It requires your own Google OAuth configuration to run; it has not been validated against a live Google account during this preparation.
