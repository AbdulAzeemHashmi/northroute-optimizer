"""
Script to generate visual figures for the Assignment 3 report.
Generates:
1. road_network.png - Graph with all 13 weighted roads and MST highlighted
2. knapsack_table.png - Knapsack DP table visualization
3. dijkstra_tree.png - Shortest path tree from hub F
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Set standard styles
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"


def generate_network_plot():
    G = nx.Graph()
    hubs = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for h in hubs:
        G.add_node(h)

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
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # Coordinated 2D layout for hubs
    pos = {
        "A": (0.5, 3.5),
        "B": (2.0, 4.0),
        "C": (1.8, 2.5),
        "D": (3.5, 3.2),
        "E": (4.0, 1.8),
        "F": (5.5, 2.5),
        "G": (6.8, 1.5),
        "H": (7.5, 3.2)
    }

    mst_edges = [
        ("B", "C"),
        ("B", "D"),
        ("D", "E"),
        ("F", "G"),
        ("A", "C"),
        ("E", "F"),
        ("G", "H")
    ]
    mst_set = set(tuple(sorted(e)) for e in mst_edges)

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)

    # Separate edges into MST and non-MST
    non_mst_edges = [e for e in G.edges() if tuple(sorted(e)) not in mst_set]

    # Draw non-MST edges
    nx.draw_networkx_edges(
        G, pos, edgelist=non_mst_edges,
        width=1.8, alpha=0.45, edge_color="#7f8c8d", style="dashed", ax=ax
    )
    # Draw MST edges
    nx.draw_networkx_edges(
        G, pos, edgelist=mst_edges,
        width=3.5, alpha=0.9, edge_color="#27ae60", ax=ax
    )

    # Draw regular nodes
    regular_nodes = [h for h in hubs if h != "F"]
    nx.draw_networkx_nodes(
        G, pos, nodelist=regular_nodes,
        node_size=650, node_color="#3498db", edgecolors="#2c3e50", linewidths=1.8, ax=ax
    )
    # Draw start node F with distinctive color
    nx.draw_networkx_nodes(
        G, pos, nodelist=["F"],
        node_size=800, node_color="#e74c3c", edgecolors="#962d22", linewidths=2.2, ax=ax
    )

    # Node labels
    nx.draw_networkx_labels(
        G, pos, font_size=11, font_weight="bold", font_color="white", ax=ax
    )

    # Edge labels
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=9, font_color="#2c3e50",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#bdc3c7", lw=0.8), ax=ax
    )

    ax.set_title("NorthRoute Road Network (Red: Start Hub F | Green Solid: MST Backbone | Total Weight = 17)", fontsize=11, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("road_network.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("road_network.png saved.")


def generate_knapsack_heatmap():
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
    W = 18
    n = len(parcels)
    table = np.zeros((n + 1, W + 1), dtype=int)

    for i in range(1, n + 1):
        name, wt, val = parcels[i - 1]
        for w in range(W + 1):
            if wt > w:
                table[i, w] = table[i - 1, w]
            else:
                table[i, w] = max(table[i - 1, w], table[i - 1, w - wt] + val)

    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    im = ax.imshow(table, cmap="YlGnBu", aspect="auto")

    # Annotate values
    for i in range(n + 1):
        for w in range(W + 1):
            color = "white" if table[i, w] > 15 else "black"
            ax.text(w, i, str(table[i, w]), ha="center", va="center", color=color, fontsize=7)

    y_labels = ["0 (None)"] + [f"{p[0]} (w={p[1]}, v={p[2]})" for p in parcels]
    ax.set_yticks(range(n + 1))
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.set_xticks(range(W + 1))
    ax.set_xticklabels(range(W + 1), fontsize=8)

    ax.set_xlabel("Knapsack Capacity w (0 to 18)", fontsize=9, fontweight="bold")
    ax.set_ylabel("Parcel Index i Included", fontsize=9, fontweight="bold")
    ax.set_title("Problem A: 0/1 Knapsack DP Tabulation Grid (Optimal Value K(8, 18) = 26)", fontsize=10, fontweight="bold")

    plt.colorbar(im, ax=ax, fraction=0.025, pad=0.03)
    plt.tight_layout()
    plt.savefig("knapsack_table.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("knapsack_table.png saved.")


if __name__ == "__main__":
    generate_network_plot()
    generate_knapsack_heatmap()
