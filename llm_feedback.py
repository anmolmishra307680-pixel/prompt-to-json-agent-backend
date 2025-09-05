from typing import Dict, List
import json

class LLMFeedbackAgent:
    """LLM-style intelligent feedback system"""
    
    def __init__(self):
        self.domain_expertise = {
            "automotive": {
                "materials": ["aluminum", "steel", "carbon fiber", "plastic", "rubber"],
                "typical_dimensions": {"car": "4.5x1.8x1.4m", "truck": "6.0x2.5x2.8m"},
                "safety_requirements": ["crash safety", "emissions", "fuel efficiency"],
                "colors": ["red", "blue", "black", "white", "silver"]
            },
            "construction": {
                "materials": ["concrete", "steel", "wood", "glass", "brick"],
                "typical_dimensions": {"house": "12x10x3m", "office": "20x15x8m"},
                "building_codes": ["structural integrity", "fire safety", "accessibility"],
                "colors": ["white", "gray", "brown", "beige"]
            },
            "aerospace": {
                "materials": ["carbon fiber", "aluminum", "titanium", "composite"],
                "typical_dimensions": {"drone": "50x50x15cm", "aircraft": "10x8x2m"},
                "regulations": ["weight limits", "flight safety", "communication"],
                "colors": ["white", "gray", "black"]
            }
        }
    
    def analyze_spec_quality(self, spec: Dict) -> Dict:
        """Analyze spec quality with domain expertise"""
        analysis = {
            "completeness": 0,
            "realism": 0,
            "domain_compliance": 0,
            "suggestions": []
        }
        
        obj_type = spec.get("type", "unknown")
        materials = spec.get("material", [])
        dimensions = spec.get("dimensions")
        purpose = spec.get("purpose")
        
        # Completeness analysis
        required_fields = ["type", "material", "dimensions", "purpose"]
        filled_fields = sum(1 for field in required_fields if spec.get(field))
        analysis["completeness"] = (filled_fields / len(required_fields)) * 100
        
        # Realism analysis
        domain = self._get_domain(obj_type)
        if domain and materials:
            realistic_materials = self.domain_expertise[domain]["materials"]
            realistic_count = sum(1 for mat in materials if mat in realistic_materials)
            analysis["realism"] = (realistic_count / len(materials)) * 100 if materials else 0
        
        return analysis
    
    def generate_intelligent_critique(self, spec: Dict, evaluation: Dict) -> List[str]:
        """Generate intelligent, contextual critique"""
        critiques = []
        obj_type = spec.get("type", "unknown")
        score = evaluation.get("spec_score", 0)
        
        # Domain-specific analysis
        domain = self._get_domain(obj_type)
        
        if score < 8:
            critiques.append(f"Specification quality is below optimal (score: {score}/10)")
        
        # Missing dimensions critique
        if not spec.get("dimensions"):
            if domain == "automotive":
                critiques.append("Missing critical dimensions. For automotive applications, precise measurements are essential for manufacturing and safety compliance.")
            elif domain == "construction":
                critiques.append("Dimensions required for structural calculations and building permits. Consider standard room sizes or building footprints.")
            else:
                critiques.append("Dimensions needed for manufacturing feasibility and cost estimation.")
        
        # Material analysis
        materials = spec.get("material", [])
        if not materials or materials == ["unknown"]:
            if domain == "automotive":
                critiques.append("Material selection critical for performance, weight, and safety. Consider aluminum for lightweight, steel for strength.")
            elif domain == "construction":
                critiques.append("Building materials must meet structural and environmental requirements. Concrete and steel are common for load-bearing.")
            else:
                critiques.append("Material choice affects durability, cost, and manufacturing process.")
        
        # Purpose analysis
        if not spec.get("purpose"):
            critiques.append("Purpose definition helps optimize design parameters and material selection for intended use case.")
        
        return critiques
    
    def suggest_improvements(self, spec: Dict, evaluation: Dict) -> List[str]:
        """Generate intelligent improvement suggestions"""
        suggestions = []
        obj_type = spec.get("type", "unknown")
        domain = self._get_domain(obj_type)
        
        # Dimension suggestions
        if not spec.get("dimensions"):
            if domain and obj_type in self.domain_expertise[domain]["typical_dimensions"]:
                typical = self.domain_expertise[domain]["typical_dimensions"][obj_type]
                suggestions.append(f"Consider typical {obj_type} dimensions: {typical}")
            else:
                suggestions.append("Add specific dimensions (length x width x height) with appropriate units")
        
        # Material optimization
        materials = spec.get("material", [])
        if domain and (not materials or materials == ["unknown"]):
            recommended = self.domain_expertise[domain]["materials"][:2]
            suggestions.append(f"Recommended materials for {obj_type}: {', '.join(recommended)}")
        
        # Purpose enhancement
        if not spec.get("purpose"):
            purpose_suggestions = {
                "car": "transportation, racing, commuting",
                "building": "residential, commercial, industrial",
                "drone": "surveillance, delivery, photography",
                "table": "dining, office work, display"
            }
            if obj_type in purpose_suggestions:
                suggestions.append(f"Consider purpose: {purpose_suggestions[obj_type]}")
        
        # Color recommendations
        if not spec.get("color") and domain:
            colors = self.domain_expertise[domain]["colors"][:3]
            suggestions.append(f"Popular colors for {obj_type}: {', '.join(colors)}")
        
        return suggestions
    
    def _get_domain(self, obj_type: str) -> str:
        """Map object type to domain"""
        domain_map = {
            "car": "automotive",
            "building": "construction", 
            "house": "construction",
            "office": "construction",
            "drone": "aerospace",
            "aircraft": "aerospace"
        }
        return domain_map.get(obj_type)
    
    def generate_comprehensive_feedback(self, spec: Dict, evaluation: Dict) -> Dict:
        """Generate comprehensive LLM-style feedback"""
        analysis = self.analyze_spec_quality(spec)
        critiques = self.generate_intelligent_critique(spec, evaluation)
        suggestions = self.suggest_improvements(spec, evaluation)
        
        return {
            "quality_analysis": analysis,
            "critiques": critiques,
            "improvement_suggestions": suggestions,
            "overall_assessment": self._generate_assessment(spec, evaluation, analysis)
        }
    
    def _generate_assessment(self, spec: Dict, evaluation: Dict, analysis: Dict) -> str:
        """Generate overall assessment"""
        score = evaluation.get("spec_score", 0)
        completeness = analysis["completeness"]
        
        if score >= 9:
            return "Excellent specification with comprehensive details and realistic parameters."
        elif score >= 7:
            return f"Good specification ({completeness:.0f}% complete) with minor improvements needed."
        elif score >= 5:
            return f"Adequate specification requiring significant enhancements for production readiness."
        else:
            return f"Incomplete specification ({completeness:.0f}% complete) requiring major improvements."