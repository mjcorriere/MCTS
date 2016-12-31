
from collections import deque
import heapq

# Python program to find bridges in a given undirected graph
# Complexity : O(V+E)
def bridgeUtil(graph, u, visited, parent, low, disc, time, bridges):

    # Count of children in current node
    children = 0

    # Mark the current node as visited and print it
    visited[u] = True

    # Initialize discovery time and low value
    disc[u] = time
    low[u] = time
    time += 1

    # Recur for all the vertices adjacent to this vertex
    for v in graph[u]:
        # If v is not visited yet, then make it a child of u in DFS tree and
        # recur for it
        if not visited[v]:
            parent[v] = u
            children += 1
            bridgeUtil(graph, v, visited, parent, low, disc, time, bridges)

            # Check if the subtree rooted with v has a connection to one of the
            # ancestors of u
            low[u] = min(low[u], low[v])

            # If the lowest vertex reachable from subtree under v is below u in
            # DFS tree, then u-v is a bridge
            if low[v] > disc[u]:
                bridges.append((u, v))

        # Update low value of u for parent function calls.
        elif v != parent[u]:
            low[u] = min(low[u], disc[v])

# DFS based function to find all bridges.
def bridge(graph, root, numVertices):

    # Mark all the vertices as not visited and initialize parent and visited
    visited = [False] * numVertices
    disc = [float("Inf")] * numVertices
    low = [float("Inf")] * numVertices 
    parent = [-1] * numVertices
    bridges = []

    bridgeUtil(graph, root, visited, parent, low, disc, 0, bridges)

    return bridges


def rowDistance(cell, row, boardSize):
    cellRow = cell / boardSize
    return abs(row - cellRow)


def greedyBestFirst(gamestate, player, heuristic=rowDistance):

        graph = gamestate.cellGraph
        boardSize = gamestate.boardSize
        root = gamestate.playerPositions[player]
        goal = [gamestate.PLAYER1_GOAL, gamestate.PLAYER2_GOAL][player]
        goalRow = [0, boardSize - 1][player]

        visited = [False] * len(graph)
        inQueue = [False] * len(graph)
        frontier = []

        heapq.heappush(frontier, (heuristic(root, goalRow, boardSize), root))

        canBeReached = False

        while len(frontier) > 0:
            current = heapq.heappop(frontier)[1]
            neighborCandidates = graph[current]
            neighbors = [n for n in neighborCandidates if not visited[n] and not inQueue[n]]

            if goal in neighbors:
                canBeReached = True
                break

            for n in neighbors:
                heapq.heappush(frontier, (heuristic(n, goalRow, boardSize), n))
                inQueue[n] = True

            visited[current] = True

        return canBeReached
