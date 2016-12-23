__author__ = 'MQC1472'
from math import sqrt, log
import random
import time

class MCTSNode(object):

    def __init__(self, gamestate, parent = None, move = None):
        self.gamestate = gamestate
        self.parent = parent
        self.move = move
        self.visits = 0
        self.value = 0
        self.children = []

        self.frontier = self.gamestate.getLegalMoves()
        random.shuffle(self.frontier)

    def isFullyExpanded(self):
        return self.frontier == []

    def selectBestChild(self):
        assert self.children != []
        return max(self.children, key=self.uct)

    def selectBestMove(self):
        bestChild = max(self.children,
                   key=lambda child: float(child.value) / float(child.visits))
        print "Best Child Value: ", str(bestChild.value)
        print "Best Child Visits: ", str(bestChild.visits)
        return bestChild.move

    def isTerminal(self):
        return self.gamestate.winner is not None

    def expand(self):
        assert self.frontier != []
        randomMove = self.frontier.pop()
        newGameState = self.gamestate.copy()
        newGameState.executeMove(randomMove)
        newNode = MCTSNode(newGameState, self, randomMove)
        self.children.append(newNode)

        return newNode

    def uct(self, node):
        w = float(node.value)
        n = float(node.visits)
        C = sqrt(2)
        N = float(self.visits)

        uct = w / n + C * sqrt(log(N) / n)

        return uct

def select(node):

    if node.isTerminal():
        return node
    elif node.isFullyExpanded():
        return select(node.selectBestChild())
    else:
        return node.expand()

def simulate(node):

    # TODO: Make this section more clear. 'currentplayer' is confusing
    # TODO: and reward values are confusing
    # Since the gamestate auto-increments the current player, we should
    # be evaluating the reward from the PREVIOUS players perspective.
    # We want to evaluate the reward from the perspective of the player
    # WHO JUST MOVED, not the player about to move.

    gamestate = node.gamestate.copy()
    currentPlayer = gamestate.currentPlayer

    simulatedMoves = 0

    while gamestate.winner is None:
        start = time.clock()
        legalMoves = gamestate.getLegalMoves()
        end = time.clock()
        # print "Legal Move Time: ", str(end - start)
        move = random.choice(legalMoves)
        gamestate.executeMove(move)
        simulatedMoves += 1

    # print "Simulated moves played: ", str(simulatedMoves)

    if gamestate.winner == 0:
        reward = 0
    elif gamestate.winner == 1 and currentPlayer == 1:
        reward = -1
    elif gamestate.winner == 2 and currentPlayer == 2:
        reward = -1
    else:
        reward = 1

    return reward

def backpropagate(node, reward):

    node.visits += 1
    node.value += reward

    if node.parent:
        backpropagate(node.parent, -reward)

def mcts(root, iterations):

    i = 0

    while i < iterations:
        # print 'Iteration: ', str(i)

        start = time.clock()
        node = select(root)
        end = time.clock()
        # print "Selection time: ", str(end - start)

        start = time.clock()
        reward = simulate(node)
        end = time.clock()
        # print "Simulation time: ", str(end - start)

        start = time.clock()
        backpropagate(node, reward)
        end = time.clock()
        # print "Backprop time: ", str(end - start)

        i += 1

    best_move = root.selectBestMove()

    return best_move