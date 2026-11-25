# Exact 68-moment spinor criterion for the unrestricted 18-qubit problem

**Status:** mathematical audit requested/completed in advisor notes; executable tests are separately identified as numerical or exact. This is an equivalent feasibility formulation, NOT an 18-qubit exclusion or a construction. Novelty is unconfirmed.

## Input: precisely the audited moment chart
Use `../generator_reformulation.md`: 24 scalar moments in tensor ranks 1–4 and 11 arbitrary Hermitian 2-by-2 moments in rank 5, totalling 68 real variables. The moment functional is complex-linear and star-preserving. Its scalar 9-by-9 degree-two error Gram G must be positive definite. The previous exact bound guarantees this for every genuine code. Form the three Hermitian 18-by-18 matrices A_x,A_y,A_z by the same Cholesky congruence as before.

Let d=18, p=19, A_±=A_x±iA_y, and

    T = [[9 I_d-A_z, A_-], [A_+, 9 I_d+A_z]],
    S = p T-T^2.

Both matrices are 36-by-36. In particular Tr T=324, independently of the moments.

## Equivalent feasibility conditions
There is an unrestricted symmetric 18-qubit distance-five rank-two code **if and only if** the 68 moments can be chosen so that:

1. G is positive definite.
2. S is positive semidefinite and rank S is at most 2.
3. rank T is exactly 18.
4. The orientation polynomial F(S) defined below is zero.

No real-code, parity, time-reversal, or pure-low-moment assumption is imposed. All ranks and equalities are exact. Rank-one S is explicitly included.

## The orientation polynomial: no auxiliary completion variables
Write B_i=σ_i⊗I_d for the standard three Pauli matrices, and define real quantities

    t = Tr S,
    H_ij = 2 Tr(S B_i S B_j)-Tr(S B_i) Tr(S B_j),
    delta = 2i Tr(S B_1 S B_2 S B_3-S B_1 S B_3 S B_2).

For Hermitian S, H is real symmetric and delta is real. Set

    F(S) = [t^4 - 2 t^2 Tr H - 8 t delta
            + 2 Tr(H^2) - (Tr H)^2]/16.

On positive semidefinite matrices S of rank at most two, F(S) is nonnegative. The equality F(S)=0 is precisely the missing orientation condition in the projection completion.

For stable numerical checking, factor S=XX* with X of size 36-by-2 (pad a zero column when rank S=1). For each physical coordinate a, collect the corresponding two rows into the 2-by-2 matrix M_a. Define the complex d-by-4 matrix

    Z_c[a,:] = [Tr M_a, i Tr(M_a σ_x), i Tr(M_a σ_y), i Tr(M_a σ_z)],

and the real 2d-by-4 matrix Z=[Re Z_c; Im Z_c]. Then

    F(S) = det(Z^T Z).

Thus the polynomial test can equivalently be checked by a real four-column rank test. It does not depend on the factor X chosen.

### Proof of the polynomial identity
Form the two-qubit positive matrix ρ_X=Σ_a |vec(M_a)><vec(M_a)|, with the spinor index first. Let C_ij=Tr(ρ_X σ_i⊗σ_j) be its real correlation matrix. Direct contraction gives CC^T=H and det C=delta; the transpose of σ_y accounts for the sign in delta. Its trace is t.

The unit quaternion coefficients (a_0,a_1,a_2,a_3) parameterize U=a_0 I+iΣ a_i σ_i in SU(2). The quadratic form Σ_a|Tr(M_a U)|² is a^T Z^T Z a. Local SU(2) changes of the two indices act orthogonally on these four real coefficients. They can reduce C by a signed singular-value decomposition to diag(c_1,c_2,c_3). In that basis the four eigenvalues of Z^T Z are

    (t-c_1-c_2-c_3)/2,
    (t-c_1+c_2+c_3)/2,
    (t+c_1-c_2+c_3)/2,
    (t+c_1+c_2-c_3)/2.

Multiplication gives the displayed invariant formula. Since Z^T Z is positive semidefinite, its determinant vanishes exactly when a nonzero real nullvector exists. Normalize this vector to obtain a unitary U satisfying Tr(M_a U)=0 for every a.

## Necessity: Schwinger bosons
Let W be the 19-by-18 syndrome-space isometry and q its one-dimensional orthogonal complement. In the spin-nine representation, let a,b map the n=18 boson sector to n=17, with

    a* a=9I+J_z,  b* b=9I-J_z,  b* a=J_-,
    a a*+b b*=19 I_18.

The full spinor matrix T_full=[b,a]*[b,a] is therefore 19 times a rank-18 orthogonal projector. Compressing to W in both spinor sectors gives T. Its omitted block has dimension two, so

    S=19T-T²=XX*, rank S<=2.

Here the rows of X are the traceless matrices

    [[-v_z, v_x-i v_y], [v_x+i v_y, v_z]],

where v_i=W*J_i q. Hence the orientation test holds. The spectrum of T is

    0 (multiplicity 18), 19 (multiplicity 16), 10±|gamma|,

where gamma_i=<q|J_i|q> and |gamma|<=9. At the coherent endpoint one of the last two eigenvalues is 19, but rank T remains exactly 18.

## Sufficiency: projection completion and spin reconstruction
From S>=0, every eigenvalue λ of T satisfies λ(19-λ)>=0, hence 0<=T<=19I. S cannot have rank zero because Tr T=324 is not divisible by 19.

Factor S=XX* with two columns. Let r=rank S, X^+ be the Moore-Penrose inverse, and P=X^+X. Define

    Y=19P-X^+ T X.

Since S is a polynomial in T, its range is T-invariant and X^+TX is Hermitian. Direct spectral calculation gives

    TX+XY=19X,   X*X+Y²=19Y.

Together with S=XX*, these show [[T,X],[X*,Y]]²=19[[T,X],[X*,Y]].

If r=2, rank T=18 and Tr T=324 imply 16 eigenvalues equal to 19 and two interior eigenvalues summing to 20; hence Tr Y=18. If r=1, there are 17 eigenvalues 19 and the sole interior eigenvalue is 1, so Y has eigenvalues 18,0 and again Tr Y=18.

Condition F(S)=0 gives U in SU(2) with every row-block of XU traceless. Replace X by XU and Y by U*YU. After arranging the two added coordinates as the two spinor copies of the same one-dimensional complement, the completed matrix has partial spinor trace 18 I_19. It therefore has the unique form

    T_hat=[[9I-Jhat_z, Jhat_x-iJhat_y],
           [Jhat_x+iJhat_y, 9I+Jhat_z]]

with Hermitian 19-by-19 Jhat_i. Expanding T_hat²=19T_hat in the Pauli basis gives

    [Jhat_x,Jhat_y]=iJhat_z and cyclic permutations,
    Jhat_x²+Jhat_y²+Jhat_z²=90 I_19.

Thus the Jhat_i constitute a single spin-nine irrep. In particular their traces vanish, so the reconstructed lower diagonal moments automatically equal -Tr A_i.

### The boundary condition is not an additional assumption
For every degree<=1 basis error E_a, the moment multiplication identities through degree five imply

    R F_a=0,  D_ij F_a=0,

where R=90I-ΣA_i², D_ij=iε_ijkA_k-[A_i,A_j], and F_a=(L*e_a)⊗I_2. Those eight vectors span the first eight degree-ordered syndrome coordinates. The blocks of S are linear combinations of R,D_ij, so S annihilates these coordinates in both spinor sectors. Positivity then forces every factor X to vanish there. The resulting v_i have exactly the boundary support required in the previous reconstruction theorem. That theorem recovers both complex code vectors and proves all Knill–Laflamme conditions through rank four.

## What this does and does not accomplish
This removes all 60 real completion-vector unknowns, with an exact scalar polynomial replacing their orientation freedom. It also handles boundary-covariance ranks one, two, and three uniformly. It does not show the 68-moment conditions are infeasible. A numerical near-zero of F, a local minimum, or a rank threshold is not a code or a proof.

## Three scalar equations, without explicit rank tests
Under S>=0, the condition rank S<=2 is equivalent to

    e3(S)=((Tr S)^3-3 Tr(S) Tr(S²)+2 Tr(S³))/6=0.

Together with Tr T=324, this leaves only two possible two-interior-eigenvalue branches: sixteen 19s with the interior eigenvalues summing to20, or seventeen 19s with them summing to1. The physical branch, including its coherent rank-one limit, is exactly selected by

    Tr(T³)-30 Tr(T²)+67536=0.

Indeed, writing t=TrS and u=Tr(ST), the first branch gives u=11t-180. The second gives u=333-35t/2, meeting the first only when the smaller interior eigenvalue is zero (the coherent boundary). Thus the complete criterion consists of G>0, S>=0, and **three scalar equations** e3(S)=0, this cubic trace equation, and F(S)=0. These are high-multiplicity boundary conditions; their small number does not imply an easy numerical problem.

## Significance and limitation of the variable count
The complex Grassmannian Gr_C(2,19) already has real dimension68. Therefore this is **not** a variable-count reduction compared with the original unrestricted code manifold. Its useful feature is a moment/spectrahedral formulation with exact rational coefficients, two linear matrix inequalities before normalization, and three explicit invariant equalities. It eliminates the 60 redundant completion variables of our intermediate128-variable model.

## Important adversarial warning for SOS use
F(S) is not nonnegative on every PSD matrix. Let d=2 and

    X=[[1,-1,1],[-1,1,-1],[0,0,1],[0,1,-1]], S=XX^T.

Then S is PSD of rank3 but F(S)=-16. Nonnegativity of F in the theorem uses rank S<=2 and must not be extended to the whole PSD cone without proof.
