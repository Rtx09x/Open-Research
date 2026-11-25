# No higher-radius perfect rank-two intrinsic-spin code

**Status, 2026-10-26:** internally independently audited theorem. The complete analytic reduction, root premise, and exact arithmetic have passed separate advisor and parent checks. This is a separate equality-rigidity extension, not a change to the frozen volume-bound package. External review and publication priority are unresolved.

## Statement and scope

A complex two-dimensional subspace of Sym^n(C²) detecting all intrinsic spin tensors through rank 2t cannot satisfy

    n+1=2(t+1)²

for any integer t≥2. Combined with the independently audited unconditional volume bound, this implies the uniform strengthening

    n≥2t²+4t+2,    t≥2,

for arbitrary physical t-qubit error correction in a fully symmetric rank-two code. It remains strictly weaker than the proposed minimum 3t²+3t+1. The known t=1,n=7 perfect code is a positive control and is not excluded. No uniqueness classification of that code is asserted.

The only additional hypothesis used below is the equality case of the volume theorem. There is no nondegeneracy, realness, parity or finite-group restriction. Equality itself forces purity and the Lloyd-root condition, as proved and independently audited in `volume_dependency/EQUALITY_COROLLARY.md`.

## 1. Exact necessary root condition

Set N=n+1=2(t+1)² and x=r(r+1). The equality corollary forces all t roots of the degree-t Lloyd polynomial to occur at distinct values x=r(r+1), for integers r>2t. In particular its monic normalization f_t(x) has integer coefficients and splits completely over the integers.

Write it in the monic integer Newton basis

    B_h(x)=∏_(i=0)^(h−1) [x−i(i+1)],  B_0=1,
    f_t(x)=Σ_(h=0)^t β_h B_h(x),  β_t=1.

Every β_h must be an integer: descending elimination of the highest-degree monomial subtracts an integer multiple of an integer monic polynomial. This condition is stronger to compute than directly expanding every monomial coefficient, but is exactly equivalent to integral monomial coefficients.

The finite hypergeometric Lloyd expression in the volume proof gives the exact ratio

    β_(h−1)/β_h
      =−h(h+1)(N²−h²)/[(t−h+1)(t+h+1)].             (1)

All factors in the denominator are nonzero for 1≤h≤t.

## 2. A uniform divisibility obstruction

For t≥3, three steps of (1), with N=2(t+1)², give

    β_(t−3)=−P(t)/[12(2t−1)],                       (2)

where the integer polynomial factors as

    P(t)=t²(t−2)(t−1)²(t+1)(t+2)(2t+5)
          ·(2t²+3t+2)(2t²+3t+3)(2t²+3t+4)
          ·(2t²+5t+1).

The following is an exact identity in Z[t]:

    2P(t)+2025=(2t−1)Q(t),                          (3)

with

    Q(t)=32t^15+288t^14+976t^13+1184t^12−1750t^11
          −8842t^10−14048t^9−7596t^8+9674t^7
          +22174t^6+17452t^5+2632t^4−6936t^3
          −7140t²−4050t−2025.

If (2) is integral, then 2t−1 divides P(t), so (3) forces

    2t−1 | 2025 = 3^4·5².                          (4)

This is the uniform step. It reduces every integer t≥3, however large, to the complete finite list

    3,5,8,13,14,23,38,41,68,113,203,338,1013.

The list comes from all 15 positive divisors of 2025, omitting the two that give t=1,2. No untested interval or asymptotic assumption remains.

## 3. Exact arithmetic eliminates the finite list

Applying recurrence (1) for at most five steps gives a nonintegral Newton coefficient in nine cases:

| t | depth k, coefficient β_(t−k) | reduced denominator |
|---:|---:|---:|
|13|5|23|
|23|5|43|
|38|5|73|
|41|3|3|
|68|5|19|
|113|5|223|
|203|3|3|
|338|5|673|
|1013|3|3|

For t=3,5,8,14 the monic polynomials are integral, but do not split completely over the indicated prime field. Removing every linear factor gives the following exact nonconstant remainders, none of which has a root in that field:

| t | prime p | removed linear factors | remaining factor in F_p[x] |
|---:|---:|---|---|
|3|19|x−18|x²+18x+2|
|5|23|x(x−2)(x−6)|x²+20x+3|
|8|23|x(x−3)(x−14)|x^5+13x^4+21x³+9x²+17x+14|
|14|3|x^7(x−2)^4|x³+x²+2|

An integer-root factorization would remain a product of linear factors modulo every prime, including multiplicities. These exact remainders therefore contradict the necessary integer-root condition. The checker reconstructs each full polynomial via (1), verifies each factorization modulo p, and evaluates the remaining factor at every element of F_p; it does not trust a numerical root finder.

Finally, for t=2,

    f_2(x)=(x−114)(x−272).

The root 114 is not r(r+1) for an integer r because 4·114+1=457 lies strictly between 21² and 22². Thus the stronger necessary spin-index condition eliminates this case even though the polynomial splits over Z.

Every t≥2 is excluded at equality. For the positive control t=1, f_1(x)=x−42 and 42=6·7, as required by the known perfect seven-qubit code.

## 4. Reproduction and falsification criteria

`check_no_perfect_rank_two.py` uses only exact integer arithmetic and `fractions.Fraction`; it has no worker imports, floating point, optimizer, SymPy or external-data dependency. Its JSON records the complete divisor list, exact obstructing coefficients, full modular polynomials, factorization witnesses, all finite-field evaluations and the t=1 control. Runtime is about 0.002 seconds.

The mathematical points requiring independent challenge are: the equality Lloyd-root premise; the monic Newton integrality implication; normalization of recurrence (1); exact formula (2); identity (3); exhaustiveness of the divisor list; and the four modular factorizations. A failure of any of those would invalidate this extension, without changing the separately frozen volume theorem.

This is an all-t result only because of the exact divisibility reduction (4), not because a finite sample suggested a pattern. It improves the uniform lower bound by one qubit; it neither proves the leading-constant3 conjecture nor resolves the current distance-seven 35–37 frontier.
