# Three-copy SU(2) projector relaxation

**Current status:** a rigorous interval dual certificate for the final lifted-KL relaxation now passes two independently implemented arithmetic verifiers. Independent physical-applicability review and the complete minimum-19 chain also pass; the result is internally established, not externally peer-reviewed. See [the current theorem and full necessity proof](theorem_and_necessity.md) and [certificate reproduction](certificate_readme.md).

**Chronology note:** this document retains the progression through weaker relaxations; their feasibility statements are historical and do not describe the final strengthened model. All SDP constraints are necessary, not sufficient, for a code. The finite hierarchy is motivated by the established state-polynomial/projector SDP approach of [Anglès Munné, Nemec, Huber, arXiv2408.10323v2](https://arxiv.org/html/2408.10323v2), not claimed as a novel general methodology.

Let P be an actual rank-two code projector on V_j, N=2j+1, and let collective SU(2) twirling define Y=twirl(P⊗P), Z=twirl(P⊗P⊗P). Then Z>=0 and commutes with S3. Exact projector identities imply

    Tr_3 Z=2Y,  Tr_3(Z Swap23)=Y.

The wedge³ sector vanishes because rankP=2. As the advisor noted, this is also implied by the displayed identities, S3 invariance, positivity and Tr(Y Swap12)=2; it is enforced for dimension reduction, not counted as an independent strengthening.

## Two-copy normalization
Let a_r be the audited intrinsic enumerators and M their SU(2) MacWilliams transform. The trace weight of Y in pair spin L is

    t_L=(4/N) Σ_r (-1)^r M[L,r] a_r.

Hence Y acts as t_L/(2L+1) on pair spin L. This formula was independently exactly checked by the advisor for n2,3,6,18,19 and numerically against a direct19-code two-copy projector calculation (error2.4e-12).

## Three-copy multiplicity blocks
Couple the first two physical spins to L, then couple to the third spin to obtain total J. Write Z=⊕_J I_(2J+1)⊗Z_J. Pair-spin diagonal marginal equations are

    Σ_J(2J+1)(Z_J)_[L,L]=2t_L,
    Σ_J(2J+1)(Z_J Swap23_J)_[L,L]=t_L.

A real relaxation suffices: averaging a feasible Hermitian Z with its complex conjugate preserves all these real constraints and positivity. This does not impose a real code.

The S3 commutant splits into symmetric, standard and antisymmetric sectors. Drop the antisymmetric sector. If pair12 is symmetric, the weighted symmetric/standard marginal contributions are respectively4t_L/3 and2t_L/3; if pair12 is antisymmetric, the standard contribution is2t_L. The n18 model has340 scalar variables and51 PSD blocks of size at most6. It is numerically strictly feasible, so it does not exclude18.

The implemented recoupling basis differs from standard Clebsch–Gordan phases by diag((-1)^L). This harmless basis gauge is tracked consistently. It does not change a fixed-(L,L') channel transformation, and S3-invariant Z has no opposite-parity entries.

## Partial transpose and complement constraints
Partial time reversal τ3 (partial transpose followed by the spin-j invariant unitary) preserves collective invariance and maps every twirled product term to a positive product. Thus τ3 Z>=0. It generally does not commute with allS3; only its surviving Swap12 parity decomposition is used.

For integer pair spins L,L', its crossing formula is

    (τ3 Z)^K_[L,L'] = Σ_J (-1)^n (2J+1)
       { L j J; L' j K } (Z_J)_[L,L'].

Direct exact small-spin CG tests checked the sign, normalization and off-diagonal cases. PPT alone also remained feasible atn18.

Putting Q=I-P gives additional valid twirled-product LMIs

    Y12-Z >=0,
    (2/N)I-Y12-Y13+Z >=0,
    (1-6/N)I+Y12+Y13+Y23-Z >=0.

All inequivalent partial-time-reversed versions are also imposed. These remain numerically feasible atn18; they are not an exclusion.

## Lifted Knill–Laflamme equations: stronger order-three information
For every detected tensor T of rank<=4, PT P=(TrPT/2)P. For arbitrary A,B,

    2 Tr(P A P T) Tr(PB)-Tr(PA) Tr(PB) Tr(PT)=0.

Equivalently,

    Pi_(operator rank<=4 on factor3) [(2Swap13-I)Z]=0.

This is a linear constraint on Z, stronger than merely imposing the quadratic enumerator equality at the earlier relaxation level. Rank0 reproduces the existing projector marginal identity.

It can be implemented without constructing the6859-dimensional three-spin space. On a fixed pair-spin (L,L') matrix entry, the local commutator Casimir on the third factor acts on the total-J label. After weighting by sqrt(2J+1), it is a real symmetric tridiagonal matrix with exact spectrum r(r+1), r=|L-L'|,...,min(L+L',n). Its rank-one tensor channel coefficients in unweighted coordinates are

    3(2J+1)(-1)^(L+L')
      { j K L; J j 1 } { j K L'; J j 1 }.

The Casimir equals 2j(j+1)I-[2N j(j+1)/3] times this channel. Keeping its eigenspaces r<=4 gives149 independent new linear rows atn18 and159 atn19. The advisor independently checked full small-spin channel matrices and exact spectra without worker imports.

The known19 fixed-enumerator SDP passes this lift. The first n18 solve returned a numerical solver failure, not infeasibility. Those checks were subsequently completed: the actual known19 twirl passes all cones, and n18 phase-I slack was positive in two solvers. A finite dual witness was then extracted and rigorously verified, as detailed in the current theorem document.
