from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import re

class Dimension(BaseModel):
    unit: str
    width: float
    depth: float
    height: float

class Spec(BaseModel):
    name: Optional[str] = None
    type: str
    material: List[str] = Field(alias='material')
    dimensions: Optional[str] = None
    color: Optional[str] = None
    purpose: Optional[str] = None
    extras: Optional[str] = None

def parse_dimensions(dim_string: str) -> Optional[Dimension]:
    """Parse dimension string like '4.5x1.8x1.4m' into Dimension model"""
    if not dim_string:
        return None
    
    # Extract unit (m, cm, mm, etc.)
    unit_match = re.search(r'([a-zA-Z]+)$', dim_string)
    unit = unit_match.group(1) if unit_match else "unknown"
    
    # Extract numbers
    numbers = re.findall(r'(\d+(?:\.\d+)?)', dim_string)
    
    if len(numbers) >= 2:
        width = float(numbers[0])
        depth = float(numbers[1])
        height = float(numbers[2]) if len(numbers) >= 3 else 1.0
        
        return Dimension(unit=unit, width=width, depth=depth, height=height)
    
    return None

def score(spec_data: dict) -> dict:
    """Score spec based on Task 2 criteria"""
    s = 0
    
    # Dimensions present and valid? (+2)
    dim_string = spec_data.get("dimensions")
    if dim_string:
        parsed_dim = parse_dimensions(dim_string)
        if parsed_dim and parsed_dim.width > 0 and parsed_dim.depth > 0:
            s += 2
    
    # Material realistic? (+2)
    realistic_materials = ["steel", "wood", "concrete", "glass", "aluminum", 
                          "carbon fiber", "brick", "stone", "plastic", "metal"]
    materials = spec_data.get("material", [])
    if any(mat.lower() in realistic_materials for mat in materials):
        s += 2
    
    # Type matches prompt? (+2)
    building_types = ["building", "house", "castle", "library", "office"]
    mechanical_types = ["gearbox", "drone", "arm", "hand", "car", "engine", "table"]
    spec_type = spec_data.get("type", "").lower()
    if spec_type in building_types or spec_type in mechanical_types:
        s += 2
    
    # Format correct JSON? (+4)
    required_fields = ["type", "material", "dimensions", "color", "purpose", "extras"]
    if all(field in spec_data for field in required_fields):
        s += 4
    
    return {"spec_score": min(s, 10)}

def validate_and_score(spec_data: dict) -> dict:
    """Validate spec and return score with validation status"""
    try:
        spec = Spec(**spec_data)
        score_result = score(spec_data)
        return {
            "valid": True,
            "spec_score": score_result["spec_score"],
            "validation_error": None
        }
    except ValidationError as e:
        return {
            "valid": False,
            "spec_score": 0,
            "validation_error": str(e)
        }