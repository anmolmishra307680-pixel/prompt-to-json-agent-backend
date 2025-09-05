from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Simple schemas
class PromptIn(BaseModel):
    prompt: str

class SpecIn(BaseModel):
    prompt: str
    spec: Dict[str, Any]

class IterateIn(BaseModel):
    spec: Optional[Dict[str, Any]] = None
    spec_id: Optional[str] = None
    max_iters: Optional[int] = 3

class ValuesIn(BaseModel):
    honesty: Optional[str] = None
    integrity: Optional[str] = None
    discipline: Optional[str] = None
    gratitude: Optional[str] = None

# Simple agent
class SimpleAgent:
    def run(self, input_data):
        prompt = input_data.get("prompt", "").lower()
        if "car" in prompt:
            return {"type": "car", "material": ["steel"], "dimensions": "4.5x1.8x1.4m", "color": "red" if "red" in prompt else None, "purpose": "transportation", "extras": None}
        elif "building" in prompt:
            return {"type": "building", "material": ["concrete"], "dimensions": "20x15x8m", "color": None, "purpose": "office", "extras": None}
        return {"type": "object", "material": ["steel"], "dimensions": "100x50x30cm", "color": None, "purpose": "general use", "extras": None}

# Mock database functions
def mock_get_db():
    return None

def mock_save_spec(db, prompt, spec):
    class MockSpec:
        id = "mock-spec-id"
    return MockSpec()

def mock_save_report(db, spec_id, evaluation, score):
    class MockReport:
        id = "mock-report-id"
    return MockReport()

def mock_get_report(db, report_id):
    return {"id": report_id, "evaluation": {}, "score": 8}

def mock_save_values_log(db, **kwargs):
    class MockValues:
        id = "mock-values-id"
    return MockValues()

# Initialize app and agent
app = FastAPI(title="Prompt to JSON Agent API", version="1.0.0")
prompt_agent = SimpleAgent()

@app.post("/generate")
def generate(payload: PromptIn):
    out = prompt_agent.run(payload.dict())
    return out

@app.post("/evaluate")
def evaluate(payload: SpecIn):
    spec = payload.spec
    score = 5
    if spec.get("type"): score += 1
    if spec.get("material"): score += 1
    if spec.get("dimensions"): score += 2
    if spec.get("color"): score += 1
    
    spec_row = mock_save_spec(None, payload.prompt, payload.spec)
    report_row = mock_save_report(None, spec_row.id, {}, min(score, 10))
    return {"report_id": report_row.id, "score": min(score, 10)}

@app.post("/iterate")
def iterate(payload: IterateIn):
    if not payload.spec:
        raise HTTPException(status_code=400, detail="spec required")
    
    spec = payload.spec
    improved_spec = spec.copy()
    if not improved_spec.get("color"): improved_spec["color"] = "gray"
    if not improved_spec.get("purpose"): improved_spec["purpose"] = "general use"
    
    return {
        "iterations": 1,
        "history": [{
            "iteration": 1,
            "before": spec,
            "after": improved_spec,
            "feedback": ["Added missing fields"],
            "reward": 1
        }],
        "final_spec": improved_spec
    }

@app.get("/reports/{report_id}")
def get_report_by_id(report_id: str):
    return mock_get_report(None, report_id)

@app.post("/log-values")
def log_values(payload: ValuesIn):
    values_log = mock_save_values_log(None, **payload.dict())
    return {"id": values_log.id, "message": "Values logged successfully"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "prompt-to-json-agent"}

@app.get("/metrics")
def get_metrics():
    return {"total_requests": 0, "success_rate": 100, "avg_response_time": 0.1}

# run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000