var board, game = new Chess();

var movesNumber = [];
var movesWhite = [];
var movesBlack = [];

var pieceToAbb = { 'queen': 'q', 'rook': 'r', 'bishop': 'b', 'knight': 'n' };

function appendWhiteMoves() {
  appendMoves('white-moves', movesWhite);
}

function appendBlackMoves() {
  appendMoves('black-moves', movesBlack);
}

function appendMoveNumber() {
  appendMoves('move-number', movesNumber);
}

// logic to determine game winner
function gameWinner() {
  let winner = (game.turn() === 'w') ? "Black" : "White";
  return winner
}

// logic for resign button
function resignButton() {
  let winner = gameWinner();
  let resigner = (winner === 'White') ? "Black": "White";
  gameOverModal(`${resigner} resigns! ${winner} has won the game.`);
}

// when game is reset
function newGame() {
  game.reset();
  board.start();
  movesWhite = [];
  movesBlack = [];
  movesNumber = [];
  appendWhiteMoves();
  appendBlackMoves();
  appendMoveNumber();
}

// actions to execute when game is over
function gameOverModal(text) {
  document.getElementById('gameOverText').innerHTML = text;
  document.getElementById('gameOverDialog').showModal();

  document.getElementById('gameOverButton').addEventListener('click', function() {
    document.getElementById('gameOverDialog').close();
    newGame();
  })

}

// retrieve move from LLM
function getLLMMove() {
    var url = "/move?pgn=" + encodeURIComponent(game.pgn());
    $.get(url, function(data) {
      var source = data.substring(0, 2).trim();
      var target = data.substring(2).trim();
      var piece = game.get(source);
      movePiece(source, target, piece);
      setTimeout(function(){ board.position(game.fen()); }, 100);
    });
}

// append to move list and insert into html notation section
function appendMoves(id, moveList) {
  var listHTML = "<ul>";

  for (var i=0; i<moveList.length; i++) {
    listHTML += "<li>" + moveList[i] + "</li>";
  }
  listHTML += "</ul>";
  document.getElementById(id).innerHTML = listHTML;
}

// when piece is snapped
function onSnapPiece() {
  board.position(game.fen());
}

// all illegal moves
function illegalMove(move) {
  if (move === null) {
    return 'snapback';
  }
}

// parsing of correct notation
function chessNotation(piece, newPiece, move, source, target, doPromotion) {
  var pieceAdd = null;

  // notation for capture or not
  if (piece.type == 'p' && move.flags.includes('c')) {
    pieceAdd = source[0].concat('x').concat(target);
  } else if (piece.type === 'p') {
    pieceAdd = target;
  } else if (move.flags.includes('c')) {
    pieceAdd = piece.type.toUpperCase().concat('x').concat(target);
  } else {
    pieceAdd = piece.type.toUpperCase().concat(target);
  }
  
  // notation for castling
  if (move.flags.includes('k')) {
    pieceAdd = 'O-O';
  } else if (move.flags.includes('q')) {
    pieceAdd = 'O-O-O';
  }

  // notation if promotion ocurred
  if (doPromotion) {
    pieceAdd = pieceAdd.concat(`=${newPiece.toUpperCase()}`);
  }

  // notation for check or checkmate
  if (game.in_checkmate()) {
    pieceAdd = pieceAdd.concat('#');
  } else if (game.in_check()) {
    pieceAdd = pieceAdd.concat('+');
  }
  return pieceAdd;
}


// logic to move a piece and record notation
function movePieceLogic(source, target, piece, newPiece, doPromotion) {
  var move = game.move({
    from: source,
    to: target,
    promotion: newPiece
  });
  illegalMove(move);

  // parsing of correct notation
  if (move != null) {
    pieceAdd = chessNotation(piece, newPiece, move, source, target, doPromotion);

    // update white and black moves in variable in html notation
    if (game.turn() === 'b') {
      movesWhite.push(pieceAdd);
      appendWhiteMoves();

      // update move number in html
      movesNumber.push(movesWhite.length);
      appendMoveNumber();
    } else {
      movesBlack.push(pieceAdd);
      appendBlackMoves();
    }

    // automatic scroll down
    var movesDiv = document.getElementById("moves");
    movesDiv.scrollTop = movesDiv.scrollHeight;
  }
}

// logic when moving a piece
function movePiece(source, target, piece) {
  var doPromotion = false;
  
  if (piece.type === 'p' && (target[1] === '8' || target[1] === '1') &&
     (source[1] === '7' || source[1] === '2')) {
    doPromotion = true;

    if (game.turn() === 'b') {
      if (target.length === 3) {
        var promotionPiece = target.substring(2);
        target = target.substring(0, 2);
        movePieceLogic(source, target, piece, promotionPiece, doPromotion);
      } else {
      movePieceLogic(source, target, piece, 'q', doPromotion);
      }
    } else {

      // show promotion piece options
      document.getElementById('promotionDialog').showModal();

      // iterate through all possible promotion options
      Object.entries(pieceToAbb).forEach(function(tuple) {
        var pieceSelection = tuple[0];
        var abbreviation = tuple[1];
        promotionPieceSelected(pieceSelection, piece, abbreviation, source, target);
      });

    }
  } else {
    movePieceLogic(source, target, piece, 'q', doPromotion);
  }

  // checkmate
  if (game.in_checkmate()) {
    let winner = gameWinner();
    gameOverModal(`Checkmate! ${winner} has won the game.`);
  }

  // threefold repetition
  else if (game.in_threefold_repetition()) {
    gameOverModal('Threefold repetition! It is a draw.');
  }

  // stalemate
  else if (game.in_draw()) {
    gameOverModal('Stalemate! It is a draw.');
  }

}

// logic for promoting a piece and selecting one
function promotionPieceSelected(id, piece, newPiece, source, target) {

  document.getElementById(id).addEventListener('click', function() {
    movePieceLogic(source, target, piece, newPiece, true);
    document.getElementById('promotionDialog').close();
    board.position(game.fen());
  });
}

// after piece is dropped
function onDropPiece(source, target) {
  var piece = game.get(source);
  movePiece(source, target, piece);
  getLLMMove();
}

// when piece is initially dragged to target
function onDragPiece (source, piece, position, orientation) {
  if (game.game_over()) {
    return false;
  };

  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (piece.search(/^b/) !== -1)) {
    return false;
  };
}

// generate base chess board
function generateChessBoard() {
  board = ChessBoard('board', {
    draggable: true,
    position: 'start',
    onDrop: onDropPiece,
    onDragStart: onDragPiece,
    onSnapEnd: onSnapPiece
  });
}

setTimeout(generateChessBoard, 1);

// ignore all interactions with escape button
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
  }
});

window.addEventListener('resize', function() {
  board.resize();
});