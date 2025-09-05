from abc import ABC, abstractmethod
from typing import Dict, Any

class AgentBase(ABC):
    @abstractmethod
    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Run agent with input dict and return output dict"""
        ...