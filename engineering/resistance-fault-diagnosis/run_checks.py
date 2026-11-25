"""Replay only evidence supporting the current main manuscript.

The default is a practical regression suite. --full adds the exhaustive atlas,
access, family and margin audits cited by the manuscript. Run in a disposable
copy: individual checks can write adjacent generated results.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

if not __debug__:
    raise RuntimeError('Scientific verification requires assertions; do not use Python -O.')

ROOT = Path(__file__).resolve().parent
CORE = [
    ['test_adversarial_exact_search.py'],
    ['test_adversarial_certificates.py'],
    ['test_fresh_terminal_multigraphs.py'],
    ['test_fresh_single_change_boundaries.py'],
    ['research/planner/test_planner.py'],
    ['research/connected_planner/test_connected_planner.py'],
    ['research/universal_recovery/check_recovery.py'],
    ['research/new_theorem_audit/audit_unknown_increase.py'],
    ['research/noise_extension/verify.py'],
    ['research/clique_noise_extension/verify.py'],
    ['explicit_gap.py', '3', '5', '10'],
    ['research/structural_extension/audit_prism_noise.py'],
]
FULL = [
    ['research/terminal_extension/verify_terminal_theorem.py'],
    ['research/terminal_extension/verify_access_optimization.py'],
    ['research/access_optimality_extension/audit_access_preservation.py'],
    ['research/structural_extension/audit_biconnected.py'],
    ['research/structural_extension/audit_cubic.py'],
    ['research/structural_extension/audit_cubic_rational.py'],
    ['research/new_theorem_audit/audit_structural_larger.py'],
    ['research/new_theorem_audit/independent_parallel_checks.py'],
    ['research/connected_extension/audit_connected.py'],
    ['research/connected_extension/audit_bridgeless.py'],
    ['research/connected_extension/independent_audit.py'],
    ['research/connected_extension/audit_access.py'],
    ['research/connected_extension/independent_access_audit.py'],
    ['research/realistic_fault_extension/check_partial.py'],
    ['research/realistic_fault_extension/check_laplacian.py'],
    ['research/realistic_fault_extension/check_robust_support.py'],
    ['explicit_gap.py', '30', '100'],
    ['precision_tradeoff.py'],
    ['weighted_noise_lower.py'],
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='include all retained manuscript audits')
    parser.add_argument('--output', type=Path, help='optional JSON report path')
    args = parser.parse_args()
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    results = []
    checks = CORE + (FULL if args.full else [])
    for command in checks:
        start = time.monotonic()
        result = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]],
                                cwd=ROOT, env=env, text=True, capture_output=True)
        record = {'command': command, 'returncode': result.returncode,
                  'seconds': round(time.monotonic() - start, 3),
                  'stdout': result.stdout, 'stderr': result.stderr}
        results.append(record)
        if args.output:
            args.output.write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps({k: record[k] for k in ('command', 'returncode', 'seconds')}), flush=True)
        if result.returncode:
            print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
            raise SystemExit(result.returncode)
    print(f'All {len(checks)} current-manuscript verification programs passed.')


if __name__ == '__main__':
    main()
