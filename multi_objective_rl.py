"""
Multi-Objective Reinforcement Learning Agent
Optimizes specifications across multiple objectives with weighted scoring
"""

from core.agent_base import AgentBase
from typing import Dict, Any, List
import json

class MultiObjectiveRLAgent(AgentBase):
    def __init__(self, evaluator, feedbacker):
        self.evaluator = evaluator
        self.feedbacker = feedbacker
        
        # Multi-objective weights (sum to 1.0)
        self.objectives = {
            "completeness": 0.30,    # Required fields filled
            "realism": 0.25,         # Material and design feasibility  
            "feasibility": 0.20,     # Manufacturing/construction viability
            "innovation": 0.15,      # Advanced materials and design
            "cost_efficiency": 0.10  # Economic optimization
        }
    
    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Run multi-objective optimization"""
        spec = input.get("spec", {})
        max_iters = input.get("max_iters", 3)
        
        return self.optimize_multi_objective(spec, max_iters)
    
    def optimize_multi_objective(self, spec: Dict[str, Any], max_iters: int = 3) -> Dict[str, Any]:
        """Optimize spec across multiple objectives"""
        history = []
        current = spec.copy()
        
        for iteration in range(1, max_iters + 1):
            # Evaluate current spec across all objectives
            scores = self._evaluate_objectives(current)
            total_score = sum(scores[obj] * weight for obj, weight in self.objectives.items())
            
            # Identify weakest objective for targeted improvement
            weakest_obj = min(scores.keys(), key=lambda x: scores[x])
            
            # Get targeted feedback for weakest area
            feedback = self._get_targeted_feedback(current, weakest_obj, scores)
            
            # Apply improvements
            improved_spec = self._apply_multi_objective_fixes(current, feedback, weakest_obj)
            
            # Evaluate improved spec
            new_scores = self._evaluate_objectives(improved_spec)
            new_total_score = sum(new_scores[obj] * weight for obj, weight in self.objectives.items())
            
            # Calculate multi-objective reward
            reward = self._calculate_multi_objective_reward(scores, new_scores)
            
            # Record iteration
            history.append({
                "iteration": iteration,
                "before": current,
                "after": improved_spec,
                "scores_before": scores,
                "scores_after": new_scores,
                "total_score_before": total_score,
                "total_score_after": new_total_score,
                "targeted_objective": weakest_obj,
                "feedback": feedback,
                "reward": reward,
                "improvement": new_total_score - total_score
            })
            
            # Update current spec if improved
            if new_total_score > total_score:
                current = improved_spec
            else:
                break  # Stop if no improvement
        
        return {
            "history": history,
            "final_spec": current,
            "iterations": len(history),
            "final_scores": self._evaluate_objectives(current)
        }
    
    def _evaluate_objectives(self, spec: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate spec across all objectives (0-100 scale)"""
        scores = {}
        
        # Completeness: Check required fields
        required_fields = ["type", "material", "dimensions", "color", "purpose"]
        filled_fields = sum(1 for field in required_fields if spec.get(field))
        scores["completeness"] = (filled_fields / len(required_fields)) * 100
        
        # Realism: Material and design assessment
        scores["realism"] = self._assess_realism(spec)
        
        # Feasibility: Manufacturing/construction viability
        scores["feasibility"] = self._assess_feasibility(spec)
        
        # Innovation: Advanced materials and design
        scores["innovation"] = self._assess_innovation(spec)
        
        # Cost Efficiency: Economic optimization
        scores["cost_efficiency"] = self._assess_cost_efficiency(spec)
        
        return scores
    
    def _assess_realism(self, spec: Dict[str, Any]) -> float:
        """Assess material and design realism (0-100)"""
        score = 100
        
        obj_type = spec.get("type", "").lower()
        materials = spec.get("material", [])
        
        # Check material-type compatibility
        realistic_materials = {
            "car": ["steel", "aluminum", "carbon fiber", "plastic", "glass"],
            "building": ["concrete", "steel", "glass", "brick", "wood"],
            "drone": ["carbon fiber", "aluminum", "plastic", "titanium"],
            "table": ["wood", "metal", "glass", "plastic"]
        }
        
        if obj_type in realistic_materials:
            for material in materials:
                if material.lower() not in realistic_materials[obj_type]:
                    score -= 20
        
        return max(0, score)
    
    def _assess_feasibility(self, spec: Dict[str, Any]) -> float:
        """Assess manufacturing/construction feasibility (0-100)"""
        score = 90  # Base feasibility
        
        # Check dimension reasonableness
        dimensions = spec.get("dimensions")
        if dimensions:
            try:
                # Parse dimensions like "4.5x1.8x1.4m"
                if "x" in str(dimensions):
                    parts = str(dimensions).lower().replace("m", "").replace("cm", "").split("x")
                    if len(parts) >= 2:
                        dims = [float(p.strip()) for p in parts[:3]]
                        # Check for unrealistic dimensions
                        if any(d > 1000 for d in dims):  # Too large
                            score -= 30
                        elif any(d < 0.01 for d in dims):  # Too small
                            score -= 20
            except:
                score -= 10  # Invalid dimension format
        
        return max(0, score)
    
    def _assess_innovation(self, spec: Dict[str, Any]) -> float:
        """Assess innovation level (0-100)"""
        score = 60  # Base innovation
        
        materials = spec.get("material", [])
        advanced_materials = ["carbon fiber", "titanium", "graphene", "smart glass", "aerogel"]
        
        # Bonus for advanced materials
        for material in materials:
            if material.lower() in advanced_materials:
                score += 15
        
        # Bonus for detailed purpose
        purpose = spec.get("purpose", "")
        if purpose and len(purpose) > 20:
            score += 10
        
        return min(100, score)
    
    def _assess_cost_efficiency(self, spec: Dict[str, Any]) -> float:
        """Assess cost efficiency (0-100)"""
        score = 85  # Base efficiency
        
        materials = spec.get("material", [])
        expensive_materials = ["carbon fiber", "titanium", "gold", "platinum"]
        cheap_materials = ["steel", "aluminum", "plastic", "wood"]
        
        # Adjust based on material costs
        for material in materials:
            if material.lower() in expensive_materials:
                score -= 15
            elif material.lower() in cheap_materials:
                score += 5
        
        return max(0, min(100, score))
    
    def _get_targeted_feedback(self, spec: Dict[str, Any], target_objective: str, scores: Dict[str, float]) -> List[str]:
        """Generate feedback targeted at specific objective"""
        feedback = []
        
        if target_objective == "completeness":
            if not spec.get("dimensions"):
                feedback.append("Add specific dimensions with units")
            if not spec.get("material"):
                feedback.append("Specify realistic materials")
            if not spec.get("purpose"):
                feedback.append("Define clear purpose or use case")
        
        elif target_objective == "realism":
            feedback.append("Use materials appropriate for the object type")
            feedback.append("Ensure design is physically realistic")
        
        elif target_objective == "feasibility":
            feedback.append("Optimize dimensions for manufacturing")
            feedback.append("Consider production constraints")
        
        elif target_objective == "innovation":
            feedback.append("Consider advanced materials or features")
            feedback.append("Add innovative design elements")
        
        elif target_objective == "cost_efficiency":
            feedback.append("Balance performance with cost-effective materials")
            feedback.append("Optimize for economic production")
        
        return feedback[:2]  # Limit to top 2 suggestions
    
    def _apply_multi_objective_fixes(self, spec: Dict[str, Any], feedback: List[str], target_objective: str) -> Dict[str, Any]:
        """Apply fixes targeted at specific objective"""
        improved = spec.copy()
        obj_type = spec.get("type", "").lower()
        
        for fix in feedback:
            if "dimensions" in fix.lower() and not improved.get("dimensions"):
                improved["dimensions"] = self._get_optimal_dimensions(obj_type, target_objective)
            
            elif "material" in fix.lower():
                improved["material"] = self._get_optimal_materials(obj_type, target_objective)
            
            elif "purpose" in fix.lower() and not improved.get("purpose"):
                improved["purpose"] = self._get_optimal_purpose(obj_type, target_objective)
        
        return improved
    
    def _get_optimal_dimensions(self, obj_type: str, objective: str) -> str:
        """Get dimensions optimized for specific objective"""
        if objective == "cost_efficiency":
            # Smaller, more economical dimensions
            dims = {"car": "4.0x1.6x1.3m", "building": "15x12x6m", "drone": "40x40x12cm", "table": "120x80x75cm"}
        elif objective == "innovation":
            # Larger, more advanced dimensions
            dims = {"car": "5.0x2.0x1.5m", "building": "25x20x12m", "drone": "60x60x20cm", "table": "200x100x75cm"}
        else:
            # Standard dimensions
            dims = {"car": "4.5x1.8x1.4m", "building": "20x15x8m", "drone": "50x50x15cm", "table": "180x90x75cm"}
        
        return dims.get(obj_type, "100x50x30cm")
    
    def _get_optimal_materials(self, obj_type: str, objective: str) -> List[str]:
        """Get materials optimized for specific objective"""
        if objective == "cost_efficiency":
            materials = {"car": ["steel"], "building": ["concrete"], "drone": ["aluminum"], "table": ["wood"]}
        elif objective == "innovation":
            materials = {"car": ["carbon fiber", "titanium"], "building": ["smart glass", "steel"], "drone": ["carbon fiber"], "table": ["carbon fiber"]}
        else:
            materials = {"car": ["aluminum", "steel"], "building": ["concrete", "glass"], "drone": ["carbon fiber"], "table": ["wood"]}
        
        return materials.get(obj_type, ["steel"])
    
    def _get_optimal_purpose(self, obj_type: str, objective: str) -> str:
        """Get purpose optimized for specific objective"""
        if objective == "innovation":
            purposes = {"car": "autonomous electric racing vehicle", "building": "smart sustainable office complex", "drone": "AI-powered surveillance and delivery", "table": "smart interactive workspace"}
        else:
            purposes = {"car": "efficient transportation", "building": "commercial office space", "drone": "aerial surveillance", "table": "dining and workspace"}
        
        return purposes.get(obj_type, "general purpose use")
    
    def _calculate_multi_objective_reward(self, before_scores: Dict[str, float], after_scores: Dict[str, float]) -> float:
        """Calculate weighted multi-objective reward"""
        total_improvement = 0
        
        for objective, weight in self.objectives.items():
            improvement = after_scores[objective] - before_scores[objective]
            weighted_improvement = improvement * weight
            total_improvement += weighted_improvement
        
        # Normalize to -1 to +1 scale
        return max(-1.0, min(1.0, total_improvement / 100))