#!/usr/bin/env python3
"""Independent literal-tuple checker; does NOT import either solver.

Enumerates eligible positions and Python combinations (not bit submasks).
Checks every Bellman equation, an independently produced ternary table,
reflection+sign-reversal, time/substate monotonicity, and fixed points.
"""
from itertools import combinations, product
from pathlib import Path
import csv
import hashlib
import json
import resource
import time

ROOT = Path(__file__).parent
LEAD = ROOT.parent/'theory'/'exact'


def legal_successors(board, j):
    eligible = [i for i, s in enumerate(board)
                if (i < j and s == -1) or (i > j and s == 1)]
    for size in range(len(eligible)+1):
        for deleted in combinations(eligible, size):
            b = list(board)
            for i in deleted:
                b[i] = 0
            for sign in [-1,1]:
                b[j] = sign
                yield tuple(b)


def main():
    reports = []
    overall = time.perf_counter()
    for n in range(1,9):
        start = time.perf_counter()
        table = {}
        with (ROOT/'results'/f'n{n}_values.csv').open() as f:
            for row in csv.DictReader(f):
                p, m = int(row['p']), int(row['m'])
                assert p & m == 0
                b = tuple(1 if p & (1<<i) else -1 if m & (1<<i) else 0 for i in range(n))
                assert b not in table
                table[b] = tuple(int(row[f'h{h}']) for h in range(17))
        assert set(table) == set(product([-1,0,1], repeat=n))
        lead_path = LEAD/f'values_n{n}.bin'
        raw = lead_path.read_bytes()
        assert len(raw) == 17*3**n, (str(lead_path),len(raw))
        local_equations = local_actions = compared_values = 0
        first_bad_sign_symmetry = None
        first_fixed = None
        for b, values in table.items():
            occupied = sum(s != 0 for s in b)
            assert values[0] == occupied
            trit_code = sum((0 if s == 0 else 1 if s == 1 else 2)*3**i for i,s in enumerate(b))
            for h, value in enumerate(values):
                assert raw[h*3**n+trit_code] == value, (n,b,h,value,raw[h*3**n+trit_code])
                compared_values += 1
            mirror = tuple(-s for s in reversed(b))
            assert table[mirror] == values
            if first_bad_sign_symmetry is None and table[tuple(-s for s in b)] != values:
                h = next(h for h in range(17) if table[tuple(-s for s in b)][h] != values[h])
                first_bad_sign_symmetry = {'board': b, 'h': h, 'v': values[h], 'inverted_v': table[tuple(-s for s in b)][h]}
            for i, s in enumerate(b):
                if s:
                    smaller = b[:i]+(0,)+b[i+1:]
                    assert all(x <= y for x,y in zip(table[smaller],values))
            successors = [(j,list(legal_successors(b,j))) for j,s in enumerate(b) if not s]
            for h in range(1,17):
                expected = occupied
                for j, options in successors:
                    expected = max(expected, min(table[child][h-1] for child in options))
                    local_actions += len(options)
                assert values[h] == expected, (n,b,h,values[h],expected)
                assert values[h] >= values[h-1]
                if occupied == n:
                    assert values[h] == n
                local_equations += 1
        for h in range(1,17):
            if all(values[h] == values[h-1] for values in table.values()):
                first_fixed = h-1
                break
        report = {
            'n':n, 'bellman_equations_checked':local_equations,
            'legal_response_values_checked':local_actions,
            'independent_solver_values_compared':compared_values,
            'all_checks_passed':True,
            'whole_table_fixed_point_at_h':first_fixed,
            'empty_all_horizon_value':table[(0,)*n][first_fixed] if first_fixed is not None else None,
            'sign_reversal_alone_counterexample':first_bad_sign_symmetry,
            'lead_file_sha256':hashlib.sha256(raw).hexdigest(),
            'own_csv_sha256':hashlib.sha256((ROOT/'results'/f'n{n}_values.csv').read_bytes()).hexdigest(),
            'seconds':time.perf_counter()-start,
            'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        }
        reports.append(report)
        print(json.dumps(report),flush=True)
    out = {'implementation_independence':'tuple+combinations checker; no solver import',
           'runs':reports, 'seconds':time.perf_counter()-overall}
    (ROOT/'results'/'independent_check.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__ == '__main__':
    main()
