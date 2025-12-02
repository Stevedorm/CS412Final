#!/usr/bin/env bash
#
# compute_all_three_wallclock.sh
#
# Runs exact, approx, and augmented (part E) TSP solvers on all test cases in input/
# and writes a combined CSV with:
#   test_case,input_size,
#   exact_runtime,approx_runtime,aug_runtime,
#   exact_cost,approx_cost,aug_cost
#
set -euo pipefail

# Directory containing this script: approx_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Paths to solvers
EXACT_SOL="$SCRIPT_DIR/../../exact_solution/cs412_tsp_exact.py"
APPROX_SOL="$SCRIPT_DIR/../cs412_tsp_approx.py"
AUG_SOL="$SCRIPT_DIR/../cs412_tsp_approx_partE.py"

INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_CSV="$SCRIPT_DIR/all_three_results.csv"

if [[ ! -f "$EXACT_SOL" ]]; then
  echo "ERROR: Cannot find exact solver at $EXACT_SOL" >&2
  exit 1
fi

if [[ ! -f "$APPROX_SOL" ]]; then
  echo "ERROR: Cannot find approx solver at $APPROX_SOL" >&2
  exit 1
fi

if [[ ! -f "$AUG_SOL" ]]; then
  echo "ERROR: Cannot find augmented solver at $AUG_SOL" >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "ERROR: Missing input/ directory at $INPUT_DIR" >&2
  exit 1
fi

echo "Exact solver:     $EXACT_SOL"
echo "Approx solver:    $APPROX_SOL"
echo "Augmented solver: $AUG_SOL"
echo "Input folder:     $INPUT_DIR"
echo "Output CSV:       $OUTPUT_CSV"
echo

# Initialize CSV header
echo "test_case,input_size,exact_runtime,approx_runtime,aug_runtime,exact_cost,approx_cost,aug_cost" > "$OUTPUT_CSV"

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

  # Assume solver prints (at least) one numeric cost; take first token on first line
  exact_cost="$(printf '%s\n' "$exact_output" | awk '{print $1; exit}')"

  # ---- Approx solver ----
  SECONDS=0
  approx_output="$(python3 "$APPROX_SOL" < "$infile")"
  approx_runtime="$SECONDS"

  approx_cost="$(printf '%s\n' "$approx_output" | awk '{print $1; exit}')"

  # ---- Augmented solver (part E) ----
  SECONDS=0
  aug_output="$(python3 "$AUG_SOL" < "$infile")"
  aug_runtime="$SECONDS"

  aug_cost="$(printf '%s\n' "$aug_output" | awk '{print $1; exit}')"

  # Append to CSV
  echo "${base},${input_size},${exact_runtime},${approx_runtime},${aug_runtime},${exact_cost},${approx_cost},${aug_cost}" >> "$OUTPUT_CSV"

  echo "  exact:     time=${exact_runtime}s, cost=${exact_cost}"
  echo "  approx:    time=${approx_runtime}s, cost=${approx_cost}"
  echo "  augmented: time=${aug_runtime}s,  cost=${aug_cost}"
  echo
done

echo "Wrote combined results to: $OUTPUT_CSV"
