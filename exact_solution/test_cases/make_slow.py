#!/usr/bin/env python3
import itertools

# 13 cities: A .. M
nodes = [chr(ord('a') + i) for i in range(13)]  # ['A', 'B', ..., 'M']

def weight(i, j):
    # Deterministic symmetric weights in [1, 10]
    return float(((i + 1) * (j + 3)) % 10 + 1)

filename = "tc13_super_slow_13nodes.in"

with open(filename, "w") as f:
    n = len(nodes)
    m = n * (n - 1) // 2
    f.write(f"{n} {m}\n")
    for i, j in itertools.combinations(range(n), 2):
        u, v = nodes[i], nodes[j]
        w = weight(i, j)
        f.write(f"{u} {v} {w:.1f}\n")

print(f"Wrote {filename}")
