from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict
import httpx
import time


class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query")


class WebSearchOutput(BaseModel):
    query: str
    results: Dict[str, Any]


class WebSearchTool:
    def run(self, query: str) -> Dict:
        inp = WebSearchInput(query=query)
        # mock external call
        try:
            time.sleep(0.3)
            # return mock
            return {"query": inp.query, "results": {"top": ["result1", "result2"]}}
        except Exception as e:
            raise RuntimeError(f"WebSearch failed: {e}")


class CalculatorInput(BaseModel):
    expression: str


class CalculatorOutput(BaseModel):
    expression: str
    value: float


class CalculatorTool:
    def run(self, expression: str) -> Any:
        inp = CalculatorInput(expression=expression)
        try:
            # WARNING: eval used only for demo; replace with safe parser
            value = eval(inp.expression, {"__builtins__": {}})
            out = CalculatorOutput(expression=inp.expression, value=value)
            return out.value
        except Exception as e:
            raise RuntimeError(f"Calculator error: {e}")


class FileIOInput(BaseModel):
    path: str
    content: str


class FileIOOutput(BaseModel):
    path: str
    ok: bool


class FileIOTool:
    def save(self, path: str, content: str) -> Dict:
        inp = FileIOInput(path=path, content=content)
        try:
            with open(inp.path, "w", encoding="utf-8") as f:
                f.write(inp.content)
            return {"path": inp.path, "ok": True}
        except Exception as e:
            return {"path": inp.path, "ok": False, "error": str(e)}
