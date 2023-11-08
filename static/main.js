var board, game = new Chess();
var movesWhite = [];

window.onload = function() {
  document.getElementById("white moves").innerHTML = movesWhite.join(", ");
}

function onSnapPiece() {
  board.position(game.fen());
}

function illegalMove(move) {
  if (move === null) {
    return 'snapback';
  }
}

function movePiece(source, target, newPiece) {
  var move = game.move({
    from: source,
    to: target,
    promotion: newPiece
  });
  illegalMove(move);
}

function promotionPieceSelected(id, piece, source, target) {

  document.getElementById(id).addEventListener('click', function() {
    movePiece(source, target, piece);
    document.getElementById('promotion').classList.add('hide');
    board.position(game.fen());
  });
}

function onDropPiece(source, target) {
  var piece = game.get(source);

  if (piece.type === 'p' && (target[1] === '8' || target[1] === '1')) {
      document.getElementById('promotion').classList.remove('hide');
      document.getElementById('promotion').classList.add('show');

      promotionPieceSelected('queen', 'q', source, target);
      promotionPieceSelected('rook', 'r', source, target);
      promotionPieceSelected('bishop', 'b', source, target);
      promotionPieceSelected('knight', 'n', source, target);
  } else {
    movePiece(source, target, 'q');
  }

  if (game.turn() === 'b') {
    if (piece.type === 'p') {
      var pieceAdd = target
    } else {
      var pieceAdd = piece.type.toUpperCase().concat(target)
    }
    movesWhite.push(pieceAdd);
    document.getElementById("white moves").innerHTML = movesWhite.join(", ");
  }
}

function onDragPiece (source, piece, position, orientation) {
  if (game.game_over()) {
    return false
  };

  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  };
}

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