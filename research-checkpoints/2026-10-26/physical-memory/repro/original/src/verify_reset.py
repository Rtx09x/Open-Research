#!/usr/bin/env python3
"""Verify the two nominal scalar reset protocols, using exact rational events.

The reset protocol is additional to the operating counter. It is not constrained
by the one-flip-per-half-pulse budget and has no certified perturbation tolerance.
Python 3.10+, standard library only. Run from any working directory.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
from verify import RESULTS, require, six_model, five_model, stability_margins, leg


def check_reset(model: dict, reset_field: int, pulses: int) -> dict:
    """Exhaust all baseline-stable configurations; purge, then set labeled zero."""
    low, high = F(model['low']), F(model['high'])
    baseline = [s for s in range(1 << model['n'])
                if min(stability_margins(model, s, low)) > 0]
    require(len(baseline) > 0, 'No baseline-stable configurations')
    for state in baseline:
        purged, _ = leg(model, state, low, F(reset_field))
        restored, _ = leg(model, purged, F(reset_field), low)
        require(purged == restored == 0, 'Purge did not reach the all-off state')
    state, trace = 0, []
    for _ in range(pulses):
        peak, up_events = leg(model, state, low, high)
        nxt, down_events = leg(model, peak, high, low)
        trace.append({'from': state, 'peak': peak, 'to': nxt,
                      'up_events': up_events, 'down_events': down_events})
        state = nxt
    require(state == model['path'][0], 'Reset did not reach the labeled zero')
    return {'model': model['name'], 'reset_field': reset_field,
            'ordinary_pulses_after_purge': pulses,
            'all_baseline_stable_states': baseline,
            'target_mask': state, 'trace_from_zero': trace,
            'limitation': 'Nominal exact global reset only. Switching budget and stated operational perturbation bound do not cover reset.'}


def main() -> None:
    checks = [check_reset(six_model(), -40, 6), check_reset(five_model(), -3, 10)]
    stored = json.loads((RESULTS / 'nominal_reset_certificate.json').read_text())
    require(checks == stored, 'Nominal reset certificate mismatch')
    for result in checks:
        print(f"PASS: {result['model']}: all {len(result['all_baseline_stable_states'])} "
              f"baseline-stable states reset to mask {result['target_mask']}; "
              f"purge {result['reset_field']}, then {result['ordinary_pulses_after_purge']} pulses")
    print('Scope: nominal initialization only; operational budget/error bound not applied to reset.')


if __name__ == '__main__':
    main()
