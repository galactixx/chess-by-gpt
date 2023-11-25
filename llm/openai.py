from openai import OpenAI
import requests

from llm.base import BaseLLM
from llm.models import (
    OpenAIInstructions,
    OpenAIModels)

def valid_openai_key(api_key: str) -> bool:
    """Test OpenAI API key for validity."""

    # Connection to OpenAI endpoint and check validity
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        return False

class OpenAILLM(BaseLLM):
    """Simple interface for OpenAI LLM."""
    def __init__(self,
                 api_key: str,
                 model_name: OpenAIModels = OpenAIModels.GPT_3_5_TURBO_INSTRUCT,
                 instruction: OpenAIInstructions = OpenAIInstructions.CHESS,
                 temperature: float = 1.0):
        self._api_key = api_key
        self._model_name = model_name
        self._instruction = instruction
        self._temperature = temperature

        # Instantiate a client object for interacting with the OpenAI API
        self._client = OpenAI(api_key=self._api_key)

        if not isinstance(self._model_name, OpenAIModels):
            raise ValueError(f'{model_name} is not a valid model name for OpenAI API')
        
    def get_completion(self, prompt: str) -> str:
        """Get prompt completion from OpenAI API."""

        # Chat completion
        response = self._client.completions.create(
            model=self._model_name.value,
            prompt=self._instruction.value + prompt,
            temperature=self._temperature,
            stream=False,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].text