"""Six-k-query approximation of a known block-forest support.

The decoder receives only forward/transpose vector-product callables.  Its
comparator is the best matrix on the KNOWN support, not the full HSS class.
"""
from __future__ import annotations

import numpy as np


def depths(parent):
    """Validate a rooted forest and return its vertex depths."""
    m = len(parent)
    out = [-1] * m
    for i in range(m):
        seen = set()
        j = i
        while j != -1 and out[j] == -1:
            if j in seen:
                raise ValueError("parent array contains a cycle")
            seen.add(j)
            if not -1 <= parent[j] < m:
                raise ValueError("invalid parent")
            j = parent[j]
        d = -1 if j == -1 else out[j]
        j = i
        path = []
        while j != -1 and out[j] == -1:
            path.append(j)
            j = parent[j]
        for j in reversed(path):
            d += 1
            out[j] = d
    return np.array(out, dtype=int)


def support(parent, k=1):
    m = len(parent)
    out = np.eye(m, dtype=bool)
    for i, p in enumerate(parent):
        if p != -1:
            out[i, p] = out[p, i] = True
    return np.kron(out, np.ones((k, k), dtype=bool))


def probes(parent, k, signs):
    c = depths(parent) % 3
    out = np.zeros((len(parent) * k, 3 * k), dtype=int)
    for i, s in enumerate(signs):
        out[i*k:(i+1)*k, c[i]*k:(c[i]+1)*k] = s * np.eye(k, dtype=int)
    return out


def approximate(matvec, rmatvec, parent, k, sigma, tau):
    """Exactly 3k forward and 3k transpose vector calls, without entry access."""
    m = len(parent)
    c = depths(parent) % 3
    omega, psi = probes(parent, k, sigma), probes(parent, k, tau)
    y = np.column_stack([matvec(omega[:, j]) for j in range(3*k)])
    z = np.column_stack([rmatvec(psi[:, j]) for j in range(3*k)])
    b = np.zeros((m*k, m*k), dtype=np.result_type(y, z))
    for i, p in enumerate(parent):
        ii = slice(i*k, (i+1)*k)
        ci = slice(c[i]*k, (c[i]+1)*k)
        b[ii, ii] = sigma[i] * y[ii, ci]
        if p != -1:
            pp = slice(p*k, (p+1)*k)
            cp = slice(c[p]*k, (c[p]+1)*k)
            b[ii, pp] = sigma[p] * y[ii, cp]
            b[pp, ii] = tau[p] * z[ii, cp].T
    return b


def leakage_weights(parent):
    c = depths(parent) % 3
    m = len(parent)
    out = np.zeros((m, m), dtype=int)
    for i in range(m):
        for j in range(m):
            out[i, j] = (int(c[j] == c[i])
                         + int(parent[i] != -1 and c[j] == (c[i]-1) % 3)
                         + int(parent[j] != -1 and c[i] == (c[j]-1) % 3))
    out[support(parent)] = 0
    return out


def expected_error_squared(a, parent, k):
    e = np.where(support(parent, k), 0, a)
    w = np.kron(leakage_weights(parent), np.ones((k, k), dtype=int))
    return np.sum((1+w)*e*e)
