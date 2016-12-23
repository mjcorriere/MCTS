import time

import mcts
import quoridor

def playMCTSgame():

    q = quoridor.QuoridorGameState()
    root = mcts.MCTSNode(q)
    node = root

    while q.winner is None:
        start = time.clock()
        move = mcts.mcts(node, 10000)
        end = time.clock()
        print "Move time: " , str(end - start)
        q.executeMove(move)
        node = mcts.MCTSNode(q)

        print "Player", str(3 % q.currentPlayer), "Move:", move
        print q

    print "Winner is player", q.winner

if __name__ == "__main__":
    playMCTSgame()


