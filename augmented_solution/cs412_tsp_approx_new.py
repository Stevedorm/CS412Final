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
    # Read graph from stdin: O(E)
    V, E, edges, nodes = read_graph_from_stdin()

    # Sort labels and build map label -> index
    nodes = sorted(nodes)
    idx = {label: i for i, label in enumerate(nodes)}

    # Build full distance matrix: O(V^2)
    dist = [[float("inf")] * V for _ in range(V)]

    for i in range(V):
        dist[i][i] = 0.0

    for u, v, w in edges:
        ui = idx[u]
        vi = idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w
    if (V < 1000):
        best_tour, best_cost, per_run_costs, history = approx_tsp(dist, total_time=0.1)
    else:
        best_tour, best_cost, per_run_costs, history = approx_tsp(dist, total_time=5.0)


    tour_labels = [nodes[i] for i in best_tour]
    tour_labels.append(tour_labels[0])

    print(f"{best_cost:.4f}")
    print(" ".join(tour_labels))

    write_stats(per_run_costs, history, prefix="new")



def read_graph_from_stdin():
    """
    Reads:
        First line: V E
        Next E lines: u v w
    Runtime: O(E) to read all edges + O(V + E) to build sets/lists.
    """
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
    """
    Compute cost of a tour (cycle).
    Loop over n vertices and sum 2 edges per step → O(n).
    """
    n = len(tour)
    total = 0.0
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        total += dist[u][v]
    return total


def greedy_tour(dist, start=0):
    """
    Nearest-neighbor tour starting at `start`.

    Runtime analysis:
        Let n = number of vertices.
        - visited list allocation: O(n)
        - Outer loop runs (n - 1) times → O(n)
        - Inner loop scans all n vertices each time → O(n) per outer iteration
        ⇒ Total time: O(n) * O(n) = O(n^2)
    """
    n = len(dist)
    # O(n): allocate and initialize list of length n
    visited = [False] * n
    tour = [start]        
    visited[start] = True 
    current = start       

    # Outer loop: selects the next city (n - 1) times → O(n)
    for _ in range(n - 1):
        best_v = None
        best_d = float("inf")
        row = dist[current]

        # Inner loop: scan all cities to find nearest unvisited → O(n)
        for v in range(n):
            if not visited[v]:    
                d = row[v]        
                if d < best_d:    
                    best_d = d
                    best_v = v

        visited[best_v] = True   
        tour.append(best_v)
        current = best_v
    # Overall: O(n^2) time, O(n) extra space
    return tour


def two_opt(tour, dist, runtime_limit=None, start_time=None):
    """
    2-opt local search. Improves a tour by reversing segments.
    First-improvement strategy, stops when no improvement or time limit.

    Runtime analysis (per call):
        Let n = length of the tour.

        - The nested loops over (i, j) examine O(n^2) edge pairs.
        - For each improving move, we reverse a segment tour[i:j+1] in O(n) time.
        - Let R be the number of improving moves until no better 2-opt move exists.
            In the worst case, R can be O(n).
        ⇒ Worst-case time: O(R * n^2) ≤ O(n^3)
        In practice, R is usually much smaller, and 2-opt behaves closer to O(n^2).
    """
    if start_time is None:
        start_time = time.time()
    n = len(tour)
    improved = True
    # Each iteration of this while-loop corresponds to at least one improving 2-opt move.
    while improved:
        improved = False
        # Outer loop: i ranges over positions in the tour → O(n)
        for i in range(1, n - 2):
            a = tour[i - 1]
            b = tour[i]
            # Inner loop: j ranges over positions after i → O(n)
            for j in range(i + 1, n - 1):
                # Time limit check is O(1)
                if runtime_limit is not None and time.time() - start_time > runtime_limit:
                    return tour
                c = tour[j]
                d = tour[(j + 1) % n]
                old_cost = dist[a][b] + dist[c][d]
                new_cost = dist[a][c] + dist[b][d]
                if new_cost + 1e-12 < old_cost:
                    # Apply the 2-opt move.
                    # Reversing a slice of length k costs O(k), worst-case O(n).
                    tour[i : j + 1] = reversed(tour[i : j + 1])
                    improved = True
                    break  # restart search from scratch
            if improved:
                break
    # Overall worst-case: O(n^3); typical performance often closer to O(n^2).
    return tour


def approx_tsp(dist, total_time=0.0):
    """
    Advanced Part E approximation:
      - Multi-restart greedy + 2-opt within a global time budget.
      - Tracks:
          * per_run_costs: cost from each restart (for variance)
          * history: (elapsed_time, best_cost_so_far) for best-vs-time plot

    Runtime analysis:
      Let n be the number of vertices.
      For each restart:
        - GREEDY_TOUR: O(n^2)
        - TWO_OPT: worst-case O(n^3), typically closer to O(n^2)
        - TOUR_COST: O(n)

      If we perform R restarts within the time budget:
        - Worst-case: O(R * n^3)
        - In practice, R is bounded by total_time, so runtime is effectively
          min(algorithm work, time budget).
    """
    start_time = time.time()
    best_cost = float("inf")
    best_tour = None
    per_run_costs = []  # one cost per restart
    history = []        # (elapsed_time, best_cost_so_far)
    n = len(dist)

    # Multi-restart loop: number of iterations R is limited by total_time.
    while time.time() - start_time < total_time:
        # New starting tour: greedy from a random start node → O(n^2)
        start_node = random.randrange(n)
        tour = greedy_tour(dist, start=start_node)

        remaining = total_time - (time.time() - start_time)
        if remaining <= 0:
            break
        # Local improvement with 2-opt → worst-case O(n^3)
        tour = two_opt(tour, dist, runtime_limit=remaining, start_time=start_time)
        # Compute cost of this tour → O(n)
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


def write_stats(per_run_costs, history, prefix="partE"):
    """
    Write CSV files for Part E:
      - prefix_runs.csv:       run_index, cost
      - prefix_history.csv:    elapsed_time, best_cost

    Complexity:
      - Writing runs:    O(R) where R = number of restarts
      - Writing history: O(H) where H = number of history samples
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
