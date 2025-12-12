#!/usr/bin/env python3
"""
collect_lower_bounds.py

Scans test_cases/input/*.in, runs your approx TSP solver,
computes a simple MST-based lower bound, and writes results
to test_cases/lower_bound_results.csv.

CSV columns:
    test_case, input_size, lower_bound, approx_cost, delta, runtime_seconds
"""

import os
import glob
import time
import csv

from cs412_tsp_approx_new import approx_tsp  # uses your existing code


INPUT_DIR = "test_cases/input"
CSV_OUT   = "test_cases/lower_bound_results.csv"


def read_graph_from_file(path):
    """Read graph from a .in file. Same format as stdin version."""
    with open(path) as f:
        first = f.readline().strip()
        if not first:
            raise ValueError(f"{path}: missing 'V E' line")
        V, E = map(int, first.split())

        edges = []
        nodes = set()
        for _ in range(E):
            line = f.readline().strip()
            if not line:
                raise ValueError(f"{path}: missing or empty edge line.")
            u, v, w = line.split()
            w = float(w)
            edges.append((u, v, w))
            nodes.add(u)
            nodes.add(v)

    return V, E, edges, nodes


def build_dist_matrix(V, edges, nodes):
    """Build full V×V distance matrix from edges."""
    nodes = sorted(nodes)
    label_to_idx = {label: i for i, label in enumerate(nodes)}

    dist = [[float("inf")] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0.0

    for u, v, w in edges:
        ui = label_to_idx[u]
        vi = label_to_idx[v]
        dist[ui][vi] = w
        dist[vi][ui] = w

    return dist, nodes


def mst_lower_bound(dist):
    """
    Prim's algorithm on the complete graph given by dist.
    Lower bound: cost of MST (every TSP tour contains a spanning tree).
    Runtime: O(V^2)
    """
    V = len(dist)
    in_mst = [False] * V
    key = [float("inf")] * V
    key[0] = 0.0
    total = 0.0

    for _ in range(V):
        # pick next vertex with smallest key not in MST
        u = None
        best_key = float("inf")
        for i in range(V):
            if not in_mst[i] and key[i] < best_key:
                best_key = key[i]
                u = i
        in_mst[u] = True
        total += key[u]

        # relax edges
        row = dist[u]
        for v in range(V):
            if not in_mst[v] and row[v] < key[v]:
                key[v] = row[v]

    return total


def main():
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.in")))
    os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)

    with open(CSV_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["test_case", "input_size", "lower_bound",
             "approx_cost", "delta", "runtime_seconds"]
        )

        for path in files:
            base = os.path.basename(path)
            test_case = os.path.splitext(base)[0]

            V, E, edges, nodes = read_graph_from_file(path)
            dist, _ = build_dist_matrix(V, edges, nodes)

            start = time.perf_counter()
            # use same time budget logic as your main program
            total_time = 0.1 if V < 1000 else 5.0
            best_tour, best_cost, _, _ = approx_tsp(dist, total_time=total_time)
            runtime = time.perf_counter() - start

            lb = mst_lower_bound(dist)
            delta = best_cost - lb

            writer.writerow(
                [test_case, V, f"{lb:.6f}", f"{best_cost:.6f}", f"{delta:.6f}", f"{runtime:.6f}"]
            )
            print(f"{test_case}: n={V}, LB={lb:.3f}, cost={best_cost:.3f}, Δ={delta:.3f}, t={runtime:.3f}s")

    print(f"\nWrote CSV to {CSV_OUT}")


if __name__ == "__main__":
    main()
