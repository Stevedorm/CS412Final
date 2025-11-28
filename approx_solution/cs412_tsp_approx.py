"""
    name : Your name ( s ) here

    Honor Code and Acknowledgments :
    This work complies with the JMU Honor Code .
    Comments here on your code and submission
"""

import random
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
    tour, cost = stochastic_greedy_tsp(dist)

    # Convert indices back to node labels & print final cycle
    tour_labels = [nodes[i] for i in tour]
    # Return to start node:
    tour_labels.append(tour_labels[0])

    # Output format required:
    # Steve - changed this to match format from imported tests
    # Out puts are not the same, but it shouldn't be, right?
    print(f"Minimum cost: {cost:.4f}")   # 4 decimals
    print("Minimum path:", tour_labels)
    # print(f"{cost:.4f}")
    # print(" ".join(tour_labels))



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




def stochastic_greedy_tsp(dist, runtime_limit=None):
    """Stochastic nearest-neighbor with inverse-distance weighting.
       Runtime: O(n^2). Works for n > 1000.
    """
    n = len(dist)
    best_tour = None
    best_cost = float('inf')

    start_time = time.time()
    while True:
        if runtime_limit and time.time() - start_time > runtime_limit:
            break

        visited = [False] * n
        start = random.randrange(n)
        tour = [start]
        visited[start] = True
        cost = 0.0
        current = start

        for _ in range(n - 1):
            candidates = []
            weights = []

            for v in range(n):
                if not visited[v]:
                    d = dist[current][v]
                    # Inverse-distance weighting encourages greedy behavior
                    w = 1.0 / (d + 1e-12)
                    candidates.append(v)
                    weights.append(w)

            next_city = random.choices(candidates, weights=weights)[0]
            visited[next_city] = True
            tour.append(next_city)
            cost += dist[current][next_city]
            current = next_city

        # Close the tour
        cost += dist[current][start]

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

        # If no anytime limit, only run once
        if not runtime_limit:
            break

    return best_tour, best_cost



# FIXED: remove extra spaces
if __name__ == "__main__":
    main()
