from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)