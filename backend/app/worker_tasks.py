from celery import Celery
import os
from .tools import WebSearchTool

CELERY_BROKER = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery = Celery("worker", broker=CELERY_BROKER)


@celery.task(bind=True)
def async_web_search(self, query: str):
    tool = WebSearchTool()
    try:
        res = tool.run(query=query)
        return {"ok": True, "result": res}
    except Exception as e:
        return {"ok": False, "error": str(e)}
