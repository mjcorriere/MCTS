var mcts = mcts || {};

(function(mcts) {

  function MCTSNode(gamestate, parent, move) {
    this.gamestate = gamestate;
    this.parent = parent ? parent : null;
    this.move = move !== undefined ? move : null;
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

    var maxUct = this.uct(this.children[0]);
    var maxChildIndex = 0;

    for (var i = 1; i < this.children.length; i++) {
      var child = this.children[i];
      var uct = this.uct(child);

      if (uct > maxUct) {
        maxUct = uct;
        maxChildIndex = i;
      }

    }

    return this.children[maxChildIndex];

  };

  MCTSNode.prototype.selectBestMove = function () {

    var maxScore = this.children[0].value / this.children[0].visits;
    var bestChildIndex = 0;

    for (var i = 1; i < this.children.length; i++) {
      var child = this.children[i];
      var score = child.value / child.visits;

      if (score > maxScore) {
        maxScore = score;
        bestChildIndex = i;
      }

    }

    var bestChild = this.children[bestChildIndex];

    return bestChild.move;

  };

  MCTSNode.prototype.isTerminal = function () {
    return this.gamestate.winner !== null;
  };

  MCTSNode.prototype.expand = function () {
    var randomMove = this.frontier.pop();
    if (randomMove === null) {
      console.log('this is fucking stuid');
    }
    var newGameState = this.gamestate.copy();
    newGameState.executeMove(randomMove);
    var newNode = new MCTSNode(newGameState, this, randomMove);
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

  mcts.MCTSNode = MCTSNode;

  mcts.select = function(node) {

    if (node.isTerminal()) {
      return node;
    } else if (node.isFullyExpanded()) {
      return mcts.select(node.selectBestChild());
    } else {
      return node.expand();
    }
  }

  mcts.simulate = function(node) {

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

  mcts.backpropagate = function(node, reward) {
    node.visits += 1;
    node.value += reward;
    if (node.parent) {
      mcts.backpropagate(node.parent, -reward);
    }

  }

  mcts.mcts = function(root, iterations) {
    var i = 0;

    while (i < iterations) {
      var node = mcts.select(root);
      var reward = mcts.simulate(node);
      mcts.backpropagate(node, reward);
      i += 1;
    }

    var bestMove = root.selectBestMove();

    return bestMove;

  }

})(mcts);
