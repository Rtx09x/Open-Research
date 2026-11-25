"""Falsification test: one-bank-independent arbitrary input transport.

Fixed forward tree frame; initial forward samples arbitrary, transpose zero.
Average only transpose-bank complement signs. A uniform energy bound here
could control one part of an ad-column sector. This is not asserted.
"""
import itertools
import json
import pathlib
import sys
import time

import numpy as np
from scipy.linalg import block_diag

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from baseline import make_hss
from frozen_operator import sign_frame


def energy_operators(fixed, om, ps, include_cross=False):
    n = len(om)
    y = np.eye(2*n).reshape(2*n, n, 2)
    z = np.zeros_like(y)
    out = []
    crosses = []
    for us, vs in fixed:
        u, v = block_diag(*us), block_diag(*vs)
        d = np.zeros((2*n, len(om), len(om)))
        cross = np.zeros((2*n, 2*n))
        for i, (ui, vi) in enumerate(zip(us, vs)):
            sl = slice(2*i, 2*i+2)
            pu, pv = ui@ui.T, vi@vi.T
            d[:, sl, sl] = ((np.eye(2)-pu)@y[:, sl]@om[sl].T
                            +pu@(((np.eye(2)-pv)@z[:, sl]@ps[sl].T).transpose(0,2,1)))
            if include_cross:
                wy = np.array([[-ui[1, 0]], [ui[0, 0]]])
                wz = np.array([[-vi[1, 0]], [vi[0, 0]]])
                ya, yd = ui.T@y[:, sl], wy.T@y[:, sl]
                za, zd = vi.T@z[:, sl], wz.T@z[:, sl]
                f, g = vi.T@om[sl], wz.T@om[sl]
                p, q = ui.T@ps[sl], wy.T@ps[sl]
                dadg = (p@zd.transpose(0, 2, 1))@g
                ddatq = (yd@f.T).transpose(0, 2, 1)@q
                cross += (ya.reshape(2*n, -1)@dadg.reshape(2*n, -1).T
                          +za.reshape(2*n, -1)@ddatq.reshape(2*n, -1).T)
        y, z = u.T@(y-d@om), v.T@(z-d.transpose(0,2,1)@ps)
        om, ps = v.T@om, u.T@ps
        flat = np.concatenate([y.reshape(2*n, -1), z.reshape(2*n, -1)], axis=1)
        out.append(flat@flat.T)
        crosses.append((cross+cross.T)/2)
    return (out, crosses) if include_cross else out


def main():
    rng = np.random.default_rng(26738)
    rows = []
    for L in [1, 2, 3]:
        n = 2**(L+1)
        _, fixed = make_hss(1, L, rng)
        om = sign_frame(fixed, 'v', rng.choice((-1, 1), n-2))
        grams = [np.zeros((2*n, 2*n)) for _ in range(L)]
        start = time.monotonic()
        for count, ss in enumerate(itertools.product((-1, 1), repeat=n-2), 1):
            ps = sign_frame(fixed, 'u', ss)
            for g, add in zip(grams, energy_operators(fixed, om, ps)):
                g += add
        eigs = [float(np.linalg.eigvalsh(g/count)[-1]) for g in grams]
        row = dict(L=L, n=n, transpose_sign_assignments=count,
                   maximum_energy_eigenvalues=eigs, seconds=time.monotonic()-start)
        print(json.dumps(row), flush=True)
        rows.append(row)
        with open('one_bank_transport_results.json', 'w') as f:
            json.dump(rows, f, indent=2)
        np.savez(f'one_bank_transport_L{L}.npz', grams=np.stack(grams)/count)


if __name__ == '__main__':
    main()
