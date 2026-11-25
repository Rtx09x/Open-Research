#!/usr/bin/env bash
# Run all retained exact checks without the historical ZIP archives.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1
python -c 'assert __debug__, "Do not run Python with -O"'
mkdir -p repro/{original,generalizations,audit}/results
for script in \
  repro/original/src/verify.py \
  repro/original/src/test_verifier.py \
  repro/original/src/verify_reset.py \
  repro/generalizations/src/build_compositions.py \
  repro/generalizations/src/check_run.py \
  repro/generalizations/src/test_memory.py \
  repro/generalizations/src/adversarial_raw.py \
  repro/audit/src/resources.py \
  repro/audit/src/sparse.py \
  repro/audit/src/structural_bounds.py \
  repro/audit/src/complete_bands.py \
  repro/audit/src/seven_state_separation.py \
  repro/audit/src/exact_elimination.py \
  repro/audit/src/verify_stored.py \
  repro/audit/src/test_audit.py; do
  printf '\n== %s ==\n' "$script"
  python -u "$script"
done
printf '\nAll retained checks passed.\n'
