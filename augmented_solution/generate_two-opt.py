import matplotlib.pyplot as plt
import math

# 6 cities on a circle
n = 6
angles = [2 * math.pi * k / n for k in range(n)]
xs = [math.cos(a) for a in angles]
ys = [math.sin(a) for a in angles]

base_order = list(range(n))
original_tour = base_order + [base_order[0]]

# 2-opt: reverse segment between positions i and j in the base_order
i, j = 1, 4
new_order = base_order[:i] + list(reversed(base_order[i:j+1])) + base_order[j+1:]
new_tour = new_order + [new_order[0]]

plt.figure(figsize=(5, 5))

# Original tour
for a, b in zip(original_tour[:-1], original_tour[1:]):
    plt.plot([xs[a], xs[b]], [ys[a], ys[b]], linestyle="solid", linewidth=1.5,
             label="Original tour" if a == original_tour[0] else "")

# After 2-opt
for a, b in zip(new_tour[:-1], new_tour[1:]):
    plt.plot([xs[a], xs[b]], [ys[a], ys[b]], linestyle="dashed", linewidth=1.5,
             label="After 2-opt" if a == new_tour[0] else "")

plt.scatter(xs, ys, s=40)
for idx, (x, y) in enumerate(zip(xs, ys)):
    plt.text(x, y, f"{idx}", fontsize=10, ha="center", va="center")

plt.axis("equal")
plt.title("2-opt Swap: Original vs After Swap")
plt.legend()
plt.tight_layout()
plt.savefig("two_opt_example.png", dpi=200)
