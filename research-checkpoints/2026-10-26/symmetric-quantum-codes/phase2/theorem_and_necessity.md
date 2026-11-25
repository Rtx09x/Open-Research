# Minimum length for a symmetric two-error-correcting qubit code: computer-assisted theorem and necessity proof

**Status (2026-10-25): internally established computer-assisted result.** Two independently implemented rigorous arithmetic verifiers and separate mathematical applicability audits pass. The parent review confirms the complete finite minimum-length argument. This has **not** received external mathematical peer review or publication acceptance, and priority remains unestablished. Earlier “no certificate” statements in the research chronology describe weaker, earlier relaxations.

## 1. Precise statement and scope

**Theorem (computer-assisted).** The least integer n for which there is a two-dimensional complex subspace

    C ⊂ Sym^n(C²) ⊂ (C²)^⊗n

correcting arbitrary errors on at most two physical qubits is n=19.

Here every vector of C is fixed pointwise by every physical-qubit permutation. This is not the broader condition that permutations merely preserve C as a set. In the normalized Dicke basis, two orthonormal codewords have the form

    |c_i> = Σ_(w=0)^n c_(i,w) |D_w^n>,    c_(i,w) ∈ C, i=0,1.

There is no real-amplitude, parity, reflection, transversal-gate, nondegeneracy, or Pollatsek–Ruskai ansatz restriction. The projector P onto C has rank exactly two. “Correcting arbitrary errors on two qubits” means the Knill–Laflamme conditions for the linear span of all Pauli errors of support at most two, on arbitrary locations. Products E†F span all Pauli operators of support at most four; hence the condition is exactly detection of all physical operators of weight at most four, conventionally distance at least five.

Only the finite t=2 case is asserted. This does **not** establish the proposed general formula n_min(t)=3t²+3t+1.

### Known inputs and what is added

1. **n≤17:** Rui S. Okada, *A Quantum Analog of Delsarte's Linear Programming Bounds*, arXiv:2502.14165v1, §3.4, Table 3.1, printed p. 89; PDF page 93 (zero-index 92), tabulates the applicable single-spin bounds. In particular the distance-five entries for n=13,…,17 are one; the smaller entries are already excluded by the distance-four bounds. Our exact rational Farkas certificates independently replay the relevant n=9,…,17 instances. These exclusions are prior art, not our new result. [Primary source](https://arxiv.org/pdf/2502.14165).
2. **n=19:** Arda Aydin, Max A. Alekseyev and Alexander Barg, *A family of permutationally invariant quantum codes*, arXiv:2310.05358v3, §7, construct a ((19,2,5)) code from nine quadratic equations and certified algebraic root intervals. Our exact rational contraction/root certificate and all 50 reduced-Gram polynomial identities reproduce that known construction; rounded printed amplitudes alone are not used as a proof. Their shorter-length discussion in §7 occurs in a restricted construction context and is not used here as an unrestricted lower bound. [Primary source](https://arxiv.org/html/2310.05358v3#S7).
3. **Physical/intrinsic correspondence:** Eric Kubischta and Ian Teixeira, *MacWilliams Identities for Intrinsic Quantum Codes*, arXiv:2604.16023v2, Theorem B1, Lemma B1 and Proposition B2, identify physical distance with intrinsic tensor-rank depth in the symmetric spin representation. Their Theorem A1 and Corollary A3 give the scalar enumerator constraints used below. [Primary source](https://arxiv.org/html/2604.16023v2#A2).
4. **Added finite step:** the 18-qubit necessary three-copy relaxation described below has a rigorously checked separating witness. Together with the known shorter-length exclusions and known19 construction, this closes the only remaining length and yields the statement above. The general use of projector-moment SDP hierarchies is established methodology, not a priority claim.

For completeness, n≤8 cannot support any nontrivial distance-five quantum code: split its qubits into two sets of at most four. Detection of all operators on either set is correction of that set's erasure. Thus each disjoint complementary set could reconstruct the logical qubit, contrary to no-cloning. This is the elementary quantum Singleton/no-cloning obstruction. The exact n=9,…,17 replays plus the present n=18 step therefore cover all shorter lengths.

## 2. Spin reduction and intrinsic normalization

For n=18 the symmetric Hilbert space is the spin-j=9 irreducible representation V, of dimension N=19. Under conjugation,

    End(V) = ⊕_(r=0)^18 W_r,       dim W_r=2r+1.

Choose any Hilbert–Schmidt orthonormal tensor basis T_(r,q) of W_r, with T_(0,0)=I/√19. Compression of weight-at-most-four physical operators spans W_0⊕…⊕W_4. One can see necessity directly: J_+^r is a sum of physical weight-r raising products and generates W_r under collective rotations; conversely products of at most four one-site spin operators have tensor rank at most four. Therefore every code in §1 satisfies

    P T P = (Tr(P T)/2) P,       T ∈ W_0⊕…⊕W_4.                 (1)

Define

    a_r = (19/4) Σ_q |Tr(P T_(r,q))|².

Then a_r≥0, a_0=1, and Parseval with Tr(P²)=2 gives Σ_r a_r=19/2. This last normalization follows directly from the definition; the sentence after Eq. B18 of the cited intrinsic-code paper contains a conflicting normalization typo and is not used.

In the real standard Wigner-6j convention, put

    M_(r,k) = (-1)^(18+r+k) (2r+1) {9 9 r; 9 9 k},
    H = 2M-I.

The other quadratic enumerator is

    b_r = (19/2) Σ_q Tr(P T_(r,q)† P T_(r,q)) = (2Ma)_r.

The Hilbert–Schmidt Cauchy–Schwarz inequality on the two-dimensional code gives b_r≥a_r; equality holds exactly when each compressed rank-r tensor is scalar. Thus

    a≥0, Ha≥0, (Ha)_r=0 for r=1,2,3,4.                       (2)

These statements concern arbitrary complex P. All definitions are invariant under changes of tensor basis inside W_r.

## 3. Actual two-copy and three-copy moments

Let U_g be the spin-nine representation and normalized Haar measure be dg. Set

    Y = ∫ (U_g P U_g†)⊗2 dg,
    Z = ∫ (U_g P U_g†)⊗3 dg.

These are positive semidefinite, not normalized density operators: Tr Y=4 and Tr Z=8. They commute with collective SU(2); Z also commutes with every copy permutation. These permutations act on the three **spin-nine copies**, not the original eighteen physical qubits.

Couple copies 1 and 2 to pair spin L=0,…,18. Since V⊗V is multiplicity-free,

    Y = ⊕_L [t_L/(2L+1)] I_(2L+1),
    t_L = (4/19) Σ_r (-1)^r M_(L,r) a_r ≥0.                  (3)

Equation (3) is the standard tensor-operator/CG recoupling identity, obtained by expanding P in the orthonormal T_(r,q) and tracing against the pair-spin projector. It fixes the normalization of every two-copy term below; Σ_L t_L=4.

Couple this pair to the third spin-nine copy. Let

    Λ_J = {L: 0≤L≤18, |L-9|≤J≤L+9},    J=0,…,27.

Then

    Z = ⊕_J I_(2J+1)⊗Z_J,    X_J=(2J+1)Z_J≥0,
    Σ_J Tr X_J=8,           |Λ_J|≤19.                        (4)

The certificate uses X_J as its weighted full multiplicity variables. It does not depend on floating-point reduced S3 bases.

### Exact permutation matrices and projector identities

Use the CG phase gauge in which

    D_J[L,L'] = (-1)^(18-L) δ_(L,L'),
    F_J[L,L'] = √((2L+1)(2L'+1)) {9 9 L; 9 J L'},
    F13_J = D_J F_J D_J.

They represent Swap12, Swap23 and Swap13. They are real orthogonal matrices and obey the S3 relations. This gauge is related to another common CG choice by diag((-1)^L); every formula here uses the displayed gauge consistently.

Let Psym and Palt be the exact group-average projections onto the symmetric and alternating S3 sectors, and Pstd=I-Psym-Palt. Rank(P)=2 gives

    Z_J Palt_J=0,

because the alternating third tensor power of a two-dimensional space vanishes. Directly from P²=P and Tr P=2,

    Tr_3 Z=2Y,     Tr_3(Z Swap23)=Y.                          (5)

The L-diagonal consequences are

    Σ_J (X_J)[L,L]=2t_L,
    Σ_J (X_J F_J)[L,L]=t_L.                                  (6)

Together with the S3 commutant and the absent alternating sector, these can be expressed as the equality rows used in the certificate:

- if L is even, Σ_J(Psym_J X_J)[L,L]=4t_L/3 and Σ_J(Pstd_J X_J)[L,L]=2t_L/3;
- if L is odd, Σ_J(Pstd_J X_J)[L,L]=2t_L.

For example, on the pair12-symmetric line of the standard S3 representation, Swap23 has diagonal entry -1/2; solving the two marginal equations gives the stated 4/3 and 2/3 factors. On its pair12-antisymmetric line the entry is +1/2. These are necessary equalities, not fitted constraints.

## 4. Mixed projector/complement positivity and partial transpose

Write Q=I-P, and let Y12,Y13,Y23 denote Y embedded into the indicated pair with identity on the unused copy. Twirling positive products involving P and Q gives

    Z ≥0,
    Y12-Z ≥0,
    (2/19)I-Y12-Y13+Z ≥0,
    (1-6/19)I+Y12+Y13+Y23-Z ≥0.                              (7)

Their permutations are also valid. These follow by expanding, respectively, P⊗P⊗P, P⊗P⊗Q, P⊗Q⊗Q, and Q⊗Q⊗Q. The single-copy average is (2/19)I by irreducibility.

Define spin time reversal on one operator by

    θ(A)=C A^T C†,    C|j,m>=(-1)^(j-m)|j,-m>,

and τ3=id⊗id⊗θ. Although partial transpose is not positive on arbitrary entangled operators, every tensor product just used has positive individual factors. Its partial transpose, and hence its τ3 image, is positive. Convex integration preserves this. Thus τ3 applied to every product-derived operator in (7), including its permutations, gives further necessary PSD inequalities.

In full multiplicity blocks the crossing identity is

    (τ3 Z)^K[L,L'] = Σ_J (2J+1) {L 9 J; L' 9 K} Z_J[L,L']
                   = Σ_J {L 9 J; L' 9 K} X_J[L,L'].           (8)

For general n this has an overall (-1)^n; n=18 is even. Partial time reversal preserves collective invariance and Swap12 parity, but generally **not** full S3 invariance. The certificate retains the full parity multiplicity blocks on this output; it does not impose an invalid S3 or alternating-sector restriction there.

For explicit reproduction, in each J block put

    D=diag(t_L/(2L+1)),
    Dθ=diag(Σ_r {9 9 r;9 9 L} t_r),
    P13=F_J Dθ F_J,       P23=F13_J Dθ F13_J,
    Zθ=(τ3 Z)_J.

The five inequivalent mixed τ3 cones used by the witness, in addition to Zθ≥0, are

    D-Zθ ≥0,
    P13-Zθ ≥0,
    (2/19)I-D-P13+Zθ ≥0,
    (2/19)I-P13-P23+Zθ ≥0,
    (1-6/19)I+D+P13+P23-Zθ ≥0.                               (9)

The omitted permutations are Swap12 conjugates. Ordinary mixed blocks in (7) use Y13=F_J D F_J and Y23=F13_J D F13_J.

## 5. Lifted Knill–Laflamme equalities

This is the decisive strengthening over the feasible lower-order relaxations. For arbitrary operators A,B and any T∈W_0⊕…⊕W_4, (1) implies

    2 Tr(P A P T) Tr(P B) - Tr(P A) Tr(P B) Tr(P T)=0.          (10)

The swap trace identity identifies (10) with

    Tr([(2Swap13-I) P⊗3] [A⊗B⊗T])=0.

The detected tensor-rank space is invariant under rotations. Therefore twirling preserves the identity, and

    Π_(rank≤4 on factor3) [(2Swap13-I)Z] = 0.                 (11)

Here Π is Hilbert–Schmidt orthogonal projection onto the indicated operator subspace; the first two factors are unrestricted. Rank zero recovers the existing projector marginal, but the other ranks need not follow from quadratic enumerators.

Equation (11) can be written entirely in the full-spin blocks. For fixed pair spins L,L', define

    W_J=(2F13_J-I)Z_J,
    w_J=√(2J+1) W_J[L,L'].

On this channel the local commutator Casimir

    Δ3(A)=Σ_(i=x,y,z) [J_i^(3),[J_i^(3),A]]

has eigenvalues r(r+1), for |L-L'|≤r≤min(L+L',18). Its orthonormal recoupling eigenvectors in the w_J coordinates are

    U_(J,r)=(-1)^(L+9+J) √((2J+1)(2r+1)) {L 9 J;9 L' r}.     (12)

Consequently (11) is exactly U_r^T w=0 for each allowed r≤4. The finite witness stores arbitrary rational vectors h and uses the exact projected vectors Σ_(r≤4) U_r U_r^T h. Such multipliers give exact equality combinations regardless of how h was numerically suggested. A separate independent verifier instead bounds their low-rank projection defect using the exact Casimir spectral gap; thus the two arithmetic routes do not share an unverified numerical eigenspace assumption.

## 6. Complex amplitudes and the finite witness

All maps and coefficient matrices above are real in the stated recoupling gauge. If a genuine complex code produces Hermitian Z_J, replacing each block by its entrywise real part preserves PSD, the S3 identities, every real affine equality, and all PSD maps in (7)–(9). Its enumerators a remain unchanged. This is a relaxation of arbitrary complex codes, **not** an assumption that the original code vectors are real. Equivalently, real symmetric dual matrices have the same real functional pairing with the original Hermitian blocks.

The witness is `interval_dual_candidate.json`, SHA256

    201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79.

Every scalar inequality multiplier is a nonnegative rational. Every PSD multiplier is stored as a rational Gram factor BB^T, hence is exactly PSD. Ordinary Z tests can additionally have rational compression U, yielding UBB^TU^T≥0; U need not be an exact numerical S3 eigenbasis or be orthonormal. Exact equality multipliers use (2), (6), (11), a0=1 and Σa=19/2.

Let L(a,X) denote the resulting nonnegative linear combination of all tested inequalities. Subtracting equality multiples and using the exact S3 commutant and absent alternating block gives

    0 ≤ L(a,X) = c + r·a + Σ_J Tr(R_J X_J),                  (13)

where

    c = -1930688571530266893851 / 19000000000000000000000000
      < -1/10000.

The standalone checker computes every residual coefficient using factorial Racah 6j expressions with rigorous outward-rounded Arb balls at 256-bit precision. It proves

    |r_k| < 10^-8,       |(R_J)_(a,b)| < 10^-8.

There is no appeal to a numerical solver status, floating-point PSD eigenvalue, or approximate zero. For an m×m residual matrix with each entry bounded by ε, its operator norm is at most mε. By (4), positivity and Σa=19/2,

    |r·a + Σ_J Tr(R_J X_J)|
       ≤ (19/2 + 19·8)10^-8 = 323/200000000.

Therefore (13) would imply

    0 ≤ L(a,X) < -1/10000 + 323/200000000
                 = -19677/200000000 < 0,

which is impossible. This is a compact-domain residual certificate: the residual need not be exactly zero because its rigorous upper bound is much smaller than the strictly negative constant.

## 7. Reproduction and independent checks

Minimal worker verification requires Python, python-flint 0.9.0, `check_interval_dual.py`, and the witness JSON. No SDP solver, NumPy, SymPy, model builder, or numerical basis file is imported. Run from this problem directory:

    python phase2/check_interval_dual.py

The private environment is not part of the mathematical artifact; a fresh isolated Python environment with the stated python-flint package suffices. `interval_dual_verification.json` records the exact bound and witness hash. The numerical extraction program and solver logs are provenance only, not proof dependencies.

The independently implemented verifier is maintained outside this worker's folder in `../../quantum-independent-audit/verify_full_certificate_independent.py`; it imports no worker code and obtains exact 6j signs/squares independently, combines them with outward-rounded balls, and adds a rigorous KL eigenresidual budget. Its corresponding JSON reports PASS for the same witness hash and a strictly negative upper bound. The additional KL budget is at most 10^-40, leaving the displayed separation essentially unchanged.

Applicability controls, which supplement rather than replace the derivation, include: all 290 ordinary/mixed/PPT tests on the directly constructed known19-code twirl; exact small-spin CG crossing/Casimir checks; and independent direct full-Hilbert tests on generic **complex, non-time-reversal-invariant** rank-two projectors at n=2,…,6. These last controls exercise imaginary moment couplings and confirm that partial transpose is not mistakenly forced back into the S3 commutant. The separate exact19 algebraic root certificate and n=9,…,17 Farkas replays have also passed independent rational checks.

The independent auditor's final report, `../../quantum-independent-audit/INDEPENDENT_APPLICABILITY_REPORT.md`, explicitly records PASS for arithmetic, unrestricted complex-code applicability, and the complete minimum-19 target. The parent has reviewed that report and the advisor's separate hostile audit. These are internal research checks, not external peer review or publication acceptance. Priority remains to be investigated; no all-t conclusion is claimed.

### Minimal proof dependencies
The new n18 exclusion uses only the intrinsic enumerator constraints, three-copy projector/mixed-PPT/lifted-KL identities, and finite full-space interval witness described here. It does **not** depend on the exploratory syndrome nondegeneracy lemma, pure-complement variance gap, Schwinger/spinor reformulation, or any failed numerical searches. Those earlier results are retained separately for research provenance and are not extra assumptions.

## Appendix: arithmetic convention for the finite recoupling data

For the integer spins occurring in the n18 certificate, the checker defines the standard real 6j symbol by

    {a b c; d e f}
      = Δ(a,b,c) Δ(a,e,f) Δ(d,b,f) Δ(d,e,c)
        × Σ_z (-1)^z (z+1)! / [(z-a-b-c)! (z-a-e-f)!
             (z-d-b-f)! (z-d-e-c)! (a+b+d+e-z)!
             (a+c+d+f-z)! (b+c+e+f-z)!],

    Δ(x,y,z)²=(x+y-z)! (x-y+z)! (-x+y+z)!/(x+y+z+1)!.

The sum is over integers making every factorial argument nonnegative; a failed triangle condition gives zero. Thus each coefficient is an exact rational times a square root of a nonnegative rational. All factorials and the rational sum are computed exactly before the square root is enclosed by Arb. This fixes signs and normalization without reliance on numerical recoupling libraries. The independent verifier uses SymPy's symbolic 6j evaluation, reduces its square and sign exactly, and only then forms independent Arb enclosures.
