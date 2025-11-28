#!C:/Users/steve/anaconda3/envs/cs412f25/python.exe
"""
plot_runtime.py

Reads runtime_results.csv and produces a plot of
input_size (X axis) vs runtime_seconds (Y axis).

Assumes CSV format:
    test_case,input_size,runtime_seconds

TO RUN PLOT_RUNTIME:
    You need to update the top line with the path to the virtual environment. 
    For me, I ran this in the terminal:
        which python (on bash)
        the copied that path to the top line, then I was able to run it normally
"""

import csv
import matplotlib.pyplot as plt

csv_file = "runtime_results.csv"

input_sizes = []
runtimes = []
labels = []

with open(csv_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["input_size"])
        t = float(row["runtime_seconds"])
        label = row["test_case"]

        input_sizes.append(n)
        runtimes.append(t)
        labels.append(label)

# Sort by input size so the line doesn’t zig-zag
data = sorted(zip(input_sizes, runtimes, labels), key=lambda x: x[0])
input_sizes, runtimes, labels = zip(*data)

plt.figure()

# Line plot with markers
plt.plot(input_sizes, runtimes, marker="o")

# Optionally annotate each point with the test case name
for x, y, label in zip(input_sizes, runtimes, labels):
    plt.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(10, 6),   # offset diagonally
        ha="left",
        rotation=30,
        fontsize=8
    )

plt.xlabel("Input size (number of cities)")
plt.ylabel("Runtime (seconds)")
plt.title("Empirical Runtime of Exact TSP Solver")
plt.grid(True)
plt.tight_layout()

# Save to file and also show
plt.savefig("runtime_plot.png", dpi=200)
plt.show()
