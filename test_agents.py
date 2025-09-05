"""
Unit tests for agent classes
"""

import pytest
from agents.prompt_agent import PromptAgent
from agents.evaluator import Evaluator
from agents.feedback import FeedbackAgent
from agents.rl_agent import RLAgent

class TestAgents:
    def setup_method(self):
        """Setup test fixtures"""
        self.prompt_agent = PromptAgent()
        self.evaluator = Evaluator()
        self.feedback_agent = FeedbackAgent()
        self.rl_agent = RLAgent(self.evaluator, self.feedback_agent)
    
    def test_prompt_agent_run(self):
        """Test prompt agent run method"""
        input_data = {"prompt": "design a red sports car"}
        result = self.prompt_agent.run(input_data)
        
        assert isinstance(result, dict)
        assert "type" in result
        assert "material" in result
        assert "dimensions" in result
        assert "color" in result
        assert "purpose" in result
    
    def test_evaluator_run(self):
        """Test evaluator run method"""
        spec = {
            "type": "car",
            "material": ["steel", "aluminum"],
            "dimensions": "4.5x1.8x1.4m",
            "color": "red",
            "purpose": "transportation",
            "extras": None
        }
        input_data = {"spec": spec}
        result = self.evaluator.run(input_data)
        
        assert isinstance(result, dict)
        assert "spec_score" in result
        assert isinstance(result["spec_score"], int)
        assert 0 <= result["spec_score"] <= 10
    
    def test_feedback_agent_run(self):
        """Test feedback agent run method"""
        spec = {
            "type": "car",
            "material": ["unknown"],
            "dimensions": None,
            "color": None,
            "purpose": None,
            "extras": None
        }
        input_data = {"spec": spec, "score": 4}
        result = self.feedback_agent.run(input_data)
        
        assert isinstance(result, dict)
        assert "fixes" in result
        assert "explanation" in result
        assert isinstance(result["fixes"], list)
    
    def test_feedback_agent_apply_fixes(self):
        """Test feedback agent apply_fixes method"""
        spec = {
            "type": "car",
            "material": ["unknown"],
            "dimensions": None,
            "color": None,
            "purpose": None,
            "extras": None
        }
        fixes_result = {
            "fixes": ["add_dimensions", "fix_materials", "add_purpose"],
            "explanation": "Multiple improvements needed"
        }
        
        improved_spec = self.feedback_agent.apply_fixes(spec, fixes_result)
        
        assert improved_spec["dimensions"] is not None
        assert improved_spec["material"] != ["unknown"]
        assert improved_spec["purpose"] is not None
    
    def test_rl_agent_iterate(self):
        """Test RL agent iterate method"""
        spec = {
            "type": "car",
            "material": ["unknown"],
            "dimensions": None,
            "color": None,
            "purpose": None,
            "extras": None
        }
        
        result = self.rl_agent.iterate(spec, max_iters=2)
        
        assert isinstance(result, dict)
        assert "history" in result
        assert "final" in result
        assert "iterations" in result
        assert isinstance(result["history"], list)
        assert isinstance(result["iterations"], int)
    
    def test_empty_prompt(self):
        """Test agents with empty input"""
        result = self.prompt_agent.run({"prompt": ""})
        assert isinstance(result, dict)
    
    def test_invalid_spec_type(self):
        """Test evaluator with invalid spec"""
        spec = {"invalid": "spec"}
        result = self.evaluator.run({"spec": spec})
        assert isinstance(result, dict)
        assert "spec_score" in result