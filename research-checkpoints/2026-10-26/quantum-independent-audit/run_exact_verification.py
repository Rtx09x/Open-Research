#!/usr/bin/env python3
"""Recompute every independent finite minimum-19 arithmetic ingredient in order."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent
if not __debug__:raise SystemExit('Assertions must remain enabled.')
for name in ('check_kl_stability.py','verify_full_certificate_independent.py','replay_shorter_lengths.py','replay_known19_exact.py'):
    subprocess.run([sys.executable,str(HERE/name)],cwd=HERE,check=True)
kl=json.loads((HERE/'check_kl_stability.json').read_text());full=json.loads((HERE/'verify_full_certificate_independent.json').read_text())
assert kl['PASS'] and full['PASS'] and kl['candidate_sha256']==full['candidate_sha256']=='201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79'
short=json.loads((HERE/'shorter_lengths_exact_replay.json').read_text())['results']
assert sorted(row['n'] for row in short)==list(range(9,18)) and all(row['d']==5 and row['exact_farkas_valid'] for row in short)
known=json.loads((HERE/'known19_exact_replay.json').read_text())
assert known['exact'] and known['root_contraction'] and known['all_50_KL_reductions']
print('PASS: fresh independent KL/residual certificate, every n=9..17, and exact known19 existence.')
print('The n<=8 no-cloning argument and physical model necessity are analytic proof inputs, not computed here.')
