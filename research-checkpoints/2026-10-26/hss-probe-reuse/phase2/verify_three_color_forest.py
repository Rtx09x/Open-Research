"""Exhaustive finite-sign verification; integer arithmetic, no sampling error."""
import itertools
import json
import time

import numpy as np

from three_color_forest import (approximate, depths, expected_error_squared,
                                leakage_weights, support)


def all_rooted_forests(m):
    for parent in itertools.product(range(-1, m), repeat=m):
        try:
            depths(parent)
        except ValueError:
            continue
        yield parent


def check(a, parent, k):
    m = len(parent)
    mask = support(parent, k)
    h = np.where(mask, a, 0)
    count = 0
    error_sum = 0
    b_sum = np.zeros_like(a)
    assert leakage_weights(parent).max(initial=0) <= 1
    calls = [0, 0]

    def mv(x):
        calls[0] += 1
        return a @ x

    def rmv(x):
        calls[1] += 1
        return a.T @ x

    for signs in itertools.product((-1, 1), repeat=2*m):
        before = calls.copy()
        b = approximate(mv, rmv, parent, k, signs[:m], signs[m:])
        assert [calls[j]-before[j] for j in range(2)] == [3*k, 3*k]
        assert not np.any(b[~mask])
        b_sum += b
        error_sum += int(np.sum((a-b)**2))
        count += 1
    predicted = int(expected_error_squared(a, parent, k))
    optimum = int(np.sum((a-h)**2))
    assert np.array_equal(b_sum, count*h)
    assert error_sum == count*predicted
    assert predicted <= 2*optimum
    return {"parent": list(parent), "k": k, "sign_assignments": count,
            "error_sum": error_sum, "expected_error": predicted,
            "optimum": optimum, "query_count_each_execution": 6*k}


def main():
    start = time.monotonic()
    rng = np.random.default_rng(20261025)
    rows = []
    forests = list(all_rooted_forests(4))
    assert len(forests) == 125  # rooted-forest Cayley identity (4+1)^(4-1)
    for parent in forests:
        for k in (1, 2):
            a = rng.integers(-3, 4, size=(4*k, 4*k), dtype=np.int64)
            rows.append(check(a, parent, k))
    for parent in [(-1, 0, 1, 2, 3), (-1, 0, 0, 0, 0),
                   (-1, 0, -1, 2, -1), (3, 0, 1, -1, 3)]:
        for k in (1, 2, 3):
            a = rng.integers(-3, 4, size=(5*k, 5*k), dtype=np.int64)
            rows.append(check(a, parent, k))
            structured = np.where(support(parent, k), a, 0)
            rows.append(check(structured, parent, k))
    # Sharpness AND explicit full-HSS-comparator failure: rank-one input.
    a = np.zeros((4, 4), dtype=np.int64)
    a[0, 3] = 1
    sharp = check(a, (-1, 0, 1, 2), 1)
    assert sharp["expected_error"] == 2 and sharp["optimum"] == 1
    report = {"status": "PASS", "exact_integer_arithmetic": True,
              "all_labeled_rooted_forests_on_four_vertices": len(forests),
              "cases": len(rows), "executions": sum(x["sign_assignments"] for x in rows),
              "sharp_rank_one_scope_counterexample": sharp,
              "seconds": time.monotonic()-start, "results": rows}
    with open("three_color_forest_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))


if __name__ == "__main__":
    main()
