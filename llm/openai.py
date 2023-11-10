import os
from typing import List

from openai import OpenAI

from llm.base import BaseLLM
from llm.models import (
    OpenAIInstructions,
    OpenAIModels)

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO,
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

        if model_name.value not in [model.value for model in OpenAIModels]:
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def generate_message_prompt(self, prompt: str) -> List[dict]:
        """Generate final message prompt based on prompt parameter input."""
        messages = [{"role": "user", "content": prompt}]
        if self.instruction is not None:
            messages = [self.instruction.value] + messages
        return messages

    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        # Generate final message to be parsed by llm
        messages = self.generate_message_prompt(prompt=prompt)

        # Chat completion
        response = self.client.chat.completions.create(
            model=self.model_name.value,
            messages=messages,
            temperature=self.temperature,
            stream=False
        )

        return response.choices[0].message.content