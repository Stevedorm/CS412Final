#!/usr/bin/env python3
"""
plot_lower_bounds.py

Reads test_cases/lower_bound_results.csv and produces two plots:
  1) lb_vs_cost.png : input_size vs lower_bound & approx_cost
  2) delta_vs_n.png : input_size vs (approx_cost - lower_bound)
"""

import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_FILE = "test_cases/lower_bound_results.csv"

input_sizes = []
lower_bounds = []
approx_costs = []
deltas = []

with open(CSV_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["input_size"])
        lb = float(row["lower_bound"])
        cost = float(row["approx_cost"])
        delta = float(row["delta"])

        input_sizes.append(n)
        lower_bounds.append(lb)
        approx_costs.append(cost)
        deltas.append(delta)

# Sort by input size so lines are nice and monotone in X.
data = list(zip(input_sizes, lower_bounds, approx_costs, deltas))
data.sort(key=lambda x: x[0])
input_sizes, lower_bounds, approx_costs, deltas = zip(*data)

# ----- Plot 1: lower bound vs approx cost -----
plt.figure(figsize=(8, 5))
plt.plot(input_sizes, lower_bounds, marker="o", label="Lower bound (MST)")
plt.plot(input_sizes, approx_costs, marker="o", label="Approx tour cost")
plt.xlabel("Input size (number of cities)")
plt.ylabel("Cost")
plt.title("Approximate TSP Cost vs Lower Bound")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("lb_vs_cost.png", dpi=200)

# ----- Plot 2: delta vs n -----
plt.figure(figsize=(8, 5))
plt.plot(input_sizes, deltas, marker="o", label="Cost - Lower bound")
plt.xlabel("Input size (number of cities)")
plt.ylabel("Delta (approx_cost - lower_bound)")
plt.title("Gap to Lower Bound vs Input Size")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("delta_vs_n.png", dpi=200)

print("Saved lb_vs_cost.png and delta_vs_n.png")
