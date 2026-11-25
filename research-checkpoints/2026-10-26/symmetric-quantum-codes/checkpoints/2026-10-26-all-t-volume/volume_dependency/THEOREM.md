# Unconditional intrinsic-spin volume bound

**Status, 2026-10-26:** internally established analytic theorem. The complete mathematical argument, normalization, prior monotonicity dependency, and exact symbolic controls have been independently checked by the advisor and parent. This is not external mathematical review or publication-priority verification. The result has leading constant 2 for one logical qubit; it does **not** prove the proposed minimum formula 3t²+3t+1 or general intrinsic nondegeneracy.

The proof is analytic and uniform in t and K. Finite exact computations are normalization and algebra controls, not an extrapolation or an SDP proof of the infinite family.

## Theorem

For integers K≥2,t≥1, a K-dimensional complex code C⊂Sym^n(C²) detecting all spin tensors of ranks 1,…,min(2t,n) must satisfy

    n+1 ≥ K(t+1)².

In particular, arbitrary t-qubit error correction by one logical qubit requires n≥2t²+4t+1. The unrestricted complex model is used, without parity, realness, purity, group symmetry, or nondegeneracy assumptions.

The proof excludes the ordinary intrinsic LP at n=K(t+1)²−2 and propagates that exclusion downwards using **Manes–Subramanian–Jiang, arXiv2610.00561v1, SupplementVIII.2, Theorem6**. Their theorem concerns LP feasibility, not physical code padding. No shadow monotonicity is assumed or needed.

## 1. Normalization and the Lloyd-square identity

Let N=n+1,j=n/2,d_r=2r+1, and let T_rq be Hilbert–Schmidt-orthonormal spin tensors. For a rank-K projector P define

    a_r=(N/K²) Σ_q |Tr(P T_rq)|².

Then a_r≥0,a_0=1,Σ_ra_r=N/K. With

    M_ar=(-1)^(n+a+r) d_a {j j a; j j r},
    R_a(r)=N M_ar/d_a,

define also

    b_r=(N/K) Σ_q Tr(P T_rq P T_rq†).

The intrinsic MacWilliams identity is b=KMa. Cauchy–Schwarz gives b_r≥a_r, and scalar compression (Knill–Laflamme detection) gives equality at ranks r≤2t. Thus the ordinary necessary LP constraints are

    a≥0,  a_0=1,  Σ_r a_r=N/K,
    KMa−a≥0,  (KMa−a)_r=0 for 0≤r≤2t.

Indeed, expanding P in the orthonormal tensor basis and using the channel eigenvalues below gives b_r=K(Ma)_r directly. The Racah symmetry gives R_a(x)=R_x(a). In particular R_0=1,

    R_1(r)=1−2r(r+1)/(n(n+2)).

Define m=(t+1)² and

    L(r)=Σ_(a=0)^t d_a R_a(r),
    c_r=Σ_(a,b=0)^t d_a d_b {a b r; j j j}².

The standard irreducible-tensor product formula yields the positive linearization

    R_a(x)R_b(x)=Σ_r N d_r {a b r; j j j}² R_r(x).

One direct justification uses the covariant unital channels

    Φ_a(X)=(N/d_a)Σ_q T_aq X T_aq†.

Their rank-x eigenvalues are R_a(x). Multiplying their Kraus tensors and using Clebsch–Gordan orthogonality gives Φ_aΦ_b=Σ_r N d_r{a b r;j j j}²Φ_r, proving the formula and positivity. Consequently

    L(x)²=N Σ_(r=0)^(2t) d_r c_r R_r(x),
    c_0=m/N,   c_r=0 for r>2t.

Multiply by a_x and sum x, using KL and M_rx=d_r R_r(x)/N. This gives the exact scalar identity

    Σ_(x=0)^n [K L(x)²−N²c_x] a_x=0.                    (1)

This identity needs only the ordinary intrinsic enumerator constraints, not a three-copy SDP or the new loss-rank lemma.

## 2. A lower bound on the Lloyd response

At every n≥2m−2,

    L(r)/m = 4F3(−t,t+2,−r,r+1; 2,−n,n+2;1).

The finite-sum identity follows by summing the Racah expansion, using

    Σ_(a=0)^t (2a+1)(−a)_h(a+1)_h
      = m(−t)_h(t+2)_h/(h+1).

It can be checked by subtracting the expression at t−1; the difference is the a=t summand.

For1≤r≤2t this is an alternating series with positive term magnitudes A_h. At n_0=2m−2, the consecutive ratio obeys

    A_(h+1)/A_h
      = [(t−h)(t+h+2)(r−h)(r+h+1)]
          /[(h+1)(h+2)(n−h)(n+h+2)]
      ≤ r(r+1)/[4m(h+1)(h+2)] < 1.

Indeed [(t−h)(t+h+2)]/[(n_0−h)(n_0+h+2)]
=[m−(h+1)²]/[(2m−1)²−(h+1)²]≤1/(4m). Increasing n only lowers the ratio and the first negative term. Hence

    L(r)/m ≥ 1−r(r+1)/(8m) > 0.                       (2)

## 3. Racah escape probability

For fixed r define a Markov kernel on0,…,n,

    P^(r)_ab=N d_b {a b r; j j j}².

The positive linearization at x=0 gives stochasticity. Symmetry gives detailed balance d_aP_ab=d_bP_ba. Evaluating that same linearization at x=1 and using R_1 proves

    Σ_b P_ab [b(b+1)−a(a+1)]
      =r(r+1)[1−2a(a+1)/(n(n+2))].                    (3)

The overlap of the radius-t index set with its transition is

    c_r/c_0=(1/m)Σ_(a≤t,b≤t)d_aP_ab.

Let E_r=1−c_r/c_0 be the escape probability. Put s=max(0,r−t). By the triangle condition a+b≥r, every a<s escapes with probability1; their stationary weight is s². Sum (3) over a≤t with weights d_a. Internal transitions cancel by detailed balance. Remove the a<s rows and their **exact** drift contribution. Every remaining escaping pair has

    0<b(b+1)−a(a+1)≤r(2t+r+1).

Using Σ_(a=s)^t d_a=m−s² and
Σ_(a=s)^t d_a a(a+1)=(m−s²)(m+s²−1)/2 gives

    E_r ≥ s²/m + [(r+1)/(2t+r+1)]·[(m−s²)/m]
                       ·[1−(m+s²−1)/(n(n+2))].       (4)

The right side increases with n. At n_0=2m−2 it is strictly greater than

    q_r=r(r+1)/(4m),    1≤r≤2t.                     (5)

For r≤t, the difference has numerator
(r+1)[4m−1−r(2t+r+1)] over4m(r+2t+1), positive since r≤t.

For t≤r≤2t, write x=r/t−1∈[0,1]. Multiply the difference by the positive denominator

    D=4t(t+1)^4(t+2)(r+2t+1).

Its numerator is Σ_(i=0)^5 C(5,i) B_i(t)x^i(1−x)^(5−i), with

    B0=t(t+1)^3(t+2)(t²+7t+3),
    B1=t(t+1)²(t+2)(2t³+42t²+52t+15)/5,
    B2=t(t+1)(t⁵+89t⁴+368t³+526t²+305t+60)/10,
    B3=t(86t⁵+456t⁴+908t³+848t²+371t+60)/10,
    B4=t(42t⁵+227t⁴+458t³+429t²+188t+30)/5,
    B5=2t(t+1)(4t⁴+19t³+27t²+16t+3).

Every coefficient is positive for t≥1. This is an all-t polynomial identity, not interpolation from finite instances. Thus

    c_r/c_0 < 1−q_r,  1≤r≤2t, n≥2m−2.              (6)

## 4. Critical-length exclusion

Fix N=K m−1, so n=K m−2≥2m−2. The r0 coefficient in (1) is

    K m²−N m=m>0.

For1≤r≤2t, (2) and (6) give

    K L(r)²−N²c_r
      > K m²(1−q_r/2)²−N m(1−q_r)
      = K m² q_r²/4 + m(1−q_r) > 0,

since0<q_r<1. For r>2t, c_r=0 and the coefficient is K L(r)²≥0. Therefore the left side of (1) is strictly positive because a_0=1 and every a_r≥0, a contradiction.

The ordinary LP is infeasible at n=K m−2. For n≤2t, the detected tensors already span all End(Sym^n(C²)), impossible for K≥2. For n≥2t+1, Manes et al Theorem6 propagates the critical exclusion to every smaller n by ordinary-LP monotonicity. This proves the theorem.

For completeness, the length-transport matrix in the cited theorem has rows ℓ=0,…,n+1 and columns k=0,…,n:

    (T_n)_(ℓk)=0                                      if ℓ<k,
    (T_n)_(kk)=(n+1−k)(n+2k+2)/[(n+2)(n+k+2)],
    (T_n)_(ℓk)=(2ℓ+1)[n+2+2k(k+1)](n−k)!(n+k+1)!
                 /[(n+2)(n+1−ℓ)!(n+ℓ+2)!]             if ℓ>k.

It is nonnegative, column-stochastic and lower-triangular, satisfies
M_(n+1)T_n=T_nM_n, and has (T_n)_(00)=(n+1)/(n+2).
Consequently a′=[(n+2)/(n+1)]T_n a preserves every displayed ordinary LP constraint at the next length: nonnegativity and normalization are immediate, and lower-triangularity preserves the low-rank equality rows. The all-n intertwining identity is proved in the cited source, Lemmas 31–35 and Theorem 6; the accompanying independent symbolic and exact-rational checks supplement that dependency. We do not assume physical-code padding.

## 5. Physical-qubit applicability

A fully symmetric code is a K-dimensional complex subspace of
Sym^n(C²) inside (C²)^{⊗n}. Correction of arbitrary errors on at most t physical qubits implies scalar compression of every Pauli product supported on at most 2t qubits: each such product is an error product E†F with both E and F supported on at most t sites. Rank-r collective spin tensors are linear combinations of degree-at-most-r collective-spin products and hence of physical operators with support at most r. Their compression is therefore scalar for r≤2t. This supplies the theorem's necessary detection hypothesis without a real, parity, group-symmetry, anticoherence, or nondegeneracy restriction. The theorem does not identify the intrinsic collective-spin syndrome space with the larger full physical Pauli error-image space.

## Scope and positive controls

No intrinsic Gram invertibility was derived: degeneracy might still occur without beating this dimension inequality. The t1,n7,K2 known code saturates the bound and is not excluded; at equality N=Km the r0 coefficient vanishes, and high-rank Lloyd zeros can support the enumerator. The known19 and37 codes lie above the bound. The formula2t²+5t observed in small scalar/shadow endpoints is not proved here and is not the exact scalar frontier at t7.

Relevant prior methods: [Bumgardner1205.4517](https://arxiv.org/html/1205.4517v1) and [Okada2502.14165](https://arxiv.org/pdf/2502.14165v1) provide intrinsic MacWilliams/LP structure; their basic volume count retains a null-error quotient. More precisely, Okada §3.4, printedp89 (PDF page93), explicitly reports that LP numerics through n100 suggest the quantum volume bound may hold for degenerate su(2) codes. The theorem above addresses that explicitly stated observation; a later priority claim is not inferred from the present source search. Okada §2.2 Theorem2.2.2 retains the kernel subtraction, and §3.5 gives analytic distance2 bounds, not this general theorem.

[Zhang–Chen2606.22538v2](https://arxiv.org/html/2606.22538v2) uses Lloyd-square/two-ball methods in physical Hamming space, not this spin metric. [Manes2610.00561v1](https://arxiv.org/html/2610.00561v1) provides the necessary LP monotonicity. No priority claim is made; the search for a later unconditional intrinsic-spin theorem is not exhaustive.

`check_spin_hamming.py` and `spin_hamming_candidate_controls.json` give exact symbolic and convention controls, including the Bernstein identity,284 stochastic/drift/reversibility cases,440 full linearization cases, nine critical(K,t) instances, and the known7 saturating control. These tests supplement the analytic proof; no all-t conclusion is inferred from finite sampling.

The equality-only consequences are recorded separately in `EQUALITY_COROLLARY.md`; they are not dependencies of this theorem. The finite t=2 minimum-19 theorem and t=3 bracket 35–37 are likewise separate results.
