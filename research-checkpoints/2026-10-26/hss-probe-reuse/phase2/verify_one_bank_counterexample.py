"""Exact rational/full-recursion refutation of the one-bank <=1 shortcut.

Standard library only; no imported reconstruction implementation.
"""
from fractions import Fraction as F
from itertools import product
import json


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def combine(a, x, b, y):
    return [a*u+b*v for u, v in zip(x, y)]


def perp(x):
    return [-x[1], x[0]]


def frame(bases, signs):
    rows = [[F(1), F(0)], [F(0), F(1)]]
    offset = 0
    for level in reversed(bases):
        out = []
        for i, (a, b) in enumerate(level):
            f = rows[i]
            g = [signs[offset]*x for x in perp(f)]
            offset += 1
            out.extend([combine(a, f, -b, g), combine(b, f, a, g)])
        rows = out
    return rows


def carry(y, z, om, ps, us, vs):
    yn, zn, on, pn = [], [], [], []
    for i, (u, v) in enumerate(zip(us, vs)):
        wu, wv = perp(u), perp(v)
        ya = combine(u[0], y[2*i], u[1], y[2*i+1])
        yd = combine(wu[0], y[2*i], wu[1], y[2*i+1])
        za = combine(v[0], z[2*i], v[1], z[2*i+1])
        zd = combine(wv[0], z[2*i], wv[1], z[2*i+1])
        f = combine(v[0], om[2*i], v[1], om[2*i+1])
        g = combine(wv[0], om[2*i], wv[1], om[2*i+1])
        p = combine(u[0], ps[2*i], u[1], ps[2*i+1])
        q = combine(wu[0], ps[2*i], wu[1], ps[2*i+1])
        yn.append(combine(1, ya, -dot(p, zd), g))
        zn.append(combine(1, za, -dot(yd, f), q))
        on.append(f)
        pn.append(p)
    return yn, zn, on, pn


def main():
    us = [[(F(1), F(0)) for _ in range(2**ell)] for ell in [4,3,2,1]]
    vs = [[(F(1), F(0)) for _ in range(2**ell)] for ell in [4,3,2,1]]
    us[1][0] = (F(0), F(1))
    vs[2][0] = vs[3][0] = (F(3,5), F(4,5))
    omega = frame(vs, [1]*30)
    active_indices = [0, 2, 6, 14]
    values = []
    for ss in product((-1, 1), repeat=4):
        signs = [1]*30
        for i, s in zip(active_indices, ss):
            signs[i] = s
        psi = frame(us, signs)
        y = [[F(0), F(0)] for _ in range(32)]
        z = [[F(0), F(0)] for _ in range(32)]
        y[1] = omega[0].copy()  # independent of every transpose sign
        assert sum(dot(row, row) for row in y) == 1
        om, ps = omega, psi
        energies = []
        for u, v in zip(us, vs):
            y, z, om, ps = carry(y, z, om, ps, u, v)
            energies.append(sum(dot(row, row) for row in y+z))
        assert energies == [F(1), F(1), F(1), F(913,625)]
        values.append([str(x) for x in energies])
    report = dict(status='PASS', arithmetic='fractions.Fraction',
                  input_energy='1', final_energy='913/625',
                  final_energy_minus_input='288/625',
                  active_sign_cases=len(values), inactive_signs=26,
                  full_sign_distribution_accounted_for='2^30',
                  all_cut_energies=values[0])
    with open('one_bank_counterexample_certificate.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
