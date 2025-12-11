#!/usr/bin/env bash
#
# run_nonopt_cases.sh
#
# Runs ONE test case where the approximation solution does NOT
# achieve the optimal answer. It prints both the exact and
# approximate results for easy comparison.
#
set -euo pipefail

# Directory containing this script: approx_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Paths to solvers (adjust names if needed)
EXACT_SOL="$SCRIPT_DIR/../../exact_solution/cs412_tsp_exact.py"
APPROX_SOL="$SCRIPT_DIR/../cs412_tsp_approx.py"

INPUT_DIR="$SCRIPT_DIR/input"

# Choose a test case where approx != exact
# You can change this to any .in file that you know is non-optimal.
CASE_BASENAME="tc08_medium_7nodes"
INFILE="$INPUT_DIR/${CASE_BASENAME}.in"

if [[ ! -f "$EXACT_SOL" ]]; then
  echo "ERROR: Cannot find exact solver at $EXACT_SOL" >&2
  exit 1
fi

if [[ ! -f "$APPROX_SOL" ]]; then
  echo "ERROR: Cannot find approx solver at $APPROX_SOL" >&2
  exit 1
fi

if [[ ! -f "$INFILE" ]]; then
  echo "ERROR: Cannot find input file: $INFILE" >&2
  exit 1
fi

echo "Using test case: $CASE_BASENAME"
echo "Input:          $INFILE"
echo

echo "----- EXACT SOLUTION -----"
python3 "$EXACT_SOL" < "$INFILE"
echo

echo "----- APPROX SOLUTION -----"
python3 "$APPROX_SOL" < "$INFILE"
echo

echo "Note: This test is specifically chosen because the approximate"
echo "solution does not achieve the optimal cost, as required by the spec."
