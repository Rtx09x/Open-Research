"""Exact rational certificate: hierarchical wavelets do not give forest support.

N=8,k=1,L=2. Finest active vectors are coordinate vectors. Coarse left/right
active vectors are unrelated rational rotations (3/5,4/5) and (5/13,12/13).
All computations use standard-library Fraction, with no numerical tolerance.
"""
from fractions import Fraction as F
import json


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def tr(a):
    return list(map(list, zip(*a)))


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def outer(a, b):
    return [[x*y for y in b] for x in a]


def vec(n, i):
    return [F(j == i) for j in range(n)]


def wavelet(c, s):
    cols = [vec(8, i) for i in [1, 3, 5, 7]]
    for offset in [0, 4]:
        v = [F(0)]*8
        v[offset], v[offset+2] = -s, c
        cols.append(v)
    for offset in [0, 4]:
        v = [F(0)]*8
        v[offset], v[offset+2] = c, s
        cols.append(v)
    return tr(cols)


def main():
    qu = wavelet(F(3, 5), F(4, 5))
    qv = wavelet(F(5, 13), F(12, 13))
    assert mul(tr(qu), qu) == eye(8)
    assert mul(tr(qv), qv) == eye(8)
    # Orthogonal coefficient atoms for the fixed class in physical coordinates.
    atoms = []
    for i in range(4):
        a, d = vec(8, 2*i), vec(8, 2*i+1)
        atoms.extend([outer(a, d), outer(d, a), outer(d, d)])
    u, v = tr(qu), tr(qv)
    for i in range(2):
        atoms.extend([outer(u[6+i], v[4+i]),
                      outer(u[4+i], v[6+i]),
                      outer(u[4+i], v[4+i])])
    for i in range(2):
        for j in range(2):
            atoms.append(outer(u[6+i], v[6+j]))
    assert len(atoms) == 22
    grams = [[sum(x*y for r, s in zip(a, b) for x, y in zip(r, s))
              for b in atoms] for a in atoms]
    assert grams == eye(22)
    transformed = [mul(mul(tr(qu), a), qv) for a in atoms]
    support = {(i, j) for b in transformed for i in range(8)
               for j in range(8) if b[i][j] != 0}
    assert len(support) == 30
    # First atom is e0 e1^T, its two nonzero transformed entries are tied.
    nonzero = {(i, j): transformed[0][i][j] for i in range(8)
               for j in range(8) if transformed[0][i][j]}
    assert nonzero == {(4, 0): F(-4, 5), (6, 0): F(3, 5)}
    assert {(0, 4), (4, 6), (0, 6)} <= support  # explicit undirected triangle
    # A single entry in the envelope is not in the transformed true class.
    isolated = outer(vec(8, 4), vec(8, 0))
    coeff = [sum(x*y for r, s in zip(isolated, b) for x, y in zip(r, s))
             for b in transformed]
    projected_norm2 = sum(x*x for x in coeff)
    assert projected_norm2 == F(16, 25)
    distance_squared = 1-projected_norm2
    assert distance_squared == F(9, 25)
    report = dict(status='PASS', arithmetic='exact rational', N=8, k=1, L=2,
                  true_subspace_dimension=22, coordinate_envelope_dimension=30,
                  forest_support_maximum_dimension=22,
                  left_coarse_active=['3/5', '4/5'],
                  right_coarse_active=['5/13', '12/13'],
                  first_atom_nonzero={str(ij): str(value) for ij, value in nonzero.items()},
                  envelope_atom_squared_distance_to_true_class=str(distance_squared),
                  triangle_vertices=[0, 4, 6], support=sorted(support))
    with open('wavelet_support_obstruction.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
