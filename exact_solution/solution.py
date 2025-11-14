import itertools
"""
    name:  Daniel Holtschneider

    Honor Code and Acknowledgments:

            This work complies with the JMU Honor Code.

           Comments here on your code and submission.
"""
import itertools


def main():
    n, m = map(int, input().strip().split())
    mat = [[0] * n for _ in range(n)]

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

    min_cost = float('inf')
    min_path = []

    # brute-force TSP
    for perm in itertools.permutations(vertices):
        cost = 0
        for i in range(n):
            u = perm[i]
            v = perm[(i + 1) % n]
            cost += mat[u][v]
        if cost < min_cost:
            min_cost = cost
            min_path = perm

    # convert path indices back to labels (FIXED: now inside main)
    index_to_label = {v: k for k, v in label_to_index.items()}
    readable_path = [index_to_label[i] for i in min_path]
    readable_path.append(readable_path[0])   # repeat start at end

    print(f"Minimum cost: {min_cost:.4f}")   # 4 decimals
    print("Minimum path:", readable_path)


def add_edge(mat, i, j, w):
    mat[i][j] = w
    mat[j][i] = w


if __name__ == "__main__":
    main()
