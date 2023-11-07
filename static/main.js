var board, game = new Chess();

function handlePromotion(target, piece) {
  var newPiece = prompt('Promotion! Choose a piece (q, r, b, n)');
  game.put({type: newPiece, color: piece.color}, target);
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
  illegalMove(move)
}

function onDropPiece(source, target) {
  var piece = game.get(source);
  if (piece.type === 'p' && (target[1] === '8' || target[1] === '1')) {
    var newPiece = prompt('Promotion! Choose a piece (q, r, b, n)');
    movePiece(source, target, newPiece);
  } else {
    movePiece(source, target, 'q');
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