# AML Agent Memory System

This repository contains the source code for the Agent Memory Challenge submission.

## System Overview
- **Architecture**: FastAPI-based web service.
- **Storage**: In-memory dictionary (ephemeral, resets on cold start).
- **Retrieval**: Simple keyword matching baseline.
- **Deployment**: Deployed on Alibaba Cloud Function Compute (FC) using Python 3.10 custom runtime.

## API Endpoints
- `GET /health`: Health check, returns `{"status": "ok"}`.
- `POST /add`: Ingests messages and stores them in memory. Also supports `HEAD` for platform health probing.
- `POST /search`: Retrieves relevant memory snippets based on the query. Returns `{"data": [...]}`. Also supports `HEAD`.

## Authentication
The API supports both `X-Api-Key` and `Authorization: Token` headers. The key is validated against a hardcoded variable `my-secret-key-123` (as per the submission form).

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
3. Run the test script: `python test_api.py`

## Deployment Details
- **Platform**: Alibaba Cloud Function Compute
- **Entrypoint**: `app/main.py`
- **Startup Command**: `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 9000`