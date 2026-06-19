# EVALUATION — Agentic System Design

Summary
- Orchestration pattern: coordinator-driven linear pipeline (Planner -> Researcher -> Analyst) with a shared state object that flows between agents. The coordinator persists state and events, routes tool calls (synchronous or via Celery), and streams events to frontend via WebSocket.

Orchestration pattern details
- Coordinator (`backend/app/orchestrator.py`):
  - Accepts user request, generates run_id, initializes state.
  - Calls Planner to decompose the task.
  - Iterates subtasks and delegates to Researcher / Analyst agents.
  - For long-running tool calls, submits Celery tasks and updates state on completion.
  - Persists every message, tool call, and final outcome to DB.

Agent roles
- Planner: decomposes the user query into subtasks and selects tools.
- Researcher: queries external sources via `WebSearchTool` and persists artifacts via `FileIOTool`.
- Analyst: runs computations via `CalculatorTool` and synthesizes final outputs.

Shared state design
- State object (persisted per run_id) fields:
  - run_id, user_id, query, subtasks, artifacts, logs, result
- Benefits: traceability, reentrancy, auditability.

Custom tools
- `WebSearchTool` — Pydantic input/output; currently mocked; intended for httpx-based API calls with retries and timeouts.
- `CalculatorTool` — Pydantic I/O; demo uses a restricted `eval` (replace in production with a safe parser).
- `FileIOTool` — saves artifacts to disk.

Function-calling & Pydantic
- Tools expose strict Pydantic models making them compatible with LLM function-calling.

Persistence & DB schema
- Core models (SQLAlchemy): Run, Message, ToolCall (see `backend/app/models.py`).
- Logging policy: persist every agent message and tool call with inputs and outputs; log errors and stack traces for debugging.

Concurrency & Celery
- Celery (Redis broker) used for long-running or parallel tool calls.

WebSocket streaming
- WebSocket manager streams structured events: agent_start, tool_call_start/end, agent_result, run_complete, errors.

Security & notes
- Rotated leaked credential and removed sensitive files from repo history. Do not commit `.env` or secret values.

Testing & evaluation plan
- Unit tests for tools and orchestrator flow (mock tools).
- Integration test: POST start + WS event sequence validation.

Observability & improvements
- Add structured logs (JSON), metrics (Prometheus), and a supervisory manager for retries and DLQ.
