"""Experimental coordinate-faithful three-frame construction from advisor.

No approximation theorem asserted. The coordinate limit implements depth-mod-3
on the representative forest rather than on hierarchy levels.
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


def ordered_frame(fixed, side, signs):
    e = np.eye(3)
    # At root, the two active coordinates and a shared third direction.
    incoming = [(e[0], e[1], e[2]), (e[1], e[2], e[0])]
    p = 0
    for us, vs in reversed(fixed):
        bases = us if side == 'u' else vs
        out, following = [], []
        for i, b in enumerate(bases):
            f, g, h = incoming[i]
            g = signs[p]*g
            p += 1
            a, bb = b[:, 0]
            f1, f2 = a*f-bb*g, bb*f+a*g
            out.extend([f1, f2])
            following.extend([(f1, f2, h), (f2, h, f1)])
        incoming = following
    return np.stack(out)


def main():
    rng = np.random.default_rng(382652)
    rows = []
    for L, reps, basis in [(1, 16, 'dense'), (2, 4096, 'coordinate'),
                            (2, 4096, 'dense'), (3, 500, 'dense')]:
        n = 2**(L+1)
        _, fixed = make_hss(1, L, rng)
        if basis == 'coordinate':
            fixed = [([np.array([[1.], [0.]]) for _ in us],
                      [np.array([[1.], [0.]]) for _ in vs]) for us, vs in fixed]
        ns = n-2
        exact = reps == 2**(2*ns)
        stream = (itertools.product((-1., 1.), repeat=2*ns) if exact
                  else (rng.choice((-1., 1.), 2*ns) for _ in range(reps)))
        gram = np.zeros((n*n, n*n))
        mean = np.zeros_like(gram)
        start = time.monotonic()
        for count, ss in enumerate(stream, 1):
            om = ordered_frame(fixed, 'v', ss[:ns])
            ps = ordered_frame(fixed, 'u', ss[ns:])
            r = recovery_operator(fixed, om, ps)
            error = np.eye(n*n)-r
            gram += error.T@error
            mean += r
        gram /= count
        mean /= count
        eig, vec = np.linalg.eigh(gram)
        row = dict(L=L, n=n, reps=count, basis=basis, exhaustive_signs=exact,
                   maximum_expected_error_eigenvalue=float(eig[-1]),
                   mean_symmetry_defect=float(np.linalg.norm(mean-mean.T)),
                   seconds=time.monotonic()-start)
        rows.append(row)
        print(json.dumps(row), flush=True)
        np.savez(f'ordered_frame_L{L}_{basis}.npz', error_gram=gram,
                 mean_decoder=mean, worst_input=vec[:, -1].reshape(n, n))
        with open('ordered_frame_results.json', 'w') as f:
            json.dump(rows, f, indent=2)


if __name__ == '__main__':
    main()
