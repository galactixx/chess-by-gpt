import os

from openai import OpenAI

from llm.base import BaseLLM
from llm.models import (
    OpenAIInstructions,
    OpenAIModels)

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO_INSTRUCT,
                 instruction: OpenAIInstructions = OpenAIInstructions.CHESS,
                 temperature: float = 1.0):
        self.model_name = model_name
        self.instruction = instruction
        self.temperature = temperature

        # Retrieve API key
        self._open_ai_key = os.environ['OPENAI_API_KEY']

        # The API key is blank or not set
        if not self._open_ai_key:
            raise ValueError("OPENAI_API_KEY is not set or is blank")

        # Instantiate a client object for interacting with the OpenAI API
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

        if not isinstance(self.model_name, OpenAIModels):
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        # Chat completion
        response = self.client.completions.create(
            model=self.model_name.value,
            prompt=self.instruction.value + prompt,
            temperature=self.temperature,
            stream=False,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].text