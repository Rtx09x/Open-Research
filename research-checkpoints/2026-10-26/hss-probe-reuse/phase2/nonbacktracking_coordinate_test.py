"""Exact integer single-channel stress test of experimental nonbacktracking frames.

Coordinate bases only. Computes output energy via its orthogonal coefficient
ledger instead of materializing an N-by-N reconstruction. This is NOT the
successful direct three-color forest decoder.
"""
import itertools
import json

import numpy as np


def coordinate_frame(L, signs):
    x = np.eye(3, dtype=np.int64)[:2]
    planes = [x, x]
    offset = 0
    for ell in range(1, L+1):
        out, new = [], []
        for i in range(2**ell):
            f = x[i]
            g = signs[offset]*np.cross(planes[i][0], planes[i][1])
            offset += 1
            out.extend([f, g])
            new.extend([np.stack([f, g])]*2)
        x, planes = np.stack(out), new
    return x


def unit_noise_energy(L, i, j, sigma, tau):
    om, ps = coordinate_frame(L, sigma), coordinate_frame(L, tau)
    y, z = np.zeros_like(om), np.zeros_like(ps)
    y[i] = om[j]
    z[j] = ps[i]
    levels = []
    for _ in range(L):
        dad = np.sum(ps[::2]*z[1::2], axis=1)
        dda = np.sum(y[1::2]*om[::2], axis=1)
        ddd = np.sum(y[1::2]*om[1::2], axis=1)
        levels.append(int(np.sum(dad**2+dda**2+ddd**2)))
        y, z = (y[::2]-dad[:, None]*om[1::2],
                z[::2]-dda[:, None]*ps[1::2])
        om, ps = om[::2], ps[::2]
    root = int(np.sum((y@om.T)**2))
    return 1+sum(levels)+root, levels, root


def main():
    rng = np.random.default_rng(612094)
    rows = []
    for L in [2, 4, 6, 8, 10]:
        n = 2**(L+1)
        i, j = (2**L-1)//3, (2**L-1)//3+2**L
        ns = n-2
        stream = (itertools.product((-1, 1), repeat=2*ns) if L == 2
                  else (rng.choice((-1, 1), 2*ns) for _ in range(20)))
        energies = set()
        ledgers = set()
        count = 0
        for ss in stream:
            value, lev, root = unit_noise_energy(L, i, j, ss[:ns], ss[ns:])
            energies.add(value)
            ledgers.add(tuple(lev+[root]))
            count += 1
        row = dict(L=L, n=n, input_entry=[i, j], fixed_class_optimum=1,
                   sign_assignments=count, exhaustive=(L == 2),
                   observed_exact_errors=sorted(energies),
                   observed_exact_coefficient_ledgers=sorted(ledgers))
        rows.append(row)
        print(json.dumps(row), flush=True)
        with open('nonbacktracking_coordinate_results.json', 'w') as f:
            json.dump(rows, f, indent=2)


if __name__ == '__main__':
    main()
