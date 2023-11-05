var board, game = new Chess();

function generateChessBoard() {
  board = ChessBoard('board', {
    draggable: true,
    position: 'start'
  });
};

setTimeout(generateChessBoard, 1);