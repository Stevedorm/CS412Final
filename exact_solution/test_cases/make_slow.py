#!/usr/bin/env python3
import itertools
import string

def generate_city_names(count):
    """Generate 'aa', 'ab', ... style names until we reach count."""
    letters = string.ascii_lowercase
    name_list = []
    
    # Generate names of increasing length
    length = 4
    while len(name_list) < count:
        for tup in itertools.product(letters, repeat=length):
            name_list.append("".join(tup))
            if len(name_list) == count:
                return name_list
        length += 1  # If we exhaust all 2-letter names, go to 3-letter

    return name_list

def weight(i, j):
    # Deterministic symmetric weights in [1, 10]
    return float(((i + 1) * (j + 3)) % 10 + 1)

# Generate 1000 cities
nodes = generate_city_names(2000)

filename = "tc17_2000_super_duper_slow.in"

with open(filename, "w") as f:
    n = len(nodes)
    m = n * (n - 1) // 2  # complete graph
    f.write(f"{n} {m}\n")
    for i, j in itertools.combinations(range(n), 2):
        u, v = nodes[i], nodes[j]
        w = weight(i, j)
        f.write(f"{u} {v} {w:.1f}\n")

print(f"Wrote {filename}")
