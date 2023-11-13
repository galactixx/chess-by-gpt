import io
from typing import Optional

import chess
import random
import chess.pgn
from enum import Enum

from llm.openai import OpenAILLM

MAX_TRIES = 5

class BoardSide(Enum):
    """Side of the board that is being played by LLM."""
    WHITE = 'white'
    BLACK = 'black'

class Engine:
    """Chess engine run entirely by response and output from GPT 3.5."""
    def __init__(self, pgn: str, llm_side: BoardSide, llm: OpenAILLM):
        self._pgn = pgn
        self._llm_side = llm_side
        self._llm = llm

        self.counter_error = 0

        # Chess boards
        self._chess_board = chess.Board()

        # Record position
        self._record_current_position_in_board()

        # Generate all current legal moves
        self._legal_moves = list(self._chess_board.legal_moves)

        # Check that llm_side parameter is of the correct (expected) type
        if not isinstance(self._llm_side, BoardSide):
            raise Exception('incorrect llm_side parameter specified, must be of type BoardSide')
        
    @property
    def current_move_number(self) -> int:
        """Retrieve current move number from board position."""
        return (self._chess_board.ply() // 2) + 1

    def offer_draw_response(self) -> str:
        """Logic for offering a draw to LLM."""
        prompt = f"""
        You are offered a draw in the chess game.
        The position is as follows {self._pgn}. Do you accept the draw? Respond yes or no."""
        respone = self._llm.get_completion(prompt=prompt)
        return 'Yes' if 'yes' in respone.lower() else 'No'

    def _record_current_position_in_board(self) -> None:
        """Record all moves from pgn in chess board."""

        # Create a StringIO object from the PGN string
        pgn = io.StringIO(self._pgn)

        # Read the game from the PGN
        game = chess.pgn.read_game(pgn)

        # Apply all moves from the game to the board
        for move in game.mainline_moves():
            self._chess_board.push(move)

    def _validate_response_move(self, target_move: str) -> Optional[str]:
        """Validate move response from LLM."""

        # Find a move to the target square
        for move in self._legal_moves:
            if self._chess_board.san(move) == target_move:
                return str(move)
            
    def _prepare_clean_response_move(self, move: str) -> str:
        """Clean and prepare move from LLM based on expected format of reponse."""
        return move.split()[0].strip()
    
    def _random_pick_given_no_response(self) -> str:
        """
        Pick random move from list of possible moves only if it cannot generate valid response.
        This has not actually happened through testing, but preparing for worst case scenario.
        """
        return random.choice(self._legal_moves)

    def get_chess_move_response(self) -> str:
        """Execute llm inference to determine what the appropriate chess move should be."""

        while True:
            if self.counter_error > MAX_TRIES:
                move = self._random_pick_given_no_response()
            else:

                prompt = f"""
                In this chess game you are playing as {self._llm_side.value}.
                The following moves in the chess game have been made: {self._pgn}"""
                move = self._llm.get_completion(prompt=prompt)

                # Clean response from LLM
                move_cleaned = self._prepare_clean_response_move(move=move)

            # Validate the response from LLM
            move_validated = self._validate_response_move(target_move=move_cleaned)

            if move_validated is not None:
                return move_validated
            self.counter_error += 1