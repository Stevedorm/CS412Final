"""
    Name : Steve Dormady

    Honor Code and Acknowledgments :
    
        This work complies with the JMU Honor Code .
        Comments here on your code and submission
"""

import time
import random
import csv


def main():
    # Read graph
    V, E, edges, nodes = read_graph_from_stdin()

    # Map node labels → indices 0..V-1
    nodes = sorted(list(nodes))
    idx = {nodes[i]: i for i in range(V)}

    # Build full distance matrix (initialize with infinities)
    dist = [[float("inf")] * V for _ in range(V)]

    # Distance from node to itself = 0
    for i in range(V):
        dist[i][i] = 0.0

    # Fill edges (undirected)
    for u, v, w in edges:
        ui = idx[u]
        vi = idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w

    # Run advanced approximation algorithm (multi-restart + tracking)
    best_tour, best_cost, per_run_costs, history = approx_tsp(dist, total_time=5.0)

    # Convert indices back to node labels & print final cycle
    tour_labels = [nodes[i] for i in best_tour]
    tour_labels.append(tour_labels[0])  # return to start node

    # --- REQUIRED stdout format for autograder ---
    print(f"{best_cost:.4f}")
    print(" ".join(tour_labels))

    # --- Extra: write stats for Part E plots (no extra stdout noise) ---
    write_partE_stats(per_run_costs, history, prefix="partE")


def read_graph_from_stdin():
    first = input().strip()
    if not first:
        raise ValueError("Missing graph size line (expected: V E).")

    V, E = map(int, first.split())

    edges = []
    nodes = set()

    for _ in range(E):
        line = input().strip()
        if not line:
            raise ValueError("Missing or empty edge line.")

        u, v, w = line.split()
        w = float(w)

        edges.append((u, v, w))
        nodes.add(u)
        nodes.add(v)

    return V, E, edges, nodes


def tour_cost(tour, dist):
    """Compute cost of a tour (cycle)."""
    n = len(tour)
    total = 0.0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        total += dist[u][v]
    return total


def greedy_tour(dist, start=0):
    """Nearest-neighbor tour starting at `start`. O(n^2)."""
    n = len(dist)
    visited = [False] * n
    tour = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        best_v = None
        best_d = float("inf")
        row = dist[current]
        for v in range(n):
            if not visited[v]:
                d = row[v]
                if d < best_d:
                    best_d = d
                    best_v = v
        visited[best_v] = True
        tour.append(best_v)
        current = best_v

    return tour


def two_opt(tour, dist, runtime_limit=None, start_time=None):
    """
    2-opt local search. Improves a tour by reversing segments.
    First-improvement strategy, stops when no improvement or time limit.
    """
    if start_time is None:
        start_time = time.time()

    n = len(tour)
    improved = True

    while improved:
        improved = False
        # we keep the start fixed at index 0 to avoid equivalent rotations
        for i in range(1, n - 2):
            a = tour[i - 1]
            b = tour[i]
            for j in range(i + 1, n - 1):
                if runtime_limit is not None and time.time() - start_time > runtime_limit:
                    return tour

                c = tour[j]
                d = tour[(j + 1) % n]

                # Cost delta if we reverse segment [i..j]
                old_cost = dist[a][b] + dist[c][d]
                new_cost = dist[a][c] + dist[b][d]

                if new_cost + 1e-12 < old_cost:
                    # Apply the 2-opt move
                    tour[i : j + 1] = reversed(tour[i : j + 1])
                    improved = True
                    break  # restart search from scratch
            if improved:
                break

    return tour


def approx_tsp(dist, total_time=5.0):
    """
    Advanced Part E approximation:
      - Multi-restart greedy + 2-opt within a global time budget.
      - Tracks:
          * per_run_costs: cost from each restart (for variance)
          * history: (elapsed_time, best_cost_so_far) for best-vs-time plot
    """
    start_time = time.time()
    best_cost = float("inf")
    best_tour = None

    per_run_costs = []  # one cost per restart
    history = []        # (elapsed_time, best_cost_so_far)

    n = len(dist)

    while time.time() - start_time < total_time:
        # new starting tour: greedy from a random start node
        start_node = random.randrange(n)
        tour = greedy_tour(dist, start=start_node)

        remaining = total_time - (time.time() - start_time)
        if remaining <= 0:
            break

        tour = two_opt(tour, dist, runtime_limit=remaining, start_time=start_time)
        cost = tour_cost(tour, dist)
        per_run_costs.append(cost)

        if cost < best_cost:
            best_cost = cost
            best_tour = list(tour)

        elapsed = time.time() - start_time
        history.append((elapsed, best_cost))

    # Safety fallback: if time budget was too tiny and we never improved
    if best_tour is None:
        tour = greedy_tour(dist, start=0)
        tour = two_opt(tour, dist)
        best_tour = tour
        best_cost = tour_cost(tour, dist)
        if not history:
            history.append((time.time() - start_time, best_cost))
        if not per_run_costs:
            per_run_costs.append(best_cost)

    return best_tour, best_cost, per_run_costs, history


def write_partE_stats(per_run_costs, history, prefix="partE"):
    """
    Write CSV files for Part E:
      - prefix_runs.csv:       run_index, cost
      - prefix_history.csv:    elapsed_time, best_cost
    These are for plotting variance and best-cost vs time.
    """
    # Per-run costs (for variance)
    with open(f"{prefix}_runs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["run_index", "cost"])
        for i, c in enumerate(per_run_costs):
            writer.writerow([i, f"{c:.6f}"])

    # Best-so-far vs time
    with open(f"{prefix}_history.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["elapsed_time", "best_cost"])
        for t, c in history:
            writer.writerow([f"{t:.6f}", f"{c:.6f}"])


if __name__ == "__main__":
    main()
