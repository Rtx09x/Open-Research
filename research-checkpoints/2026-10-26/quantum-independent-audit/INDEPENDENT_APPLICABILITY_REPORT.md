# Independent adversarial audit: minimum length for two-error symmetric qubit codes

**Audit date:** 25 October 2026. **No external publication or priority claim.**

## Separated verdicts

1. **Certificate arithmetic: PASS.** A separately written checker reproduces a strict contradiction from the fixed integer witness, using exact rational Gram factors and rigorous Arb interval arithmetic. It imports no worker code. Its six-j values are obtained from SymPy exact rational signs and squares, independently of the primary checker's factorial Racah evaluator. A second independent check bounds any possible error in treating the KL vectors as exact low-rank vectors; this adds less than `10^-40` to the final bound.
2. **Applicability at n=18: PASS.** Every Hermitian rank-two projector onto a code in `Sym^18(C²)` correcting arbitrary errors on at most two physical qubits must satisfy the constraints used in the contradiction. No reality, time-reversal, parity, sparse-Dicke, Pollatsek–Ruskai, or nondegeneracy restriction is imposed. I find no omitted-sector, transpose, conjugation, or normalization restriction that narrows the stated class.
3. **Precise selected minimum-19 target: YES, with no length gap.** Lengths n≤8 are impossible by the erasure/no-cloning argument below; all exact certificates for n=9,...,17 replay successfully; the n=18 certificate above excludes the remaining length; the exact n=19 root and all fifty four-qubit KL reductions also replay successfully. Thus these proofs establish the stated two-error minimum `n_min^PI(2)=19`. They do **not** establish the general all-t formula, or a result about arbitrary code projectors merely invariant under permutations while supported outside the fully symmetric subspace. The proof is computer-assisted; journal review and literature novelty are separate questions.

The selected [open-problem record](https://qiqc-op.com/problem/op_a72722e455d85d55/) explicitly concerns pointwise symmetric codewords with arbitrary complex coefficients and both length parities. That is exactly the class audited here. Its website status is not evidence for or against the newly checked proof.

## Fixed witness and independent arithmetic

Witness:

`../symmetric-quantum-codes/phase2/interval_dual_candidate.json`

SHA256:

`201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79`

The exact constant is

`c = -1930688571530266893851 / 19000000000000000000000000 < -1/10000`.

The independent verifier proves that each intrinsic-enumerator residual and each full multiplicity-matrix residual entry has absolute value below `10^-8`. With `Σ a_r=19/2`, `a_r≥0`, and weighted positive moments `S_J=(2J+1)Z_J` satisfying `Σ Tr S_J=8`, this gives

`|residual| ≤ (19/2+8·19)10^-8 +10^-40 = 0.000001615 +10^-40`.

The `10^-40` term is an independently certified safety allowance for the KL linear combination. Consequently the nonnegative cone combination is strictly less than

`-0.000098385 +10^-40 <0`.

The dual matrices are rational `L Lᵀ`, so positive semidefiniteness is algebraic, not inferred from floating eigenvalues. Rational `basis_U` matrices only form arbitrary PSD compressions: they need not be exact eigenbases or orthonormal. The verifier works with full pair-spin multiplicity matrices, not the numerically reduced variable space. Exact S3 averaging and antisymmetric-support removal are applied only to the residual functional on the original Z.

Files:

- `verify_full_certificate_independent.py` and `.json`: independent full-cone assembly and strict interval bound.
- `check_kl_stability.py` and `.json`: all 252 KL vectors, exact Casimir residuals.
- `rigorous_residual_strategy.md`: bounded-residual Farkas proof and conventions.

## Why the constraints are necessary

### Physical errors and intrinsic tensors

Put `j=9`, `N=19`, and let P be any Hermitian rank-two projector in spin j. An arbitrary two-qubit error-correcting code detects every Pauli operator of weight at most four: products of two weight-at-most-two errors span those operators. Conversely, rank-r spherical tensor operators on spin j, for r≤4, lie in the restriction of the span of physical operators of weight at most r. For example `J_+^r` is a sum of products on r distinct qubits, and collective rotations span its entire irreducible rank-r operator space. Thus

`P T P = Tr(P T) P/2`

holds for every tensor of ranks zero through four, without assumptions on phases.

### Intrinsic normalization and pair moments

Take a Hilbert–Schmidt orthonormal spherical tensor basis and set `ρ=P/2`, `a_r=N||Π_r ρ||²_HS`. Then `a_r≥0`, `a_0=1`, and `Σa_r=N/2` follow immediately from normalization and `P²=P`. The intrinsic transform is

`M_rk=(-1)^(n+r+k)(2r+1){j j r; j j k}`.

With `b=2Ma`, Cauchy–Schwarz gives `b_r≥a_r`, and KL gives equality for r≤4. The pair twirl `Y=twirl(P⊗P)` has trace weights

`t_L=(4/N) Σ_r (-1)^r M_Lr a_r`,

and acts as `t_L/(2L+1)` in pair-spin L. This is the standard recoupling identity, with the factor four from `Tr P=2`. Direct controls cover integer and half-integer spins, including complex projectors; previous exact controls include n=18 and 19.

### Three-copy identities and all sectors

`Z=twirl(P⊗P⊗P)` is PSD, has trace eight, commutes with all copy permutations, and obeys

`Tr_3 Z=2Y`, `Tr_3(Z Swap23)=Y`.

These identities hold before twirling from `Tr P=2` and `P²=P`. The fully antisymmetric sector vanishes because `wedge³ range(P)=0`. No other sector is removed: all symmetric and standard multiplicities survive. Every total spin J=0,...,27 is included. Each multiplicity is at most nineteen.

In pair-spin L of symmetric copy12 parity, the symmetric and standard contributions to the marginal are `4t_L/3` and `2t_L/3`; in antisymmetric pair parity the standard contribution is `2t_L`. These follow by solving the two partial-trace identities, because Swap23 has diagonal action +1 on the symmetric sector and −1/2,+1/2 on the copy12 even/odd standard components.

### Complement and partial-time-reversal cones

Set `Q=I−P`. Twirling the positive product operators PPQ, PQQ, QQQ gives

`Y12−Z`,
`(2/N)I−Y12−Y13+Z`,
`(1−6/N)I+Y12+Y13+Y23−Z`.

The one-factor mean is `twirl(P)=2I/N`, explaining every constant. Partial time reversal is partial transpose followed by the fixed spin-j conjugating unitary. Applied to each positive product term, it remains positive. This—not positivity of partial transpose for arbitrary entangled PSD matrices—is the justification for the PPT cones.

Importantly, partial time reversal of Z is **not** assumed S3-invariant. Only surviving Swap12 parity is used in the numerical construction; the final certificate uses full output multiplicities. The antisymmetric sector is removed from the **input Z residual**, never incorrectly from the partially transposed output.

The crossing formula in the weighted source variables is

`(τ3 Z)_K[L,L′] = Σ_J (-1)^n {L j J; L′ j K} S_J[L,L′]`.

Thus no extra dimension factor belongs in its adjoint. By contrast the untwisted physical block is `Z_J=S_J/(2J+1)`. Both factors were checked separately in the independent assembly.

### Lifted KL and complex conjugation

For arbitrary operators A,B and detected T,

`Tr[P^⊗3 (A⊗B⊗T) Swap13] = Tr(P A P T) Tr(PB)`.

KL makes twice this equal to `Tr(PA)Tr(PB)Tr(PT)`. Twirling preserves the rank filtration, giving

`Π_(rank≤4 on factor3)[(2Swap13−I)Z]=0`.

In a real coupled basis, all permutation, recoupling and Casimir coefficients are real. Averaging a feasible Hermitian moment with its entrywise conjugate preserves every necessary equality and PSD cone. This is a valid moment relaxation, not an assumption that the code itself is real. The final full-space residual argument also pairs real symmetric coefficients with Hermitian moments correctly: imaginary skew parts contribute zero to the real trace functional.

For each fixed L,L′, the local operator Casimir has spectrum `r(r+1)`, with `r=|L−L′|,...,min(L+L′,n)`. KL removes r≤4. The independent check verifies every proposed low-rank vector u by bounding `(Cas−r(r+1)I)u`, rather than assuming an eigensolver or closed Racah formula is exact. The high-rank spectral gap is at least ten; `||(2Swap13−I)Z||_HS≤24`; each eigenresidual component is below `10^-50`; the summed defect is below `10^-40`. This also closes the floating-SVD row-selection loophole.

## Adversarial controls—not substitutes for proof

- Actual known19 direct moments pass all 290 ordinary/mixed/PPT tests; the worst eigenvalue is about `−6.76e−14`, consistent with numerical roundoff.
- Independent direct-CG full-Hilbert controls for random complex rank-two projectors at n=2,3,4,5,6 strongly violate time reversal (norm differences 1.30–1.96). At n≥4, the moments have genuinely imaginary off-diagonals. Complex crossing, real S3 reconstruction, reduced PPT and all complement identities agree within `6e−16`.
- In those same controls, partially time-reversed moments **fail** to commute with Swap23 (commutator norms 0.33–0.87), while the implemented maps reconstruct them correctly. This directly tests the most dangerous accidental-S3 restriction.
- A generic complex n=18 rank-two projector also passes direct J²-coupling controls: time-reversal violation 1.709, genuinely imaginary weighted moments up to 0.00629, real S3 reconstruction error below 2e−16, pair-map/marginal residuals below 8e−12, independent tensor MacWilliams residual about 1.06e−10, and strictly positive PPT minimum 7.90e−5. KL was correctly not imposed on this arbitrary noncode. See `generic_n18_control.py` and `.json`.
- SCS independently reproduces Clarabel's positive phase-I value, but neither solver status is used by the proof.

## No gap at shorter lengths or at existence

### n≤8

Split the n qubits into disjoint sets A and B each of size at most four. A distance-five code corrects erasure of either set. Encode half of a maximally entangled logical-reference pair, obtaining a pure state RAB. Erasure correction implies `I(R:A)=I(R:B)=0`. Purity then gives

`S(B)=S(R)+S(A)` and `S(A)=S(R)+S(B)`.

Hence `S(R)=0`, contradicting one encoded qubit. This is the relevant quantum Singleton/no-cloning argument and includes all n≤8.

### n=9,...,17

All nine stored exact rational Farkas witnesses were replayed. Each has nonnegative inequality multipliers, exact equality of coefficient vectors, and exact constant `−1`. Both even and odd lengths are present. See `replay_shorter_lengths.py` and `shorter_lengths_exact_replay.json`. The replay is a local copy of the parent's independent stdlib-Fraction checker, preserving its provenance.

### n=19

The known construction was independently replayed using the advisor's stdlib-Fraction polynomial/Jacobian/Hessian checker, copied locally without altering source artifacts. The rational root box has radius `10^-40`; its exact contraction tests pass (`eta≈2.66e−66`, `L·radius≈1.95e−36`). All fifty four-qubit reduced-Gram polynomials exactly lie in the defining nine-equation span. The codewords have disjoint parity support, equal nonzero norms by reversal, and `q0=1`; normalization therefore yields an exact two-dimensional code. Symmetry transfers the four-qubit KL conditions to every set of at most four physical qubits. See `replay_known19_exact.py` and `known19_exact_replay.json`.

## Trust and scope

The remaining ordinary mathematical inputs are finite-dimensional quantum error correction/erasure identities, SU(2) Clebsch–Gordan recoupling and local-Casimir representation theory, and correctness of the stated exact/interval arithmetic libraries. Numerical positive controls and a second solver are bug detectors only. No numerical search failure, approximate primal infeasibility, claimed exact floating eigenspace, or real-code ansatz is part of the proof. This audit does not certify historical priority or solve the all-error-number conjecture.
