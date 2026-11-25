# An exact nondegeneracy reduction for the remaining 18-qubit case

## Status
**Validated reduction, not a solution of the 18-versus-19 question.** Novelty has not been established. The lower bound 18 and the 19-qubit construction are already known. All statements here cover arbitrary complex rank-two code subspaces, not a PR ansatz.

## Theorem (conditional structural necessity)
If a two-dimensional subspace C of Sym^18(C²) corrects arbitrary errors on at most two physical qubits, then its nine intrinsic error syndromes of spin-tensor ranks 0,1,2 are linearly independent on each logical state. The joint syndrome image has dimension18 inside the19-dimensional symmetric sector, and its orthogonal complement is one-dimensional.

More quantitatively, choose a Hilbert–Schmidt orthonormal error basis E1,...,E9 for W0⊕W1⊕W2 and let ρ=P_C/2. The9×9 syndrome Gram G_ab=Tr(ρ E_a†E_b) obeys

    ||G−I9/19||_F² ≤ 1/722,
    λ_min(G) ≥ (1−1/sqrt(2))/19 > 0.

## Proof
Write N=19. Conjugation of the spin9 irreducible representation decomposes its operator space orthogonally as ⊕_(r=0)^18 W_r. Define a_r=N||Π_rρ||_HS². Since ρ=P/2 is a rank-two normalized projector,

    a0=1,  Σ a_r=N/2.

The standard intrinsic MacWilliams constraints give a≥0, Ha≥0, and (Ha)_r=0 for r=1,2,3,4, where

    H=2M−I,
    M_rk=(-1)^(18+r+k)(2r+1) {9 9 r;9 9 k}.

These constraints apply because physical errors of weight<=4 compress to tensor ranks<=4; no restriction on coefficient phases is used.

Define the linear map Φ(X)_ab=Tr(X E_a†E_b). It is equivariant under the spin9 conjugation action and the induced error-basis action. Schur's lemma implies Φ†Φ acts by a scalar c_r on each W_r. Products E_a†E_b have tensor rank at most4, so c_r=0 beyond4. Direct Hilbert–Schmidt evaluation on one unit q=0 tensor in each rank gives

    c0=9/19,
    c1=91/285,
    c2=288199/1187025,
    c3=33176/237405,
    c4=10120/142443.

These numbers also follow from the finite exact sum

    c_r=Σ_(a,b=0)^2 (2a+1)(2b+1) {a b r;9 9 9}².

Two independent implementations checked them: the worker uses exact6j arithmetic; the advisor constructs exact spin matrices and raw commutators, without6j symbols. Since Φ(I/N)=I9/N, orthogonal decomposition gives

    ||G−I9/N||_F² = (1/N)Σ_(r=1)^4 c_r a_r.

The exact rational dual certificate in `gram_bound_exact_certificate.json` proves that this last linear functional is at most1/722. Specifically, E has rows e0ᵀ,onesᵀ,H1,...,H4; b=(1,19/2,0,0,0,0); Q has rows I19,H5,...,H18. Stored rational y,z satisfy

    Eᵀy−Qᵀz=o,
    bᵀy=1/722,
    z≥0,

where o=(0,c1/19,...,c4/19,0,...,0). Thus oᵀa=bᵀy−zᵀQa≤1/722. The parent independently replayed the certificate with Python standard-library rational arithmetic and a factorial Racah formula, using neither solver output nor our module.

The spectral norm is bounded by the Frobenius norm. Hence G has the positive lower eigenvalue bound stated above. For orthonormal logical vectors u,v, the exact Knill–Laflamme equations make the18-vector joint error Gram equal to G⊗I2. Its rank is18, proving the dimension claim. ∎

## Exact next obstruction
Appending seven rank-three errors on each logical vector gives a32×32 Gram matrix. In dimension19, the Schur complement over the invertible18×18 degree<=2 block must be positive semidefinite of rank<=1. Product decomposition makes every entry a linear combination of spin moments of degree<=6, with all logical nonscalar moments through degree4 zero. This is a rigorous necessary condition. We have not proved it infeasible, and it is not yet asserted to be a sufficient description of physical code projectors.

## Reproduction
Run with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1:

    python intrinsic_lp.py
    python certify_lp.py
    python code19_exact.py
    python certify_gram_bound.py

`code19_exact.py` certifies existence of the known code's algebraic root and verifies all50 four-qubit reduced-Gram equations exactly. No floating near-zero is used as an exact-code certificate.

## References
- Intrinsic LP and physical-distance bridge: https://arxiv.org/html/2604.16023v2
- Prior evaluated spin bound and shadow constraints: https://arxiv.org/abs/2502.14165
- Known19-qubit construction: https://arxiv.org/html/2310.05358v3

# Additional restricted theorem: no 4-anticoherent 18-qubit code

**Scope warning:** this excludes only codes whose normalized intrinsic enumerators satisfy a1=a2=a3=a4=0. It does not exclude every18-qubit code. The known19-qubit control is not in this restricted pure class (its a2 is nonzero). Novelty remains unconfirmed.

Under the extra assumption, ρ has no tensor components of ranks1–4. Since products of the nine errors have rank<=4, G=I9/19 exactly. Therefore

    Ω=19 Σ_a E_a P E_a†

is the projector onto the18-dimensional error image, and Q=I−Ω is a rank-one orthogonal projector. Put t_r=Σ_(a=0)^2 M_ar. Twirl equivariance gives Q_r=−19 t_r P_r for r>0. The normalized intrinsic enumerator b of Q consequently obeys

    b0=1,
    b_r=4·19² t_r² a_r for r>0,
    M b=b.

The last identity holds because every rank-one code detects every operator. Define L=diag(1,4·19²t1²,...,4·19²t18²). Adding (M−I)L a=0 and a1=...=a4=0 to the ordinary code equalities yields an exact affine one-parameter system a=p+a18·v. Positivity gives contradictory rational bounds:

    a18 >= 133545301843278520173986684081 / 784303781203066926115600000000
         ≈ 0.17027241872840318       [from a8>=0],

    a18 <= 23408350603368311128956445043 / 147056958975575048646675000000
         ≈ 0.1591788023255414        [from (Ha)8>=0].

Exact elimination and a standalone rational Farkas certificate are stored in `pure_complement_elimination.json` and `pure_complement_certificate.json`. The latter has only two nonzero positivity multipliers. Run `python certify_pure_complement.py` to reconstruct and check the identity. The advisor independently approved the physical argument; advisor independently replayed the equality rank and contradictory bounds using standard-library rational arithmetic and a hypergeometric transform, without our imports.

## General spectral extension (not yet an exclusion)
Without the pure assumption, Ω0=19ΣE_aPE_a† still has nine eigenvalues19λ_i(G), each of multiplicity two, plus one zero. Its affine complement Q0=I−Ω0 has one eigenvalue1 and nine doubled eigenvalues1−19λ_i(G). It is not generally positive or a projector. If Q is the actual rank-one syndrome-complement projector, then

    ||Q0−Q||_F²=2·19² ||G−I9/19||_F² <=1.

This exact repeated-spectrum condition and the rank-one Schur complement are possible routes beyond the restricted theorem; no full contradiction is claimed.

## Conservative robustness extension (independently audited)
The short pure-complement certificate uses only complement ranks1 and3. It also yields a weak but strictly positive lower bound on the syndrome variance of any hypothetical unrestricted18-qubit code:

    10^-8 < ν := ||G−I9/19||_F² ≤1/722.

This does not come close to ruling out the remaining interval. Here is the perturbative argument, recorded for possible interval/SOS refinement.

Let y_low be the four multipliers for a1,...,a4, and y_c the two multipliers for ((M−I)L a)_1,3, in `pure_complement_short_certificate.json`. The dual identity for an arbitrary code implies

    y_low·a_low + y_c·((M−I)L a)_(1,3) >=1.

Let Q be the actual rank-one syndrome-complement projector, R=I−19ΣE_aPE_a†, and D=R−Q. Then ||D||_F²=2·19²ν. Put W=Σ_(r=1,3)(y_c)_r(Twirl_r−Π_r). Equivariance gives

    ||W||_(HS→HS)=w=max_k |Σ_(r=1,3)(y_c)_r(M_rk−δ_rk)|.

Because Q has rank one, Tr(QWQ)=0. Thus the second dual term is bounded above by19w(2||D||_F+||D||_F²). The first term is at most Aν, where A=19 max(0,max_r y_low,r/c_r). Exact rational values A,w appear in `robust_pure_gap_certificate.json`.

If ν<=10^-8, using sqrt(2)<3/2 bounds the total right-hand side by an exactly computed rational number smaller than0.426. This contradicts the lower bound1. `robust_pure_gap.py` checks the rational arithmetic; the advisor independently audited both the exact arithmetic and the analytical perturbation argument.

### Optimized robustness certificate
A subsequent exact optimization of the same dual perturbation argument strengthens the lower bound to

    ν > 1/102400 ≈9.765625×10^-6.

The new certificate (`optimized_robust_gap_certificate.json`) uses all complement rows and jointly optimizes the pure-separation multipliers and valid upper bounds A,w. At q=1/320, exact rational arithmetic verifies

    A q² +19 w (3·19q+2·19²q²) <0.975<1.

The inequalities N y_low,r<=c_r A and |Σ y_c,r(M_rk−δ_rk)|<=w are checked exactly by `optimize_robust_gap.py`, together with the Farkas identity and nonnegative multipliers. The analytical perturbation argument is unchanged. Worker and independent advisor exact replays passed (the latter uses standard-library Fractions and a hypergeometric transform). Even this stronger necessary condition leaves a substantial interval below the upper bound1/722.
