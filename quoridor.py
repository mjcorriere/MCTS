import time
import random
from collections import deque, OrderedDict

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
        self.numCells = self.boardSize**2

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

        # The movement map
        self.distance = OrderedDict([
            ('N', -self.boardSize),
            ('S', self.boardSize),
            ('E', 1),
            ('W', -1),
        ])

        # Static relationships about the board
        self._createCellVertexGraph()
        # TODO: self._createVertexVertexGraph()
        # TODO: self._createVertexCellGraph

        # Dynamic relationship about the board
        self._createCellGraph()

        # Starting positions and starting number of walls to place
        # Player 1 starts at center bottom, player 2 at center top
        player1Start = self.boardSize * self.boardSize - self.boardSize / 2 - 1
        player2Start = self.boardSize / 2
        self.playerPositions = [player1Start, player2Start]

        self.numPlayerWalls = [10, 10]

        self.currentPlayer = 1
        self.winner = None


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

        wallMoves = self._getValidWallMoves()
        # Determine pawn moves
        pawnPosition = self.playerPositions[self.currentPlayer - 1]
        pawnMoves = self._getValidPawnMoves(pawnPosition)

        # TODO: Add the logic for jumping over players
        # Currently, players will be able to occupy the same spot

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

            # Update the wall list and reduce the walls for that player
            self.walls[position] = self.currentPlayer + WallType.HORIZONTAL
            self.numPlayerWalls[self.currentPlayer - 1] -= 1

            # Remove the edges from the graph that have been blocked by the wall
            cellNeighbors = self._getVertexCellNeighbors(position)
            assert len(cellNeighbors) == 4

            cellNeighbors.sort()
            NW, NE, SW, SE = cellNeighbors

            self.cellGraph[NW].remove(SW)
            self.cellGraph[SW].remove(NW)
            self.cellGraph[NE].remove(SE)
            self.cellGraph[SE].remove(NE)

        elif move[0] == 'v':

            position = int(move[1:])

            # Update the wall list and reduce the walls for that player
            self.walls[position] = self.currentPlayer + WallType.VERTICAL
            self.numPlayerWalls[self.currentPlayer - 1] -= 1

            # Remove the edges from the graph that have been blocked by the wall
            cellNeighbors = self._getVertexCellNeighbors(position)
            assert len(cellNeighbors) == 4

            cellNeighbors.sort()
            NW, NE, SW, SE = cellNeighbors

            self.cellGraph[NW].remove(NE)
            self.cellGraph[NE].remove(NW)
            self.cellGraph[SW].remove(SE)
            self.cellGraph[SE].remove(SW)

        else:
            raise Exception("Invalid Move: ", str(move))

        self.checkForWin()
        self.currentPlayer = 3 - self.currentPlayer

    def checkForWin(self):
        p1, p2 = self.playerPositions[0], self.playerPositions[1]
        if p1 < self.boardSize:
            self.winner = 1
        elif p2 >= self.boardSize**2 - self.boardSize:
            self.winner = 2

    def _createCellGraph(self):
        self.cellGraph = []
        for cell in xrange(self.numCells):
            neighbors = []
            N, S, E, W = [cell + d for d in self.distance.itervalues()]
            if self._isValidCell(N):
                neighbors.append(N)
            if self._isValidCell(S):
                neighbors.append(S)
            if self._isValidCell(E) and self._inSameRow(cell, E):
                neighbors.append(E)
            if self._isValidCell(W) and self._inSameRow(cell, W):
                neighbors.append(W)
            self.cellGraph.append(sorted(neighbors))

    def _getValidWallMoves(self):
        # Determine wall moves if the current player has walls to place
        wallMoves = []
        if self.numPlayerWalls[self.currentPlayer - 1] > 0:
            for v in self.nonRimWalls:
                # There will always be N, S, E, W neighbors since we are only
                # sampling the non-rim walls in the board
                # TODO: This should be replaced with a look-up table for speed
                N, S, E, W = self._getVertexVertexNeighbors(v)

                # I can place a vertical wall here if it is empty and there are
                # no vertical walls above or below me
                if not self.walls[N] & WallType.VERTICAL and \
                    not self.walls[S] & WallType.VERTICAL and \
                        self.walls[v] == WallType.EMPTY and \
                        not self._doesWallBlockVictory(v, WallType.VERTICAL):
                    wallMoves.append('v' + str(v))

                # I can place a horizontal wall here if it is empty and there
                # are no horizontal walls to the left or right of me
                if not self.walls[E] & WallType.HORIZONTAL and \
                    not self.walls[W] & WallType.HORIZONTAL and \
                        self.walls[v] == WallType.EMPTY and \
                        not self._doesWallBlockVictory(v, WallType.HORIZONTAL):
                    wallMoves.append('h' + str(v))

        return wallMoves

    def _getValidPawnMoves(self, cell):
        NW, NE, SW, SE = self.cellVertexGraph[cell]

        canMoveNorth = not self.walls[NW] & WallType.HORIZONTAL and \
                        not self.walls[NE] & WallType.HORIZONTAL
        canMoveSouth = not self.walls[SW] & WallType.HORIZONTAL and \
                        not self.walls[SE] & WallType.HORIZONTAL
        canMoveEast = not self.walls[NE] & WallType.VERTICAL and \
                        not self.walls[SE] & WallType.VERTICAL
        canMoveWest = not self.walls[NW] & WallType.VERTICAL and \
                        not self.walls[SW] & WallType.VERTICAL

        return [d for d, canMove in zip('NSEW', [canMoveNorth, canMoveSouth,
                                                 canMoveEast, canMoveWest])
                if canMove]

    def _isValidCell(self, cell):
        return cell >= 0 and cell < self.numCells

    def _inSameRow(self, cell1, cell2):
        return cell1 / self.boardSize == cell2 / self.boardSize

    def _doesWallBlockVictory(self, wall, wallType):

        iterations = 0

        self.walls[wall] = wallType

        if not self._doesWallTouchAnotherWall(wall):
            blocksVictory = False

        else:
            visited = [False] * self.numCells
            frontier = deque()

            opponent = 3 - self.currentPlayer
            root = self.playerPositions[opponent - 1]
            frontier.append(root)
            blocksVictory = True

            if opponent == 1:
                victoryCells = range(0, self.boardSize)
                sortDescending = True
            elif opponent == 2:
                victoryCells = range(self.boardSize**2 - self.boardSize,
                                     self.boardSize**2)
                sortDescending = False
            else:
                raise Exception("Invalid opponent")

            while len(frontier) > 0:
                current = frontier.pop()
                neighbors = [current + self.distance[d] for d in
                            self._getValidPawnMoves(current)
                            if self._isValidCell(current + self.distance[d])
                            and not visited[current + self.distance[d]]]

                if any(n in victoryCells for n in neighbors):
                    blocksVictory = False
                    break

                neighbors.sort(reverse=sortDescending)

                frontier.extend(neighbors)
                visited[current] = True
                iterations += 1

        # print "DFS iterations: ", str(iterations)

        self.walls[wall] = WallType.EMPTY

        return blocksVictory

    def _doesWallTouchAnotherWall(self, wall):
        # TODO: This should check to see if we touch TWO other walls
        # The only way to close off a path is if a new wall makes contact
        # with more than one other wall.
        # More sophisticated versions of this would be to keep track of
        # chains of walls, and only make the DFS check if a chain is closed

        N, S, E, W = self._getVertexVertexNeighbors(wall)
        N2 = N + self.distance['N']
        S2 = S + self.distance['S']
        E2 = E + self.distance['E']
        W2 = W + self.distance['W']
        NE = N + self.distance['E']
        NW = N + self.distance['W']
        SE = S + self.distance['E']
        SW = S + self.distance['W']

        if self._isHorizontalWall(wall):
            return self._isVerticalWall(NW) or self._isVerticalWall(N) \
                or self._isVerticalWall(NE) or self._isVerticalWall(SW) \
                or self._isVerticalWall(S) or self._isVerticalWall(SE) \
                or self._isVerticalWall(W) or self._isVerticalWall(E) \
                or self._isHorizontalWall(W2) or self._isHorizontalWall(E2)
        elif self._isVerticalWall(wall):
            return self._isHorizontalWall(NW) or self._isHorizontalWall(N) \
                or self._isHorizontalWall(NE) or self._isHorizontalWall(SW) \
                or self._isHorizontalWall(S) or self._isHorizontalWall(SE) \
                or self._isHorizontalWall(W) or self._isHorizontalWall(E) \
                or self._isVerticalWall(N2) or self._isVerticalWall(S2)

    def _getVertexVertexNeighbors(self, vertex):
        # TODO: Replace this with a look-up table (adjacency list)
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

    def _getCellVertexNeighbors(self, cell):
        # TODO: Replace this with a look-up table (adjacency list)
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

    def _getVertexCellNeighbors(self, vertex):

        neighbors = []

        vertexRow = vertex / self.vertexSize
        vertexCol = vertex % self.vertexSize

        SE = vertex - vertexRow
        SEcol = SE % self.boardSize
        SW = SE - 1
        SWcol = SW % self.boardSize
        NE = SE - self.boardSize
        NEcol = NE % self.boardSize
        NW = NE - 1
        NWcol = NW % self.boardSize

        if SEcol == vertexCol and self._isValidCell(SE):
            neighbors.append(SE)
        if SWcol == vertexCol - 1 and self._isValidCell(SW):
            neighbors.append(SW)
        if NEcol == vertexCol and self._isValidCell(NE):
            neighbors.append(NE)
        if NWcol == vertexCol - 1 and self._isValidCell(NW):
            neighbors.append(NW)

        return neighbors

    def _createCellVertexGraph(self):
        self.cellVertexGraph = []
        for cell in xrange(self.numCells):
            self.cellVertexGraph.append(
                list(self._getCellVertexNeighbors(cell)))

    def _createVertexVertexGraph(self):
        pass

    def _createVertexCellGraph(self):
        pass

    def _isVerticalWall(self, wall):
        if wall < 0 or wall >= self.numVertexes:
            return False
        return self.walls[wall] & WallType.VERTICAL

    def _isHorizontalWall(self, wall):
        if wall < 0 or wall >= self.numVertexes:
            return False

        return self.walls[wall] & WallType.HORIZONTAL

    def __repr__(self):
        h_wall = '--'
        h_wall_empty = '  '
        v_wall_empty = ' '
        v_wall = '|'
        cell_empty = '  '
        vertex = '+'
        player1 = 'p1'
        player2 = 'p2'

        empty_h_row = [vertex, h_wall_empty] * self.boardSize + [vertex, '\n']
        empty_v_row = [v_wall_empty, cell_empty] * self.boardSize + [v_wall_empty, '\n']

        board = []
        for _ in xrange(self.boardSize):
            board.append(list(empty_h_row))
            board.append(list(empty_v_row))
        board.append(empty_h_row)

        for v in xrange(self.numVertexes):
            row = v / self.vertexSize
            col = v % self.vertexSize

            # If a player placed the wall, draw it
            if self.walls[v] & WallType.PLAYER1 or self.walls[v] & WallType.PLAYER2:
                if self.walls[v] & WallType.HORIZONTAL:
                    board[2 * row][col * 2 - 1] = h_wall
                    board[2 * row][col * 2 + 1] = h_wall
                elif self.walls[v] & WallType.VERTICAL:
                    board[row * 2 - 1][col * 2] = v_wall
                    board[row * 2 + 1][col * 2] = v_wall

        p1row = self.playerPositions[0] / self.boardSize
        p2row = self.playerPositions[1] / self.boardSize
        p1col = self.playerPositions[0] % self.boardSize
        p2col = self.playerPositions[1] % self.boardSize

        board[p1row * 2 + 1][p1col * 2 + 1] = player1
        board[p2row * 2 + 1][p2col * 2 + 1] = player2

        return ''.join(map(''.join, board))


def playGame():
    q = QuoridorGameState()
    move = ''
    while move != 'q' or q.winner is None:
        print q
        move = raw_input('Enter Move: ')
        if move in q.getLegalMoves():
            q.executeMove(move)
        else:
            print 'Invalid move: ', move

    print "Winner: ", q.winner


def main():

    playGame()

    # q = QuoridorGameState()
    # print q.getLegalMoves()
    # for i in xrange(0, len(q.walls), q.vertexSize):
    #     print str(i) + '-' + str(i+q.vertexSize) + ': ' + \
    #           ' '.join(map(str, q.walls)[i:i+q.vertexSize])

if __name__ == '__main__':
    main()
