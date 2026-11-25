# Exact elimination of the final spinor gauge: audit

**Status:** the worker's quartic invariant passes an independent analytic derivation and20 exact Gaussian-integer controls. This removes a gauge-existence test from a feasibility reformulation; it is not an n18 exclusion.

Let S=XX†≥0 have rank≤2, with X a2d×2 matrix (padzero columns). Its rows are grouped into2×2 matrices M_a, a=1,…,d. Let Z be the real2d×4 matrix whose complex rows before realification are

    [TrM_a, iTr(M_aσ1), iTr(M_aσ2), iTr(M_aσ3)].

A nonzero real nullvector of Z normalizes to U=a0I+iΣa_iσ_i∈SU2 and gives Tr(M_aU)=0. This is exactly the required gauge, as established in `spinor_compression.md`.

Define B_i=σ_i⊗I_d and

    t=TrS,
    H_ij=2Tr(SB_iSB_j)−Tr(SB_i)Tr(SB_j),
    δ=2iTr(SB1SB2SB3−SB1SB3SB2).

Then

    det(ZᵀZ) = [t⁴−2t²TrH−8tδ+2Tr(H²)−(TrH)²]/16.

## Independent derivation, including the sign

Put Y_i=X†B_iX and write Y_i=(a_iI+c'_i·σ)/2. Pauli multiplication gives

    H_ij=c'_i·c'_j.

View the matrices M_a as amplitudes of a two-qubit positive matrix ρ=Σ_a |vecM_a><vecM_a|, with Trρ=t. Its correlation matrix is

    C_ij=Tr(ρ(σ_i⊗σ_j))=Tr(Y_iσ_jᵀ).

Consequently C=c' diag(1,−1,1), not c'. Hence H=CCᵀ and detC=−detc'. Also

    2iTr(Y1[Y2,Y3])=−detc'=detC,

so δ=detC. The transpose in the second Pauli factor is the essential sign check.

Proper localSU2 transformations diagonalize C by left/right SO3 rotations and act as real orthogonal changes of the quaternion coefficient basis for Z. Thus determinant(ZᵀZ) is unchanged. For diagonalC=diag(c1,c2,c3), the real quaternion Gram has eigenvalues

    (t+c1−c2+c3)/2,
    (t+c1+c2−c3)/2,
    (t−c1−c2−c3)/2,
    (t−c1+c2+c3)/2.

Local one-qubit Bloch terms contribute only to the imaginary antisymmetric part in this basis and hence not to ZᵀZ. Multiplying the four displayed factors gives the formula. Calibration X=I2 gives t2,H=4I,δ−8 and determinant0; the opposite cubic sign would fail.

Since ZᵀZ is automatically PSD, the quartic numerator vanishes if and only if Z has a nonzero real nullvector. Therefore, combined with the prior conditions, it is an exact gauge elimination rather than a mere necessary condition.

For the68-moment quantum model, the complete candidate criterion can use G>0, S=T(19I−T)≥0, rankS≤2, rankT18, and this quartic equality. Hermiticity of T makes S≥0 imply0≤T≤19I. The automatic degree≤1 boundary closure and projection-completion proof remain essential to sufficiency.

`check_quaternion_invariant.py` is an independently written stdlib-only checker using Gaussian integer pairs and Fraction elimination, not SymPy or worker imports. It passes20 cases at d=1,2,3,5,18 in under1second. See `quaternion_invariant_checks.json`. Finite tests are controls; the derivation above establishes the identity.

## Further audited scalar rank/branch elimination

Because S=T(19I−T)≥0 and T is Hermitian, 0≤T≤19I. The equality

    e3(S)=[(TrS)³−3TrS·Tr(S²)+2Tr(S³)]/6=0

is equivalent to rankS≤2: every term in the third elementary symmetric polynomial of nonnegative eigenvalues is nonnegative.

With TrT324, at most two eigenvalues may lie strictly between0 and19. If two do, either16 eigenvalues equal19 and their interior sum is20, or17 equal19 and their interior sum is1. With one interior eigenvalue it must be1, accompanied by17 eigenvalues19. Zero interior eigenvalues are impossible.

Write t=TrS,u=Tr(ST). In the physical two-interior branch, with productp, t=2p−20,u=22p−400, hence u=11t−180. In the spurious branch t=18+2p,u=18−35p=333−35t/2. Imposing u=11t−180 makes p0, collapsing this branch to the coherent boundary. Consequently rankT18 can be replaced exactly by

    Tr(T³)−30Tr(T²)+67536=0.

Thus the candidate exact68-moment criterion is G>0, one PSD constraint S≥0, and three scalar equalities: e3(S)=0, the displayed cubic trace equality, and the quartic gauge numerator=0. This is still a nonconvex feasibility problem, not an infeasibility result.

For a radical-free metric representation Tbar=M^−1 Ttilde, enforce PSD on the Hermitian matrix M Sbar=19Ttilde−Ttilde M^−1Ttilde, not on the generally non-Hermitian Sbar itself. Trace invariants agree by similarity. The inserted Pauli matrices commute with M=I_spin⊗(G⊗I_logical), so the quartic expressions transfer as well.
