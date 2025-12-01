"""
    name:  Daniel Holtschneider

    Honor Code and Acknowledgments:

        This work complies with the JMU Honor Code.

        Comments here on your code and submission.
"""
import itertools


def main():
    n, m = map(int, input().strip().split())
    INF = float("inf")
    mat = [[INF] * n for _ in range(n)]

    # map vertex labels (letters) → integer indices
    label_to_index = {}
    current_index = 0

    def get_index(label):
        nonlocal current_index
        if label not in label_to_index:
            label_to_index[label] = current_index
            current_index += 1
        return label_to_index[label]

    # read edges
    for _ in range(m):
        u, v, w = input().strip().split()
        ui = get_index(u)       # convert label → index
        vi = get_index(v)       # convert label → index
        w = float(w)            # weight can be a double
        add_edge(mat, ui, vi, w)

    vertices = list(range(n))

    min_cost = INF
    min_path = None  # None means "no tour found yet"

    # brute-force TSP
    for perm in itertools.permutations(vertices):
        cost = 0.0
        valid = True

        for i in range(n):
            u = perm[i]
            v = perm[(i + 1) % n]
            w = mat[u][v]
            if w == INF:
                valid = False
                break  # this tour uses a missing edge, skip it
            cost += w

        if valid and cost < min_cost:
            min_cost = cost
            min_path = perm

    # If no Hamiltonian cycle exists, avoid crashing
    if min_path is None:
        # Fallback: pick some existing vertex if we have any labels
        if label_to_index:
            # take the first index we assigned
            start_index = next(iter(label_to_index.values()))
            min_path = (start_index,)
            # there is no tour, so cost is 0 or whatever convention you prefer
            min_cost = 0.0
        else:
            # truly degenerate case (no labels/edges)
            min_path = ()
            min_cost = 0.0

    # convert path indices back to labels
    index_to_label = {v: k for k, v in label_to_index.items()}
    readable_path = [index_to_label[i] for i in min_path] if min_path else []

    # repeat start at end if we have at least one vertex
    if readable_path:
        readable_path.append(readable_path[0])

    print(f"{min_cost:.4f}")   # 4 decimals
    print(" ".join(readable_path))


def add_edge(mat, i, j, w):
    mat[i][j] = w
    mat[j][i] = w


if __name__ == "__main__":
    main()
