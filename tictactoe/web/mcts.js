function MCTSNode(gamestate, parent, move) {
  this.gamestate = gamestate;
  this.parent = parent ? parent : null;
  this.move = move ? move : null;
  this.visits = 0;
  this.value = 0;
  this.children = [];

  this.frontier = this.gamestate.getLegalMoves();
  this.frontier = shuffle(this.frontier);
}

MCTSNode.prototype.isFullyExpanded = function () {
  return this.frontier.length === 0;
};

MCTSNode.prototype.selectBestChild = function () {

  var uctValues = this.children.map(function(node) {
    return this.uct(node);
  });

  return max(uctValues);

};

MCTSNode.prototype.selectBestMove = function () {
  var bestChild;

  bestChild = max(this.children.map(function(child) {
    return child.value / child.visits;
  }));

  return bestChild.move;

};

MCTSNode.prototype.isTerminal = function () {
  return this.gamestate.winner !== null;
};

MCTSNode.prototype.expand = function () {
  var randomMove = this.frontier.pop();
  var newGameState = this.gamestate.copy();
  newGameState.executeMove(randomMove);
  var newNode = MCTSNode(newGameState, this, randomMove);
  this.children.push(newNode);

  return newNode;
};

MCTSNode.prototype.uct = function (node) {
  var w = node.value;
  var n = node.visits;
  var C = Math.sqrt(2);
  var N = this.visits;

  var uct = w / n + C * Math.sqrt(Math.log(N) / n);

  return uct;

};

function select(node) {
  if (node.isTerminal()) {
    return node;
  } else if (node.isFullyExpanded()) {
    return select(node.selectBestChild());
  } else {
    return node.expand();
  }
}

function simulate(node) {

  var reward;
  var gamestate = node.gamestate.copy();
  var currentPlayer = gamestate.currentPlayer;

  while (gamestate.winner === null) {
    var legalMoves = gamestate.getLegalMoves();
    var move = legalMoves[Math.floor(Math.random() * legalMoves.length)];
    gamestate.executeMove(move);

  }

  if (gamestate.winner === 0) {
    reward = 0;
  } else if (gamestate.winner === 1 && currentPlayer === 1) {
    reward = -1;
  } else if (gamestate.winner === 2 && currentPlayer === 2) {
    reward = -1;
  } else {
    reward = 1;
  }

  return reward;

}

function backpropagate(node, reward) {
  node.visits += 1;
  node.value += reward;
  if (node.parent) {
    backpropagate(node.parent, -reward);
  }

}

function mcts(root, iterations) {
  var i = 0;

  while (i < iterations) {
    var node = select(root);
    var reward = simulate(node);
    backpropagate(node, reward);
    i += 1;
  }

  var bestMove = root.selectBestMove();

  return bestMove;

}
