from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional

app = FastAPI(title="Prompt to JSON Agent API", version="1.0.0")

class PromptRequest(BaseModel):
    prompt: str

class SpecRequest(BaseModel):
    prompt: str
    spec: Dict[str, Any]

class IterateRequest(BaseModel):
    spec: Optional[Dict[str, Any]] = None
    spec_id: Optional[str] = None
    max_iters: Optional[int] = 3

class ValuesRequest(BaseModel):
    honesty: Optional[str] = None
    integrity: Optional[str] = None
    discipline: Optional[str] = None
    gratitude: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "prompt-to-json-agent"}

@app.post("/generate")
def generate(request: PromptRequest):
    prompt = request.prompt.lower()
    
    # Simple prompt parsing
    if "car" in prompt:
        obj_type = "car"
        materials = ["steel", "aluminum"]
        dimensions = "4.5x1.8x1.4m"
    elif "building" in prompt:
        obj_type = "building" 
        materials = ["concrete", "glass"]
        dimensions = "20x15x8m"
    elif "drone" in prompt:
        obj_type = "drone"
        materials = ["carbon fiber"]
        dimensions = "50x50x15cm"
    else:
        obj_type = "object"
        materials = ["steel"]
        dimensions = "100x50x30cm"
    
    # Extract color
    color = None
    for c in ["red", "blue", "green", "black", "white"]:
        if c in prompt:
            color = c
            break
    
    return {
        "type": obj_type,
        "material": materials,
        "dimensions": dimensions,
        "color": color,
        "purpose": "general use",
        "extras": None
    }

@app.post("/evaluate")
def evaluate(request: SpecRequest):
    # Simple evaluation
    spec = request.spec
    score = 5  # Base score
    
    if spec.get("type"):
        score += 1
    if spec.get("material"):
        score += 1
    if spec.get("dimensions"):
        score += 2
    if spec.get("color"):
        score += 1
    
    return {"score": min(score, 10), "report_id": "mock-report-id"}

@app.post("/iterate")
def iterate(request: IterateRequest):
    spec = request.spec or {}
    
    # Simple improvement
    improved_spec = spec.copy()
    if not improved_spec.get("color"):
        improved_spec["color"] = "gray"
    if not improved_spec.get("purpose"):
        improved_spec["purpose"] = "general use"
    
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
def get_report(report_id: str):
    return {
        "id": report_id,
        "evaluation": {"mock": "data"},
        "score": 8,
        "created_at": "2024-01-01T00:00:00Z"
    }

@app.post("/log-values")
def log_values(request: ValuesRequest):
    return {"id": "mock-values-id", "message": "Values logged successfully"}

@app.get("/metrics")
def get_metrics():
    return {
        "total_requests": 0,
        "success_rate": 100,
        "avg_response_time": 0.1
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)