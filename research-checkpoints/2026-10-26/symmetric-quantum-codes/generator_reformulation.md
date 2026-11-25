# A compressed-generator reformulation of the unrestricted18-qubit problem

**Status:** exact equivalence independently mathematically audited by the advisor. This is a reformulation, not an infeasibility proof. It does not assume a real code, time-reversal symmetry, or pure low moments.

## Fixed algebra and unknown moments
Work in the spin9 representation and choose a degree-ordered Hilbert–Schmidt orthonormal Hermitian tensor basis E0,...,E8 for ranks0,1,2, with E0=I/sqrt(19). Degree means intrinsic tensor rank / filtered spin-polynomial degree. All multiplication coefficients of products through degree5 are fixed algebraic numbers in this representation.

Choose a Hermitian matrix-valued linear functional ℓ on tensor ranks0,...,5:
- ℓ(I)=I2.
- For ranks1,...,4, ℓ(T)=x_T I2 with real x_T:24 real unknowns.
- For the11 rank-five Hermitian tensors, ℓ(T) is an arbitrary Hermitian2×2 matrix:44 real unknowns.

Extend ℓ complex-linearly and *-preservingly from this Hermitian tensor basis. Thus there are68 real moment parameters. Define the9×9 scalar G by

    ℓ(Ea† Eb)=G_ab I2,

and the18×18 Hermitian matrices

    (K_i)_(aα,bβ) = [ℓ(Ea† J_i Eb)]_(αβ), i=x,y,z.

These products have degrees at most4 and5, respectively. Require G positive definite. Factor G=L L† by Cholesky, with positive real diagonal, and let

    A_i=(L^−1⊗I2) K_i (L^−†⊗I2).

The Gram-nondegeneracy theorem proves that every genuine18-qubit code is covered by this positive-definite chart.

## Only boundary completion variables remain
Introduce v_x,v_y,v_z in C^18, each supported on the last10 coordinates (the rank-two syndrome shell after degree-ordered Gram–Schmidt). This adds60 real unknowns. Set γ_i=−Tr(A_i), and define19×19 Hermitian matrices

    Jhat_i = [ A_i   v_i ]
             [ v_i† γ_i ].

Impose

    [Jhat_x,Jhat_y]=i Jhat_z,
    [Jhat_y,Jhat_z]=i Jhat_x,
    [Jhat_z,Jhat_x]=i Jhat_y,
    Jhat_x²+Jhat_y²+Jhat_z²=90 I19.

The claim is: **this128-real-variable system is feasible if and only if an unrestricted18-qubit symmetric distance-five code exists.**

## Necessity
A genuine code gives ℓ(F)=C† F C. Exact KL makes ℓ scalar through degree4. The validated Gram theorem gives G>0. The18 error vectors Ea|logicalα> span the syndrome space W. Degree-ordered orthonormalization identifies W with C^18, and the physical J_i compress to A_i by the displayed formula. Since J_i maps degree<=1 error images into degree<=2 images, its coupling to the one-dimensional residual complement vanishes on the first8 coordinates, so v_i has the required boundary support. Tr(J_i)=0 fixes γ_i. The physical commutator and Casimir relations give all remaining equations.

## Sufficiency: reconstruct the code rather than assume moment representability
Suppose the system is solved. The Hermitian Jhat_i are a finite-dimensional unitary su(2) representation. Its Casimir is90I. The only nonnegative spin j with j(j+1)=90 is j=9; because the total dimension is19, the representation is exactly one spin9 irrep. It is therefore unitarily equivalent to the symmetric18-qubit representation.

Let C consist of the first two coordinate vectors in C^19. Let F be the19×18 matrix whose first18 rows are L†⊗I2 and whose final row is zero. Its columns F_a, each a19×2 matrix, satisfy

    F†F=G⊗I2,
    F_0=C/sqrt(19).

(The second identity uses E0 first and lower-triangular Cholesky.) For every basis error Ea of degree at most1, write the fixed algebra identity

    J_i Ea = Σ_(b=0)^8 c_(i,a,b) Eb.

By definition of K_i and ℓ, its a-th block column is G times this coefficient vector, tensor I2. Therefore

    A_i (L† e_a⊗I2) = Σ_b c_(i,a,b)(L†e_b⊗I2).

The residual component also vanishes: L†e_a is supported in the first4 syndrome coordinates for a<=3, whereas v_i is supported in the last10 physical coordinates. Hence

    Jhat_i F_a = Σ_b c_(i,a,b)F_b     for degree(Ea)<=1.

Starting from F0=C/sqrt(19), these identities first recover the rank-one tensor images, then the rank-two images. All rank-two tensors lie in the span of products J_i J_j and lower-degree terms. Consequently

    F_a=Ea(Jhat) C    for every a=0,...,8.

Thus the actual reconstructed code obeys

    C† Ea(Jhat)† Eb(Jhat) C=G_ab I2.

Products of degree<=2 tensors span all tensor ranks<=4 in spin9. Therefore every rank<=4 operator compresses to a scalar on C, exactly the distance-five condition. Transporting C through the unitary equivalence gives a permutation-invariant18-qubit code. This proves sufficiency without assuming in advance that the chosen moments come from a physical rank-two projector.

## Boundary invariants that avoid explicit v variables
Writing

    R=90I18−Σ_i A_i²,
    D_ij=i ε_ijk A_k−[A_i,A_j],

the equations imply

    R=Σ_i v_i v_i† >=0, rank(R)<=3,
    D_ij=v_i v_j†−v_j v_i†,
    rank(D_ij)<=2,
    R±iD_ij >=0, rank(R±iD_ij)<=2.

All defect ranges lie in the common span of the three v_i and within the10-dimensional boundary shell. If rank(R)=3, whitening on its range turns the three iD_ij into a unitary conjugate of the standard spin-one antisymmetric generators, with spectra{-1,0,1}. These are necessary constraints on the68 moment parameters alone; their sufficiency without the remaining block commutator equations is not asserted.

## Numerical validation status
`generator_defect_diagnostics.py` constructs A_i from moments of the known19-qubit code. Its codimension-two analogue has R positive semidefinite of rank6 and R±iD_ij positive semidefinite of rank4, as predicted. This checks normalization and signs numerically, not the new sufficiency proof. The18-qubit relaxed local optimum fails Casimir positivity, so it is explicitly rejected rather than promoted to a code.
