"""
TSP Approximation + Lower Bound (MST 1-tree lower bound)

Computes:
 - Approximate TSP solution
 - Lower bound using MST + two smallest edges from root
 - Delta = approx_cost - lower_bound

Author: Steve Dormady
"""

import time
import random
import csv
import heapq

# -----------------------------
# Read Graph
# -----------------------------
def read_graph_from_stdin():
    first = input().strip()
    if not first:
        raise ValueError("Missing graph size line.")

    V, E = map(int, first.split())
    edges = []
    nodes = set()

    for _ in range(E):
        u, v, w = input().split()
        w = float(w)
        edges.append((u, v, w))
        nodes.add(u)
        nodes.add(v)

    return V, E, edges, nodes

# -----------------------------
# Build distance matrix
# -----------------------------
def build_dist_matrix(V, edges, nodes):
    nodes = sorted(nodes)
    idx = {nodes[i]: i for i in range(V)}

    dist = [[float("inf")] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0.0

    for u, v, w in edges:
        ui, vi = idx[u], idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w

    return dist, nodes, idx


# ============================================================
#     LOWER BOUND: MST + TWO SMALLEST INCIDENT EDGES
# ============================================================
def mst_cost(dist):
    """Prim's algorithm: O(V^2)"""
    V = len(dist)
    visited = [False] * V
    min_edge = [float("inf")] * V
    min_edge[0] = 0
    total = 0.0

    for _ in range(V):
        u = min((i for i in range(V) if not visited[i]), key=lambda i: min_edge[i])
        visited[u] = True
        total += min_edge[u]

        for v in range(V):
            if not visited[v] and dist[u][v] < min_edge[v]:
                min_edge[v] = dist[u][v]

    return total


def lower_bound(dist):
    """
    1-tree lower bound:
        LB = MST + two smallest edges out of root
    """
    V = len(dist)

    mst = mst_cost(dist)

    # get two lightest edges from node 0
    best1, best2 = float("inf"), float("inf")

    for j in range(1, V):
        d = dist[0][j]
        if d < best1:
            best2 = best1
            best1 = d
        elif d < best2:
            best2 = d

    return mst + best1 + best2


# ============================================================
# GREEDY TOUR (nearest neighbor)
# ============================================================
def greedy_tour(dist, start=0):
    n = len(dist)
    visited = [False] * n
    tour = [start]
    visited[start] = True
    cur = start

    for _ in range(n - 1):
        best_v = None
        best_d = float("inf")
        row = dist[cur]

        for v in range(n):
            if not visited[v] and row[v] < best_d:
                best_d = row[v]
                best_v = v

        visited[best_v] = True
        tour.append(best_v)
        cur = best_v

    return tour


# ============================================================
# TWO-OPT
# ============================================================
def tour_cost(tour, dist):
    n = len(tour)
    total = 0.0
    for i in range(n):
        total += dist[tour[i]][tour[(i+1) % n]]
    return total


def two_opt(tour, dist, time_limit, start_time):
    n = len(tour)
    improved = True

    while improved and time.time() - start_time < time_limit:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                if time.time() - start_time >= time_limit:
                    return tour
                a, b = tour[i - 1], tour[i]
                c, d = tour[j], tour[(j + 1) % n]

                old = dist[a][b] + dist[c][d]
                new = dist[a][c] + dist[b][d]

                if new < old:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
                    break
            if improved:
                break

    return tour


# ============================================================
# MULTI-RESTART APPROX TSP
# ============================================================
def approx_tsp(dist, total_time):
    start = time.time()
    n = len(dist)

    best_tour = None
    best_cost = float("inf")

    while time.time() - start < total_time:
        start_node = random.randrange(n)
        tour = greedy_tour(dist, start=start_node)

        remaining = total_time - (time.time() - start)
        if remaining <= 0:
            break

        tour = two_opt(tour, dist, remaining, start)
        c = tour_cost(tour, dist)

        if c < best_cost:
            best_cost = c
            best_tour = tour[:]

    return best_tour, best_cost


# ============================================================
# MAIN
# ============================================================
def main():
    V, E, edges, nodes = read_graph_from_stdin()
    dist, nodes, idx = build_dist_matrix(V, edges, nodes)

    # Compute lower bound
    lb = lower_bound(dist)

    # Approximate solution
    tlimit = 0.1 if V < 1000 else 5.0
    tour, cost = approx_tsp(dist, tlimit)

    # Convert to labels
    tour_labels = [nodes[i] for i in tour] + [nodes[tour[0]]]

    print(f"{cost:.4f}")
    print(" ".join(tour_labels))
    print(f"LOWER_BOUND {lb:.4f}")
    print(f"DELTA {cost - lb:.4f}")      # Difference between approx and LB (required)


if __name__ == "__main__":
    main()
