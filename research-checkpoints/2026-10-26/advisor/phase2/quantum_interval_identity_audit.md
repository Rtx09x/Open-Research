# Eighteen-qubit exclusion certificate: independent identity audit

**21:47 UTC: mathematical identity audit PASS.** Numerical discovery and the
worker's rigorous Arb replay are separate from this review. The independent auditor has now replayed the same certificate without worker
imports and passed arbitrary complex controls; see the21:53UTC update below.

Audited verifier:
`symmetric-quantum-codes/phase2/check_interval_dual.py`.
Candidate SHA256:
201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79.

## Physical variables and necessary identities
For any hypothetical rank-two distance-five code in spin9, set
Y=twirl(P⊗P), Z=twirl(P⊗P⊗P). In total-spin J blocks use the **weighted**
variables X_J=(2J+1)Z_J. They are PSD and Σ_J TrX_J=TrZ=8. The normalized
intrinsic enumerators satisfy a≥0, a0=1, Σa=19/2 and (2M−I)a≥0, with rows1..4
zero. The pair-spin masses are t=(4/19)M diag((-1)^r)a.

The code projector's cube commutes with S3 and annihilates the three-copy
antisymmetric sector because rankP=2. Its symmetric marginal is (4/3)Y_sym;
the standard-sector marginal is (2/3)Y_sym+2Y_antisym. This follows by expanding
the six permutation terms in the symmetric projector and taking the third
partial trace. It explains the verifier's marginal equality factors without
assuming any chosen numerical S3 basis.

All twirls of tensor products of P and Q=I−P are PSD. Their partial time
reversals on one factor are also PSD, since each unaveraged term is still a
tensor product of positive matrices. The five inequivalent mixed τ3 conditions
are PPQ,PQP,PQQ,QQP,QQQ; swap12 gives the omitted variants.

For every third-factor tensor T of rank≤4, PTP=Tr(PT)P/2. Therefore
Π_≤4^(3)[(2Swap13−I)Z]=0. The verifier imposes an exact linear combination of
these identities using the closed Racah low-rank projector, not the floating
eigenvectors or SVD used during discovery.

## Functional/scaling checks
- Equality multipliers contribute y·b−y·E x, so the constant starts with
  y0+(19/2)y1; the residual enumerator signs and marginal signs agree.
- Ordinary mixed cones contain unweighted Z_J=X_J/(2J+1), explaining those
  denominators in their adjoints.
- The partial-time-reversal map on weighted X has coefficient
  {L 9 J;L′ 9 K} at n=18. Thus its dual adjoint has a bare six-j, not an extra
  source or target spin multiplicity. Pair-time-reversal eigenvalues use the
  separate crossing matrix {9 9 L;9 9 r}.
- The orthonormal intertwiner coordinate of the KL expression is
  [(2F13−I)X_J]/sqrt(2J+1), explaining the verifier's square-root denominator.
  Symmetrizing its real coefficient tests its real part, a valid zero identity
  even for complex Hermitian X_J.
- Every PSD multiplier is a rational Gram matrix LLᵀ. A supplied rational
  compression basis U need not be an exact eigenbasis: UᵀX_JU is PSD for every
  U. This removes numerical-basis dependence from ordinary cone tests.
- Averaging the residual coefficient over the six exact S3 matrices does not
  change its trace pairing with X_J. Projecting away the antisymmetric sector
  likewise leaves that pairing unchanged for genuine rank-two P.

The final verifier computes all six-j symbols by the factorial Racah expression
with exact rationals and outward-rounded square roots. No optimizer, floating
eigensolver, S3 basis, or KL SVD is trusted in the certificate identity.

## Compact rigorous residual bound
The certified entry bound is ε=1/100000000. Every spin block has dimension≤19,
so its Hermitian residual coefficient has operator norm≤19ε. Consequently

    |Σ_J Tr(R_J X_J)| ≤ 19ε Σ_J TrX_J = 152ε.
    |r·a| ≤ ε Σ_r a_r = (19/2)ε.

This is valid for arbitrary complex PSD X, not only real code states. Total
residual magnitude is at most323/200000000. The exact constant is

    −1930688571530266893851/19000000000000000000000000 < −1/10000.

Thus the positive-cone combination would be at most

    −1/10000 + 323/200000000 = −19677/200000000 < 0,

contradicting nonnegativity. Conditional on the independently checked model
and the interval replay, this excludes all complex rank-two symmetric
eighteen-qubit distance-five codes. The earlier exact n9–17 certificates,
Singleton bound below9, and independently audited length19 construction are
separate ingredients for the minimum-length conclusion.

This audit does not certify publication priority or substitute for external
expert/formal review. It identifies no remaining mathematical/scaling flaw.

## Independent replay closure (21:53 UTC)
Inspected `quantum-independent-audit/verify_full_certificate_independent.json`: PASS, same candidate hash, same exact constant, independently reconstructed full-space cone adjoints, and a separately bounded low-rank Casimir defect<10^-40. The resulting strict negative upper is still approximately−9.8385e−5. No internally checkable mathematical blocker remains identified after this replay and the hostile applicability audit. External review and priority remain separate.
