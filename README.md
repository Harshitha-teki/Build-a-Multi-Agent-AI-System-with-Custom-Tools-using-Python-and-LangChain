## Multi-Agent AI Orchestration Scaffold

This repository contains a runnable scaffold for the "Build a Multi-Agent AI System" project. It demonstrates the architecture and core patterns required for the assignment: a FastAPI backend (REST + WebSocket), a simple multi-agent orchestrator, Pydantic-defined tools, SQL logging, and a React frontend for real-time visualization.

What this repository includes
- Backend: `backend/app` — FastAPI app, orchestrator, tools, DB models, Celery wiring for async tasks.
- Frontend: `frontend/` — minimal React app that connects to the backend WebSocket and displays agent events.
- Infrastructure: `docker-compose.yml` for Postgres + Redis + backend + worker (uses env var config).

Security & submission note
- A credential was accidentally committed earlier but has been rotated and the repository history was cleaned.
- The repository tip no longer contains the secret. I rotated the Postgres password and purged the sensitive files from history. A local `.env` was created for you with the new password — do NOT commit that file.

Quick run (local development)

1) Prepare environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Start backend (dev):

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3) Start frontend (separate shell):

```powershell
cd frontend
npm install
npm start
```

4) (Optional) Start full stack with Docker Compose (recommended for demo):

```powershell
copy .env.example .env
notepad .env  # update values if needed (do not commit)
docker compose --env-file .env up --build
```

API quick usage
- POST /api/start — start a run; returns `{ "status": "started", "run_id": "..." }`.
- WS /ws/{run_id} — connect to receive real-time agent events for the given run.

Repository layout (important files)
- `backend/app` — FastAPI app and orchestrator
- `backend/app/tools.py` — custom Pydantic tools
- `backend/app/models.py` — SQLAlchemy models (Run, Message, ToolCall)
- `frontend/src/App.js` — React UI + WS client
- `docker-compose.yml` — Postgres + Redis + backend + worker (uses env vars)

Recording the demo
- Steps: start the stack, open frontend, submit a task, record the UI showing agent steps and final result, and show DB entry for the run.

Next recommended steps
- Replace mock LLM calls with LangChain/LangGraph or AutoGen integrations.
- Replace any eval-based logic with safe parsers (CalculatorTool currently uses eval for demo).
- Add `pre-commit` with `detect-secrets` to prevent future leaks.

If you need a submission package or short video script, I can produce them for you.
# Multi-Agent AI Orchestration Scaffold

This repository contains a minimal scaffold for the "Build a Multi-Agent AI System" project.

What's included:
- FastAPI backend (`backend/app`) that exposes a REST endpoint to start a task and a WebSocket to stream real-time updates.
- A simple orchestrator that coordinates three agents (Planner, Researcher, Analyst) and uses three custom tools with Pydantic schemas.
- SQLAlchemy models to log runs, agent messages, and tool calls. Defaults to SQLite for local dev; Docker Compose provides Postgres for production-like runs.
- Celery wiring for long-running tool calls (Redis broker). Worker tasks are declared in `backend/worker_tasks.py`.
- A minimal React frontend in `frontend/` that connects to the WebSocket and visualizes agent events.

This scaffold intentionally uses mock LLM/tool implementations so you can run and test locally without API keys. It is designed to be extended to LangGraph/AutoGen and real LLM providers.

How to run (local dev, quick):

1. Create a Python virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Start the backend:

```powershell
cd backend; uvicorn app.main:app --reload
```

3. Start the frontend (in a separate shell):

```powershell
cd frontend; npm install; npm start
```

Optional full stack with Docker Compose (Postgres + Redis):

```powershell
docker compose up --build
```

Next steps:
- Swap the mock orchestrator LLM calls for LangChain/LangGraph or AutoGen integrations.
- Add real LLM keys via environment and implement function-calling schemas for better tool compatibility.
- Add Celery workers for production-scale long-running tools.
