
class TicTacToeGameState(object):

    def __init__(self):
        self.currentPlayer = 1
        self.board = [0] * 9
        self.winner = None

    def copy(self):
        gamestate = TicTacToeGameState()
        gamestate.board = list(self.board)
        gamestate.currentPlayer = self.currentPlayer
        gamestate.winner = self.winner

        return gamestate

    def executeMove(self, move):
        assert self.winner is None

        self.board[move] = self.currentPlayer
        self.currentPlayer = 3 - self.currentPlayer
        self.checkForWin()

    def getLegalMoves(self):
        return filter(lambda x: self.board[x] == 0, xrange(len(self.board)))

    def checkForWin(self):

        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Horizontals
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Verticals
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]

        for (i, j, k) in wins:
            if self.board[i] == self.board[j] == self.board[k]:
                if self.board[i] != 0:
                    self.winner = self.board[i]

        if self.winner is None and self.getLegalMoves() == []:
            self.winner = 0

    def __repr__(self):
        icons = ['-', 'x', 'o']
        iconBoard = [icons[i] for i in self.board]
        for i in (9, 6, 3):
            iconBoard.insert(i, "\n")
        return ''.join(iconBoard)