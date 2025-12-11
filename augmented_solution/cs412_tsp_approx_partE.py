"""
    Name : Steve Dormady

    Honor Code and Acknowledgments :
    
        This work complies with the JMU Honor Code .
        Comments here on your code and submission
"""

import time

"""
Example TSP Input
3 3
a b 3.0
b c 4.2
a c 5.4

Next goal forward is to add a timer 

"""


def main():
    # Read graph
    V, E, edges, nodes = read_graph_from_stdin()

    # Map node labels → indices 0..V-1
    nodes = sorted(list(nodes))
    idx = {nodes[i]: i for i in range(V)}

    # Build full distance matrix (initialize with infinities)
    dist = [[float('inf')] * V for _ in range(V)]

    # Distance from node to itself = 0
    for i in range(V):
        dist[i][i] = 0.0

    # Fill edges (undirected)
    for u, v, w in edges:
        ui = idx[u]
        vi = idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w

    # Run approximation algorithm
    tour, cost = approx_tsp(dist, runtime_limit=None)

    # Convert indices back to node labels & print final cycle
    tour_labels = [nodes[i] for i in tour]
    # Return to start node:
    tour_labels.append(tour_labels[0])

    # Output format required:
    print(f"{cost:.4f}")
    print(" ".join(tour_labels))



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


import time

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
    """
    Nearest-neighbor tour starting at `start`.

    Runtime Notes:
        Let n = number of cities (len(dist)).

        - Outer loop runs (n - 1) times (we choose one new city each step) → O(n).
        - In each iteration, we scan all n cities to find the nearest unvisited neighbor → O(n).
        - Total runtime: O(n) * O(n) = O(n^2).
    """
    n = len(dist)  
    visited = [False] * n  # O(n) to allocate and initialize the list, doesn't effect asymptotic runtime
    tour = [start]         
    visited[start] = True  
    current = start        

    # Outer loop: runs (n - 1) times → O(n)
    for _ in range(n - 1):
        best_v = None
        best_d = float("inf")
        row = dist[current]

        # Inner loop: scan all vertices to find nearest unvisited neighbor → O(n)
        for v in range(n):
            if not visited[v]:          
                d = row[v]
                if d < best_d:
                    best_d = d
                    best_v = v
        visited[best_v] = True
        tour.append(best_v)
        current = best_v
    # Overall:
    #   - Outer loop: O(n)
    #   - Inner loop: O(n) per outer iteration
    #   → Total: O(n^2)

    return tour

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

    Runtime Notes:
        - Let n = number of cities.
        - The nested (i, j) loops enumerate O(n^2) edge pairs.
        - Each improving move reverses a tour segment in O(n) time.
        - If R improving moves occur, total runtime is O(R * n^2).
        - Worst-case 2-opt runtime is O(n^3), though typical performance is closer to O(n^2).
    """
    if start_time is None:
        start_time = time.time()
    n = len(tour)
    improved = True
    while improved:
        improved = False
        # Outer loop over indices i → O(n)
        for i in range(1, n - 2):
            a = tour[i - 1]
            b = tour[i]
            # Inner loop over indices j → O(n)
            for j in range(i + 1, n - 1):
                if runtime_limit is not None and time.time() - start_time > runtime_limit:
                    return tour
                c = tour[j]
                d = tour[(j + 1) % n]
                # Cost change check — constant-time operations
                old_cost = dist[a][b] + dist[c][d]
                new_cost = dist[a][c] + dist[b][d]
                # If reversing segment improves the tour
                if new_cost + 1e-12 < old_cost:
                    # Reversing tour[i : j+1] costs O(k), where k = j - i + 1 (worst-case O(n))
                    tour[i : j + 1] = reversed(tour[i : j + 1])
                    improved = True
                    break   # restart search from scratch (does not change asymptotic cost)
            if improved:
                break   # break outer loop to restart from i = 1
    return tour


def approx_tsp(dist, runtime_limit=None):
    """
    Greedy + 2-opt TSP heuristic.
    - Build a nearest-neighbor tour.
    - Improve with 2-opt until no better move or time limit.
    """
    start_time = time.time()

    # 1) greedy starting at node 0 (could randomize if you want)
    tour = greedy_tour(dist, start=0)

    # 2) local improvement
    remaining = None
    if runtime_limit is not None:
        remaining = max(0.0, runtime_limit - (time.time() - start_time))

    tour = two_opt(tour, dist, runtime_limit=remaining, start_time=start_time)
    cost = tour_cost(tour, dist)
    return tour, cost


if __name__ == "__main__":
    main()
