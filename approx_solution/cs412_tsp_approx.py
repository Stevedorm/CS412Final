"""
    name : Your name ( s ) here

    Honor Code and Acknowledgments :
    This work complies with the JMU Honor Code .
    Comments here on your code and submissi on
"""

import random
import time
import math

"""
Example TSP Input
3 3
a b 3.0
b c 4.2
a c 5.4

Next goal forward is to add a timer 

TODO:
Finish slide deck
work on approx notes pdf
work on README
Update code on here to make more readible and add more comments

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
    # if V <= 8:
    #     runtime_limit = None      # One fast greedy run
    # elif V <= 12:
    #     runtime_limit = 0.01      # 10 ms
    # elif V <= 20:
    #     runtime_limit = 0.05      # 50 ms
    # else:
    #     limit = .1 * math.log(V)
    #     runtime_limit = min(limit, 1.5)
        
        
    tour, cost = stochastic_greedy_tsp(dist)

    # Convert indices back to node labels & print final cycle
    tour_labels = [nodes[i] for i in tour]
    # Return to start node:
    tour_labels.append(tour_labels[0])

    # Output format required:
    # Steve - changed this to match format from imported tests
    # Out puts are not the same, but it shouldn't be, right?
    # print(f"Minimum cost: {cost:.4f}")   # 4 decimals
    # print("Minimum path:", tour_labels)
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



def stochastic_greedy_tsp(dist, runtime_limit=None):
    """
    Stochastic nearest-neighbor TSP heuristic.
    Assumes:
      - Complete graph
      - Undirected (dist[u][v] == dist[v][u])
    Runtime: O(n^2)
    Supports anytime mode via runtime_limit.
    """
    n = len(dist)
    best_tour = None
    best_cost = float('inf')

    start_time = time.time()

    while True:
        # Anytime exit condition
        if runtime_limit and (time.time() - start_time) > runtime_limit:
            break

        visited = [False] * n
        start = random.randrange(n)
        current = start

        tour = [start]
        visited[start] = True
        cost = 0.0

        for _ in range(n - 1):
            candidates = []
            weights = []

            # Since the graph is complete, every unvisited vertex is reachable.
            for v in range(n):
                if not visited[v]:
                    d = dist[current][v]
                    # inverse-distance weighting (greedy but stochastic)
                    w = 1.0 / (d + 1e-12)
                    candidates.append(v)
                    weights.append(w)

            # stochastic weighted greedy choice
            next_city = weighted_random_choice(candidates, weights)

            visited[next_city] = True
            tour.append(next_city)

            cost += dist[current][next_city]
            current = next_city

        # close the Hamiltonian cycle
        cost += dist[current][start]

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

        # No time limit? Single run.
        if runtime_limit is None:
            break

    return best_tour, best_cost


def weighted_random_choice(values, weights):
    """Pick one element from values using weights in O(n) time."""
    total = sum(weights)  # O(n)
    r = random.random() * total
    s = 0
    for v, w in zip(values, weights):  # O(n)
        s += w
        if s >= r:
            return v


# FIXED: remove extra spaces
if __name__ == "__main__":
    main()
