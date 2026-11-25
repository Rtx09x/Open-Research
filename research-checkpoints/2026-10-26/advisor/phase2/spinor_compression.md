# Phase2: exact spinor compression and completion audit

**Status:** analytic identities and the worker's V-free equivalence pass independent algebra audit. No n18 code or nonexistence proof follows. Initial-phase artifacts are frozen. Numerical controls below are explicitly not proof certificates. Schwinger factorization, interlacing and projection dilation are standard tools; novelty of this application is unestablished.

## 1. Conventions and a direct factorization

Let n=2j, V_n=Sym^n(C²), with orthonormal basis |w>, w=0,…,n and Jz|w>=(w−j)|w>. Define rectangular annihilation maps a,b:V_n→V_(n−1):

- a|w>=sqrt(w)|w−1>;
- b|w>=sqrt(n−w)|w>.

Then a†a=jI+Jz, b†b=jI−Jz, b†a=J_−, a†b=J_+, and aa†+bb†=(n+1)I_n.

For any isometry W:C^m→V_n let A_i=W†J_iW, A_±=Ax±iAy. The Hermitian spinor block

    T = [[jI−Az, A_−], [A_+, jI+Az]]
      = [bW,aW]†[bW,aW]

is positive semidefinite of rank at most n. This proof makes no reality, parity, code or genericity assumption.

For n18,m18, rankT=18: if Q=qq†=I−WW†, then

    [bW,aW][bW,aW]† = 19I18−[bq,aq][bq,aq]†.

The2×2 Gram of [bq,aq] has eigenvalues9±g, where γ_i=<q|J_i|q> and g=|γ|≤9. Thus the complete spectrum of T is

    0 ×18, 19 ×16, 10−g, 10+g.

The formula includes g=9: one exceptional eigenvalue merges into19. In particular T≤19I and S=T(19I−T) is PSD rank≤2. For a generic axis H=9I−Az is invertible (equivalently q overlaps the highest-weight coherent state); the Schur complement gives the full matrix equality

    9I+Az = A_+ H^−1 A_−.

Do not impose H invertible at a preselected axis without handling the exceptional chart. The block formulation has no such gap.

For n19,m18 the factor is19×36, so T may have rank19; if H is invertible its Schur complement is PSD rank≤1, not necessarily zero. This is the required positive-control distinction.

## 2. Complement Gram and directional constraints

In a genuine codim1 completion write

    J_i=[[A_i,v_i],[v_i†,γ_i]],   γ_i=−TrA_i.

Since Tr(J_iJ_j)=570δ_ij and the bottom commutator is v_i†v_j−v_j†v_i=iε_ijkγ_k, the3×3 Gram K_ij=v_i†v_j is forced by A:

    K_ij=(570δ_ij−Tr(A_iA_j)−γ_iγ_j)/2 + (i/2)ε_ijkγ_k.

Consequently K≥0 and its nonzero spectrum equals R=90I−ΣA_i². Necessary eliminated identities are Tr(R^p)=Tr(K^p), p=1,2,3, with rankR≤3. The first gives TrR+|γ|²=90. These are useful before full defect compatibility is enforced, not claimed independent of the full completion system.

Every directional compression A(u), |u|=1, interlaces −9,…,9. More explicitly, with p_J(t)=∏_(m=−9)^9(t−m),

    det(tI18−A(u))=Σ_m p_m(u) p_J(t)/(t−m),
    p_m(u)=det(mI−A(u))/p_J'(m)≥0,  Σ_m p_m(u)=1.

The p_m are the complement state's spin-measurement probabilities. This supplies determinant-sign tests without v variables. A stronger coherent-state identity is obtained from

    B(z,zbar)=(9I−Az)−zA_−−zbar A_+ +z zbar(9I+Az).

Since B=(bW−z aW)†(bW−z aW) is a square-factor Gram, detB=|det(bW−z aW)|². Its19×19 bivariate coefficient matrix is PSD rank1. This determinant condition is superseded computationally by the simpler full spinor block rank condition, not an independent theorem.

Directional cubic trace identities also hold:

    Tr A(u)^3 +3v(u)†A(u)v(u)+3γ(u)||v(u)||²+γ(u)^3=0.

Once a spinor projection completion exists they are automatic; no additional nonredundant cubic obstruction has been established.

## 3. Relation to the old R,D constraints: do not overcount progress

Set D_ij=iε_ijk A_k−[A_i,A_j]. Direct multiplication gives

    S=19T−T²
     =[[R+iDxy, −Dzx+iDzy], [adjoint, R−iDxy]].

If R=Σv_iv_i† and D_ij=v_iv_j†−v_jv_i† are already enforced, then S=UU† with

    U=[(-vz,v_+)^T, (v_−,vz)^T].

Thus joint rank2 packages compatibility more tightly than separate block ranks, but is not extra once a common V exists. Tracing the upper commutator implies the bottom one, so U†U has eigenvalues TrR±g.

With the additional scalar bottom Casimir TrR+g²=90, these facts force the physical spectrum of T. Indeed S≥0 implies0≤T≤19, with at most2 eigenvalues outside{0,19}; TrT=324 leaves only the physical branch or a putative branch with17 eigenvalues19 and two summing1. In the latter, comparing the difference and sum of the S eigenvalues yields λ±=(1±g/9)/2 and TrR=37/4−g²/324. The bottom trace then gives g²=81, so one λ vanishes and the branch merges into the coherent boundary. This removes the apparent independent rank obstruction.

## 4. Audit of the worker's exact68-moment completion criterion

Construct A_i from the68 moments and positive G exactly as in the initial generator reformulation. The following conditions are necessary and sufficient for a code:

1. 0≤T≤19I, rankT=18, rankS≤2, where S=T(19I−T).
2. Factor S=XX†, X of size36×2, padding a zero column if rankS=1. Partition its rows for physical coordinate a into a2×2 matrix M_a (spinor row, completion-column index).
3. The real36×4 matrix with complex coefficient rows

       [TrM_a, iTr(M_aσx), iTr(M_aσy), iTr(M_aσz)]

   (real and imaginary parts as separate rows) has a nonzero real nullvector.

**Gauge step.** A normalized real nullvector(a0,ax,ay,az) gives U=a0I+iΣa_iσ_i∈SU2, and Tr(M_aU)=0 for every a. Conversely every U2 matrix is a phase times such an SU2 matrix; the irrelevant phase does not change the zero condition. Thus this real linear test exactly captures the unitary factor gauge, not merely a relaxation.

**Projection completion.** Replace X by XU. If rankS=2, set Y=19I−X^+TX. Functional calculus for S (which commutes with T) verifies TX+XY=19X and X†X+Y²=19Y. The two nontrivial eigenvalues of T sum20 because rankT18 and TrT324; therefore TrY=18. If rankS=1, the sole nontrivial eigenvalue of T is1. Set Y=18 on ranX† and0 on kerX; the same identities and trace hold. RankS0 is impossible because324 is not divisible by19.

The block matrix [[T,X],[X†,Y]] therefore squares to19 times itself. The zero partial-spin trace of X, the built-in partial-spin trace18I18 of T, and TrY18 imply that its full partial-spin trace is18I19. Regroup by spinor coordinates. It has the form [[9I−Jz,J_−],[J_+,9I+Jz]] with Hermitian J_i. Expanding the projection identity gives Casimir90I and all su2 commutators. Dimension19 then forces one spin9 irrep.

**Boundary support / code reconstruction.** This is the essential sufficiency check. For each formal error column F_a of degree≤1, multiplication identities give A_iF_a equal to the degree≤2 product column. A second multiplication uses only moments through degree5, so the Casimir and commutator identities imply RF_a=D_ijF_a=0. Hence S vanishes on both spinor copies of the first8 degree-ordered physical coordinates, and every factor X has zero rows there. The reconstructed v_i therefore satisfy the required rank-two-shell support. The previously audited generator reconstruction then recovers all degree≤2 error images with scalar GramG⊗I2, proving KL through degree4. No assumed physical representability of the moments is smuggled into sufficiency.

## 5. Controls and remaining test

`check_spinor_compression.py` independently builds annihilation matrices and degree≤2 syndrome spaces, without worker imports. Exact rational coherent controls pass for n1…24. A generic complex codim1 n18 compression matches factorization, spectrum, K and Schur identities numerically. The previously exact-certified known19 code has T rank19 and a nonzero rank-one Schur defect≈.713454, as required. See `spinor_controls.json`.

The worker owns reduced rectangular-tensor Gram construction and gauge/adversarial controls. Useful next test: determine whether the24×24 effective Gram (after12 automatic nulls) has a rank/parity obstruction compatible with the68-moment constraints. Kill any claimed no-go if a relaxation witness survives or the argument imposes reality/parity. No unrestricted exclusion has been established.
