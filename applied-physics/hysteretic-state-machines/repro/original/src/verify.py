#!/usr/bin/env python3
"""Independent, exact certificate verification. Python 3.10+, standard library only.

No scipy, floating-point LP, downloaded code, or random search is used here.
The two lower-bound checks use different combinatorial enumerations.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'


def require(test: bool, message: str) -> None:
    if not test:
        raise AssertionError(message)


def bits(s: int, n: int) -> list[int]:
    return [i for i in range(n) if (s >> i) & 1]


def parity(p: list[int] | tuple[int, ...]) -> int:
    return sum(p[i] > p[j] for i in range(len(p))
               for j in range(i + 1, len(p))) % 2


def matching_check() -> dict:
    """Enumerate every incidence matching, using no stored enumeration."""
    low = [s for s in range(32) if s.bit_count() == 2]
    high = [s for s in range(32) if s.bit_count() == 3]
    possible = [[j for j, t in enumerate(high) if s & t == s] for s in low]
    all_matchings = []

    def visit(row: int, used: int, p: list[int]) -> None:
        if row == len(low):
            all_matchings.append(tuple(p))
            return
        for j in possible[row]:
            if not (used >> j) & 1:
                visit(row + 1, used | (1 << j), p + [j])

    visit(0, 0, [])
    counts = Counter(parity(p) for p in all_matchings)
    require(counts == {0: 6, 1: 54}, 'Unexpected incidence-matching parity counts')
    even = [p for p in all_matchings if parity(p) == 0]
    features = []
    for p in even:
        v = [0] * 25  # five bare thresholds; twenty ordered pair coefficients
        pair_order = [(i, j) for i in range(5) for j in range(5) if i != j]
        for s, j in zip(low, p):
            added = (s ^ high[j]).bit_length() - 1
            v[added] += 1
            for active in bits(s, 5):
                v[5 + pair_order.index((added, active))] += 1
        features.append(v)
    target = [2] * 5 + [1] * 20
    require(all(v == target for v in features), 'An even matching is not balanced')
    require(len({p for p in even}) == 6, 'Duplicate matching')
    # Complement maps either ten-element layer to the other in reverse order.
    require([high.index(31 ^ s) for s in low] == list(range(9, -1, -1)),
            'Complement ordering mismatch')
    require(parity(list(range(9, -1, -1))) == 1, 'Complement parity mismatch')
    out = {'total_matchings': len(all_matchings), 'even': counts[0],
           'odd': counts[1], 'low_masks': low,
           'even_high_mask_lists': [[high[j] for j in p] for p in even],
           'common_feature_vector': target,
           'claim': 'Any strict affine up-selector bijection is odd; same for down.'}
    return out


def all_cycles() -> list[tuple[int, ...]]:
    """Unpruned DFS, unlike the discovery script: all 20-cycles containing 3->7."""
    vertices = [s for s in range(32) if s.bit_count() in (2, 3)]
    adj = {s: [t for t in vertices if (s ^ t).bit_count() == 1] for s in vertices}
    answer = []

    def visit(path: list[int], used: set[int]) -> None:
        if len(path) == 20:
            if path[0] in adj[path[-1]]:
                answer.append(tuple(path))
            return
        for t in adj[path[-1]]:
            if t not in used:
                visit(path + [t], used | {t})

    visit([3, 7], {3, 7})
    return answer


def winner_matrix(path: list[int] | tuple[int, ...]) -> tuple[list[list[int]], list]:
    """Reconstruct 50-variable split-branch affine winner inequalities A x > 0."""
    n = 5
    pair_order = [(i, j) for i in range(n) for j in range(n) if i != j]

    def threshold(i: int, s: int, up: bool) -> list[int]:
        v = [0] * 50
        v[i if up else 5 + i] = 1
        for j in bits(s, n):
            if j != i:
                v[10 + (0 if up else 20) + pair_order.index((i, j))] = 1
        return v

    rows, labels = [], []
    for t in range(0, 20, 2):
        a, p, c = path[t], path[t + 1], path[(t + 2) % 20]
        add = (a ^ p).bit_length() - 1
        remove = (p ^ c).bit_length() - 1
        # Reproduce certificate row-label order, not the discovery matrix values.
        for i in range(n):
            if not (a >> i) & 1 and i != add:
                x, y = threshold(i, a, True), threshold(add, a, True)
                rows.append([u - v for u, v in zip(x, y)])
                labels.append(['up', a, add, i])
            if (p >> i) & 1 and i != remove:
                x, y = threshold(remove, p, False), threshold(i, p, False)
                rows.append([u - v for u, v in zip(x, y)])
                labels.append(['down', p, remove, i])
    return rows, labels


def dual_check() -> dict:
    cycles = all_cycles()
    require(len(cycles) == len(set(cycles)) == 16, 'Hamiltonian enumeration mismatch')
    certs = json.loads((RESULTS / 'five_affine_impossibility_certificates.json').read_text())
    require({tuple(c['path']) for c in certs} == set(cycles), 'Incomplete certificate coverage')
    supports = []
    for cert in certs:
        a, labels = winner_matrix(cert['path'])
        require(a == cert['matrix'], 'Stored matrix differs from reconstructed inequalities')
        require(labels == cert['labels'], 'Certificate label mismatch')
        y = cert['weights']
        require(len(y) == len(a) and all(isinstance(v, int) and v >= 0 for v in y),
                'Non-integer or negative dual weight')
        require(sum(y) > 0, 'Zero dual certificate')
        residue = [sum(y[r] * a[r][j] for r in range(len(a))) for j in range(50)]
        require(residue == [0] * 50, 'Nonzero exact dual residual')
        supports.append(sum(v != 0 for v in y))
    return {'fixed_directed_edge': [3, 7], 'complete_cycles': len(cycles),
            'exact_dual_certificates': len(certs), 'support_sizes': supports,
            'affine_variables': 50, 'maximum_absolute_dual_residual': 0}


def make_pairwise(n: int, a: list[int], b: list[int], j: list[list[int]],
                  high: int, path: list[int], name: str) -> dict:
    return {'name': name, 'n': n, 'degree': 1, 'low': '0', 'high': str(high),
            'a': [str(F(a[i]) + F(i + 1, 100)) for i in range(n)],
            'b': [str(F(b[i]) + F(i + 1, 100)) for i in range(n)],
            'terms': [[{'mask': 1 << k, 'coefficient': str(j[i][k])}
                       for k in range(n) if k != i] for i in range(n)],
            'path': path,
            'convention': 'plus-sign shifts; positive coefficients are inhibitory',
            'initialization': 'Prepare path[0] at low; reset is not part of the target FSM.'}


def compile_cycle(n: int, path: list[int], name: str) -> dict:
    """General nonnegative degree-k construction from an adjacent-layer cycle."""
    require(n >= 3, 'Need at least three hysterons')
    require(all(isinstance(v, int) and 0 <= v < (1 << n) for v in path), 'Invalid bitmask')
    require(len(path) >= 6 and len(path) % 2 == 0, 'Need a nontrivial simple cycle')
    require(len(set(path)) == len(path), 'Repeated cycle vertex')
    k = path[0].bit_count()
    require(1 <= k <= n - 2, 'Adjacent layers cannot support a cycle')
    require(all(s.bit_count() == k + (t % 2) for t, s in enumerate(path)), 'Ranks not alternating')
    require(all((path[t] ^ path[(t + 1) % len(path)]).bit_count() == 1
                for t in range(len(path))), 'Non-edge in cycle')
    edges = {}
    for t in range(0, len(path), 2):
        low, peak, nxt = path[t], path[t + 1], path[(t + 2) % len(path)]
        added = (low ^ peak).bit_length() - 1
        removed = (peak ^ nxt).bit_length() - 1
        require((added, low) not in edges, 'Repeated up edge')
        edges[(added, low)] = 0
        require((removed, nxt) not in edges, 'Repeated down edge')
        edges[(removed, nxt)] = 4
    base = 2 * comb(n - 1, k)
    offset_denominator = max(100, 4 * (n + 1))
    terms = []
    for i in range(n):
        row = []
        for subset in combinations([j for j in range(n) if j != i], k):
            mask = sum(1 << j for j in subset)
            row.append({'mask': mask, 'coefficient': str(edges.get((i, mask), 2))})
        require(sum(F(t['coefficient']) for t in row) == base, 'Unbalanced edge counts')
        terms.append(row)
    return {'name': name, 'n': n, 'degree': k, 'low': '0', 'high': str(base + 1),
            'a': [str(F(base) + F(i + 1, offset_denominator)) for i in range(n)],
            'b': [str(F(-2) + F(i + 1, offset_denominator)) for i in range(n)],
            'terms': terms, 'path': path,
            'convention': 'plus-sign polynomial shifts; degree k uses up to k+1-body effects',
            'initialization': 'Prepare path[0] at low; reset is not part of the target FSM.'}


def threshold(model: dict, i: int, state: int, up: bool) -> F:
    val = F(model['a' if up else 'b'][i])
    for term in model['terms'][i]:
        if state & term['mask'] == term['mask']:
            val += F(term['coefficient'])
    return val


def stability_margins(model: dict, state: int, field: F) -> list[F]:
    return [(field - threshold(model, i, state, False)) if (state >> i) & 1
            else (threshold(model, i, state, True) - field) for i in range(model['n'])]


def leg(model: dict, state: int, start: F, end: F) -> tuple[int, list[dict]]:
    """Independent exact quasistatic event simulation, with avalanche detection."""
    require(min(stability_margins(model, state, start)) > 0, 'Unstable start')
    up = end > start
    field, events = start, []
    for _ in range(2 ** model['n'] + 1):
        candidates = [(threshold(model, i, state, up), i) for i in range(model['n'])
                      if bool((state >> i) & 1) != up]
        event = (min(candidates) if up else max(candidates)) if candidates else None
        if event is None or (event[0] >= end if up else event[0] <= end):
            require(min(stability_margins(model, state, end)) > 0, 'Unstable endpoint or tie')
            return state, events
        value, index = event
        require(value > field if up else value < field, 'Unresolved avalanche')
        require(sum(t == value for t, i in candidates) == 1, 'Tied critical hysterons')
        old = state
        state ^= 1 << index
        require(min(stability_margins(model, state, value)) > 0, 'Post-flip avalanche')
        events.append({'from_mask': old, 'to_mask': state, 'hysteron': index + 1,
                       'field': str(value), 'direction': 'up' if up else 'down'})
        field = value
    raise AssertionError('Event limit exceeded')


def model_check(model: dict) -> dict:
    n, path = model['n'], model['path']
    require(len(path) >= 6 and len(path) % 2 == 0 and len(set(path)) == len(path), 'Not a simple alternating cycle')
    require(all(0 <= s < (1 << n) for s in path), 'Out-of-range state')
    require(all((path[t] ^ path[(t+1) % len(path)]).bit_count() == 1 for t in range(len(path))), 'Not a cube edge')
    require(all(s.bit_count() == path[0].bit_count() + t % 2 for t, s in enumerate(path)), 'Wrong rank profile')
    lo, hi = F(model['low']), F(model['high'])
    all_margins = []
    traces = []
    for t in range(0, len(path), 2):
        low, peak, nxt = path[t], path[t + 1], path[(t + 2) % len(path)]
        actual_peak, up_events = leg(model, low, lo, hi)
        actual_nxt, down_events = leg(model, actual_peak, hi, lo)
        require(actual_peak == peak and actual_nxt == nxt, 'Unexpected pulse trace')
        require(len(up_events) == len(down_events) == 1, 'Switching-budget violation')
        tu, td = F(up_events[0]['field']), F(down_events[0]['field'])
        added, removed = up_events[0]['hysteron'] - 1, down_events[0]['hysteron'] - 1
        ms = [tu - lo, hi - tu, td - lo, hi - td]
        ms += stability_margins(model, low, lo)
        ms += stability_margins(model, peak, hi)
        ms += stability_margins(model, peak, tu)
        ms += stability_margins(model, nxt, td)
        ms += stability_margins(model, nxt, lo)
        ms += [threshold(model, i, low, True) - tu for i in range(n)
               if not (low >> i) & 1 and i != added]
        ms += [td - threshold(model, i, peak, False) for i in range(n)
               if (peak >> i) & 1 and i != removed]
        require(min(ms) > 0, 'Nonpositive exact trace margin')
        all_margins += ms
        traces.append({'digit': t // 2, 'low_mask': low, 'peak_mask': peak,
                       'next_low_mask': nxt, 'up': up_events[0], 'down': down_events[0],
                       'minimum_margin': str(min(ms))})
    # Separate all-configuration audit of physical consistency and no ties.
    up_values, down_values = [], []
    for state in range(1 << n):
        ups = [threshold(model, i, state, True) for i in range(n) if not (state >> i) & 1]
        downs = [threshold(model, i, state, False) for i in range(n) if (state >> i) & 1]
        require(len(ups) == len(set(ups)) and len(downs) == len(set(downs)), 'Off-orbit tie')
        up_values += ups
        down_values += downs
        for i in range(n):
            require(threshold(model, i, state, True) > threshold(model, i, state, False),
                    'Nonpositive hysteresis span')
    global_gap = min(up_values) - max(down_values)
    require(global_gap > 0, 'Overlapping global switching bands')
    require(all(F(term['coefficient']) >= 0 for row in model['terms'] for term in row),
            'Non-inhibitory interaction')
    margin = min(all_margins)
    return {'name': model['name'], 'n': n, 'period': len(path) // 2,
            'degree': model['degree'], 'trace': traces,
            'minimum_trace_margin': str(margin),
            'effective_threshold_and_endpoint_error_bound_strict': str(margin / 2),
            'number_trace_inequalities_checked': len(all_margins),
            'configurations_audited': 1 << n,
            'global_min_up': str(min(up_values)), 'global_max_down': str(max(down_values)),
            'global_band_gap': str(global_gap), 'all_checks_passed': True}


def six_nonuniform_model() -> dict:
    return make_pairwise(6,
        [49, 49, 55, 67, 58, 73], [-22, -29, -23, -21, -26, -15],
        [[0, 13, 14, 11, 10, 13], [19, 0, 10, 10, 24, 5],
         [0, 18, 0, 10, 0, 10], [28, 0, 16, 0, 0, 16],
         [20, 0, 13, 20, 0, 12], [0, 10, 0, 1, 10, 0]],
        78, [3, 7, 6, 22, 20, 21, 5, 37, 36, 38, 34, 50, 18, 26, 24, 28, 12, 14, 10, 11],
        'six_hysteron_pairwise_decimal')



def six_model() -> dict:
    """Stronger six-element witness: common width 104 and every J_ij > 0."""
    return make_pairwise(6,
        [75, 79, 75, 75, 86, 84], [-29, -25, -29, -29, -18, -20],
        [[0, 14, 21, 2, 13, 24], [20, 0, 5, 37, 8, 20],
         [10, 17, 0, 24, 17, 20], [24, 15, 5, 0, 17, 10],
         [13, 13, 5, 12, 0, 1], [8, 15, 10, 10, 15, 0]],
        107, [3, 7, 6, 14, 12, 13, 9, 41, 33, 49, 48, 56, 24, 25, 17, 21, 20, 22, 18, 19],
        'six_hysteron_uniform_pairwise_decimal')


def five_model() -> dict:
    path = [3, 7, 6, 14, 12, 13, 5, 21, 17, 25, 9, 11, 10, 26, 24, 28, 20, 22, 18, 19]
    return compile_cycle(5, path, 'five_hysteron_three_body_decimal')


def main() -> None:
    lower = {'matching_parity_proof': matching_check(), 'independent_dual_proof': dual_check()}
    models = [six_model(), five_model(), six_nonuniform_model()]
    require({F(a)-F(b) for a,b in zip(models[0]['a'], models[0]['b'])} == {F(104)}, 'Six-element span not uniform')
    require(all(F(t['coefficient']) > 0 for row in models[0]['terms'] for t in row), 'Six-element pair not strictly inhibitory')
    # General compiler checks, including an affine one-hot family.
    for n in (3, 4, 5, 6, 7):
        path = []
        for i in range(n):
            path += [1 << i, (1 << i) | (1 << ((i + 1) % n))]
        models.append(compile_cycle(n, path, f'one_hot_period_{n}'))
    # Further exact witnesses for saturation of the adjacent-layer capacity.
    for n in (6, 7):
        d = json.loads((RESULTS / f'capacity_cycle_n{n}.json').read_text())
        require(len(d['path']) // 2 == comb(n, (n-1)//2), 'Capacity not saturated')
        models.append(compile_cycle(n, d['path'], f'capacity_n{n}_period_{d["period"]}'))
    # Test the compiler on every five-hysteron Hamiltonian cycle.
    compiler_cases = [model_check(compile_cycle(5, list(path), 'compiler_validation'))
                      for path in all_cycles()]
    for q in (6, 7, 8, 9):
        d = json.loads((RESULTS / f'five_period_{q}.json').read_text())
        x, n = d['integer_x'], d['n']
        j = [[0] * n for _ in range(n)]
        for coeff, (i, k) in zip(x[2 * n:], d['pairs']):
            j[i][k] = coeff
        models.append(make_pairwise(n, x[:n], x[n:2*n], j, x[-2], d['path'],
                                    f'five_hysteron_pairwise_period_{q}'))
    checks = []
    for model in models:
        check = model_check(model)
        checks.append(check)
        (RESULTS / f"{model['name']}.json").write_text(json.dumps(model, indent=2) + '\n')
        (RESULTS / f"{model['name']}_trace.json").write_text(json.dumps(check, indent=2) + '\n')
    output = {'status': 'PASS', 'arithmetic': 'integers and fractions.Fraction only',
              **lower, 'models': checks,
              'general_compiler_additional_hamiltonian_cycles_verified': len(compiler_cases),
              'small_counter_minima': {'3': 3, '4': 4, '5': 5, '6': 5, '7': 5, '8': 5, '9': 5, '10': 6},
              'scope': 'Strict quasistatic one-up/one-down pulse counters; no reset requirement.'}
    (RESULTS / 'verification_report.json').write_text(json.dumps(output, indent=2) + '\n')
    print('PASS: complete matching enumeration = 60; six even matchings share exact feature totals')
    print('PASS: independent complete Hamiltonian enumeration = 16; 16 integer dual certificates')
    for check in checks:
        print(f"PASS: {check['name']}: period {check['period']}, "
              f"margin {check['minimum_trace_margin']}, global gap {check['global_band_gap']}")
    print('PASS: general compiler checked on all 16 five-hysteron Hamiltonian cycles')
    print('Full exact results: results/verification_report.json')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        raise
