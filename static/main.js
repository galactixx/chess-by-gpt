var board, game = new Chess();

function generateChessBoard() {
  board = ChessBoard('board', {
    draggable: true,
    position: 'start'
  });
};

function addWhiteMove() {
  
}

setTimeout(generateChessBoard, 1);