import time
import random

from quoridor import *
import graph_algorithms

def testValidPawnMovesTiming():
    print "TEST: testValidPawnMovesTiming()"

    q = QuoridorGameState()

    times = []
    for _ in xrange(100000):
        start = time.clock()
        q._getValidPawnMoves(25)
        times.append(time.clock() - start)

    print "Average time: ", str(float(sum(times)) / float(len(times)))
    print "Max time: ", str(max(times))


def testGamesPerSecond():
    print "TEST: testGamesPerSecond()"

    gameNo = 0
    playTimes = []
    while gameNo < 100:
        gameNo += 1
        q = QuoridorGameState()
        start = time.clock()
        while q.winner is None:
            move = random.choice(q.getLegalMoves())
            q.executeMove(move)
        end = time.clock()
        playTimes.append(end - start)
        print '.',
        if gameNo % 50 == 0:
            print '\n'

    avgPlayTime = float(sum(playTimes)) / float(len(playTimes))
    gamesPerSec = 1.0 / avgPlayTime

    print '\n\n'
    print 'Average play time: ',str(avgPlayTime)
    print 'Max play time: ', str(max(playTimes))
    print 'Games per second: ', str(gamesPerSec)


def testVertexCellNeighbors():
    print "TEST: testVertexCellNeighbors()"

    q = QuoridorGameState()
    neighbors = sorted(q._getVertexCellNeighbors(24))
    assert neighbors == [12, 13, 21, 22]

    neighbors = sorted(q._getVertexCellNeighbors(0))
    assert neighbors == [0]

    neighbors = sorted(q._getVertexCellNeighbors(9))
    assert neighbors == [8]


def testNeighborRemoval():
    print "TEST: testNeighborRemoval()"

    q = QuoridorGameState()

    q.executeMove('h23')
    assert 20 not in q.cellGraph[11]
    assert 11 not in q.cellGraph[20]
    assert 21 not in q.cellGraph[12]
    assert 12 not in q.cellGraph[21]

    q.executeMove('v15')
    assert 4 not in q.cellGraph[5]
    assert 5 not in q.cellGraph[4]
    assert 13 not in q.cellGraph[14]
    assert 14 not in q.cellGraph[13]


def testHorizontalWallPlacement():
    print "TEST: testHorizontalWallPlacement()"

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


def testWallBlockingVictory():
    print "TEST: testWallBlockingVictory()"

    q = QuoridorGameState()
    q.executeMove('h41')
    q.executeMove('h43')
    q.executeMove('h45')
    q.executeMove('h47')
    q.executeMove('v48')
    print q

    assert 'h38' not in q.getLegalMoves()
    assert 'h58' not in q.getLegalMoves()


def testPrintBoard():
    print "TEST: testPrintBoard()"

    q = QuoridorGameState()
    q.executeMove('h24')
    q.executeMove('v25')
    q.executeMove('h11')
    q.executeMove('h13')
    q.executeMove('13')
    q.executeMove('67')
    print q


def testBridgeAlgorithm():
    print "TEST: testBridgeAlgorithm()"

    q = QuoridorGameState()
    q.executeMove('h41')
    q.executeMove('h43')
    q.executeMove('h45')
    q.executeMove('h47')
    q.executeMove('v48')

    bridges = graph_algorithms.bridge(q.cellGraph, q.playerPositions[0],
                                      q.numCells)
    print q
    print "BRIDGES: ", str(bridges)

def runAllTests():
    testVertexCellNeighbors()
    testWallBlockingVictory()
    testHorizontalWallPlacement()
    testNeighborRemoval()
    testValidPawnMovesTiming()
    testGamesPerSecond()


def runPassFailTests():
    testVertexCellNeighbors()
    testWallBlockingVictory()
    testHorizontalWallPlacement()
    testNeighborRemoval()


def main():
    runPassFailTests()
    testBridgeAlgorithm()
    testValidPawnMovesTiming()
    testPrintBoard()
    testGamesPerSecond()

if __name__ == '__main__':
    main()
