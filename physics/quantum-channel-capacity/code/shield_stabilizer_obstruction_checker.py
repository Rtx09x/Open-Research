#!/usr/bin/env python3
"""Exact, standard-library certificate for a random-stabilizer shield obstruction.

The *mathematical* theorem (included in the answer) imports only the exact
collision probability of uniform random isotropic binary subspaces.
This program independently proves the numerical inequality

   P[Bin(m,41/200) < t] + (1/2) sqrt(2**(m+2)*C_tail) < 1/q

at the indicated (m,t,q), where
   C_tail = sum_{w=t}^m binom(m,w) 3**w (159/200)**(2*(m-w))
                                     (41/600)**(2*w).

All arithmetic and all comparisons are exact Python integers, no float.
"""
from fractions import Fraction
from time import perf_counter


def certify(m: int, t: int, q: int) -> dict:
    start = perf_counter()
    # Single Pauli probability a=159/200=477/600, b=41/600.
    # Probability of nonidentity Pauli error p=41/200=123/600.
    a, b, p, den = 477, 41, 123, 600
    D = pow(den, m)

    # A / D = Pr[Bin(m, p) < t], with exact numerator A.
    v = pow(a, m)
    A = 0
    for w in range(t):
        A += v
        if w + 1 < t:
            numer = v * (m - w) * p
            divisor = (w + 1) * a
            v, rem = divmod(numer, divisor)
            assert rem == 0, (m, w, 'binomial numerator recurrence')

    # B / D**2 = C_tail, including all 3^w Pauli error strings.
    v = pow(a, 2*m)
    B = 0
    for w in range(m + 1):
        if w >= t:
            B += v
        if w < m:
            numer = v * (m - w) * 3 * b*b
            divisor = (w + 1) * a*a
            v, rem = divmod(numer, divisor)
            assert rem == 0, (m, w, 'collision numerator recurrence')

    # Prove A/D + (1/2) sqrt(2**(m+2) B/D**2) < 1/q.
    gap = D - q * A
    assert gap > 0, 'the discarded low-weight mass already exceeds 1/q'
    lhs = (q*q) * (2**(m+2)) * B
    rhs = 4 * gap * gap
    assert lhs < rhs, 'the collision tail bound is too weak'

    return {
        'm': m, 't': t, 'q': q,
        'proved_expectation_upper_bound': f'1/{q}',
        'strict_gap_bits': rhs.bit_length() - lhs.bit_length(),
        'elapsed_seconds': round(perf_counter() - start, 3),
    }


def exact_half_erasure_knapsack(rows, denominator):
    """Optimize a fixed stabilizer syndrome reliability table exactly.

    rows: iterable of (syndrome_total_integer_mass, maximum_coset_integer_mass).
    The physical Pauli distribution has common denominator `denominator`.
    Returns the exact *optimal* Choi half-trace distance to 50% erasure.
    """
    data = [(Fraction(p), Fraction(mm)) for p, mm in rows]
    assert sum(p for p, _ in data) == denominator
    data.sort(key=lambda row: row[1]/row[0], reverse=True)
    remaining = Fraction(denominator, 2)
    recovered_mass = Fraction(0)
    for p, mm in data:
        if not remaining:
            break
        accepted_mass = min(p, remaining)
        recovered_mass += accepted_mass * (mm / p)
        remaining -= accepted_mass
    assert remaining == 0
    return Fraction(1,2) - recovered_mass / denominator


def small_code_control():
    """Enumerate all 256 Pauli errors of the [[4,2,2]] XXXX/ZZZZ code.

    Verifies the syndrome/logical coset table without assuming its values.
    """
    m = 4
    mask = (1 << m)-1
    gens = [mask, mask << m]  # XXXX, ZZZZ in (x | z<<m) notation
    stabs = [0, gens[0], gens[1], gens[0] ^ gens[1]]

    def syndrome(e):
        x, z = e & mask, e >> m
        answer = 0
        for j, g in enumerate(gens):
            gx, gz = g & mask, g >> m
            bit = ((x & gz).bit_count() + (z & gx).bit_count()) % 2
            answer |= bit << j
        return answer

    # The probability of an exact Pauli string is 477^(m-w)*41^w / 600^m.
    chosen_reps, coset_masses = {}, {}
    for e in range(1 << (2*m)):
        x, z = e & mask, e >> m
        s = syndrome(e)
        chosen_reps.setdefault(s, e)
        logical_coset = min(e ^ chosen_reps[s] ^ h for h in stabs)
        wt = (x | z).bit_count()
        key = (s, logical_coset)
        coset_masses[key] = coset_masses.get(key, 0) + 477**(m-wt)*41**wt

    den = 600**m
    rows = []
    for s in range(4):
        vals = [v for (ss, _), v in coset_masses.items() if ss == s]
        assert len(vals) == 16
        rows.append((sum(vals), max(vals)))

    a = Fraction(159, 200)
    b = Fraction(41, 600)
    eta = Fraction(109, 150)
    p0 = (1 + 3*eta**4) / 4
    p1 = (1 - eta**4) / 4
    m0 = a**4 + 3*b**4
    m1 = a**3*b + a*b**3 + 2*b**4
    assert rows[0] == (p0*den, m0*den)
    assert all(row == (p1*den, m1*den) for row in rows[1:])
    error = exact_half_erasure_knapsack(rows, den)
    assert error == Fraction(7165372619, 77357250000)
    return str(error)


if __name__ == '__main__':
    print('[[4,2,2]] exact optimum Choi half-distance:', small_code_control())
    for triple in ((4096, 777, 100), (8192, 1553, 4000)):
        print(certify(*triple))
    print('PASS: both rational-exact finite-block inequalities certified.')
