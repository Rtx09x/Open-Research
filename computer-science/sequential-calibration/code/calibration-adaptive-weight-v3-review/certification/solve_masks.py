#!/usr/bin/env python3
"""Independent SPR solver; disjoint bitmask encoding, no symmetry reduction.

Cell zero is leftmost. A set bit in p/m means plus/minus respectively.
The finite-horizon payoff includes pointer stopping at every layer.
No input or transitions are imported from another implementation.
"""
import argparse
import csv
import hashlib
import json
import resource
import time
from pathlib import Path


def subsets(mask):
    s = mask
    while True:
        yield s
        if not s:
            break
        s = (s - 1) & mask


def boards(n):
    full = (1 << n) - 1
    for p in range(full + 1):
        for m in subsets(full ^ p):
            yield p, m


def code(p, m, n):
    return p | (m << n)


def transitions(n, p, m, greedy=False):
    full = (1 << n) - 1
    for j in range(n):
        b = 1 << j
        if (p | m) & b:
            continue
        left = b - 1
        right = full ^ (left | b)
        eligible = (m & left) | (p & right)
        options = []
        for deleted in [eligible] if greedy else subsets(eligible):
            pp, mm = p & ~deleted, m & ~deleted
            options.extend((code(pp | b, mm, n), code(pp, mm | b, n)))
        yield j, tuple(options)


def solve(n, horizon, greedy=False, allow_stop=True):
    started = time.perf_counter()
    allboards = list(boards(n))
    moves = {}
    base = bytearray([255]) * (1 << (2*n))
    count = 0
    for p, m in allboards:
        c = code(p, m, n)
        base[c] = (p | m).bit_count()
        moves[c] = tuple(transitions(n, p, m, greedy))
        count += sum(len(dst) for _, dst in moves[c])
    built = time.perf_counter()
    layers = [base]
    for h in range(1, horizon + 1):
        old = layers[-1]
        new = bytearray([255]) * len(base)
        for p, m in allboards:
            c = code(p, m, n)
            best = base[c] if allow_stop or not moves[c] else 0
            for _, successors in moves[c]:
                response = min(old[x] for x in successors)
                best = max(best, response)
            new[c] = best
        layers.append(new)
    ended = time.perf_counter()
    return layers, {
        'n': n, 'horizon': horizon, 'valid_boards': len(allboards),
        'successor_entries': count, 'transition_build_seconds': built-started,
        'bellman_seconds': ended-built, 'total_seconds': ended-started,
        'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'empty_values': [x[0] for x in layers],
        'layers_sha256': [hashlib.sha256(x).hexdigest() for x in layers],
    }


def first_difference(a, b, n):
    for h in range(len(a)):
        for p, m in sorted(boards(n), key=lambda pm: ((pm[0]|pm[1]).bit_count(), pm)):
            c = code(p, m, n)
            if a[h][c] != b[h][c]:
                return {'n': n, 'h': h, 'p': p, 'm': m,
                        'a': a[h][c], 'b': b[h][c]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n', type=int, default=8)
    ap.add_argument('--horizon', type=int, default=16)
    ap.add_argument('--out', type=Path, default=Path(__file__).parent/'results')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    summary = {'rules': 'Dai-Fishelson 2610.07623v2 section 2.2',
               'encoding': 'leftmost bit=0, p=plus mask, m=minus mask; index=p+(m<<n)',
               'stop': True, 'all_legal_deletion_subsets': True,
               'reuse': True, 'full_board_terminal': True, 'symmetry_pruning': False,
               'runs': [], 'variant_counterexamples': []}
    for n in range(1, args.max_n+1):
        a, report = solve(n, args.horizon)
        (args.out/f'n{n}_values.bin').write_bytes(b''.join(a))
        with (args.out/f'n{n}_values.csv').open('w') as f:
            wr = csv.writer(f)
            wr.writerow(['p', 'm'] + [f'h{h}' for h in range(args.horizon+1)])
            for p, m in sorted(boards(n)):
                c = code(p,m,n)
                wr.writerow([p,m]+[layer[c] for layer in a])
        for name, kw in [('delete_all_only', {'greedy':True}),
                         ('no_pointer_stop', {'allow_stop':False})]:
            other, _ = solve(n, args.horizon, **kw)
            diff = first_difference(a, other, n)
            summary['variant_counterexamples'].append({'variant':name,'n':n,'first':diff})
        summary['runs'].append(report)
        print(json.dumps(report), flush=True)
        (args.out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')


if __name__ == '__main__':
    main()
