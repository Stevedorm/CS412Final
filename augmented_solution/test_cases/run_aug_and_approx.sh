#!/usr/bin/env bash
# run_both_approx.sh
#
# Runs BOTH approx solvers on each test case input and prints (for each):
#  - wallclock time the script took
#  - the program's printed answer (cost & path)
set -euo pipefail

# Directory containing this script: approx_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

APPROX1="$SCRIPT_DIR/../../approx_solution/cs412_tsp_approx.py"
APPROX2="$SCRIPT_DIR/../cs412_tsp_approx_new.py"

INPUT_DIR="$SCRIPT_DIR/input"

if [[ ! -f "$APPROX1" ]]; then
  echo "ERROR: Cannot find cs412_tsp_approx.py at $APPROX1" >&2
  exit 1
fi

if [[ ! -f "$APPROX2" ]]; then
  echo "ERROR: Cannot find cs412_tsp_approx_augmented.py at $APPROX2" >&2
  exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "ERROR: Missing input/ directory at $INPUT_DIR" >&2
  exit 1
fi

echo "Approx 1: $APPROX1"
echo "Approx 2: $APPROX2"
echo "Input folder: $INPUT_DIR"
echo

RESULT_CSV="$SCRIPT_DIR/approx_vs_new.csv"

# CSV header
echo "test_case,approx_result,approx_time,augmented_result,augmented_time" > "$RESULT_CSV"

for infile in "$INPUT_DIR"/*.in; do
  base="$(basename "$infile" .in)"
  echo "================================================================"
  echo "=== Test case: $base"

  # print input size (first token on first line)
  input_size="$(head -n 1 "$infile" | awk '{print $1}')"
  echo "Input size: ${input_size}"

  # ---- Approx solver 1 ----
  start_time=$(date +%s.%N)
  approx1_output="$(python3 "$APPROX1" < "$infile")"
  end_time=$(date +%s.%N)
  approx1_time=$(awk "BEGIN{print $end_time - $start_time}")

  echo
  echo "-- cs412_tsp_approx.py (approx 1) --"
  echo "time: ${approx1_time}s"
  echo "output:" 
  printf "    %s
" "${approx1_output}" | sed 's/$/\n/' | sed 's/^/    /'

  # ---- Approx solver 2 (augmented) ----
  start_time=$(date +%s.%N)
  approx2_output="$(python3 "$APPROX2" < "$infile")"
  end_time=$(date +%s.%N)
  approx2_time=$(awk "BEGIN{print $end_time - $start_time}")

  echo
  # sanitize outputs into single-line CSV-friendly strings
  # replace newlines with space and escape double-quotes
  sanitize() {
    echo "$1" | tr '\n' ' ' | sed -E 's/"/""/g' | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' | sed -E 's/[[:space:]]+/ /g'
  }

  approx1_result=$(sanitize "$approx1_output")
  approx2_result=$(sanitize "$approx2_output")

  # append CSV row (quote fields)
  printf '"%s","%s","%s","%s","%s"\n' "$base" "$approx1_result" "$approx1_time" "$approx2_result" "$approx2_time" >> "$RESULT_CSV"
  echo "-- cs412_tsp_approx_new.py (approx 2) --"
  echo "time: ${approx2_time}s"
  echo "output:" 
  printf "    %s
" "${approx2_output}" | sed 's/$/\n/' | sed 's/^/    /'

  echo
done

echo "All done."
echo "Wrote combined approx vs augmented results to: $RESULT_CSV"
