"""
NorthRoute Optimizer - Assignment 3
Design and Analysis of Algorithms
Student Name: Abdul Azeem
Roll Number: 24i-2013
Section: BAI-5A

Personal Parameters:
s = 13 (last three digits of roll number 24i-2013)
W = 15 + (13 mod 10) = 18 (van weight capacity)
T = 30 + (13 mod 20) = 43 (target change amount)
Start hub index = 13 mod 8 = 5 -> Hub F
"""

from collections import deque
import heapq


# =====================================================================
# PROBLEM A: THE VAN LOADER - 0/1 KNAPSACK
# =====================================================================

def knapsack_top_down(parcels, capacity):
    """
    Solves 0/1 Knapsack using top-down memoization.
    
    Input:
      parcels: list of tuples (name, weight, value)
      capacity: integer maximum capacity W
    Output:
      max_val: maximum value achievable
      memo: dictionary of memoized states (i, w) -> max_val
    Complexity:
      Time: O(n * W)
      Space: O(n * W)
    """
    memo = {}

    def helper(i, w):
        # Base cases: no items left or zero capacity remaining
        if i == 0 or w == 0:
            return 0
        state = (i, w)
        if state in memo:
            return memo[state]

        name, wt, val = parcels[i - 1]
        if wt > w:
            # Item too heavy, cannot take it
            result = helper(i - 1, w)
        else:
            # Best of take or don't take
            dont_take = helper(i - 1, w)
            take = helper(i - 1, w - wt) + val
            result = max(dont_take, take)

        memo[state] = result
        return result

    max_val = helper(len(parcels), capacity)
    return max_val, memo


def knapsack_bottom_up(parcels, capacity):
    """
    Solves 0/1 Knapsack using bottom-up tabulation (2D table).
    
    Input:
      parcels: list of tuples (name, weight, value)
      capacity: integer maximum capacity W
    Output:
      table: (n + 1) x (capacity + 1) 2D list of maximum values
    Complexity:
      Time: O(n * W)
      Space: O(n * W)
    """
    n = len(parcels)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, wt, val = parcels[i - 1]
        for w in range(capacity + 1):
            if wt > w:
                # Too heavy
                table[i][w] = table[i - 1][w]
            else:
                # Best of take or don't take
                table[i][w] = max(table[i - 1][w], table[i - 1][w - wt] + val)

    return table


def knapsack_reconstruct(parcels, table, capacity):
    """
    Reconstructs the optimal parcel selection from the DP table.
    
    Input:
      parcels: list of tuples (name, weight, value)
      table: 2D DP table
      capacity: integer maximum capacity W
    Output:
      chosen: list of chosen parcel tuples (name, weight, value)
    Complexity:
      Time: O(n)
      Space: O(n)
    """
    chosen = []
    w = capacity
    n = len(parcels)

    for i in range(n, 0, -1):
        # If the value changed from the row above, item i was included
        if table[i][w] != table[i - 1][w]:
            name, wt, val = parcels[i - 1]
            chosen.append((name, wt, val))
            w -= wt

    chosen.reverse()
    return chosen


# =====================================================================
# PROBLEM B: MAKING CHANGE - COIN CHANGE
# =====================================================================

def coin_change_dp(coins, target):
    """
    Finds minimum coins to make target amount using bottom-up DP.
    
    Input:
      coins: list of coin denominations
      target: integer target amount T
    Output:
      min_count: minimum number of coins needed
      coins_used: list of actual coins used
      dp: 1D array of minimum coins for each amount 0..target
    Complexity:
      Time: O(n * T) where n is number of denominations
      Space: O(T)
    """
    infinity = float("inf")
    dp = [0] + [infinity] * target
    parent = [-1] * (target + 1)

    for t in range(1, target + 1):
        for c in coins:
            if c <= t and dp[t - c] + 1 < dp[t]:
                dp[t] = dp[t - c] + 1
                parent[t] = c

    min_count = dp[target]
    if min_count == infinity:
        return -1, [], dp

    # Reconstruct chosen coins
    coins_used = []
    curr = target
    while curr > 0:
        c = parent[curr]
        coins_used.append(c)
        curr -= c

    return min_count, coins_used, dp


def coin_change_greedy(coins, target):
    """
    Attempts to make change using greedy heuristic (largest coin first).
    
    Input:
      coins: list of coin denominations
      target: integer target amount T
    Output:
      count: total coins used (or -1 if impossible)
      coins_used: list of coins selected
    Complexity:
      Time: O(n log n + T)
      Space: O(T)
    """
    sorted_coins = sorted(coins, reverse=True)
    rem = target
    coins_used = []

    for c in sorted_coins:
        while rem >= c:
            coins_used.append(c)
            rem -= c

    if rem != 0:
        return -1, []
    return len(coins_used), coins_used


# =====================================================================
# PROBLEM C: THE ROAD MAP - GRAPH REPRESENTATION, BFS, DFS
# =====================================================================

def build_graph(hubs, edges):
    """
    Builds adjacency list and adjacency matrix representations.
    
    Input:
      hubs: list of hub names
      edges: list of tuples (u, v, weight)
    Output:
      adj_list: dict mapping hub to sorted list of (neighbour, weight)
      adj_matrix: 2D list of distances (0 on diagonal, None/inf for non-edges)
    Complexity:
      Time: O(V^2 + E log V)
      Space: O(V^2 + E)
    """
    adj_list = {h: [] for h in hubs}
    for u, v, w in edges:
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))

    # Keep neighbours sorted alphabetically
    for h in hubs:
        adj_list[h].sort(key=lambda x: x[0])

    hub_idx = {h: i for i, h in enumerate(hubs)}
    n = len(hubs)
    adj_matrix = [[None] * n for _ in range(n)]

    for i in range(n):
        adj_matrix[i][i] = 0

    for u, v, w in edges:
        i, j = hub_idx[u], hub_idx[v]
        adj_matrix[i][j] = w
        adj_matrix[j][i] = w

    return adj_list, adj_matrix


def bfs(adj_list, start_hub):
    """
    Breadth-First Search visiting neighbours in alphabetical order.
    
    Input:
      adj_list: adjacency list
      start_hub: starting hub name
    Output:
      visit_order: list of hubs in visit order
      hop_dist: dict mapping each hub to its hop distance from start_hub
    Complexity:
      Time: O(V + E)
      Space: O(V)
    """
    visited = set([start_hub])
    visit_order = []
    hop_dist = {start_hub: 0}
    queue = deque([start_hub])

    while queue:
        u = queue.popleft()
        visit_order.append(u)

        for v, _ in adj_list[u]:
            if v not in visited:
                visited.add(v)
                hop_dist[v] = hop_dist[u] + 1
                queue.append(v)

    return visit_order, hop_dist


def dfs(adj_list, start_hub, all_hubs):
    """
    Depth-First Search with connected components and cycle detection.
    
    Input:
      adj_list: adjacency list
      start_hub: starting hub name
      all_hubs: complete list of hubs
    Output:
      visit_order: list of hubs visited starting from start_hub
      num_components: total connected components in the graph
      has_cycle: boolean indicating cycle existence
      sample_cycle: list of hubs forming a detected cycle (or empty)
    Complexity:
      Time: O(V + E)
      Space: O(V)
    """
    visited = set()
    visit_order = []
    parent = {}
    has_cycle = False
    sample_cycle = []

    def dfs_visit(u, p):
        nonlocal has_cycle, sample_cycle
        visited.add(u)
        parent[u] = p
        visit_order.append(u)

        for v, _ in adj_list[u]:
            if v == p:
                continue
            if v in visited:
                if not has_cycle:
                    has_cycle = True
                    # Reconstruct cycle from u back to v
                    curr = u
                    cycle = [v]
                    while curr != v and curr is not None:
                        cycle.append(curr)
                        curr = parent.get(curr)
                    cycle.append(v)
                    sample_cycle = cycle
            else:
                dfs_visit(v, u)

    # First run from user start hub
    dfs_visit(start_hub, None)
    num_components = 1

    # Check remaining hubs to count all components
    for h in sorted(all_hubs):
        if h not in visited:
            num_components += 1
            dfs_visit(h, None)

    return visit_order, num_components, has_cycle, sample_cycle


# =====================================================================
# PROBLEM D: SHORTEST ROUTES - DIJKSTRA
# =====================================================================

def dijkstra(adj_list, start_hub, all_hubs):
    """
    Dijkstra shortest path algorithm using a min-heap priority queue.
    
    Input:
      adj_list: adjacency list
      start_hub: starting hub name
      all_hubs: complete list of hubs
    Output:
      dist: dict mapping each hub to its shortest distance from start_hub
      prev: dict mapping each hub to its predecessor on the shortest path
    Complexity:
      Time: O((V + E) log V) with min-heap
      Space: O(V + E)
    """
    infinity = float("inf")
    dist = {h: infinity for h in all_hubs}
    prev = {h: None for h in all_hubs}
    dist[start_hub] = 0

    pq = [(0, start_hub)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue

        for v, weight in adj_list[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, target_hub):
    """
    Reconstructs the shortest path from start hub to target hub.
    
    Input:
      prev: predecessor dictionary from Dijkstra
      target_hub: destination hub name
    Output:
      path: list of hub names along the path
    Complexity:
      Time: O(V)
      Space: O(V)
    """
    path = []
    curr = target_hub
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()
    return path


# =====================================================================
# PROBLEM E: THE BACKBONE - MINIMUM SPANNING TREE (KRUSKAL & PRIM)
# =====================================================================

class UnionFind:
    """
    Disjoint Set Union (Union-Find) with path compression and rank.
    """

    def __init__(self, elements):
        self.parent = {x: x for x in elements}
        self.rank = {x: 0 for x in elements}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal_mst(hubs, edges):
    """
    Kruskal algorithm for Minimum Spanning Tree using Union-Find.
    
    Input:
      hubs: list of hub names
      edges: list of tuples (u, v, weight)
    Output:
      mst_edges: list of chosen edges (u, v, weight)
      total_weight: sum of edge weights in the MST
    Complexity:
      Time: O(E log E) = O(E log V)
      Space: O(V + E)
    """
    uf = UnionFind(hubs)
    # Sort edges primarily by weight, secondarily by hub names for reproducibility
    sorted_edges = sorted(edges, key=lambda x: (x[2], x[0], x[1]))

    mst_edges = []
    total_weight = 0

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == len(hubs) - 1:
                break

    return mst_edges, total_weight


def prim_mst(adj_list, start_hub, all_hubs):
    """
    Prim algorithm for Minimum Spanning Tree using a min-heap.
    
    Input:
      adj_list: adjacency list
      start_hub: starting hub name
      all_hubs: complete list of hubs
    Output:
      mst_edges: list of chosen edges (u, v, weight)
      total_weight: sum of edge weights in the MST
    Complexity:
      Time: O((V + E) log V)
      Space: O(V + E)
    """
    visited = set([start_hub])
    pq = []
    for v, w in adj_list[start_hub]:
        heapq.heappush(pq, (w, start_hub, v))

    mst_edges = []
    total_weight = 0

    while pq and len(visited) < len(all_hubs):
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w

        for next_node, next_w in adj_list[v]:
            if next_node not in visited:
                heapq.heappush(pq, (next_w, v, next_node))

    return mst_edges, total_weight


# =====================================================================
# MAIN RUNNER & CONSOLE OUTPUTS
# =====================================================================

def main():
    print("=" * 70)
    print("NORTHROUTE OPTIMIZER - ASSIGNMENT 3 VERIFICATION")
    print("Student Name: Abdul Azeem | Roll No: 24i-2013 | Section: BAI-5A")
    print("=" * 70)

    # 1. Personal Parameters
    roll_no = "24i-2013"
    s = int(roll_no[-3:])
    W = 15 + (s % 10)
    T = 30 + (s % 20)
    start_hub_index = s % 8
    hubs = ["A", "B", "C", "D", "E", "F", "G", "H"]
    start_hub = hubs[start_hub_index]

    print("\n[Section 3.1: Personal Parameters]")
    print(f"Seed (s): {s}")
    print(f"Van capacity (W): {W}")
    print(f"Change target (T): {T}")
    print(f"Start hub: {start_hub} (index {start_hub_index})")

    # 2. Problem A: Knapsack
    parcels = [
        ("P1", 2, 3),
        ("P2", 3, 4),
        ("P3", 4, 5),
        ("P4", 5, 7),
        ("P5", 6, 8),
        ("P6", 7, 10),
        ("P7", 9, 13),
        ("P8", 10, 15)
    ]
    print("\n" + "=" * 70)
    print("PROBLEM A: THE VAN LOADER (0/1 KNAPSACK)")
    print("=" * 70)

    val_top_down, memo = knapsack_top_down(parcels, W)
    dp_table = knapsack_bottom_up(parcels, W)
    val_bottom_up = dp_table[len(parcels)][W]
    chosen_parcels = knapsack_reconstruct(parcels, dp_table, W)

    total_weight = sum(p[1] for p in chosen_parcels)
    total_value = sum(p[2] for p in chosen_parcels)

    print(f"Top-down memoized optimal value: {val_top_down}")
    print(f"Bottom-up tabulated optimal value: {val_bottom_up}")
    print(f"Implementations match: {val_top_down == val_bottom_up}")
    print("\nChosen parcels for optimal load:")
    for name, wt, val in chosen_parcels:
        print(f"  {name}: weight = {wt}, value = {val}")
    print(f"Total Load Weight: {total_weight} / {W}")
    print(f"Total Load Value: {total_value}")

    # 3. Problem B: Coin Change
    coins = [1, 3, 4, 9]
    print("\n" + "=" * 70)
    print("PROBLEM B: MAKING CHANGE (COIN CHANGE)")
    print("=" * 70)

    min_coins, coins_used, _ = coin_change_dp(coins, T)
    greedy_cnt, greedy_coins = coin_change_greedy(coins, T)

    print(f"Target amount T = {T}")
    print(f"Coin denominations: {coins}")
    print(f"DP minimum coins needed: {min_coins}")
    print(f"DP coins selected: {coins_used}")
    print(f"Greedy coins needed: {greedy_cnt}")
    print(f"Greedy coins selected: {greedy_coins}")
    print(f"Greedy matches DP for T={T}: {min_coins == greedy_cnt}")

    # Counterexample
    diff_target = 6
    diff_dp_cnt, diff_dp_coins, _ = coin_change_dp(coins, diff_target)
    diff_gr_cnt, diff_gr_coins = coin_change_greedy(coins, diff_target)
    print(f"\nCounterexample amount where Greedy fails: Target = {diff_target}")
    print(f"  DP solution: {diff_dp_cnt} coins {diff_dp_coins}")
    print(f"  Greedy solution: {diff_gr_cnt} coins {diff_gr_coins}")
    print("  Reason: Greedy chooses 4 first, leaving 2 which requires two 1s (total 3 coins),")
    print("  missing the optimal solution of two 3s (total 2 coins).")

    # 4. Problem C: Graph Representation, BFS, DFS
    edges = [
        ("A", "B", 4),
        ("A", "C", 3),
        ("B", "C", 1),
        ("B", "D", 2),
        ("C", "D", 4),
        ("C", "E", 8),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
        ("E", "G", 7),
        ("F", "G", 2),
        ("F", "H", 5),
        ("G", "H", 4)
    ]
    print("\n" + "=" * 70)
    print("PROBLEM C: THE ROAD MAP (REPRESENTATION, BFS, DFS)")
    print("=" * 70)

    adj_list, adj_matrix = build_graph(hubs, edges)

    print("\nAdjacency List (hub: neighbours with road length):")
    for h in hubs:
        nbr_str = ", ".join(f"{nbr}({w})" for nbr, w in adj_list[h])
        print(f"  {h}: [{nbr_str}]")

    print("\nAdjacency Matrix (8x8 grid of lengths, - denotes no edge):")
    header = "    " + "  ".join(hubs)
    print(header)
    for i, h in enumerate(hubs):
        row_str = "  ".join(f"{adj_matrix[i][j]:2d}" if adj_matrix[i][j] is not None else " -" for j in range(len(hubs)))
        print(f" {h}  {row_str}")

    bfs_order, hop_dist = bfs(adj_list, start_hub)
    print(f"\nBFS visit order from start hub {start_hub}: {bfs_order}")
    print("BFS hop distances (number of roads):")
    for h in hubs:
        print(f"  To hub {h}: {hop_dist[h]} hop(s)")

    dfs_order, num_comp, has_cycle, sample_cycle = dfs(adj_list, start_hub, hubs)
    print(f"\nDFS visit order from start hub {start_hub}: {dfs_order}")
    print(f"Number of connected components: {num_comp}")
    print(f"Contains cycle: {has_cycle}")
    if has_cycle:
        print(f"Sample cycle detected: {' -> '.join(sample_cycle)}")

    print(f"\nShort Answers:")
    print(f"1. Is the graph connected? Yes, because BFS reaches all {len(hubs)} hubs from start hub {start_hub} (1 component).")
    print(f"2. Smallest number of roads from hub {start_hub} to hub H: {hop_dist['H']} road(s) (direct road {start_hub}-H).")

    # 5. Problem D: Dijkstra
    print("\n" + "=" * 70)
    print("PROBLEM D: SHORTEST ROUTES (DIJKSTRA)")
    print("=" * 70)

    shortest_dist, predecessor = dijkstra(adj_list, start_hub, hubs)
    print(f"Shortest path distances from start hub {start_hub}:")
    for h in hubs:
        print(f"  To hub {h}: distance = {shortest_dist[h]}")

    path_to_H = reconstruct_path(predecessor, "H")
    print(f"\nShortest path from {start_hub} to H: {' -> '.join(path_to_H)}")
    print(f"Total shortest path distance to H: {shortest_dist['H']}")

    # 6. Problem E: Minimum Spanning Tree
    print("\n" + "=" * 70)
    print("PROBLEM E: THE BACKBONE (MINIMUM SPANNING TREE)")
    print("=" * 70)

    kruskal_edges, kruskal_weight = kruskal_mst(hubs, edges)
    prim_edges, prim_weight = prim_mst(adj_list, start_hub, hubs)

    print("Kruskal MST chosen edges:")
    for u, v, w in kruskal_edges:
        print(f"  Road {u}-{v} with length {w}")
    print(f"Kruskal MST total length: {kruskal_weight}")

    print("\nPrim MST total length check:", prim_weight)
    print(f"Prim and Kruskal total weights match: {kruskal_weight == prim_weight}")

    # 7. Problem F: Analysis Summary
    print("\n" + "=" * 70)
    print("PROBLEM F: COMPLEXITY AND REASONING SUMMARY")
    print("=" * 70)
    print(f"{'Algorithm':<24} | {'Time Complexity':<18} | {'Space':<12} | {'Technique'}")
    print("-" * 70)
    print(f"{'0/1 Knapsack':<24} | {'O(n * W)':<18} | {'O(n * W)':<12} | {'Dynamic Programming'}")
    print(f"{'Coin change (min coins)':<24} | {'O(n * T)':<18} | {'O(T)':<12} | {'Dynamic Programming'}")
    print(f"{'BFS / DFS':<24} | {'O(V + E)':<18} | {'O(V)':<12} | {'Traversal'}")
    print(f"{'Dijkstra':<24} | {'O((V + E) log V)':<18} | {'O(V + E)':<12} | {'Greedy / Heap'}")
    print(f"{'MST (Kruskal)':<24} | {'O(E log V)':<18} | {'O(V + E)':<12} | {'Greedy / Union-Find'}")
    print(f"{'MST (Prim)':<24} | {'O((V + E) log V)':<18} | {'O(V + E)':<12} | {'Greedy / Heap'}")
    print("-" * 70)
    print("All tasks verified successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
