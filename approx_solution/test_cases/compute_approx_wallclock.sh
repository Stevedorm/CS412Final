#!/usr/bin/env bash
#
# compute_approx_wallclock.sh
#
# Runs BOTH the exact and approximate TSP solvers on all test cases in input/
# and writes a combined CSV with:
#   test_case,input_size,exact_runtime,approx_runtime,exact_cost,approx_cost
#
# This CSV can be used to:
#   - plot runtime (exact vs approx) vs input size
#   - plot solution quality (exact vs approx) vs input size
#
set -euo pipefail

# Directory containing this script: approx_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Paths to solvers (adjust if yours are named differently)
EXACT_SOL="$SCRIPT_DIR/../../exact_solution/cs412_tsp_exact.py"
APPROX_SOL="$SCRIPT_DIR/../cs412_tsp_approx.py"

INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_CSV="$SCRIPT_DIR/approx_vs_exact_results.csv"

if [[ ! -f "$EXACT_SOL" ]]; then
  echo "ERROR: Cannot find exact solver at $EXACT_SOL" >&2
  exit 1
fi

if [[ ! -f "$APPROX_SOL" ]]; then
  echo "ERROR: Cannot find approx solver at $APPROX_SOL" >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "ERROR: Missing input/ directory at $INPUT_DIR" >&2
  exit 1
fi

echo "Exact solver:   $EXACT_SOL"
echo "Approx solver:  $APPROX_SOL"
echo "Input folder:   $INPUT_DIR"
echo "Output CSV:     $OUTPUT_CSV"
echo

# Initialize CSV header
echo "test_case,input_size,exact_runtime,approx_runtime,exact_cost,approx_cost" > "$OUTPUT_CSV"

# Loop over all .in test cases
for infile in "$INPUT_DIR"/*.in; do
  base="$(basename "$infile" .in)"
  echo "=== Running $base ==="

  # Input size: first number on first line = number of vertices
  input_size="$(head -n 1 "$infile" | awk '{print $1}')"

  # ---- Exact solver ----
  SECONDS=0
  exact_output="$(python3 "$EXACT_SOL" < "$infile")"
  exact_runtime="$SECONDS"

  # Extract exact cost from "Minimum cost: X" line
  exact_cost="$(printf "%s\n" "$exact_output" | awk '/Minimum cost:/ {print $3}' )"

  # ---- Approx solver ----
  SECONDS=0
  approx_output="$(python3 "$APPROX_SOL" < "$infile")"
  approx_runtime="$SECONDS"

  # Extract approx cost from "Minimum cost: X" line
  approx_cost="$(printf "%s\n" "$approx_output" | awk '/Minimum cost:/ {print $3}' )"

  # Append to CSV
  echo "${base},${input_size},${exact_runtime},${approx_runtime},${exact_cost},${approx_cost}" >> "$OUTPUT_CSV"

  echo "  exact:  time=${exact_runtime}s,  cost=${exact_cost}"
  echo "  approx: time=${approx_runtime}s, cost=${approx_cost}"
  echo
done

echo "Wrote combined results to: $OUTPUT_CSV"
