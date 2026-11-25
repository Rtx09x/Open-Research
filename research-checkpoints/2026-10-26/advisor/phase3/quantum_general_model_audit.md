# General-spin three-copy model audit

Status23:07UTC: analytic applicability and independent n33 arithmetic replay PASS. All516 KL eigenvectors passed an independently evaluated Casimir residual check; the strict total upper remains negative. Thus n33,t3 is excluded within the stated unrestricted fully symmetric rank-two model. Together with shorter-length certificates and exact37 existence,34≤nmin(3)≤37. The separate n34 replay is pending; no stronger lower bound is promoted yet.

## Scope and normalization

The model applies to every complex rank-two projector P supported in spin j=n/2, not only real, parity/reversal, pure or nondegenerate codes. Z=twirl(P⊗3) is PSD, S3-invariant and vanishes on the totally antisymmetric sector because Λ³(rangeP)=0. The unknown full-J matrices in the general checker are dimension-weighted blocks Zhat_J=(2J+1)Z_J; thus Σ_J Tr Zhat_J=8. Enumerators satisfy a0=1, sum a=(n+1)/2, a≥0, (2M−I)a≥0, and detected ranks1..2t have zero gap. The shadow inequalities follow from overlap with the time-reversed projector, without a time-reversal symmetry assumption on P.

For n odd, all J are half-integers. Enumerating J2=n mod2,n mod2+2,...,3n includes every multiplicity sector. The swap12 matrix is diag((-1)^(n−L)); swap23 uses (-1)^n sqrt((2L+1)(2K+1)){j j L;j J K}. The same (-1)^n occurs in the partial-time-reversal crossing map. Omitting it at odd n would reverse a whole cone and invalidate the result. The supplied generic code retains it consistently. Pair parity blocks for PPT are L mod2; this is exactly swap12 invariance, not an unjustified full-S3 restriction after partial time reversal.

The pair marginal equations use the +1 swap12 parity L≡n mod2. Its symmetric/standard coefficients4/3 and2/3, and the negative parity standard coefficient2, follow from the two rank-two projector partial traces. They do not depend on integer versus half-integer spin. Dimension weighting removes the factor2J+1 from the dual crossing sum, while the Racah KL coefficient retains division by sqrt(2J+1).

## Lifted KL and complex scope

PTP=Tr(PT)P/2 for every tensor rank≤2t implies projection onto those local ranks of (2Swap13−I)Z is zero. The low-rank tensor space is a complex linear, adjoint-stable space. Real coefficient maps allow replacing complex Hermitian moment blocks by their real parts: PSD and all required equalities survive. This is a relaxation containing every complex code, not an assumption that code coefficients are real.

The independent replay uses exact SymPy6j values converted via rational sign/square into Arb, different from the worker's factorial Racah evaluator. It also verifies each KL row through its local-Casimir eigenresidual. The first excluded eigenvalue is(2t+1)(2t+2), so at t3 the gap above rank6 is14. No numerical eigenbasis or SVD rank is trusted.

If all residual entries are≤epsilon, the physical objective error is at most[(n+1)/2+8(n+1)]epsilon, since a≥0, sum a=(n+1)/2, each block dimension≤n+1, and sum Tr Zhat=8. A separately bounded tiny KL eigenresidual contribution is added. Ordinary dual factors are rational Gram matrices in full multiplicity coordinates; approximate discovery bases do not invalidate their PSD property.

## Traceless-logical face identity

For general rank K, D13=P⊗θP−|P〉〉θ〈〈P|/K is an orthogonal PSD projector of rankK²−1. After inserting P on copy2 and twirling, D=τ3Z−τ3(ZSwap13)/K is PSD with traceK(K²−1), while R=τ3(ZSwap13) is PSD with traceK². For K2 these traces are6 and4. Detection gives DΠ_(pair13 spin≤2t)=0, with no zero-scalar/anticoherence assumption.

The supplied realignment equation was checked index by index. After suppressing the fixed time-reversal unitary, 2D_(abc;ub'v)=2Z_(abv;ub'c)−Z_(abv;cb'u). Simultaneous swap13 invariance converts the first term to2Z_(vba;cb'u); relabeling v=x,u=y yields the local trace pairing of(2Swap13−I)Z. Thus the face equalities match the earlier lifted KL under realignment. D≥0 and R≥0 are genuine extra cones; they are NOT used in the current n33 certificate.

These identities are uniform in t. The finite numerical dual coefficients are not a symbolic all-t inequality, and no interpolation of their signs proves the conjectured3t²+3t+1 threshold.
