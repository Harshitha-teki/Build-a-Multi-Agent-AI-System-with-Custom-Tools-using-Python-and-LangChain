from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import BackgroundTasks
import uuid
from pydantic import BaseModel
from .orchestrator import run_task
from typing import Dict

router = APIRouter()


class TaskRequest(BaseModel):
    user_id: str
    query: str


@router.post("/start")
async def start_task(req: TaskRequest, background_tasks: BackgroundTasks):
    # generate run id and kick off the orchestrator in background
    run_id = str(uuid.uuid4())
    background_tasks.add_task(run_task, req.user_id, req.query, run_id)
    return {"status": "started", "run_id": run_id}


class WSConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, run_id: str, ws: WebSocket):
        await ws.accept()
        self.active[run_id] = ws

    def disconnect(self, run_id: str):
        self.active.pop(run_id, None)

    async def send(self, run_id: str, payload: dict):
        ws = self.active.get(run_id)
        if ws:
            await ws.send_json(payload)


manager = WSConnectionManager()


@router.websocket('/ws/{run_id}')
async def websocket_endpoint(ws: WebSocket, run_id: str):
    await manager.connect(run_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(run_id)
