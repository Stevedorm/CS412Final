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

    # Map labels → indices 0..n-1 based on the labels that actually appear
    nodes = sorted(labels)
    n = len(nodes)
    label_to_index = {nodes[i]: i for i in range(n)}

    # Build adjacency matrix with INF for missing edges
    INF = float("inf")
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0.0

    # Fill in edges
    for u, v, w in raw_edges:
        ui = label_to_index[u]
        vi = label_to_index[v]
        add_edge(mat, ui, vi, w)

    vertices = list(range(n))

    min_cost = float("inf")
    min_path = None

        # BRUTE-FORCE TSP
    # TIME COMPLEXITY: O(n! * n)
    # - itertools.permutations(vertices): generates all n! permutations
    # - Inner loop (for i in range(n)): calculates cost of each n-node tour
    # - Each edge lookup mat[u][v]: O(1) constant time
    # DOMINANT TERM: The n! permutations dominate; for n=13, this is ~6.2 billion operations
    for perm in itertools.permutations(vertices):
        cost = 0.0
        valid = True
        for i in range(n): # n edges in the tour
            u = perm[i] #all constant time operations in loop
            v = perm[(i + 1) % n]  # wrap around to start
            w = mat[u][v]
            if w == INF:
                valid = False
                break
            cost += w
        if valid and cost < min_cost:
            min_cost = cost
            min_path = perm

    # We assume test graphs have at least one Hamiltonian cycle
    # so min_path should not be None here.
    if min_path is None:
        # If this ever happens, something is seriously wrong with the input or assumptions.
        min_cost = 0.0
        min_path = (0,)

    # convert path indices back to labels
    index_to_label = {i: lbl for i, lbl in enumerate(nodes)}
    readable_path = [index_to_label[i] for i in min_path]
    readable_path.append(readable_path[0])   # repeat start at end

    print(f"{min_cost:.4f}")   # 4 decimals
    print(" ".join(readable_path))


def add_edge(mat, i, j, w):
    mat[i][j] = w
    mat[j][i] = w


if __name__ == "__main__":
    main()
