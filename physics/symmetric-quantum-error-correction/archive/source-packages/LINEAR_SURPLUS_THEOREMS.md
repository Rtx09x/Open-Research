# Linear-surplus amplitude barriers and exact sharp-grid exclusions

**Scope.** 26 October 2026. Fully permutation-symmetric qubit codes, normalized Dicke states. These are necessary-obstruction results within the alternating-disjoint-support, uniform-grid amplitude-polynomial family, not unrestricted bounds on `n_min(t)`. The user-provided exact [M]/[S] reduction is restated and used below. Publication priority has not been established.

## Theorems

Let integers `t >= 10000`, `0 <= s <= floor(t/1000)`, `m=3t+s`, `g=t+1`, `n=mg`, `D=t-1`. Let `q` be a real polynomial of degree `<=t+s-1` with `q(i)>0` for every integer `i=0,...,m`. Put `h(i)=q(i)q(i+1)`, `c=(m-1)/2`. Let `i_e` be the edge index of parity `e` nearest `c`.

**Theorem 1 (full-degree amplification necessity).** If the alternating-grid logical code with squared amplitudes `binom(m,i)q(i)` corrects `t` arbitrary physical-qubit errors, then for EACH `e=0,1`,

    max_{0<=i<m, i≡e (mod 2)} h(i) / h(i_e) >= exp(t/4).

No upper degree restriction beyond the stipulated `t+s-1` is used in this theorem. In particular, any centrally unimodal `h`, or any `h` growing from its parity center by less than `exp(t/4)`, is impossible.

**Theorem 2 (uniform low-degree exclusion).** The same code cannot correct `t` physical errors if `deg q <= floor(t/100)`. This exclusion remains true for a nonzero real polynomial that is only nonnegative, rather than strictly positive, on `0,...,m`, with edge phases irrelevant when an edge weight is zero. Thus for fixed `s`, every successful code in this family for sufficiently large `t` requires polynomial degree greater than `t/100`. No existence at higher degree is asserted.

**Theorem 3 (five exact, full-degree exclusions).** At `s=0`, for each `t=4,5,6,7,8`, the degree-`<=t-1` necessary interpolation equations for `q` have only the trivial solution, even over complex coefficients. In particular, there is no real positive `q` and no phase assignment in the proposed family at `n=3t(t+1)` for these values. This does not exclude unrestricted symmetric codes at those lengths.

## Part I. Physical moment equations and the central ladder product

The erasure of `k=2t` qubits has normalized Dicke Kraus coefficients

    E_a |D_n^w> = sqrt[binom(k,a) binom(n-k,w-a)/binom(n,w)] |D_{n-k}^{w-a}>.

The diagonal logical Gram differences vanish because `deg(q(i)i^r)<=m-1` for `r<=2t`. Because `t<g<=2t<2g`, only adjacent grid transitions contribute to cross-logical Gram entries. The exact falling-factorial identity in the input shows that full physical KL is equivalent to the two parity systems

    sum_{i≡e (mod2)} A_i sqrt[h(i)] eta_i P(i) = 0

for each `e=0,1`, every polynomial `P` of degree `<=D`, and phases `|eta_i|=1`. Here

    A_i^2=binom(m,i)binom(m,i+1) (g(m-i))_g (g(i+1))_g.

These are necessary conditions even if some `h(i)=0`, with the corresponding term absent. The full physical normalization factors are common nonzero scalars and have not been discarded from the actual validity claim.

Factorial cancellation gives

    A_i = g(m-i)binom(m,i) * product_{v=1}^{g-1}
          [(gi+v)(g(m-i-1)+v)]^(1/2).

Interpolate this positive function at real `i` in `(−min(v/g),m−1+min(v/g))`, and write `i=c+x`. Gamma's Weierstrass product yields the EXACT central expression

    A(c+x)/A(c)
      = product_{j=0}^infinity (1-x^2/(c+1+j)^2)
        * product_{v=1}^{g-1} (1-x^2/(c+v/g)^2)^(1/2).

Let

    a_t = sum_{j=0}^infinity (c+1+j)^(-2)
          + 1/2 sum_{v=1}^{g-1}(c+v/g)^(-2).

Using `-log(1-z)>=z`, and `-log(1-z)<=z/(1-z)` for `0<=z<1`, proves

    A(c+x)<=A(c)exp(-a_t x^2)                         (1)
    A(c+x)>=A(c)exp(-a_t x^2/(1-x^2/c^2))            (2)

for the relevant physical `|x|<=c` in (1), and `|x|<c` in (2).

Integral comparison for the decreasing reciprocal-square sum gives

    2/(m+1)+2t/(m+1)^2 <= a_t
    <= 2/(m+1)+4/(m+1)^2+2t/(m-1)^2.

Thus uniformly for the stated `t,s`,

    887/1000 <= t*a_t <= 9/10.                       (3)

The inequalities are elementary rational comparisons certified in `check_linear_surplus_constants.py`.

## Part II. One polynomial kills the neighboring parity edges

Let `d=floor(D/2)`, `delta=2d/t>=995/1000`. For any edge index `i0` of parity `e` with `h(i0)>0`, take

    P(i)=product_{j=1}^{d}[1-(i-i0)^2/(2j)^2].

Then `deg(P)=2d<=D`, `P(i0)=1`, and `P(i0±2j)=0` for `1<=j<=d`. Every other contributing edge has `i=i0+2l` with `|l|>=d+1`, so

    u=|i-i0|/t >= 1.

Direct factorial cancellation gives the exact identity

    |P(i)|=binom(|l|-1,d) binom(|l|+d,d).

The usual bound `binom(N,k)<=exp(N H(k/N))`, with binary entropy `H`, yields

    log|P(i)| <= t F(delta,u),
    F(a,u)=[(u+a)log(u+a)-(u-a)log(u-a)-2a log a]/2.

Writing `F(a,u)=a f(u/a)`, where

    f(z)=[(z+1)log(z+1)-(z-1)log(z-1)]/2,

one has the elementary **GLOBAL** bound `f(z)<3z^2/4` for `z>=1`. Here is a proof avoiding numerical maximization. `f''(z)=-1/(z^2-1)<0`. Its tangent at `13/12`, where `f'(13/12)=log 5`, gives

    f(z)<= (z+1)log 5 - log 12.

The minimum over real `z` of

    3z^2/4-(z+1)log 5+log 12

is `log(12/5)-(log 5)^2/3>0`. The rational exponential-series certificates `log5<161/100` and `log(12/5)>87/100`, with `87/100>(161/100)^2/3`, establish strict positivity exactly. Consequently

    log|P(i)| <= 0.755*t*u^2,                       (4)

since `3/(4delta)<0.755`.

## Part III. Exponential amplification, with no low-degree hypothesis

Take `i0=i_e` nearest `c`, so `|i0-c|<=1`. Equations (1)–(3) imply, for every surviving edge and `t>=10000`,

    log(A_i/A_i0) <= t[-0.887(u-0.0001)^2+0.0001].

Combining with (4), for every `u>=1`,

    log(A_i |P(i)|/A_i0)
       <= t[0.755u^2-0.887(u-0.0001)^2+0.0001]
       < -0.13t.                                       (5)

The quadratic in brackets decreases on `u>=1`, and its value at `u=1` is exactly `-0.13172260887`.

Let `R_e=max_{i≡e}h(i)/h(i0)`. Isolating the central nonzero term in the corresponding complex moment sum, taking absolute values, and using (5), gives

    1 <= m exp(-0.13t) sqrt(R_e).

Therefore `R_e >= exp(0.26t)/m^2`. Finally, `m<=3.001t` and for `t>=10000`,

    exp(t/100)>=(t/100)^6/720 > (3.001t)^2 >=m^2.

This proves `R_e>=exp(t/4)` separately for both parity classes. The phases cannot evade the triangle inequality. The theorem does not claim that an exponential shape is sufficient.

## Part IV. A positive proportion of polynomial amplitude freedom is necessary

Now allow `q(i)>=0` (possibly zeros), and suppose `r=2deg(q)<=t/50`. Fix a parity and consider its central edges in `|i-c|<=epsilon*t` for `epsilon=3/100`. There are at least `epsilon*t-2` such edges. A nonzero degree-`deg(q)` polynomial has at most `deg(q)` distinct integer roots, and the edges of a fixed parity are pairwise vertex-disjoint. Hence at least one central edge has `h(i)>0`; choose `i0` to maximize `h` over ALL edges of that parity in the window.

For `r>=1`, choose `r+1` such grid nodes `x_j`, with minimum spacing `Delta>=epsilon*t/(2r)`. Such nodes exist because the window has `~epsilon*t` parity edges, whereas `r<=.02t`; taking evenly spaced indices and rounding to the step-2 grid proves the displayed spacing for `t>=10000` (in fact `t>=1200` suffices for the rounding inequality). Values `h(x_j)` all lie between zero and `h(i0)`. Lagrange interpolation at these nodes, for any physical edge `i`, gives

    h(i)/h(i0) <= (m/Delta)^r * sum_{j=0}^r 1/(j!(r-j)!)
                = (m/Delta)^r * 2^r/r!
                <= (16e/epsilon)^r.

It follows, including `r=0`, that

    sqrt[h(i)/h(i0)] <= exp(0.073t),                 (6)

because `deg(q)<=t/100` and the rational exponential check proves `log(16e/epsilon)<7.3`.

Since `|i0-c|<=epsilon*t`, (1)–(3) also give

    log(A_i/A_i0)<=t[-0.887(u-epsilon)^2+0.001].

Combining this with (4),(6), every surviving term of the parity polynomial satisfies

    |a_iP(i)|/a_i0 <= exp(t[0.755u^2-0.887(u-0.03)^2+0.074])
                     <= exp(-t/200),                 (7)

since the quadratic is decreasing for `u>=1`, and at `u=1` it is the exact rational `-55783/10000000<-1/200`.

Full physical KL would force

    1 <= sum_{surviving i!=i0}|a_iP(i)|/a_i0
      <= m exp(-t/200) < 1,

using `exp(t/200)>=(t/200)^4/24>3.001t` for `t>=10000`. Contradiction. Hence `deg(q)>t/100` is necessary. The argument covers zero edge weights because the central interpolation nodes still exist and any zero-weight terms only reduce the upper bound.

## Part V. Full-degree sharp-grid exclusions using a modular Macaulay certificate

For `s=0` and every `t=4,...,8`, set `m=3t`, `g=t+1`, `D=t-1`. Write the most general polynomial in the *Newton/binomial basis*,

    q(X)=sum_{a=0}^{t-1} u_a binom(X,a),

where the `u_a` are indeterminates over `C`. For parity `e`, let `i=e+2j`, `j=0,...,M_e-1`, `k_e=M_e-D-2`. The exact [S] factorization forces a polynomial `R_e` of degree at most `2k_e` with

    R_e(j)= A_{e+2j}^2 q(e+2j)q(e+2j+1)/binom(M_e-1,j)^2.

Finite differences annihilate `j^r R_e(j)` for `0<=r<=M_e-2-2k_e`. Thus the homogeneous quadrics

    H_{e,r}(u)=sum_{j=0}^{M_e-1}
        (-1)^j A_{e+2j}^2 j^r/binom(M_e-1,j)
        *q(e+2j)q(e+2j+1) = 0                      (8)

are necessary. There are exactly `t+2` such quadrics altogether. All coefficients in (8) are rational; clear denominators, divide integer content, and fix each sign by its first nonzero coefficient.

Let `I` be the homogeneous ideal they generate in `Q[u_0,...,u_{t-1}]`. At total degree `h`, construct the integer Macaulay matrix whose rows are the coefficient vectors of *every* monomial of degree `h-2` multiplied by each `H_{e,r}`, in the degree-`h` monomial basis. These are not floating-point ranks:

| t | n | h | Matrix rows x columns | Rank modulo 101 |
|--:|--:|--:|--:|--:|
|4|60|3|24 x 20|20|
|5|90|4|105 x 70|70|
|6|126|4|168 x 126|126|
|7|168|5|756 x 462|462|
|8|216|5|1200 x 792|792|

Because each integer matrix has full column rank over `F_101`, it has full column rank over `Q`. Therefore `I` contains every monomial of degree `h`; in particular `u_a^h` belongs to `I` for each `a`. At any common zero over `C` this forces `u_a=0` for all `a`. Hence **the necessary equations (8) have no nonzero complex solution** for these five `t`. This proof requires neither positivity nor globally nonnegative SOS interpolation, since it disproves a weaker necessary condition. It does not disprove other physical code ansatzes at the same `n`.

## Exact reproducibility

Run from the extracted directory:

    python check_linear_surplus.py
    python check_linear_surplus_constants.py

Both programs use only Python's standard library and exact integer/Fraction arithmetic. No numerical optimization, irrational matrix approximation, or tolerance is involved in their verdicts. The Macaulay program builds every quadratic coefficient directly from falling factorials and binomial values; it does not trust a supplied quadratic list. The field-rank check uses modular row operations. An independent SymPy construction in the authoring session agreed coefficientwise, up to harmless overall signs, for all 38 quadratic forms across the five values of `t`.

The physical positive control is the known seven-qubit distance-three symmetric code

    |0> = sqrt(3/10)|D_7^0> + sqrt(7/10)|D_7^5>,
    |1> = sqrt(7/10)|D_7^2> - sqrt(3/10)|D_7^7>.

The first checker independently verifies all nine two-erasure cross Gram entries vanish and all nine diagonal Gram differences vanish, using the rational reduced Dicke coefficients. Reversing the sign of the final basis amplitude is deliberately rejected. This control ensures that an error in the cross-KL convention cannot masquerade as the sharp-family obstruction.

**Remaining gap.** For `t>=9`, the sharp family with arbitrary genuinely linear-degree `q` is not excluded by Theorem 3. For any fixed `s>=0`, a polynomial of degree between `t/100` and `t+s-1` might still satisfy both global nonnegative interpolation systems; no such exact code was found. None of these theorems bounds unrestricted `n_min(t)` beyond prior work. There is no claim of priority/external peer review.
