"""
    name:  Daniel Holtschneider

    Honor Code and Acknowledgments:

        This work complies with the JMU Honor Code.

        Comments here on your code and submission.
"""
import sys
import itertools


def main():
    first = sys.stdin.readline().strip()
    if not first:
        return

    declared_n, m = map(int, first.split())

    raw_edges = []
    labels = set()

    # Read all edges, collect labels
    for _ in range(m):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        u, v, w = line.split()
        w = float(w)
        raw_edges.append((u, v, w))
        labels.add(u)
        labels.add(v)

    # Map labels → indices 0..n-1 based on actual labels
    nodes = sorted(labels)
    n = len(nodes)
    label_to_index = {nodes[i]: i for i in range(n)}

    # Build adjacency matrix with INF for missing edges
    INF = float("inf")
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0.0

    # Fill edges (undirected)
    for u, v, w in raw_edges:
        ui = label_to_index[u]
        vi = label_to_index[v]
        add_edge(mat, ui, vi, w)

    vertices = list(range(n))

    best_cost = float("inf")
    best_perm = None

    # PURE BRUTE FORCE: try every tour (n! permutations)
    for perm in itertools.permutations(vertices):
        cost = 0.0
        valid = True
        for i in range(n):
            u = perm[i]
            v = perm[(i + 1) % n]  # wrap back to start
            w = mat[u][v]
            if w == INF:
                valid = False
                break
            cost += w
        if valid and cost < best_cost:
            best_cost = cost
            best_perm = perm

    # We assume tests for exact TSP have a Hamiltonian cycle
    if best_perm is None:
        # No tour – fall back to something non-crashy
        best_cost = 0.0
        best_perm = (0,)

    # Convert back to labels
    index_to_label = {i: lbl for i, lbl in enumerate(nodes)}
    readable_path = [index_to_label[i] for i in best_perm]
    readable_path.append(readable_path[0])

    print(f"{best_cost:.4f}")
    print(" ".join(readable_path))


def add_edge(mat, i, j, w):
    mat[i][j] = w
    mat[j][i] = w


if __name__ == "__main__":
    main()
