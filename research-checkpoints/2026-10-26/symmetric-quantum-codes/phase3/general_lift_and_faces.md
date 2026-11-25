# Uniform-in-t three-copy identities and a traceless-logical PSD face

These are necessary conditions for arbitrary complex rank-two codes, not an all-t length obstruction. The generic projector/PPT hierarchy has prior antecedents (Yu et al2021/2022; Anglès Munné–Nemec–Huber). Novelty of this particular rearrangement is unconfirmed.

Let V be spin j=n/2, N=n+1, P a rank-K projector, and θ(A)=C A^T C† the spin time-reversal operation. Use row vectorization |X〉〉=Σ_ab X_ab|a〉|b〉 and |X〉〉θ=(I⊗C)|X〉〉. Then

    (P⊗θP)|X〉〉θ = |PXP〉〉θ.

The vector |P〉〉θ belongs to the rank-K² projector P⊗θP and has squared norm K. Consequently

    D13(P)=P⊗θP - |P〉〉θ〈〈P|/K

is a PSD orthogonal projector of rank K²−1. For K=2 it projects onto the three-dimensional traceless logical-operator space, represented physically in two copies.

Insert P on copy2 and twirl over collective SU(2). With Z=twirl(P⊗3), S13 the copy swap, and τ3 partial time reversal,

    A = τ3 Z,
    R = τ3(Z S13),
    D = A - R/K >= 0,     R >= 0,
    TrD = K(K²−1),        TrR = K².

The identity for R follows by direct matrix entries: the partial transpose of (P⊗P)Swap is |P〉〉〈〈P|. A further fixed local unitary implements θ. For K=2, TrD=6 and TrR=4. These two cones strengthen ordinary PPT, which retains only A>=0.

## Exact known face from detection

If P detects operator T, then PTP=(TrPT/K)P. Therefore

    D13(P)|T〉〉θ = 0.

Under the operator-to-two-spin intertwiner X↦|X〉〉θ, tensor-rank-r operators correspond to pair total spin r. Thus a distance≥2t+1 code satisfies

    D Π_(pair13 spin<=2t) = Π_(pair13 spin<=2t) D = 0.

This face is known from n,t, without knowledge of the code. It does not assume anticoherence or a zero scalar compression.

The same conclusion follows from the scalar enumerators plus D>=0. Normalize a_r=N||Π_r(P)||²/K², b=KMa. The pair13 marginal Tr2D has rank-r trace weight

    (K²/N)(b_r-a_r),

and therefore eigenvalue (K²/N)(b_r-a_r)/(2r+1). For K=2 this is (4/N)(Ha)_r/(2r+1), H=2M-I. Detection makes these weights zero for r<=2t; positivity forces the whole corresponding block row and column to vanish. The formula follows from Tr2Z=KY and the vectorized pair twirl, and is meaningful for the projector-moment relaxation as well as actual codes.

## Relationship to the earlier lifted KL equations

For K=2 the earlier equation was

    Π_(operator rank<=2t on factor3)[(2S13-I)Z]=0.

Here is the explicit realignment identity, suppressing the harmless C unitary. Assume [Z,S13]=0, as holds for every S3-invariant moment. Write A=Z^T3, R=(ZS13)^T3, D=A-R/2. For any matrix T,

    2 Σ_(u,v) D_(a,b,c;u,b',v) T_(u,v)
      = Σ_(x,y) [(2S13-I)Z]_(a,b,x;c,b',y) T_(y,x).

To verify it, expand partial transpose:

    2D_(a,b,c;u,b',v)
      = 2Z_(a,b,v;u,b',c) - Z_(a,b,v;c,b',u),

and use swap13 invariance on the first term to replace it by 2Z_(v,b,a;c,b',u). Relabel v=x,u=y. Since the detected tensor space is closed under adjoint, the trace pairing on the right is exactly its Hilbert–Schmidt zero-projection condition. Restoring C gives the θ-vectorized statement above.

Hence on the S3-invariant input space, the known-face linear equations for D are exactly the earlier lifted KL equations (up to realignment), not a separately guessed selection of moments. The **additional strengthening** is D>=0 and R>=0. Equivalently, one can impose the scalar detection constraints and D>=0, and let PSD zero-marginal faces force the lift. For numerical work it is preferable to enforce the face explicitly and compress D to its known complement, avoiding a poorly conditioned zero face.

## What this does and does not generalize

The whole construction is symbolic for every t,n,K. The detector cutoff changes from4 at t2 to2t. The local-Casimir eigenvalues r(r+1), Racah recoupling coefficients and S3 matrices give an exact finite SDP for each n,t. However, the numerical dual coefficients at n18 have no proved t-dependent formula; their signs or sparsity cannot be interpolated into a universal length theorem.

The phase2 witness simplifies further: all mixedP/Q cones can be dropped while preserving a rigorous contradiction, leaving only Z>=0, A=τ3Z>=0 and scalar/marginal/lifted-KL constraints. This justifies testing the same small cone family at t3 before adding D/R. It does not establish that this level always detects every nonexistent code, or that the conjectured threshold is correct.

## Algebraic inverse and a possible compressed formulation

On the full matrix space let T(A)=τ3((τ3 A)S13), where τ3²=identity in the fixed spin convention. Right multiplication by S13 is an involution, hence T²=identity. For the invariant Hermitian input space, D=(I−T/K)A. For K>1 this map is invertible:

    A = K²/(K²−1) · (D + T(D)/K),
    R = K²/(K²−1) · (T(D) + D/K).

For K2 the coefficients are4/3 and2/3. This is a linear change of variables, not a bound. It suggests parametrizing D directly on its known pair13-spin>2t face and recovering Z=τ3A, then imposing S3 symmetry, projector marginals, Z>=0 and R>=0. Hermiticity and S3 constraints must still be imposed; arbitrary PSD D is not automatically a valid projector moment. Such a parametrization could remove the nearly singular detected face before optimization. It has not yet been implemented or audited here.
