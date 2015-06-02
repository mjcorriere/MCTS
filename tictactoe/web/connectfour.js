var WIDTH = 7;
var HEIGHT = 6;

function Gamestate() {
  //TODO: Make this dynamically created
  this.board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
  ];

  this.currentPlayer = 1;
  this.width = WIDTH;
  this.height = HEIGHT;
  this.winner = null;

}

Gamestate.prototype.executeMove = function(move) {
  var column = [];
  var row = -1;

  for (var r = 0; r < this.board.length; r++) {
    column.push(this.board[r][move]);
  }

  for (var r = column.length - 1; r >= 0; r--) {
    if (column[r] == 0) {
      row = r;
      break;
    }
  }

  if (row != -1) {
    this.board[row][move] = this.currentPlayer;
    this.checkForWin(row, move, this.currentPlayer);
    this.currentPlayer = 3 - this.currentPlayer;
  }

  return row;

}

Gamestate.prototype.getLegalMoves = function() {

  var first_row = this.board[0];
  var legalMoves = [];

  for (var i = 0; i < first_row.length; i++) {
    if (first_row[i] == 0) {
      legalMoves.push(i);
    }
  }

  return legalMoves;

}

Gamestate.prototype.checkForWin = function(_r, _c, player) {

  var rmin = clamp(_r - 3, 0, this.height);
  var rmax = clamp(_r + 3, 0, this.height - 1);
  var cmin = clamp(_c - 3, 0, this.width);
  var cmax = clamp(_c + 3, 0, this.width - 1);

  row = this.board[_r];
  var col = [];
  for (var r = 0; r < this.board.length; r++) {
    col.push(this.board[r][_c]);
  }

  // Check column for victory
  var count = 0;
  for (var c = cmin; c <= cmax; c++) {
    if (row[c] == player) {
      count += 1;
    } else {
      count = 0;
    }

    if (count == 4) {
      this.winner = player;
    }
  }

  // Check row for victory
  var count = 0;
  for (var r = rmin; r <= rmax; r++) {
    if (col[r] == player) {
      count += 1;
    } else {
      count = 0;
    }

    if (count == 4) {
      this.winner = player;
    }
  }

  // Check diagonal direction -> /
  var count = 0;
  var row_indicies = [];
  var col_indicies = [];

  for (var i = rmax; i >= rmin; i--) {
    row_indicies.push(i);
  }

  for (var i = cmin; i <= cmax; i++) {
    col_indicies.push(i);
  }

  var indicies = zip(row_indicies, col_indicies);

  for (var i = 0; i < indicies.length; i++) {
    var r = indicies[i][0];
    var c = indicies[i][1];

    if (this.board[r][c] == player) {
      count += 1;
    } else {
      count = 0;
    }

    if (count == 4) {
      this.winner = player;
    }

  }

  // Check diagonal direction -> \
  var count = 0;
  var row_indicies = [];
  var col_indicies = [];

  for (var i = rmin; i <= rmax; i++) {
    row_indicies.push(i);
  }

  for (var i = cmin; i <= cmax; i++) {
    col_indicies.push(i);
  }

  var indicies = zip(row_indicies, col_indicies);

  for (var i = 0; i < indicies.length; i++) {
    var r = indicies[i][0];
    var c = indicies[i][1];

    if (this.board[r][c] == player) {
      count += 1;
    } else {
      count = 0;
    }

    if (count == 4) {
      this.winner = player;
    }

  }

  // If the top row has no empty slots and we got here, its a draw
  if (this.board[0].indexOf(0) == -1) {
    this.winner = 0;
  }


}

Gamestate.prototype.copy = function() {

  var gameState = new Gamestate();
  for (var r = 0; r < this.board.length; r++) {
    gameState.board[r] = this.board[r].slice(0);
  }
  gameState.currentPlayer = this.currentPlayer;
  gameState.winner = this.winner;

  return gameState;

}
