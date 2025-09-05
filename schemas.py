from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

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

class ReportOut(BaseModel):
    id: uuid.UUID
    spec_id: uuid.UUID
    evaluation: Dict[str, Any]
    score: int
    created_at: datetime
    
    class Config:
        from_attributes = True