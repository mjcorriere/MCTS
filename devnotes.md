# Development Notes

## 12/21/16 - Preparing for Tarjan's Algorithm
The new plan is to keep the graph of connected cells as the game progresses. In this way, I can make connectivity checks to identify bridges and articulation points, representing illegal wall placements. This should significantly reduce the amount of time necessary to find these illegal placements.

Additionally, I am preparing to move all static board information into a look-up table to reduce the calculation time for these checks. For example, finding valid pawn moves only takes on the order of 1e6, but this is called millions of times. Reducing this to a list lookup should result in an order of magnitude (or better!) performance improvement for this function. This means many more games per second, as profiling has shown this function to be a hotspot.
