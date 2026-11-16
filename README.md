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

## Tech Stack

The project is built using Python with clean, modular algorithmic implementations and automated reporting.

- Programming Language: Python 3.12
- Core Data Structures and Algorithms (Built from scratch):
  - collections.deque: Used for First-In-First-Out (FIFO) queue operations in Breadth-First Search (BFS).
  - heapq: Standard min-heap priority queue used for Dijkstra shortest path and Prim MST algorithms.
  - Disjoint Set Union (Union-Find): Custom implementation with path compression and union by rank for Kruskal MST algorithm.
  - 2D Tabulation and Recursion with Memoization: For 0/1 Knapsack and Coin Change Dynamic Programming.
- Visualization and Diagram Generation:
  - Matplotlib: Used to draw the road network topology and generate the DP tabulation heatmap.
  - NetworkX: Graph structure modeling and coordinate positioning for hubs and roads.
  - NumPy: 2D array representation for DP grid rendering.
- PDF Report Generation:
  - ReportLab: Programmatic PDF document generation using SimpleDocTemplate, Flowable elements, Custom Styles, and a two-pass NumberedCanvas for dynamic page numbering.
- Document and Code Verification:
  - PyPDF2: PDF extraction and page count validation to strictly enforce the 5-page ceiling.
- Version Control:
  - Git and GitHub: Code tracking and remote repository synchronization.

---

## File and Folder Structure

```text
northroute-optimizer/
|-- 24i-2013-A3-BAI-5A.pdf    # Final typed 5-page PDF submission report
|-- 24i-2013-A3-BAI-5A.zip    # Final submission archive containing source code and README
|-- build_report.py           # ReportLab script generating the complete 5-page PDF report
|-- generate_plots.py         # Matplotlib and NetworkX script generating graph and DP figures
|-- knapsack_table.png        # Generated heatmap image of the 0/1 Knapsack DP table
|-- main.py                   # Primary executable script implementing all algorithms (A to F)
|-- README.md                 # Project documentation, tech stack, and execution guide
`-- road_network.png          # Generated network diagram highlighting hubs, roads, and MST
```

### File Descriptions:
1. `main.py`:
   - Contains all self-contained algorithm implementations:
     - Problem A: 0/1 Knapsack (top-down memoization, bottom-up tabulation, parcel reconstruction, complexity analysis).
     - Problem B: Coin Change (bottom-up DP, greedy heuristic comparison, target 6 counterexample).
     - Problem C: Graph representations (Adjacency List and Adjacency Matrix), BFS traversal, DFS traversal, connected component counter, and cycle detection.
     - Problem D: Dijkstra shortest path algorithm with min-heap, shortest path sequence to Hub H, predecessor tracing, and BFS equivalence analysis.
     - Problem E: Minimum Spanning Tree using Kruskal algorithm with custom Union-Find, verified against Prim algorithm.
     - Problem F: Algorithmic complexity table and theoretical trade-off analysis.
2. `build_report.py`:
   - Programmatically builds `24i-2013-A3-BAI-5A.pdf` using ReportLab.
   - Enforces a clean 5-page layout with formal typography, tables, and embedded network figures.
3. `generate_plots.py`:
   - Produces high-resolution visual plots (`road_network.png` and `knapsack_table.png`) for visual clarity and report embedding.
4. `24i-2013-A3-BAI-5A.pdf`:
   - The required typed assignment report formatted within 5 pages.
5. `24i-2013-A3-BAI-5A.zip`:
   - The submission archive containing all Python source files, generated visual assets, and this README.

---

## Requirements and Setup
The algorithm implementations in `main.py` use only Python standard library modules (`collections` and `heapq`).

To generate the plots and compile the PDF report, install the following packages:
```bash
pip install reportlab matplotlib networkx numpy PyPDF2
```

---

## How to Run and Reproduce Results

### 1. Run the Main Algorithm Suite
To execute all algorithms and display all outputs in the console:
```bash
python main.py
```
or
```bash
python3 main.py
```

### 2. Generate Plots (Optional)
To regenerate the road network and knapsack diagrams:
```bash
python generate_plots.py
```

### 3. Rebuild the PDF Report (Optional)
To recompile the 5-page PDF report:
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
- Start Hub: Hub F
- Adjacency List: Space O(V + E) = O(8 + 13) = 21 entries. Preferred because the graph is sparse.
- Adjacency Matrix: Space O(V^2) = 64 cells.
- BFS visit order from Hub F: F, D, E, G, H, B, C, A
- Hop distances from Hub F:
  - To Hub F: 0 hop
  - To Hubs D, E, G, H: 1 hop
  - To Hubs B, C: 2 hops
  - To Hub A: 3 hops
- DFS visit order from Hub F: F, D, B, A, C, E, G, H
- Connected components: 1 (all 8 hubs reachable)
- Cycle detected: Yes (e.g. B -> C -> A -> B)
- Smallest roads from F to H: 1 road (direct road F-H)

### Problem D: Shortest Routes (Dijkstra)
- Start Hub: Hub F
- Shortest path distances:
  - Hub A: 11 (Path: F -> E -> D -> B -> A)
  - Hub B: 7 (Path: F -> E -> D -> B)
  - Hub C: 8 (Path: F -> E -> D -> B -> C)
  - Hub D: 5 (Path: F -> E -> D)
  - Hub E: 3 (Path: F -> E)
  - Hub F: 0 (Path: F)
  - Hub G: 2 (Path: F -> G)
  - Hub H: 5 (Path: F -> H)
- Shortest path from Hub F to Hub H: F -> H (Length = 5)
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
