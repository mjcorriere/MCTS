__author__ = 'Mark'


class QuoridorGameState(object):

    def __init__(self, size=9):

        assert size % 2 == 1
        self.size = size
        self.horizontalEdges = [0] * (size * size)
        self.verticalEdges = [0] * (size * size)

        # Add walls to the rim of the board
        self.horizontalEdges[:size] = [3] * size
        self.horizontalEdges[-size:] = [3] * size
        self.verticalEdges[:size] = [3] * size
        self.verticalEdges[-size:] = [3] * size

        p1 = size / 2
        p2 = size * size - size / 2
        self.playerPositions = [p1, p2]
        self.numPlayerWalls = [size + 1, size + 1]

        self.currentPlayer = 1

        self.winner = None

        self.distance = {
            'N': -self.size,
            'S': self.size,
            'E': 1,
            'W': -1
        }

    def getLegalMoves(self):
        # Moves can be:
        # Place horizontal wall at position P 'hP'
        # Place vertical wall at position P 'vP'
        # Move player in any of the 4 cardinal directions

        pos = self.playerPositions[self.currentPlayer - 1]

        # Get horizontal + vertical moves
        h = ['h' + str(i) for i, p in
                enumerate(self.horizontalEdges) if p == 0]
        v = ['v' + str(i) for i, p in
                enumerate(self.verticalEdges) if p == 0]

        # Get player moves
        # N, S, E, W
        verticalNeighbors, horizontalNeighbors = self._getNeighboringEdges(pos)

        p = []

        if self.horizontalEdges[horizontalNeighbors[0]] == 0:
            p.append('N')
        if self.horizontalEdges[horizontalNeighbors[1]] == 0:
            p.append('S')
        if self.verticalEdges[verticalNeighbors[0]] == 0:
            p.append('W')
        if self.verticalEdges[verticalNeighbors[1]] == 0:
            p.append('E')

        # TODO: Add the logic for jumping over players
        # Currently, players will be able to occupy the same spot

        # TODO: Add logic for determining if a wall blocks a player from goal
        # Use algorithm for determining percolation

        return h + v + p

    def executeMove(self, move):
        assert self.winner is None

        if move in 'NSEW':
            self.playerPositions[self.currentPlayer - 1] += self.distance[move]

        elif move[0] == 'h':
            if self.numPlayerWalls[self.currentPlayer - 1] > 0:
                pos = int(move[1:])
                self.horizontalEdges[pos] = self.currentPlayer
                self.numPlayerWalls[self.currentPlayer - 1] -= 1

        elif move[0] == 'v':
            if self.numPlayerWalls[self.currentPlayer - 1] > 0:
                pos = int(move[1:])
                self.verticalEdges[pos] = self.currentPlayer
                self.numPlayerWalls[self.currentPlayer - 1] -= 1

        else:
            raise Exception("Invalid Move: ", str(move))

        self.checkForWin()
        self.currentPlayer = 3 - self.currentPlayer

    def checkForWin(self):
        p1, p2 = self.playerPositions[0], self.playerPositions[1]
        if p1 < self.size:
            self.winner = p1
        elif p2 >= self.size**2 - self.size:
            self.winner = p2

    def _getNeighboringEdges(self, pos):

        row = pos / self.size
        col = pos - self.size * row

        L = pos / self.size + self.size * col
        R = L + self.size
        U = pos
        D = U + self.size

        v = (L, R)
        h = (U, D)

        return v, h


def main():
    q = QuoridorGameState()

    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')
    q.executeMove('W')

    print "Player: ", q.currentPlayer
    print "Position: ", q.playerPositions[0]
    print q.getLegalMoves()
if __name__ == '__main__':
    main()