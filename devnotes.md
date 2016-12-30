# Development Notes

## 12/30/16 - The Addition of the Goal Node
The addition of the goal node may not have been as clever as I had previously though. The initial reason for adding the node was to give A* (or other search algorithms) a single target to aim for when traversing the graph. However, I am currently having a problem where the distance to this goal node cannot be estimated. Why? The goal node does not live in the 2d space of the grid. Instead, it represents a group of nodes (all the nodes resulting in a victory condition). The idea of distance to this goal node would become the shortest distance to any of the nodes in the goal set. While this is feasible, it doesn't result in nice, clear, general code. The best first search code will be specific to this problem. Though I suppose if the only change to the algorithm lies in the distance heuristic, it may not be a problem after all.

## 12/28/16 - Cython Experiments
Created a toy Cython implementation. The code was taken 100% as is and passed over to Cython to get a sense of the speed-up. Cython provided ~2x games per second speed-up essentially for free. Cython will be a great option for squeezing out additional performance once I've established a solid foundation of data structures and algorithms. 'cdef'ing variable types and providing fixed length arrays should really get this thing moving.

## 12/23/16 - Play Strength Investigation (and bugs!)
I began to watch games played between two MCTS players of equal strength (iterations = 100). It looked an awful lot like they were playing random moves for the first 90% of the game. Sure enough, investigating the number of visits to each "best move" node selected in the MCTS tree revealed these nodes had only been visited once. 

Ramping up the number of iterations to 1000, these nodes were now being visited approximately 15-20 times, but the win rates were hovering about 50%. 

Jumping up another order of magnitude to 10000 iterations uncovered a sneaky bug in the calculation of legal moves. Many times during the simulation phase I received an exception from random.choice() -- it was being called on an empty list. Digging deeper, I discovered that the players were blocking _themselves_ in. The legal move check was only making sure the current player wasn't stopping the opponent from winning. Oops.

## 12/22/16 - Implementing Tarjan's Algorithm
The algorithm for finding graph bridges is implemented and tested, but needs to be applied to the game domain. I need to map the output of the algorithm (bridges in the form of node pairs (u, v)) to actual wall locations. Even though these edges may be bridges, they may not actually block a player from reaching a goal. For example, a player may draw a square around an interior region, separating that region from the graph. However, so long as a player is not inside this region, it would not be an illegal wall placement.

Additionally, the simplification of findValidPawnMoves has resulted in a 2x games per second speedup!

Adding more instrumentation to getLegalMoves() and the most recent bridge finding algorithm has shown that there is a nearly 2 order of magnitude speedup in switching to bridge finding over brute force DFS. Brute force DFS takes 8 ms, while bridge finding seems to be about 0.1 ms.

## 12/21/16 - Preparing for Tarjan's Algorithm
The new plan is to keep the graph of connected cells as the game progresses. In this way, I can make connectivity checks to identify bridges and articulation points, representing illegal wall placements. This should significantly reduce the amount of time necessary to find these illegal placements.

Additionally, I am preparing to move all static board information into a look-up table to reduce the calculation time for these checks. For example, finding valid pawn moves only takes on the order of 1e6, but this is called millions of times. Reducing this to a list lookup should result in an order of magnitude (or better!) performance improvement for this function. This means many more games per second, as profiling has shown this function to be a hotspot.
