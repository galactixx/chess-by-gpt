import chess
from enum import Enum
from chess import InvalidMoveError

from llm.openai import OpenAILLM

MAX_TRIES = 5

class BoardSide(Enum):
    """Side of the board that is being played by LLM."""
    WHITE = 'white'
    BLACK = 'black'

class Engine:
    """Chess engine run entirely by response and output from GPT 3.5."""
    def __init__(self, pgn: str, llm_side: BoardSide, llm: OpenAILLM):
        self.pgn = pgn
        self._llm_side = llm_side
        self._llm = llm

        self.counter_error = 0
        self.incorrect_moves = []

        # Chess boards
        self._chess_board = chess.Board()

        # Check that llm_side parameter is of the correct (expected) type
        if not isinstance(self._llm_side, BoardSide):
            raise Exception('incorrect llm_side parameter specified, must be of type BoardSide')

    def get_chess_move_response(self) -> str:
        """Execute llm inference to determine what the appropriate chess move should be."""

        while True:
            prompt = f"""
            In this chess game you are playing as {self._llm_side.value}. The following moves in the chess game have been made: {self.pgn}"""
            move = self._llm.get_completion(prompt=prompt)
            print(move)

            try:
                move_board = chess.Move.from_uci(''.join([i.strip() for i in move.split(',')]))
            except InvalidMoveError:
                continue

            if self.counter_error > MAX_TRIES:
                raise ValueError('engine sucks...')
            
            if move_board in list(self._chess_board.legal_moves):
                self._chess_board.push(move_board)
                break
            self.incorrect_moves.append(move)
            self.counter_error += 1
        return move