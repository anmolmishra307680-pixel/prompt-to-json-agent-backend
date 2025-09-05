from core.agent_base import AgentBase
from evaluator.criteria import validate_and_score
from evaluator.llm_feedback import LLMFeedbackAgent
from datetime import datetime

class Evaluator(AgentBase):
    def __init__(self):
        self.llm_agent = LLMFeedbackAgent()
    
    def run(self, input):
        spec = input.get("spec", {})
        
        # Use existing evaluation system
        evaluation = validate_and_score(spec)
        
        # Add LLM feedback
        feedback = self.llm_agent.generate_comprehensive_feedback(spec, evaluation)
        
        # Return complete evaluation
        return {
            "spec_score": evaluation["spec_score"],
            "valid": evaluation["valid"],
            "validation_error": evaluation.get("validation_error"),
            "llm_feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }