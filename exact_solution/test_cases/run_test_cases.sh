#!/usr/bin/env bash
# run_test_cases.sh
#
# Runs cs412_tsp_exact.py on all test cases in the input/ directory and
# compares the program's output to the expected .out files in output/.
#
# NOTE: The test case "tc08_slow_12nodes.in" contains a complete graph
#       with 12 vertices. Because cs412_tsp_exact.py uses a brute-force
#       exact TSP algorithm that tries all permutations, this test case
#       causes the program to run for MORE THAN 20 MINUTES on a typical
#       machine (12! ≈ 4.79e8 tours).  It is intentionally included as
#       a "slow test" to demonstrate the worst-case behavior.
#
# Additionally, this script now collects *empirical runtime data* for
# each test case and writes it to a CSV file (runtime_results.csv) with
# columns:
#   test_case,input_size,runtime_seconds
#
# This data can be used to generate a plot with:
#   - X axis: input size (number of cities)
#   - Y axis: runtime in seconds
#
set -euo pipefail

# Directory containing this script: exact_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to cs412_tsp_exact.py (one directory up)
SOL="$SCRIPT_DIR/../cs412_tsp_exact.py"

# Input and output folders
INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_DIR="$SCRIPT_DIR/output"

# CSV file for empirical runtime results
RUNTIME_CSV="$SCRIPT_DIR/runtime_results.csv"

if [[ ! -f "$SOL" ]]; then
  echo "ERROR: Cannot find cs412_tsp_exact.py at $SOL" >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "ERROR: Missing input/ directory at $INPUT_DIR" >&2
  exit 1
fi

if [[ ! -d "$OUTPUT_DIR" ]]; then
  echo "ERROR: Missing output/ directory at $OUTPUT_DIR" >&2
  exit 1
fi

echo "Using solution: $SOL"
echo "Input folder:   $INPUT_DIR"
echo "Output folder:  $OUTPUT_DIR"
echo "Runtime CSV:    $RUNTIME_CSV"
echo

overall_passed=true

# Initialize / overwrite the runtime CSV with a header row
echo "test_case,input_size,runtime_seconds" > "$RUNTIME_CSV"

# Loop through all input/*.in
for infile in "$INPUT_DIR"/*.in; do
  base="$(basename "$infile" .in)"
  expected="$OUTPUT_DIR/$base.out"
  actual="$OUTPUT_DIR/$base.actual"

  echo "=== Running $base ==="

  if [[ ! -f "$expected" ]]; then
    echo "  !! Missing expected output file: $expected"
    overall_passed=false
    continue
  fi

    # Extract input size from the first line of the .in file.
  input_size="$(head -n 1 "$infile" | tr -d '[:space:]')"

  # Reset and start the timer
  SECONDS=0

  # Run the student's solution
  python3 "$SOL" < "$infile" > "$actual"

  # Elapsed wallclock time in seconds (integer)
  runtime_secs="$SECONDS"

  # Append to runtime CSV
  echo "${base},${input_size},${runtime_secs}" >> "$RUNTIME_CSV"


  # Append to runtime CSV
  echo "${base},${input_size},${runtime_secs}" >> "$RUNTIME_CSV"

  # Compare result with expected output
  if diff -u "$expected" "$actual"; then
    echo "  ✅ $base passed (runtime: ${runtime_secs}s, n = ${input_size})"
  else
    echo "  ❌ $base FAILED (see diff above)"
    overall_passed=false
  fi

  echo
done

if $overall_passed; then
  echo "All tests passed 🎉"
else
  echo "Some tests failed ❌"
  exit 1
fi

echo "Empirical runtime data written to: $RUNTIME_CSV"
echo "Use this CSV to plot input_size (X) vs runtime_seconds (Y) for your presentation."
