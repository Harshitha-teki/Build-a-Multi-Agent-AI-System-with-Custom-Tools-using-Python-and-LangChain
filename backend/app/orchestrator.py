import uuid
import time
from typing import Dict, Any
from .tools import WebSearchTool, CalculatorTool, FileIOTool
from .db import SessionLocal, engine
from . import models
# avoid importing `manager` at module import time to prevent circular imports

# create tables
models.Base.metadata.create_all(bind=engine)


def run_task(user_id: str, query: str, run_id: str = None):
    if run_id is None:
        run_id = str(uuid.uuid4())
    # log start
    db = SessionLocal()
    run = models.Run(id=run_id, user_id=user_id, query=query)
    db.add(run)
    db.commit()

    # simple state
    state: Dict[str, Any] = {"query": query, "notes": []}

    # Agents: Planner -> Researcher -> Analyst
    send_ws(run_id, {"event": "started", "run_id": run_id, "query": query})

    try:
        planner_output = planner_agent(state)
        log_message(db, run_id, "planner", planner_output)
        send_ws(run_id, {"event": "agent", "agent": "planner", "data": planner_output})

        research_output = researcher_agent(state, planner_output)
        log_message(db, run_id, "researcher", research_output)
        send_ws(run_id, {"event": "agent", "agent": "researcher", "data": research_output})

        analysis_output = analyst_agent(state, research_output)
        log_message(db, run_id, "analyst", analysis_output)
        send_ws(run_id, {"event": "agent", "agent": "analyst", "data": analysis_output})

        # final
        db.query(models.Run).filter(models.Run.id == run_id).update({"status": "completed", "result": str(analysis_output)})
        db.commit()
        send_ws(run_id, {"event": "completed", "result": analysis_output})
    except Exception as e:
        db.query(models.Run).filter(models.Run.id == run_id).update({"status": "failed", "result": str(e)})
        db.commit()
        send_ws(run_id, {"event": "error", "error": str(e)})
    finally:
        db.close()


def send_ws(run_id: str, payload: dict):
    # attempt to send via manager; ignore if no client
    import asyncio

    try:
        # import manager here to avoid circular import at module load time
        from .api import manager
        asyncio.get_event_loop().create_task(manager.send(run_id, payload))
    except Exception:
        pass


def log_message(db, run_id: str, agent: str, content: dict):
    entry = models.Message(run_id=run_id, agent=agent, content=str(content))
    db.add(entry)
    db.commit()


def planner_agent(state: Dict, ) -> Dict:
    # mock planner: break query into subtasks
    time.sleep(0.5)
    subtasks = [f"Research background for: {state['query']}", "Analyze gathered data", "Summarize recommendations"]
    return {"plan": subtasks}


def researcher_agent(state: Dict, planner_output: Dict) -> Dict:
    # use WebSearchTool and FileIOTool
    ws = WebSearchTool()
    results = []
    for item in planner_output["plan"][:1]:
        res = ws.run(query=item)
        results.append(res)
    # save to file
    fi = FileIOTool()
    saved = fi.save(path=f"research_{int(time.time())}.txt", content=str(results))
    return {"results": results, "saved": saved}


def analyst_agent(state: Dict, research_output: Dict) -> Dict:
    calc = CalculatorTool()
    # pretend we compute a metric
    value = calc.run(expression="1+1")
    return {"analysis": f"Computed metric {value}", "insights": research_output}
