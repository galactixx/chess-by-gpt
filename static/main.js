var board, game = new Chess();

var movesWhite = [];
var movesBlack = [];

function appendMoves(id, moveList) {
  var listHTML = "<ul>";

  for (var i=0; i<moveList.length; i++) {
    listHTML += "<li>" + moveList[i] + "</li>";
  }
  listHTML += "</ul>";
  document.getElementById(id).innerHTML = listHTML;
}

function onSnapPiece() {
  board.position(game.fen());
}

function illegalMove(move) {
  if (move === null) {
    return 'snapback';
  }
}

function movePiece(source, target, piece, newPiece) {
  var move = game.move({
    from: source,
    to: target,
    promotion: newPiece
  });
  illegalMove(move);

  if (move != null) {
    if (piece.type == 'p' && move.flags.includes('c')) {
      var pieceAdd = source[0].concat('x').concat(target);
    } else if (piece.type === 'p') {
      var pieceAdd = target;
    } else if (move.flags.includes('c')) {
      var pieceAdd = piece.type.toUpperCase().concat('x').concat(target);
    } else {
      var pieceAdd = piece.type.toUpperCase().concat(target);
    }
  if (game.in_check()) {
    pieceAdd = pieceAdd.concat('+')
  }

    if (game.turn() === 'b') {
      movesWhite.push(pieceAdd);
      appendMoves('white-moves', movesWhite);
    } else {
      movesBlack.push(pieceAdd);
      appendMoves('black-moves', movesBlack);
    }
  }
}

function promotionPieceSelected(id, piece, piece_promotion, source, target) {

  document.getElementById(id).addEventListener('click', function() {
    movePiece(source, target, piece, piece_promotion);
    document.getElementById('promotion').classList.add('hide');
    board.position(game.fen());
  });
}

function onDropPiece(source, target) {
  var piece = game.get(source);

  if (piece.type === 'p' && (target[1] === '8' || target[1] === '1')) {
      document.getElementById('promotion').classList.remove('hide');
      document.getElementById('promotion').classList.add('show');

      promotionPieceSelected('queen', piece, 'q', source, target);
      promotionPieceSelected('rook', piece, 'r', source, target);
      promotionPieceSelected('bishop', piece, 'b', source, target);
      promotionPieceSelected('knight', piece, 'n', source, target);
  } else {
    movePiece(source, target, piece, 'q');
  }
}

function onDragPiece (source, piece, position, orientation) {
  if (game.game_over()) {
    return false;
  };

  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
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