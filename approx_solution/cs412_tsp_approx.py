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


import random
import time
import math

# Strong OS randomness
rng = random.SystemRandom()


def main():
    # Read graph
    V, E, edges, nodes = read_graph_from_stdin()

    # Map node labels → indices 0..V-1
    nodes = sorted(list(nodes))
    idx = {nodes[i]: i for i in range(V)}

    # Build distance matrix
    dist = [[float('inf')] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0.0
    for u, v, w in edges:
        ui = idx[u]
        vi = idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w

    # -------------------------
    # MULTI-START STOCHASTIC GREEDY
    # -------------------------
    # Very fast + much more reliable than 1 run
    if V <= 200:
        K = 10
    elif V <= 600:
        K = 8
    elif V <= 1000:
        K = 4
    else:
        K = 3

    best_cost = float('inf')
    best_tour = None

    for _ in range(K): 
        tour, cost = stochastic_greedy_tsp(dist)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    # Convert back to labels
    tour_labels = [nodes[i] for i in best_tour]
    tour_labels.append(tour_labels[0])

    print(f"{best_cost:.4f}")
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


    """
    Single stochastic greedy TSP run.
    """
def stochastic_greedy_tsp(dist):
    n = len(dist)
    visited = [False] * n

    start = rng.randrange(n)
    current = start
    tour = [start]
    visited[start] = True
    cost = 0.0

    for _ in range(n - 1): #O(n) iterations
        candidates = []
        weights = []

        for v in range(n): #O(n)
            if not visited[v]:
                d = dist[current][v]
                w = 1.0 / (d + 1e-12)
                candidates.append(v)
                weights.append(w)

        next_city = weighted_random_choice(candidates, weights) # O(n)

        visited[next_city] = True
        tour.append(next_city)
        cost += dist[current][next_city]
        current = next_city
        # Total: O(n) + O(n) = O(n) per iteration → O(n^2) total
    cost += dist[current][start]

    return tour, cost



def weighted_random_choice(values, weights):
    """
    Strong randomness + weighted O(n) choice.
    """
    total = sum(weights)
    r = rng.random() * total
    s = 0
    for v, w in zip(values, weights):
        s += w
        if s >= r:
            return v

# FIXED: remove extra spaces
if __name__ == "__main__":
    main()
