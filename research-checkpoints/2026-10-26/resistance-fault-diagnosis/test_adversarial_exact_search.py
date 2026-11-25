"""Fresh counterexamples and exhaustive finite-dictionary regression checks."""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
import json
from exact_search import responses, adaptive, nonadaptive

def oracle(rows, m):
    @lru_cache(None)
    def go(state):
        if len(state) <= 1: return 0
        best = float('inf')
        for row in rows:
            children = {tuple(e for e in state if row[e] == value) for value in set(row[e] for e in state)}
            if len(children) > 1:
                best = min(best, 1 + max(go(child) for child in children))
        return best
    d = go(tuple(range(m)))
    return None if d == float('inf') else d

q, r = responses(2, [(0,1)]*3, resistances=[F(1),F(2),F(3)])
assert r == [[F(6,5),F(3,4),F(2,3)]]
parallel_cases = 0
for rs in product((F(1,3),F(1),F(7,2)), repeat=4):
    _, actual = responses(2, [(0,1)]*4, resistances=rs)
    assert actual[0] == [1/sum(1/r for i,r in enumerate(rs) if i != j) for j in range(4)]
    parallel_cases += 1
_, rows = responses(4, [(0,1),(1,2),(2,3),(3,0)], queries=[(0,1)])
d, cert, _ = adaptive(rows)
assert d is None and cert['indistinguishable'] == 14
assert nonadaptive(rows) == (None,None)
assert adaptive([], hypothesis_count=1)[0] == 0
assert adaptive([], hypothesis_count=3)[0] is None
assert nonadaptive([], hypothesis_count=1) == (0,())
assert nonadaptive([], hypothesis_count=3) == (None,None)
for bad in ([], [[]], [[0],[0,1]]):
    try: adaptive(bad)
    except ValueError: pass
    else: raise AssertionError('Invalid dictionary accepted')
cases = 0
for values in product(range(3), repeat=6):
    rows = [values[:3],values[3:]]
    d, certificate, _ = adaptive(rows)
    assert d == oracle(rows,3)
    fixed,_ = nonadaptive(rows)
    distinct = len({tuple(row[e] for row in rows) for e in range(3)}) == 3
    assert (d is not None) == distinct == (fixed is not None)
    if d is None:
        witness = [e for e in range(3) if certificate['indistinguishable'] >> e & 1]
        assert len(witness) > 1
        assert all(len({row[e] for e in witness}) == 1 for row in rows)
    cases += 1
print(json.dumps({'parallel_cases': parallel_cases+1, 'finite_dictionary_cases': cases,
                  'restricted_cycle_counterexample': 'fixed', 'empty_query_boundaries': 'passed'}))
