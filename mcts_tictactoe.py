__author__ = 'MQC1472'

import mcts
import tictactoe

def playMCTSgame():

    ttt = tictactoe.TicTacToeGameState()
    root = mcts.MCTSNode(ttt)
    node = root
    while ttt.winner is None:
        move = mcts.mcts(node, 10000)
        ttt.executeMove(move)
        node = mcts.MCTSNode(ttt)
        print ttt

def playAgainstMCTS():
    ttt = tictactoe.TicTacToeGameState()
    print ttt

    while True:

        move = int(input("Make your move: "))
        ttt.executeMove(move)

        if ttt.winner is not None:
            break

        node = mcts.MCTSNode(ttt)
        computerMove = mcts.mcts(node, 10000)
        ttt.executeMove(computerMove)
        print ttt

        if ttt.winner is not None:
            break

    print ttt
    print "Player", ttt.winner, "wins"

if __name__ == "__main__":

    #playAgainstMCTS()
    playMCTSgame()