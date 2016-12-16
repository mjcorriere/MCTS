
import mcts
import quoridor

def playMCTSgame():

    q = quoridor.QuoridorGameState()
    root = mcts.MCTSNode(q)
    node = root

    while q.winner is None:
        move = mcts.mcts(node, 1000)
        q.executeMove(move)
        node = mcts.MCTSNode(q)
        print "Move:", move
        print q

    print "Winner is player", q.winner

if __name__ == "__main__":
    playMCTSgame()


