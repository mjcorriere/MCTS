
import mcts
import connectfour

def playMCTSgame():

    cf = connectfour.ConnectFourGameState()
    root = mcts.MCTSNode(cf)
    node = root

    while cf.winner is None:
        move = mcts.mcts(node, 20000)
        cf.executeMove(move)
        node = mcts.MCTSNode(cf)
        print cf
        print "Move:", move

    print "Winner is player", cf.winner

def playAgainstMCTS():
    cf = connectfour.ConnectFourGameState()
    print cf

    while True:

        move = int(input("Make your move: "))
        cf.executeMove(move)

        if cf.winner is not None:
            break

        node = mcts.MCTSNode(cf)
        computerMove = mcts.mcts(node, 10000)
        cf.executeMove(computerMove)
        print cf

        if cf.winner is not None:
            break

    print cf
    print "Player", cf.winner, "wins"

if __name__ == "__main__":

    playMCTSgame()
    #playAgainstMCTS()

