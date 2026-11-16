# NorthRoute Optimizer

Design and Analysis of Algorithms - Assignment 3  
National University of Computer and Emerging Sciences, Islamabad Campus  
Fall 2026  

## Student Information
- Name: Abdul Azeem
- Roll Number: 24i-2013
- Section: BAI-5A

---

## Personal Parameters (Section 3.1)
- Roll Number: 24i-2013
- Last 3 digits: s = 13
- Van Weight Capacity (Problem A): W = 15 + (13 mod 10) = 15 + 3 = 18
- Amount to Make in Change (Problem B): T = 30 + (13 mod 20) = 30 + 13 = 43
- Start Hub Index: (13 mod 8) = 5 (Mapping: A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7) -> Hub F

---

## Repository Structure
- `main.py`: Main executable Python script implementing all assignment algorithms (Problems A to F) and printing all required outputs.
- `build_report.py`: Script that compiles the 5-page PDF report (`24i-2013-A3-BAI-5A.pdf`) using ReportLab.
- `generate_plots.py`: Generates the graph visualization (`road_network.png`) and DP table (`knapsack_table.png`).
- `24i-2013-A3-BAI-5A.pdf`: The complete, typed 5-page submission report.
- `24i-2013-A3-BAI-5A.zip`: Submission ZIP containing the Python source files and this README.

---

## Requirements and Setup
The code uses standard Python 3. Standard library modules used:
- `collections.deque` (for BFS)
- `heapq` (for Dijkstra and Prim priority queues)

Optional packages for plotting and report generation:
- `reportlab` (for PDF generation)
- `matplotlib` (for figure generation)
- `networkx` (for network plotting)
- `numpy` (for matrix operations)

Install dependencies if needed:
```bash
pip install reportlab matplotlib networkx numpy
```

---

## How to Run and Reproduce Results

### 1. Run the Main Algorithm Suite
To execute all algorithms and verify outputs in the terminal:
```bash
python main.py
```
or
```bash
python3 main.py
```

### 2. Generate Plots (Optional)
```bash
python generate_plots.py
```

### 3. Rebuild the PDF Report (Optional)
```bash
python build_report.py
```

---

## Summary of Results

### Problem A: The Van Loader (0/1 Knapsack)
- Capacity W: 18
- Top-down memoized optimal value: 26
- Bottom-up tabulated optimal value: 26
- Chosen parcels: P1 (weight 2, value 3), P6 (weight 7, value 10), P7 (weight 9, value 13)
- Total weight: 18 / 18
- Total value: 26
- Time complexity: O(n * W) = O(8 * 18) = 144 operations
- Space complexity: O(n * W)

### Problem B: Making Change (Coin Change)
- Denominations: {1, 3, 4, 9}
- Target T: 43
- DP minimum coins needed: 6 coins
- DP coins used: [9, 9, 9, 9, 4, 3] (Sum = 43)
- Greedy result on T = 43: 6 coins [9, 9, 9, 9, 4, 3] (Matches DP)
- Greedy counterexample: Target amount 6
  - DP minimum: 2 coins [3, 3]
  - Greedy result: 3 coins [4, 1, 1]
  - Reason: Greedy takes 4 first, leaving remainder 2 which forces two 1s, missing the optimal combination of two 3s.

### Problem C: The Road Map (Representation, BFS, DFS)
- Vertices: 8 hubs (A to H), Edges: 13 undirected weighted roads
- Start Hub: F
- Adjacency List: Space O(V + E) = O(8 + 13) = 21 entries. Preferred because graph is sparse.
- Adjacency Matrix: Space O(V^2) = 64 cells.
- BFS visit order from Hub F: F, D, E, G, H, B, C, A
- Hop distances from Hub F:
  - F: 0 hop
  - D, E, G, H: 1 hop
  - B, C: 2 hops
  - A: 3 hops
- DFS visit order from Hub F: F, D, B, A, C, E, G, H
- Connected components: 1 (all 8 hubs reachable)
- Cycle detected: Yes (e.g. B -> C -> A -> B)
- Smallest roads from F to H: 1 road (direct road F-H)

### Problem D: Shortest Routes (Dijkstra)
- Start Hub: F
- Shortest path distances:
  - Hub A: 11 (Path: F -> E -> D -> B -> A)
  - Hub B: 7 (Path: F -> E -> D -> B)
  - Hub C: 8 (Path: F -> E -> D -> B -> C)
  - Hub D: 5 (Path: F -> E -> D)
  - Hub E: 3 (Path: F -> E)
  - Hub F: 0 (Path: F)
  - Hub G: 2 (Path: F -> G)
  - Hub H: 5 (Path: F -> H)
- Shortest path from F to H: F -> H (Length = 5)
- Time complexity: O((V + E) log V) with min-heap vs O(V^2) with plain array scan.
- Equivalence to BFS: If all road lengths were 1, Dijkstra distances match BFS hop distances exactly.

### Problem E: The Backbone (Minimum Spanning Tree)
- Algorithm: Kruskal with Disjoint Set Union (Union-Find with path compression and rank)
- MST Edges selected:
  1. B-C (length 1)
  2. B-D (length 2)
  3. D-E (length 2)
  4. F-G (length 2)
  5. A-C (length 3)
  6. E-F (length 3)
  7. G-H (length 4)
- Total MST Length: 17
- Prim check: Verified with Prim algorithm, yielding identical total weight of 17.
- Comparison: Prim is preferred for dense graphs (E close to V^2), while Kruskal is preferred for sparse graphs or pre-sorted edge sets.

### Problem F: Analysis and Reasoning
- Complexity Table:
  - 0/1 Knapsack: Time O(n * W), Space O(n * W), Dynamic Programming
  - Coin Change: Time O(n * T), Space O(T), Dynamic Programming
  - BFS / DFS: Time O(V + E), Space O(V), Graph Traversal
  - Dijkstra: Time O((V + E) log V), Space O(V + E), Greedy Traversal
  - Kruskal MST: Time O(E log V), Space O(V + E), Greedy
  - Prim MST: Time O((V + E) log V), Space O(V + E), Greedy
- Greedy vs DP: Greedy fails on coin change (target 6), but is provably correct in Dijkstra due to non-negative edge weights and monotonic distance accumulation.
- Doubling n vs Doubling W: Both double the table size (n * W). However, doubling W requires adding only 1 bit to the numerical representation, demonstrating the pseudo-polynomial property.
- MST vs Shortest-Path Tree: MST minimizes global edge sum across all hubs (17), whereas SPT minimizes path length from source hub F. For example, edge F-H (length 5) is on the shortest path from F to H, but is excluded from the MST in favor of G-H (length 4), which yields a tree path length of 6 from F to H.

---

## Academic Integrity and AI Use
An AI assistant was used for code structuring, style formatting, and drafting text. All algorithmic computations, table derivations, and complexity reasoning were verified using personal parameters for student Abdul Azeem (Roll No: 24i-2013).
