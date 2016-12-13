__author__ = 'Markus'


class WallType():
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    HORIZONTAL = 4
    VERTICAL = 8


class QuoridorGameState(object):

    def __init__(self):

        # A board will be size x size cells square. Must be odd.
        self.boardSize = 9

        # Sanity check on board size.
        assert self.boardSize % 2 == 1

        # The number of vertices per side
        self.vertexSize = self.boardSize + 1

        # The number of vertices in on the board
        self.numVertexes = self.vertexSize ** 2

        # Walls will be stored at the vertices. Horizontal and vertical edges
        # are kept separately to simplify the representation
        self.walls = [WallType.EMPTY] * self.numVertexes

        # Add walls to the rim of the board. This is useful to simplify finding
        # legal moves. Moving off the edge is no longer a corner case.
        self.walls[:self.vertexSize] = [WallType.HORIZONTAL] * self.vertexSize
        self.walls[-self.vertexSize:] = [WallType.HORIZONTAL] * self.vertexSize

        for i in xrange(self.vertexSize, self.numVertexes - self.vertexSize,
                            self.vertexSize):
            self.walls[i] = WallType.VERTICAL
            self.walls[i + self.boardSize] = WallType.VERTICAL

        # A list of only the non-rim wall locations, for convenience
        self.nonRimWalls = []
        for v in xrange(self.numVertexes):
            row = v / self.vertexSize
            col = v % self.vertexSize
            if row > 0 and col > 0 and row < self.vertexSize - 1 \
                and col < self.vertexSize - 1:
                self.nonRimWalls.append(v)

        # Starting positions and starting number of walls to place
        player1Start = self.boardSize / 2
        player2Start = self.boardSize * self.boardSize - self.boardSize / 2
        self.playerPositions = [player1Start, player2Start]

        self.numPlayerWalls = [10, 10]

        self.currentPlayer = 1
        self.winner = None

        # The movement map
        self.distance = {
            'N': -self.boardSize,
            'S': self.boardSize,
            'E': 1,
            'W': -1
        }

    def copy(self):
        q = QuoridorGameState()
        q.walls = list(self.walls)
        q.playerPositions = list(self.playerPositions)
        q.numPlayerWalls = list(self.numPlayerWalls)
        q.currentPlayer = self.currentPlayer
        q.winner = self.winner

        return q

    def getLegalMoves(self):
        # Moves can be:
        # Place horizontal wall at position P 'hP'
        # Place vertical wall at position P 'vP'
        # Move player in any of the 4 cardinal directions 'N', 'S', 'E', 'W'

        wallMoves = []
        for v in self.nonRimWalls:
            # There will always be N, S, E, W neighbors since we are only
            # sampling the non-rim walls in the board
            N, S, E, W = self._getVertexNeighboringVertices(v)

            # I can place a vertical wall here if it is empty and there are no
            # vertical walls above or below me
            if not self.walls[N] & WallType.VERTICAL and \
                not self.walls[S] & WallType.VERTICAL and \
                    self.walls[v] == WallType.EMPTY:
                wallMoves.append('v' + str(v))

            # I can place a horizontal wall here if it is empty and there are
            # no horizontal walls to the left or right of me
            if not self.walls[E] & WallType.HORIZONTAL and \
                not self.walls[W] & WallType.HORIZONTAL and \
                    self.walls[v] == WallType.EMPTY:
                wallMoves.append('h' + str(v))

        # Determine pawn moves

        pawnPosition = self.playerPositions[self.currentPlayer - 1]
        NW, NE, SW, SE = self._getCellNeighboringVertices(pawnPosition)

        canMoveNorth = not self.walls[NW] & WallType.HORIZONTAL and \
                        not self.walls[NE] & WallType.HORIZONTAL
        canMoveSouth = not self.walls[SW] & WallType.HORIZONTAL and \
                        not self.walls[SE] & WallType.HORIZONTAL
        canMoveEast = not self.walls[NE] & WallType.VERTICAL and \
                        not self.walls[SE] & WallType.VERTICAL
        canMoveWest = not self.walls[NW] & WallType.VERTICAL and \
                        not self.walls[SW] & WallType.VERTICAL

        pawnMoves = [d for d, canMove in zip('NSEW',
                                             [canMoveNorth, canMoveSouth,
                                              canMoveEast, canMoveWest])
                     if canMove]

        # TODO: Add the logic for jumping over players
        # Currently, players will be able to occupy the same spot

        # TODO: Add logic for determining if a wall blocks a player from goal
        # Use algorithm for determining percolation

        return wallMoves + pawnMoves

    def executeMove(self, move):

        # NOTE: The right thing to to is ensure the move is in the set of
        # legal moves given by self.getLegalMoves(). However, for simulation
        # speed, this method assumes the caller is playing by the rules.

        assert self.winner is None

        if move in 'NSEW':
            self.playerPositions[self.currentPlayer - 1] += self.distance[move]
        elif move[0] == 'h':
            position = int(move[1:])
            self.walls[position] = self.currentPlayer + WallType.HORIZONTAL
            self.numPlayerWalls[self.currentPlayer - 1] -= 1
        elif move[0] == 'v':
            position = int(move[1:])
            self.walls[position] = self.currentPlayer + WallType.VERTICAL
            self.numPlayerWalls[self.currentPlayer - 1] -= 1
        else:
            raise Exception("Invalid Move: ", str(move))

        self.checkForWin()
        self.currentPlayer = 3 - self.currentPlayer

    def checkForWin(self):
        p1, p2 = self.playerPositions[0], self.playerPositions[1]
        if p1 >= self.boardSize**2 - self.boardSize:
            self.winner = 1
        elif p2 < self.boardSize:
            self.winner = 2

    def _getVertexNeighboringVertices(self, vertex):
        """
        Returns a tuple of vertices that are cardinal neighbors of the given
        vertex. The vertex must be a non-rim vertex. In this way, neighbors
        are guaranteed to be within the board and in the same row, avoiding
        these boundary checks.

        The returned tuple contains the indices of the neighboring vertices,
        in the order of N, S, E, W from the perspective of the given vertex.
        """

        north = vertex - self.vertexSize
        south = vertex + self.vertexSize
        east = vertex + 1
        west = vertex - 1

        # Sanity checks
        assert north >= 0
        assert west >= 0
        assert east < self.numVertexes
        assert south < self.numVertexes

        return north, south, east, west

    def _getCellNeighboringVertices(self, cell):
        """
        Returns a tuple of vertices that are neighbors of the given cell.
        Cell vertex neighbors are the corners of the square cell.

        The returned tuple contains the indices of the neighboring vertices in
        the order of NW, NE, SW, SE from the perspective of the given cell.
        """

        row = cell / self.boardSize

        NW = cell + row
        NE = NW + 1
        SW = NW + self.vertexSize
        SE = SW + 1

        return NW, NE, SW, SE


def testHorizontalWallPlacement():

    q = QuoridorGameState()
    q.executeMove('h11')
    legalMoves = q.getLegalMoves()

    # Test that it and its neighbor are no longer valid moves
    assert 'h11' not in legalMoves
    assert 'h12' not in legalMoves

    # Test that a vertical wall can't be placed in the same spot
    assert 'v11' not in legalMoves

    # Test that a vertical wall can be placed below it
    assert 'v21' in legalMoves

def main():

    testHorizontalWallPlacement()

    q = QuoridorGameState()
    print q.getLegalMoves()
    for i in xrange(0, len(q.walls), q.vertexSize):
        print str(i) + '-' + str(i+q.vertexSize) + ': ' + \
              ' '.join(map(str, q.walls)[i:i+q.vertexSize])

if __name__ == '__main__':
    main()
