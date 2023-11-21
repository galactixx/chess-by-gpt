import secrets
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    session)

from engine import (
    BoardSide,
    Engine)
from llm.openai import (
    OpenAILLM, 
    OpenAITest)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index() -> str:
    return render_template("index.html")

@app.route('/store-api-key', methods=['POST'])
def store_api_key() -> bool:
    """Store OpenAI api key in session, only if a valid key."""
    
    # Unpack json data
    data = request.json
    api_key = data['apiKey']

    # Test if OpenAI key is valid
    open_ai_test = OpenAITest(api_key=api_key)
    api_key_valid = open_ai_test.is_valid_openai_key()
    if api_key_valid:
        session['api_key'] = data['apiKey']

    print(api_key_valid)
    
    return jsonify({"isValid": api_key_valid})

@app.route('/move')
def get_move() -> str:
    """Retrieve move for LLM for chess game."""

    pgn = request.args.get('pgn')
    api_key = session.get('api_key')

    # Instantiate engine
    engine_chess = Engine(
        pgn=pgn,
        llm_side=BoardSide.BLACK,
        llm=OpenAILLM(api_key=api_key))
    
    # Get move response from LLM
    move = engine_chess.get_chess_move_response()
    return move

if __name__ == '__main__':
    app.run(debug=True)

