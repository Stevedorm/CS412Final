#!/usr/bin/env bash
#
# compute_old_vs_new.sh
#
# Runs the original approx solver and the Part E (augmented) solver
# on all .in files in input/ and writes:
#
#   old_vs_new_results.csv
#
# with columns:
#   test_case,input_size,old_runtime,new_runtime,old_cost,new_cost
#

set -euo pipefail

# Directory containing this script: approx_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Paths to solvers
OLD_SOL="$SCRIPT_DIR/../cs412_tsp_approx_partE.py"
NEW_SOL="$SCRIPT_DIR/../cs412_tsp_approx_new.py"

INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_CSV="$SCRIPT_DIR/old_vs_new_results.csv"

if [[ ! -f "$OLD_SOL" ]]; then
  echo "ERROR: Cannot find original approx solver at $OLD_SOL" >&2
  exit 1
fi

if [[ ! -f "$NEW_SOL" ]]; then
  echo "ERROR: Cannot find Part E solver at $NEW_SOL" >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "ERROR: Missing input/ directory at $INPUT_DIR" >&2
  exit 1
fi

echo "Old solver (original): $OLD_SOL"
echo "New solver (Part E):   $NEW_SOL"
echo "Input folder:          $INPUT_DIR"
echo "Output CSV:            $OUTPUT_CSV"
echo

# Initialize CSV header
echo "test_case,input_size,old_runtime,new_runtime,old_cost,new_cost" > "$OUTPUT_CSV"

# Loop over all .in test cases
for infile in "$INPUT_DIR"/*.in; do
  base="$(basename "$infile" .in)"
  echo "=== Running $base ==="

  # Input size: first number on first line = number of vertices
  input_size="$(head -n 1 "$infile" | awk '{print $1}')"

  # ---- Old solver (original approx) ----
  SECONDS=0
  old_output="$(python3 "$OLD_SOL" < "$infile")"
  old_runtime="$SECONDS"

  # First token on first line is the cost (as in your current format)
  old_cost="$(printf '%s\n' "$old_output" | awk '{print $1; exit}')"

  # ---- New solver (Part E augmented) ----
  SECONDS=0
  new_output="$(python3 "$NEW_SOL" < "$infile")"
  new_runtime="$SECONDS"

  new_cost="$(printf '%s\n' "$new_output" | awk '{print $1; exit}')"

  # Append to CSV
  echo "${base},${input_size},${old_runtime},${new_runtime},${old_cost},${new_cost}" >> "$OUTPUT_CSV"

  echo "  old (orig): time=${old_runtime}s, cost=${old_cost}"
  echo "  new (PartE): time=${new_runtime}s, cost=${new_cost}"
  echo
done

echo "Wrote comparison results to: $OUTPUT_CSV"
