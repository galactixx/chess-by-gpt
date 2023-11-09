import json

from flask import Flask, request, render_template

from engine import BoardSide, Engine
from llm.openai import OpenAILLM

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/move')
def get_move():
    """Retrieve move for LLM for chess game."""
    white_moves = request.args.getlist('movesWhite')
    black_moves = request.args.getlist('movesBlack')

    print(white_moves)

    # Instantiate engine
    engine_chess = Engine(
        white_moves=white_moves,
        black_moves=black_moves,
        llm_side=BoardSide.BLACK,
        llm=OpenAILLM())
    
    # Get move response from LLM
    move = engine_chess.get_chess_move_response()

    return move

if __name__ == '__main__':
    app.run(debug=True)

