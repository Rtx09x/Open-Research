#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/manuscript"
command -v pdflatex >/dev/null || { echo 'pdflatex not installed' >&2; exit 1; }
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error structure_uncertainty_fault_diagnosis.tex >/dev/null
done
printf 'Built %s\n' "$ROOT/manuscript/structure_uncertainty_fault_diagnosis.pdf"
