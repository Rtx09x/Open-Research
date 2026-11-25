"""Experimental 3-column frames suggested by the independent advisor.

New detail direction is orthogonal to the entire parent two-frame plane,
not merely the child's active frame. Only k=1 here. No guarantee claimed.
"""
import itertools
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from baseline import make_hss
from frozen_operator import recovery_operator


def nonbacktracking_frame(fixed, side, signs):
    x = np.eye(3)[:2]
    planes = [x, x]
    p = 0
    for us, vs in reversed(fixed):
        bases = us if side == 'u' else vs
        out, next_planes = [], []
        for i, b in enumerate(bases):
            f = x[i:i+1]
            w = np.array([[-b[1, 0]], [b[0, 0]]])
            g = signs[p] * np.cross(planes[i][0], planes[i][1])[None, :]
            p += 1
            assert abs(float(f @ g.T)) < 1e-12
            assert abs(float(g @ g.T)-1) < 1e-12
            out.append(b@f+w@g)
            next_planes.extend([np.vstack([f, g])] * 2)
        x = np.vstack(out)
        planes = next_planes
    return x


def main():
    rng = np.random.default_rng(748192)
    rows = []
    for L, reps, basis in [(1, 16, 'dense'), (2, 4096, 'dense'),
                            (2, 4096, 'coordinate'), (3, 400, 'dense')]:
        n = 2**(L+1)
        h, fixed = make_hss(1, L, rng)
        if basis == 'coordinate':
            fixed = [([np.array([[1.], [0.]]) for b in us],
                      [np.array([[1.], [0.]]) for b in vs]) for us, vs in fixed]
        nsign = n-2
        exact = reps == 2**(2*nsign)
        stream = (itertools.product((-1., 1.), repeat=2*nsign) if exact
                  else (rng.choice((-1., 1.), 2*nsign) for _ in range(reps)))
        gram = np.zeros((n*n, n*n))
        mean = np.zeros_like(gram)
        start = time.monotonic()
        for count, ss in enumerate(stream, 1):
            om = nonbacktracking_frame(fixed, 'v', ss[:nsign])
            ps = nonbacktracking_frame(fixed, 'u', ss[nsign:])
            r = recovery_operator(fixed, om, ps)
            error = np.eye(n*n)-r
            gram += error.T@error
            mean += r
        gram /= count
        mean /= count
        eig, vec = np.linalg.eigh(gram)
        row = dict(L=L, n=n, reps=count, basis=basis, exhaustive_signs=exact,
                   maximum_expected_error_eigenvalue=float(eig[-1]),
                   mean_projection_defect=float(np.linalg.norm(mean@mean-mean)),
                   mean_symmetry_defect=float(np.linalg.norm(mean-mean.T)),
                   seconds=time.monotonic()-start)
        rows.append(row)
        print(json.dumps(row), flush=True)
        np.savez(f'nonbacktracking_L{L}_{basis}.npz', error_gram=gram,
                 mean_decoder=mean, worst_input=vec[:, -1].reshape(n, n))
        with open('nonbacktracking_results.json', 'w') as f:
            json.dump(rows, f, indent=2)


if __name__ == '__main__':
    main()
