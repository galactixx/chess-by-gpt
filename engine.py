from enum import Enum

from llm.openai import OpenAILLM

class BoardSide(Enum):
    """Side of the board that is being played by LLM."""
    WHITE = 'white'
    BLACK = 'black'

class Engine:
    """Chess engine run entirely by response and output from GPT 3.5."""
    def __init__(self, white_moves: list, black_moves: list, llm_side: BoardSide, llm: OpenAILLM):
        self.white_moves = white_moves
        self.black_moves = black_moves
        self._llm_side = llm_side
        self._llm = llm

        if not isinstance(self._llm_side, BoardSide):
            raise Exception('incorrect llm_side parameter specified, must be of type BoardSide')

    def get_chess_move_response(self) -> str:
        """Execute llm inference to determine what the appropriate chess move should be."""
        prompt = f"""
            You are playing a chess game against a chess grandmaster. You are playing as the
            {self._llm_side} pieces. It is move {len(self.white_moves)}.
            
            The following moves have been made for either side:

            White moves: {', '.join(self.white_moves)}

            Black moves: {', '.join(self.black_moves)}
        """

        move = self._llm.get_completion(prompt=prompt)

        return move