from enum import Enum

class OpenAIInstructions(Enum):
    CHESS = {
        "role": "system",
        "content": """
            You are a chess grandmaster, the most ambitious chess player.
            You will be given an updated notation with moves from your opponent.
            You need to select the best move and respond with the source move (notation) followed by the target move (notation) separated by a comma.
            For example, if you are moving a7 to a5, responsd with a7, a5. Or if you are moving Ba7 to Ba5, then respones Ba7, Ba5.
            Please use traditional chess notation. DO NOT OUTPUT ANYTHING BUT THE SOURCE MOVE AND TARGET MOVE separated by a comma."""}

class OpenAIModels(Enum):
    """All OpenAI models available through API"""
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_0613 = "gpt-4-0613"