#!/usr/bin/env bash
# Run all example TSP inputs and compute:
#  - approximate solution
#  - lower bound
#  - delta

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$SCRIPT_DIR/.."

SOLVER="$ROOT_DIR/cs412_tsp_approx_lb.py"
INPUT_DIR="$SCRIPT_DIR/input"

if [[ ! -f "$SOLVER" ]]; then
    echo "ERROR: Solver not found: $SOLVER"
    exit 1
fi

echo "Running TSP approximation with lower bounds..."
echo

for f in "$INPUT_DIR"/*.in; do
    base="$(basename "$f")"
    echo "=== $base ==="
    python3 "$SOLVER" < "$f"
    echo
done
