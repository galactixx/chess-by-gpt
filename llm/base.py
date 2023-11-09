from typing import List

from abc import ABC, abstractmethod

from llm.models import (
    OpenAIInstructions,
    OpenAIModels)

class BaseLLM(ABC):
    """Base interface for LLM."""

    def __init__(self, model_name: OpenAIModels, instruction: OpenAIInstructions) -> None:
        pass

    @abstractmethod
    def generate_message_prompt(self, prompt: str) -> List[dict]:
        """Generate final message prompt based on prompt parameter input."""
        pass

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from LLM."""
        pass