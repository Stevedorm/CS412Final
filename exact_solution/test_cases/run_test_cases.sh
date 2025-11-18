#!/usr/bin/env bash
set -euo pipefail

# Directory containing this script: exact_solution/test_cases
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to solution.py (one directory up)
SOL="$SCRIPT_DIR/../solution.py"

# Input and output folders
INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_DIR="$SCRIPT_DIR/output"

if [[ ! -f "$SOL" ]]; then
  echo "ERROR: Cannot find solution.py at $SOL" >&2
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
echo

overall_passed=true

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

  # Run the student's solution
  python3 "$SOL" < "$infile" > "$actual"

  # Compare result with expected output
  if diff -u "$expected" "$actual"; then
    echo "  ✅ $base passed"
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
