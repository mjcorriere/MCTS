__author__ = 'Markus'


class QuoridorGameState(object):

    def __init__(self, size=9):

        assert size % 2 == 1

        self.EMPTY_WALL = 0

        self.H1 = 1
        self.V1 = 2
        self.H2 = 4
        self.V2 = 8

        self.HBORDER = 42
        self.VBORDER = 43

        self.horizontalWalls = [self.H1, self.H2, self.HBORDER]
        self.verticalWalls = [self.V1, self.V2, self.VBORDER]

        # A board will be size x size cells square
        self.boardSize = size

        # The number of vertices per side
        self.vertexSize = self.boardSize + 1

        # The number of vertices in on the board
        self.numVertexes = self.vertexSize ** 2

        # Walls will be stored at the vertices. Horizontal and vertical edges
        # are kept separately to simplify the representation
        self.walls = [self.EMPTY_WALL] * self.numVertexes

        # Add walls to the rim of the board. This is useful to simplify finding
        # legal moves. Moving off the edge is no longer a corner case.
        self.walls[:self.vertexSize] = [self.HBORDER] * self.vertexSize
        self.walls[-self.vertexSize:] = [self.HBORDER] * self.vertexSize
        for i in xrange(self.vertexSize, self.numVertexes - self.vertexSize,
                            self.vertexSize):
            self.walls[i] = self.VBORDER
            self.walls[i + self.boardSize] = self.VBORDER

        # Starting positions and starting number of walls to place
        p1 = self.boardSize / 2
        p2 = self.boardSize * self.boardSize - self.boardSize / 2
        self.playerPositions = [p1, p2]

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

    def getLegalMoves(self):
        # Moves can be:
        # Place horizontal wall at position P 'hP'
        # Place vertical wall at position P 'vP'
        # Move player in any of the 4 cardinal directions

        wallMoves = []
        for i, w in enumerate(self.walls):
            neighbors = self._getVertexNeighboringVertices(i)

            vertexIsEmpty = w == self.EMPTY_WALL

        #     if vertexIsEmpty and eastNeighborIsEmpty and westNeighborIsEmpty:
        #         wallMoves.extend(['h' + str(i), 'v' + str(i)])

        # Determine pawn moves
        pawnMoves = []

        pawnPosition = self.playerPositions[self.currentPlayer - 1]
        NW, NE, SW, SE = self._getCellNeighboringVertices(pawnPosition)

        canMoveNorth = self.walls[NW] not in self.horizontalWalls and \
                        self.walls[NE] not in self.horizontalWalls
        canMoveSouth = self.walls[SW] not in self.horizontalWalls and \
                        self.walls[SE] not in self.horizontalWalls
        canMoveWest = self.walls[NW] not in self.verticalWalls and \
                        self.walls[SW] not in self.verticalWalls
        canMoveEast = self.walls[NE] not in self.verticalWalls and \
                        self.walls[SE] not in self.verticalWalls

        if canMoveNorth: pawnMoves.append('N')
        if canMoveSouth: pawnMoves.append('S')
        if canMoveWest: pawnMoves.append('W')
        if canMoveEast: pawnMoves.append('E')

        # TODO: Add the logic for jumping over players
        # Currently, players will be able to occupy the same spot

        # TODO: Add logic for determining if a wall blocks a player from goal
        # Use algorithm for determining percolation

        return wallMoves + pawnMoves

    def executeMove(self, move):
        assert self.winner is None

        if move in 'NSEW':
            self.playerPositions[self.currentPlayer - 1] += self.distance[move]
        elif move[0] == 'h':
            pass
        elif move[0] == 'v':
            pass
        else:
            raise Exception("Invalid Move: ", str(move))

        self.checkForWin()
        self.currentPlayer = 3 - self.currentPlayer

    def checkForWin(self):
        p1, p2 = self.playerPositions[0], self.playerPositions[1]
        if p1 < self.boardSize:
            self.winner = p1
        elif p2 >= self.boardSize**2 - self.boardSize:
            self.winner = p2

    def _getVertexNeighboringVertices(self, vertex):

        north = vertex - self.vertexSize
        south = vertex + self.vertexSize
        east = vertex + 1
        west = vertex - 1

        # North and south are valid so long as they are within the board
        northValid = north >= 0
        southValid = south < self.numVertexes

        # East and west are valid so long as they are in the same row as vertex
        # and within the board
        eastValid = vertex / self.vertexSize == east / self.vertexSize \
                        and east < self.numVertexes
        westValid = vertex / self.vertexSize == west / self.vertexSize \
                        and west >= 0

        directions = (north, south, east, west)
        validMap = (northValid, southValid, eastValid, westValid)

        neighbors = [directions[i] if valid is True else None
                        for i, valid in enumerate(validMap)]

        return neighbors

    def _getCellNeighboringVertices(self, pos):

        row = pos / self.boardSize

        NW = pos + row
        NE = NW + 1
        SW = NW + self.vertexSize
        SE = SW + 1

        return NW, NE, SW, SE


def main():

    q = QuoridorGameState()
    print q.getLegalMoves()
    print q._getVertexNeighboringVertices(0)

    for i in xrange(0, len(q.walls), q.vertexSize):
        print str(i) + '-' + str(i+q.vertexSize) + ': ' + \
              ' '.join(map(str, q.walls)[i:i+q.vertexSize])


if __name__ == '__main__':
    main()
