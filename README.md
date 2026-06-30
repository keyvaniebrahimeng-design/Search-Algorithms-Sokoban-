# Sokoban AI Solver - Search Algorithms

## Overview
This repository contains an AI-based solver for the classic puzzle game **Sokoban**. The project models the game as a state-space search problem and implements various uninformed and informed search algorithms to find the optimal path to push all boxes to their designated targets.

## Implemented Algorithms
The following search algorithms were developed and evaluated based on their memory consumption, time complexity, and the number of expanded nodes:
* **BFS (Breadth-First Search):** Explores the state space level by level.
* **IDS (Iterative Deepening Search):** Combines the space-efficiency of DFS with the completeness of BFS.
* **UCS (Uniform Cost Search):** Expands nodes based on path cost, which is crucial since normal moves and box pushes have different costs.
* **A* Search:** Utilizes the evaluation function $f(n) = g(n) + h(n)$ to efficiently find the optimal path.

## Key Features & Optimizations
* **Cost Model:** Differentiated costs for actions (Normal Move = 1, Box Push = 5) to ensure realistic optimal pathfinding.
* **Deadlock Detection:** Implemented both static and dynamic (square) deadlock detection to aggressively prune invalid states and prevent state-space explosion.
* **Custom Heuristics:** Designed a heuristic function using Manhattan distance and target pairing to guide the A* algorithm effectively.

## Technical Report
For a deep dive into the state-space representation, pruning strategies, and a comparative performance analysis of the algorithms across different map difficulties, please refer to the attached Persian technical report:
[Project_Report.pdf](./project%20ai1-1.pdf)
