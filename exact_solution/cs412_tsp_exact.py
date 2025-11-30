"""
    name:  Daniel Holtschneider

    Honor Code and Acknowledgments:

        This work complies with the JMU Honor Code.

        Comments here on your code and submission.
"""

def main():
    # First line: declared number of vertices and edges.
    # We don't *trust* the vertex count blindly; we infer the actual
    # labels from the edges that appear.
    first = input().strip()
    if not first:
        return

    declared_n, m = map(int, first.split())

    raw_edges = []
    labels = set()

    # Read edges as (label_u, label_v, weight)
    for _ in range(m):
        line = input().strip()
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

    # Build adjacency matrix; INF means "no direct edge"
    INF = float("inf")
    mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0.0

    for u, v, w in raw_edges:
        ui = label_to_index[u]
        vi = label_to_index[v]
        add_edge(mat, ui, vi, w)

    # Run Held–Karp exact TSP with fixed start at vertex 0
    min_cost, path_indices = held_karp(mat)

    # Map indices back to labels
    index_to_label = {idx: lbl for lbl, idx in label_to_index.items()}
    path_labels = [index_to_label[i] for i in path_indices]
    path_labels.append(path_labels[0])  # close the tour

    # REQUIRED output format:
    # line 1: cost (4 decimals)
    # line 2: labels separated by spaces, start repeated at end
    print(f"{min_cost:.4f}")
    print(" ".join(path_labels))


def add_edge(mat, i, j, w):
    mat[i][j] = w
    mat[j][i] = w


def held_karp(mat):
    """
    Exact TSP using Held–Karp DP.

    Time:  O(n^2 * 2^(n-1))
    Space: O(n * 2^(n-1))

    We fix the start vertex to 0 and only consider subsets of {1..n-1}.
    """
    n = len(mat)
    if n == 1:
        return 0.0, [0]

    INF = float("inf")
    # dp[(mask, j)] = (cost, prev)
    # mask encodes subset of {1..n-1}; bit (j-1) corresponds to city j.
    dp = {}

    # Base cases: paths 0 -> j with {j} visited
    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[(mask, j)] = (mat[0][j], 0)

    # Build DP for larger subsets
    for mask in range(1, 1 << (n - 1)):
        for j in range(1, n):
            bit_j = 1 << (j - 1)
            if not (mask & bit_j):
                continue
            if (mask, j) not in dp:
                continue
            cost_j, _ = dp[(mask, j)]

            # Extend to a new city k not yet in mask
            for k in range(1, n):
                bit_k = 1 << (k - 1)
                if mask & bit_k:
                    continue
                new_mask = mask | bit_k
                new_cost = cost_j + mat[j][k]
                key = (new_mask, k)
                if key not in dp or new_cost < dp[key][0]:
                    dp[key] = (new_cost, j)

    # Close the tour back to 0
    full_mask = (1 << (n - 1)) - 1
    best_cost = INF
    best_last = None

    for j in range(1, n):
        key = (full_mask, j)
        if key not in dp:
            continue
        cost_j, _ = dp[key]
        total_cost = cost_j + mat[j][0]
        if total_cost < best_cost:
            best_cost = total_cost
            best_last = j

    if best_last is None:
        # Graph is disconnected or no Hamiltonian cycle; fall back gracefully
        return INF, [0]

    # Reconstruct path 0 -> ... -> best_last
    mask = full_mask
    j = best_last
    order = [j]
    while True:
        cost_j, prev = dp[(mask, j)]
        if prev == 0:
            break
        order.append(prev)
        mask ^= 1 << (j - 1)
        j = prev

    path = [0] + list(reversed(order))  # without the final 0
    return best_cost, path


if __name__ == "__main__":
    main()
