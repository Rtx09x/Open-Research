#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/paper"
command -v pdflatex >/dev/null || { echo 'pdflatex not installed' >&2; exit 1; }
if command -v bibtex.original >/dev/null 2>&1; then BIBTEX=bibtex.original
elif [[ -x /usr/bin/bibtex.original ]]; then BIBTEX=/usr/bin/bibtex.original
else BIBTEX=bibtex; fi
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex >/dev/null
"$BIBTEX" main >/dev/null
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex >/dev/null
printf 'Built %s\n' "$ROOT/paper/main.pdf"
