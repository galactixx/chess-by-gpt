from enum import Enum

class OpenAIInstructions(Enum):
    CHESS = """You are chess grandmaster Magnus Carlsen, the best and most ambitious chess player in history.
               Respond with a single move."""

class OpenAIModels(Enum):
    """All OpenAI models available through API"""
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"
    GPT_3_5_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"