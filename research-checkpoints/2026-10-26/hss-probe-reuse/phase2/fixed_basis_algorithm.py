"""Known-dense-basis 4k-query decoder, with genuine Haar complements.

Numerical implementation for tests. The theorem concerns exact arithmetic.
The input bases must be known independently before these probes are drawn.
"""
import numpy as np
from scipy.linalg import block_diag


def haar(k, rng):
    q, r = np.linalg.qr(rng.normal(size=(k, k)))
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1
    return q*signs[None, :]


def complement(b):
    return np.linalg.qr(b, mode='complete')[0][:, b.shape[1]:]


def tree_frame(fixed, side, k, rng):
    rows = np.eye(2*k)
    for us, vs in reversed(fixed):
        bases = us if side == 'u' else vs
        out = []
        for i, b in enumerate(bases):
            active = rows[k*i:k*(i+1)]
            ambient = np.linalg.qr(active.T, mode='complete')[0][:, k:].T
            detail = haar(k, rng)@ambient
            out.append(b@active+complement(b)@detail)
        rows = np.vstack(out)
    return rows


def finite_tree_frame(fixed, side, k, rng):
    """Signed permutations with the explicitly coupled sibling-frame gauge."""
    identity = np.eye(2*k)
    incoming = [(identity[:k], identity[k:]), (identity[k:], identity[:k])]
    for us, vs in reversed(fixed):
        bases = us if side == 'u' else vs
        following = []
        rows = []
        for i, b in enumerate(bases):
            active, sibling = incoming[i]
            h = np.eye(k)[rng.permutation(k)]*rng.choice((-1., 1.), k)[:, None]
            detail = h@sibling
            local = b@active+complement(b)@detail
            f0, f1 = local[:k], local[k:]
            following.extend([(f0, f1), (f1, f0)])
            rows.append(local)
        incoming = following
    return np.vstack(rows)


def project(a, fixed):
    if not fixed:
        return a.copy()
    us, vs = fixed[0]
    k = us[0].shape[1]
    u, v = block_diag(*us), block_diag(*vs)
    d = np.zeros_like(a)
    for i, (ui, vi) in enumerate(zip(us, vs)):
        sl = slice(2*k*i, 2*k*(i+1))
        block = a[sl, sl]
        d[sl, sl] = block-ui@(ui.T@block@vi)@vi.T
    return d+u@project(u.T@a@v, fixed[1:])@v.T


def reconstruct(matvec, rmatvec, fixed, k, rng, finite=False):
    build = finite_tree_frame if finite else tree_frame
    omega, psi = build(fixed, 'v', k, rng), build(fixed, 'u', k, rng)
    y = np.column_stack([matvec(omega[:, j]) for j in range(2*k)])
    z = np.column_stack([rmatvec(psi[:, j]) for j in range(2*k)])
    energy = [float(np.linalg.norm(y)**2+np.linalg.norm(z)**2)]
    levels = []
    for us, vs in fixed:
        u, v = block_diag(*us), block_diag(*vs)
        d = np.zeros((len(omega), len(omega)))
        for i, (ui, vi) in enumerate(zip(us, vs)):
            sl = slice(2*k*i, 2*k*(i+1))
            pu, pv = ui@ui.T, vi@vi.T
            d[sl, sl] = ((np.eye(2*k)-pu)@y[sl]@omega[sl].T
                         +pu@((np.eye(2*k)-pv)@z[sl]@psi[sl].T).T)
        levels.append((u, v, d))
        y, z = u.T@(y-d@omega), v.T@(z-d.T@psi)
        omega, psi = v.T@omega, u.T@psi
        energy.append(float(np.linalg.norm(y)**2+np.linalg.norm(z)**2))
    b = y@omega.T
    for u, v, d in reversed(levels):
        b = u@b@v.T+d
    return b, energy
