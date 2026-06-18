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
