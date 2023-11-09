from enum import Enum

class OpenAIInstructions(Enum):
    CHESS = {
        "role": "system",
        "content": """
            You are a chess grandmaster, the most ambitious chess player.
            You will be given an updated notation with moves from your opponent.
            You need to select the best move you can and reply in Forsyth-Edwards notation (FEN)."""}

class OpenAIModels(Enum):
    """All OpenAI models available through API"""
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"