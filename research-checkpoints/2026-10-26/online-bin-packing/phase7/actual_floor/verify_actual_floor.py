#!/usr/bin/env python3
"""Actual fixed-algorithm lower bound from seven sizes and identical tiny items.

Rebuild positive-container rates directly from parameter proportions, without
importing any weight reconstruction or using upper-pricing constraints.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
source = ROOT / 'phase4/retune_two/retuned_certificate.json'
J = json.loads(source.read_text())
P = {int(j): {'lo': F(r['lower']), 'hi': F(r['upper']),
             'a': {F(i): F(a) for i, a in r['containers']}}
     for j, r in J['parameters'].items()}
classes = [165, 179, 205, 208, 211]
p = F(997, 2100120)
tau = F(1, 10**9)
s = p - 6 * tau
huge = F(1, 2) + tau
d = F(1, 43)
A = sorted(P[212]['a'])
alpha = [P[212]['a'][a] for a in A]
beta = alpha[1]
k = [a // s for a in A]
K = sum(a * n for a, n in zip(alpha, k))
assert k == [596, 2106] == [a // p for a in A]
assert 0 < s < p < d and huge > F(1, 2)
assert huge + sum(P[j]['lo'] + tau for j in classes) + s == 1
assert all(P[j]['lo'] < P[j]['lo'] + tau <= P[j]['hi'] for j in classes)
assert all(n * s <= a < (n + 1) * s for a, n in zip(A, k))

rates = {}
non_tiny_constant = F(2)  # Source large-class165 positive-count loss.
for j in classes:
    mean = sum(i * a for i, a in P[j]['a'].items())
    pos = sum(a for i, a in P[j]['a'].items() if i * P[j]['hi'] > F(1, 2))
    rates[j] = pos / mean
    if j != 165:
        non_tiny_constant += (len(P[j]['a']) - 1) * (rates[j] * max(P[j]['a']) + 1)
assert rates[165] == P[165]['a'][F(2)] / (1 + P[165]['a'][F(2)])
Kp = 1 + sum(rates.values())
lower = Kp + beta / K
anchor = F(J['target'])
B = sum(a * w for a, w in zip(A, alpha))
R = B - p * K
assert Kp + beta * p / (B - p) == anchor  # Check, not a premise of the proof.
gap = anchor - lower
assert gap == beta * p * (p - R) / ((B - p) * (B - R)) > 0

def counts_after(m):
    n1 = (alpha[0] * (m - 1)).__floor__() + 1
    return [n1, m - n1]

def native_trace(m):
    scale = math.lcm(s.denominator, *[a.denominator for a in A])
    size = int(s * scale)
    capacity = [int(a * scale) for a in A]
    gaps = []
    types = []
    count = [0, 0]
    seen = 0
    for number in range(m):
        typ = next(i for i in range(2) if count[i] <= (alpha[i] * number).__floor__())
        # Present exactly floor(A_typ/s) identical arrivals. Search all prior
        # advertised containers on each arrival, not merely the newest one.
        for q in range(k[typ]):
            fits = [(g, j) for j, g in enumerate(gaps) if g >= size]
            if fits:
                dest = min(fits)[1]
                assert q > 0
            else:
                assert q == 0 and len(gaps) == number
                count[typ] += 1
                gaps.append(capacity[typ])
                types.append(typ)
                dest = number
            gaps[dest] -= size
            assert dest == number and gaps[dest] >= 0
            seen += 1
        assert all(g < size for g in gaps)
    assert count == counts_after(m)
    assert seen == sum(n * kk for n, kk in zip(count, k))
    assert len(gaps) == m
    return {'containers': m, 'tiny_items': seen, 'type_counts': count,
            'all_final_gaps_less_than_identical_item': True,
            'OPT_exact': seen,
            'actual_bin_lower_from_source_invariants': str(Kp * seen + count[1] - non_tiny_constant)}

traces = [native_trace(m) for m in [1, 10, 64, 128]]
large = []
for m in [10**3, 10**6, 10**9]:
    count = counts_after(m)
    N = sum(n * kk for n, kk in zip(count, k))
    ratio_bound = Kp + (count[1] - non_tiny_constant) / N
    assert abs(F(count[0]) - alpha[0] * m) < 1
    assert abs(F(N) - K * m) < abs(k[1] - k[0])
    large.append({'containers': m, 'tiny_items_and_OPT': N, 'type_counts': count,
                  'rigorous_finite_ratio_lower': str(ratio_bound)})

out = {
    'status': 'PASS actual algorithm-specific asymptotic lower bound; no universal online lower claim',
    'source_certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'tau': str(tau), 'tiny_item_size': str(s), 'huge_size': str(huge),
    'non_tiny_sizes': {str(j): str(P[j]['lo'] + tau) for j in classes},
    'offline_bin_volume': '1', 'tiny_capacity_floor_counts': k,
    'tiny_type_proportions': list(map(str, alpha)), 'mean_items_per_tiny_container': str(K),
    'positive_container_rates': {str(j): str(w) for j, w in rates.items()},
    'non_tiny_positive_rate_including_huge': str(Kp),
    'non_tiny_count_error_constant': str(non_tiny_constant),
    'actual_algorithm_ratio_lower': str(lower), 'frozen_upper': str(anchor),
    'remaining_analysis_only_window': str(gap), 'traces': traces,
    'compressed_arbitrarily_large_instances': large,
    'scope': 'Seven fixed rational sizes, deterministic tiny BF with the frozen capacities/proportions and unchanged non-tiny AH positive-container invariants. No claim that the algorithm ratio equals this lower bound. No improvement of the universal lower bound1.542780906...; no full-gap closure.'
}
(HERE / 'actual_floor_certificate.json').write_text(json.dumps(out, indent=2) + '\n')
print('PASS actual fixed-algorithm lower', float(lower), 'analysis-only window', float(gap),
      'replayed items', sum(t['tiny_items'] for t in traces))
