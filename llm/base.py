from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Base interface for LLM."""

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        pass