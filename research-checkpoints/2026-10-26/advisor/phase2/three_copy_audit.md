# Quantum three-copy extension audit

This is a necessary SDP relaxation, not a feasibility equivalence or no-go result.

For a rank2 projectorP, let Y=twirl(P⊗P),Z=twirl(P⊗P⊗P), with collective SU2 twirl. Then Z≽0, Z commutes withS3, and

    Tr3 Z=2Y,    Tr3(Z Swap23)=Y.

These follow before twirling fromTrP=2 andP²=P, and commute with the collective twirl. In a total-spinJ multiplicity decomposition Z=⊕J I_(2J+1)⊗Z_J, pair-spinL diagonal marginal equations use factors2J+1. If t_L=Tr(Y Π_L), thenY's pair block is t_L/(2L+1).

The proposed pair map t_L=(4/(n+1))Σ_r(−1)^r M[L,r]a_r passes independent exact controls for n2,3,6,18,19. I computed enumerators for the highest-two-Dicke projector using discrete orthogonal polynomials and the MacWilliams matrix via terminating rational hypergeometric sums. Direct highest-weight coupling gives t_n=2+n/(2n−1),t_(n−1)=1,t_(n−2)=(n−1)/(2n−1), all other entries0. Every value agrees. See `check_three_copy_pair_map.py` and `three_copy_pair_map_checks.json`.

## Redundancy
The zero fully antisymmetric block follows already from positivity, S3 invariance, the two marginals andTr(YSwap12)=2. These giveTrZ=8, transposition traces4 and3-cycle traces2, henceTr(Z A3)=(8−12+4)/6=0. Positivity forces ZA3=0. It is useful for block reduction but not an additional independent constraint.

## Concrete affine strengthening
LetQ=I−P andY12=Y⊗I, withY13,Y23 its permutations. Positivity of mixed projector/complement tensor products gives

    Y12−Z >=0,
    (2/(n+1))I−Y12−Y13+Z >=0,
    (1−6/(n+1))I+Y12+Y13+Y23−Z >=0.

These use no new variables. In eachJ block, Y12 is diagonal t_L/(2L+1), and the other pair terms are recoupling conjugates. They may be stronger than plain positive extendibility and are cheap relative to the same multiplicity representation. Preserve the known19 control with denominator20 rather than19.

The general use of projector moments and complement averaging is established background in [Anglès Munné, Nemec and Huber, SDP bounds on quantum codes](https://arxiv.org/html/2408.10323v2). This particular SU2-reduced experiment's novelty and strength remain unproved.
# Lifted KL constraints and direct local-channel audit (21:30 UTC)

For every rank≤4 single-spin tensor T and arbitrary A,B, KL gives
Tr[P^⊗3(A⊗B⊗T)Swap13]=Tr(PAPT)Tr(PB)
=Tr(PT)Tr(PA)Tr(PB)/2. Thus projecting
W=(2Swap13−I)Z onto third-factor operator ranks0..4 gives zero after twirling.
W is Hermitian because Z commutes with Swap13; it need not be positive.
Rank0 is already the swap partial-trace condition, but ranks1..4 can add
nontrivial linear constraints. This is a necessary condition for arbitrary
complex rank-two codes, with no parity restriction.

`check_local_casimir.py` independently builds direct CG intertwiners and
raising/lowering matrices on the last physical spin. All24 exact coefficients,
full reconstructed channels, and the r(r+1) Casimir spectra pass. The coefficient
is 3(2J+1)(−1)^(L+L′){j K L;J j 1}{j K L′;J j 1}, with normalized rank-one
channel Σ T1q X T1q† and Casimir 2j(j+1)I−2(2j+1)j(j+1)channel/3.
No worker imports were used. These are model controls, not an n18 exclusion.

## Candidate separation and certificate boundary (21:45 UTC)
The worker's phase-I solve with all mixed PPT and lifted KL reports common
slack1.01616214339e−4. This remains a numerical candidate, not a theorem.
The newly assigned independent auditor checks complex random-projector controls,
all mixed cones on an actual known19 twirl, and rigorous residual budgets.

Reduced S3 eigenspaces and KL row compression are floating-point discovery
devices. A certificate for their rounded SDP alone is insufficient. Lift the
dual to full pair-spin J blocks, average the coefficient over exact S3 action,
and bound remaining residuals using TrZ=8 and a≥0,Σa=19/2. PSD dual factors can
be supplied as rational LLᵀ. Exact six-j values are rational multiples of square
roots, suitable for rigorous interval evaluation.

The closed local-Casimir change of basis is
U_Jr=(−1)^(L+j+J)√((2J+1)(2r+1)){L j J;j L′ r}.
It is the recoupling from total-J intertwiners to third-factor rank-r tensors;
the latter have commutator Casimir r(r+1). Six-j orthogonality makes U orthogonal.
Our direct-CG checker verifies this identity exactly on all five small-spin
controls, including its phase and weighted normalization D_JJ=√(2J+1).
The [DLMF definition](https://dlmf.nist.gov/34.4) and
[orthogonality relations](https://dlmf.nist.gov/34.5#iv) supply the standard
recoupling identities, not a new theorem. Projecting through these exact columns
avoids treating floating eigenvectors/SVD as exact model data.

Analytic review of the five mixed τ3 LMIs found the PPQ,PQP,PQQ,QQP,QQQ
expansions and pair crossing normalization correct; the omitted variants are
swap12 conjugates. Real symmetric moment variables are a relaxation valid for
arbitrary complex codes by conjugate averaging of this real linear model.

