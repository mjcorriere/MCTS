__author__ = 'Mark'

import random

class ConnectFourGameState(object):

    def __init__(self, width=7, height=6):
        self.currentPlayer = 1
        self.board = [[0] * width for _ in xrange(height)]
        self.width = width
        self.height = height
        self.winner = None

    def copy(self):
        gamestate = ConnectFourGameState()
        gamestate.board = [list(row) for row in self.board]
        gamestate.currentPlayer = self.currentPlayer
        gamestate.winner = self.winner

        return gamestate

    def executeMove(self, move):
        assert self.winner is None
        column = [row[move] for row in self.board]

        r = self.height - 1

        for i, c in enumerate(column):
            if c != 0:
                r = i - 1
                break

        self.board[r][move] = self.currentPlayer
        self.checkForWin(r, move, self.currentPlayer)
        self.currentPlayer = 3 - self.currentPlayer


    def getLegalMoves(self):

        first_row = self.board[0]
        legalMoves = [i for i, v in enumerate(first_row) if v == 0]

        return legalMoves


    def checkForWin(self, _r, _c, player):

        rmin = self._clamp(_r - 3, 0, self.height)
        rmax = self._clamp(_r + 3, 0, self.height - 1)
        cmin = self._clamp(_c - 3, 0, self.width)
        cmax = self._clamp(_c + 3, 0, self.width - 1)
        # Check only cells adjacent to the last played move

        row = self.board[_r]
        col = [_row[_c] for _row in self.board]

        count = 0
        for c in xrange(cmin, cmax + 1):
            if row[c] == player:
                count += 1
            else:
                count = 0

            if count == 4:
                self.winner = player

        count = 0
        for r in xrange(rmin, rmax + 1):
            if col[r] == player:
                count += 1
            else:
                count = 0

            if count == 4:
                self.winner = player

        count = 0
        for r, c in zip(xrange(rmax, rmin - 1, -1), xrange(cmin, cmax + 1)):
            if self.board[r][c] == player:
                count += 1
            else:
                count = 0

            if count == 4:
                self.winner = player

        count = 0
        for r, c in zip(xrange(rmin, rmax + 1), xrange(cmin, cmax + 1)):
            if self.board[r][c] == player:
                count += 1
            else:
                count = 0

            if count == 4:
                self.winner = player

        # If the top row has no empty slots, its a draw
        if 0 not in self.board[0]:
            self.winner = 0


    def _clamp(self, value, minimum, maximum):
        return max(minimum, min(value, maximum))


    def __repr__(self):
        out = []
        icons = ['-', 'x', 'o']
        iconBoard = [[icons[c] for c in row] for row in self.board]

        for row in iconBoard:
            row.append("\n")
            out.append(''.join(row))

        return ''.join(out)


def playRandomMoves(num_moves = 10):
    moves = [random.randint(0, 6) for _ in xrange(num_moves)]

    for move in moves:
        cf.executeMove(move)

if __name__ == "__main__":
    cf = ConnectFourGameState()
    #playRandomMoves()
    cf.executeMove(3)
    cf.executeMove(4)
    cf.executeMove(4)
    cf.executeMove(5)
    cf.executeMove(5)
    cf.executeMove(6)
    cf.executeMove(5)
    cf.executeMove(6)
    cf.executeMove(6)
    cf.executeMove(0)
    cf.executeMove(6)


    print cf
    print cf.getLegalMoves()



