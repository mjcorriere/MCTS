# Development Notes

## 12/22/16 - Implementing Tarjan's Algorithm
The algorithm for finding graph bridges is implemented and tested, but needs to be applied to the game domain. I need to map the output of the algorithm (bridges in the form of node pairs (u, v)) to actual wall locations. Even though these edges may be bridges, they may not actually block a player from reaching a goal. For example, a player may draw a square around an interior region, separating that region from the graph. However, so long as a player is not inside this region, it would not be an illegal wall placement.

Additionally, the simplification of findValidPawnMoves has resulted in a 2x games per second speedup!

Adding more instrumentation to getLegalMoves() and the most recent bridge finding algorithm has shown that there is a nearly 2 order of magnitude speedup in switching to bridge finding over brute force DFS. Brute force DFS takes 8 ms, while bridge finding seems to be about 0.1 ms.

## 12/21/16 - Preparing for Tarjan's Algorithm
The new plan is to keep the graph of connected cells as the game progresses. In this way, I can make connectivity checks to identify bridges and articulation points, representing illegal wall placements. This should significantly reduce the amount of time necessary to find these illegal placements.

Additionally, I am preparing to move all static board information into a look-up table to reduce the calculation time for these checks. For example, finding valid pawn moves only takes on the order of 1e6, but this is called millions of times. Reducing this to a list lookup should result in an order of magnitude (or better!) performance improvement for this function. This means many more games per second, as profiling has shown this function to be a hotspot.
