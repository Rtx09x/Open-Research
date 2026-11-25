# Independent certificate audit: exact statement and error budget

Status: **necessary-model audit and a route to rigor**, not an exclusion certificate.

## Arbitrary complex codes

Let `P` be an arbitrary Hermitian rank-two projector on the symmetric spin-j space, j=n/2. Distance at least five implies detection of all collective irreducible tensor operators of ranks 0 through 4. For each such tensor `T`, `PTP = Tr(PT) P/2`. Therefore, for arbitrary A,B,

`2 Tr[(P⊗P⊗P)(A⊗B⊗T) Swap13] = Tr(PA) Tr(PB) Tr(PT)`.

Since collective rotation preserves tensor rank, twirling gives

`Π_(third-factor ranks≤4) [(2Swap13−I) Z] = 0`, `Z=twirl(P⊗P⊗P)`.

No real-code, parity-code, or sparse-Dicke assumption occurs. In a real Clebsch–Gordan basis all scalar maps and permutation intertwiners are real. Conjugating a feasible Hermitian moment and averaging preserves every listed linear relation and PSD cone; this justifies using real symmetric moment variables as a relaxation.

The mixed complement constraints follow from the twirls of `P⊗P⊗Q`, `P⊗Q⊗Q`, `Q⊗Q⊗Q`, Q=I−P. Partial time reversal of one factor maps each positive product term to a positive product, so each listed PPT constraint is necessary. Their use does not require the (false in general) assertion that arbitrary positive tripartite operators have positive partial transpose.

## A bounded residual Farkas lemma

Let an exact necessary model be

`E x=b`, `C x≥0`, `F_i(x)=F_i0+Σ_j x_j F_ij ≽0`.

Choose exact nonnegative multipliers u and exact PSD matrices D_i, with arbitrary exact equality multiplier y. Define

`c=−yᵀb−Σ_i Tr(D_i F_i0)`,

`r=Eᵀy−Cᵀu−Σ_i F_i^*(D_i)`.

For any feasible x, `rᵀx≤−c`; equivalently `c≤−rᵀx`. Hence a contradiction follows if an explicit bound B on `|rᵀx|` satisfies `c>B>0`.

(The signs here match CVXPY constraints E x==b, C x≥0, F_i(x)≫0 and stationarity of the phase-I Lagrangian.) There is no need for exact zero stationarity. If additional exact-equality defects are bounded because the working rows approximate exact rows, add `Σ |y_k| ε_k` to B. If cone expressions approximate exact cones, add `Σ ||D_i||_* δ_i`, where δ_i bounds the operator-norm cone error. Exact rational Gram factors `D_i=L_i L_iᵀ` ensure dual positivity without eigenvalue heuristics.

## Uniform variable bounds

Intrinsic enumerators satisfy `a_r≥0`, `Σ a_r=(n+1)/2`; at n=18 this is 19/2. Consequently, for the enumerator residual,

`|r_aᵀ a| ≤ (19/2) ||r_a||∞`.

Write `Z=⊕_J I_(2J+1)⊗Z_J`, and define `S_J=(2J+1) Z_J`. Then `S_J≽0` and `Σ_J Tr S_J=Tr Z=8`. A coefficient residual expressed on these full blocks obeys

`|Σ_J Tr(R_J S_J)| ≤8 max_J ||R_J||op`.

This full-J bound is cleaner and tighter than bounding reduced scalar entries independently. If working in exact orthonormal symmetric/standard multiplicity coordinates, each reduced `X` is PSD; symmetric X trace plus twice standard X trace sums to 8, so every entry is bounded in absolute value by 8. Approximate floating U/V bases must not silently be treated as exact orthonormal bases.

## Independent way to certify low-rank KL rows

Fix pair spins L,L′. On the total-J invariant intertwiners, the third-factor commutator Casimir is a real symmetric matrix C after weighting by √(2J+1). Its exact spectrum is r(r+1), r=|L−L′|,...,min(L+L′,n). Let the exact weighted W vector contain the corresponding entries of `(2Swap13−I)Z`.

KL means W has spectral support only at ranks r≥5. Take *any rational vector* v approximating a low-rank eigenvector, and its intended exact eigenvalue λ=r(r+1)≤20. If high ranks are present,

`|vᵀW| ≤ ||(C−λI)v||₂ ||W||₂ / (30−λ)`.

This follows directly by spectral decomposition: on the high-rank subspace C−λI has singular values at least 30−λ. If no high ranks occur then W=0 exactly. Thus one need not certify a numerical eigensolver or evaluate an ill-conditioned polynomial spectral projector. Interval-enclosing the exact square-root-rational entries of C suffices to bound the eigenresidual.

The universally safe moment bound is `||W||₂≤24`: `||2Swap13−I||op=3`, `||Z||HS≤Tr Z=8`, and each L,L′ weighted vector norm is at most the full Hilbert–Schmidt norm. For an actual code the sharper bound `||W||HS≤√24` follows by twirl contraction and `Tr[((2Swap13−I)P⊗3)^2]=5·8−4·4=24`; the looser bound already leaves ample numerical margin.

The compressed KL matrix was computed by SVD `Eraw=UΣVᵀ`, `Ekl=V_rᵀ`. To lift a compressed dual y, choose a rational vector α approximating `U_r Σ_r^{-1} y`. Treat `yᵀEkl−αᵀEraw` as an ordinary coefficient residual. The exact eigenresidual bound above controls each raw row weighted by α. No claim that floating SVD rows belong *exactly* to the true row-space is needed.

## Remaining rigor conditions

A final certificate must record exact rational dual factors/multipliers; precise coefficient and basis definitions; interval-enclosed objective and residual terms; a strict positive final gap; and reproducible verification. Testing another solver or known19 is valuable bug detection but cannot replace these conditions.
