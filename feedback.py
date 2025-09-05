def suggest_fixes(spec, eval_notes, llm_feedback=None):
    """Generate intelligent fixes integrating heuristic and LLM-based suggestions"""
    fixes = []
    spec_type = spec.get("type", "unknown").lower()
    
    # Prioritize LLM suggestions if available
    if llm_feedback and llm_feedback.get('improvement_suggestions'):
        fixes.extend(llm_feedback['improvement_suggestions'][:2])
    
    # Add heuristic fixes for missing critical fields
    if not spec.get("dimensions"):
        fixes.append(_get_dimension_suggestion(spec_type))
    
    if not spec.get("material") or spec.get("material") == ["unknown"]:
        fixes.append(_get_material_suggestion(spec_type))
    
    if not spec.get("purpose") and len(fixes) < 3:
        fixes.append("Add purpose or use case description.")
    
    return fixes[:3]  # Limit to top 3 most important fixes

def _get_dimension_suggestion(spec_type):
    """Get contextual dimension suggestion"""
    suggestions = {
        "car": "Add car dimensions (typical: 4.5x1.8x1.4m for sports car)",
        "building": "Add building dimensions (consider: 20x15x8m for office)",
        "table": "Add table dimensions (standard: 180x90x75cm dining)",
        "drone": "Add drone dimensions (typical: 50x50x15cm for quadcopter)"
    }
    return suggestions.get(spec_type, "Add dimensions with unit, width, depth, height.")

def _get_material_suggestion(spec_type):
    """Get contextual material suggestion"""
    suggestions = {
        "car": "Add automotive materials (aluminum, steel, carbon fiber)",
        "building": "Add construction materials (concrete, glass, steel)",
        "drone": "Add aerospace materials (carbon fiber, aluminum)",
        "table": "Add furniture materials (wood, metal, glass)"
    }
    return suggestions.get(spec_type, "List realistic materials for this object type")

def apply_fixes(spec, fixes):
    """Apply suggested fixes with sophisticated logic"""
    improved_spec = dict(spec)
    obj_type = improved_spec.get("type")
    
    for fix in fixes:
        # Smart dimension application
        if "dimension" in fix.lower() and not improved_spec.get("dimensions"):
            improved_spec["dimensions"] = _apply_smart_dimensions(obj_type)
        
        # Smart material application
        if "material" in fix.lower() and (not improved_spec.get("material") or improved_spec.get("material") == ["unknown"]):
            improved_spec["material"] = _apply_smart_materials(obj_type)
        
        # Smart purpose application
        if "purpose" in fix.lower() and not improved_spec.get("purpose"):
            improved_spec["purpose"] = _apply_smart_purpose(obj_type)
        
        # Smart color application
        if "color" in fix.lower() and not improved_spec.get("color"):
            improved_spec["color"] = _apply_smart_color(obj_type)
    
    return improved_spec

def _apply_smart_dimensions(obj_type):
    """Apply contextually appropriate dimensions"""
    dims = {"car": "4.5x1.8x1.4m", "building": "20x15x8m", "table": "180x90x75cm", "drone": "50x50x15cm"}
    return dims.get(obj_type, "100x50x30cm")

def _apply_smart_materials(obj_type):
    """Apply contextually appropriate materials"""
    materials = {"car": ["aluminum", "steel"], "building": ["concrete", "glass"], "drone": ["carbon fiber"], "table": ["wood"]}
    return materials.get(obj_type, ["steel"])

def _apply_smart_purpose(obj_type):
    """Apply contextually appropriate purpose"""
    purposes = {"car": "transportation", "building": "commercial use", "drone": "surveillance", "table": "dining"}
    return purposes.get(obj_type, "general use")

def _apply_smart_color(obj_type):
    """Apply contextually appropriate color"""
    colors = {"car": "red", "building": "gray", "drone": "black", "table": "brown"}
    return colors.get(obj_type, "gray")

def calculate_reward(score, completeness=None):
    """Calculate enhanced reward with multiple factors"""
    base_reward = 1 if score >= 8 else -1
    if completeness:
        completeness_bonus = (completeness / 100) * 0.5
        return base_reward + completeness_bonus
    return base_reward