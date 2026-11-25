# Hostile applicability audit: what the certificate excludes

**21:52 UTC.** No applicability counterexample was found. This note separates
the mathematical model from arithmetic replay and from publication priority.

## No hidden code ansatz
Let P be any rank-two orthogonal projector whose range lies in Sym^18(C²).
Coefficients may be arbitrary complex numbers. There is no real, parity,
time-reversal, nondegeneracy, or sparse-Dicke assumption. For exclusion it is
enough that physical distance5 implies detection of collective tensor ranks0..4:
each rank-r tensor is a degree-r polynomial in collective spin generators,
hence a linear combination of Pauli operators of weight≤r. No converse is
needed in this direction.

The term permutation invariant here means **every code vector is fully
symmetric**, not merely that the code projector commutes with permutations on
the full 2^18-dimensional space. The latter broader notion is not excluded.

## Antisymmetric absence is exact
On three copies, P⊗P⊗P restricted to the fully antisymmetric sector has range
Λ³(range P), which is zero because rankP=2. The collective SU2 action commutes
with every copy permutation. Hence twirling preserves this zero sector, giving
Z A3=A3 Z=0. This uses rank two, not an unjustified Bose-symmetry assumption:
the standard S3 sector is retained and need not vanish.

## Lifted KL identity for complex codes
For arbitrary A,B and any detected tensor T,

 Tr[P^⊗3(A⊗B⊗T)Swap13] = Tr(PAPT)Tr(PB)
 = Tr(PT)Tr(PA)Tr(PB)/2.

The second equality follows by cyclicity and PTP=Tr(PT)P/2. Thus the difference
with the no-swap expression vanishes after multiplication by2. The detected
rank≤4 space is closed under conjugation by SU2 and under adjoint, so twirling
and interpreting trace duality as Hilbert–Schmidt orthogonality are legitimate.
This proves Π_≤4^(3)[(2Swap13−I)Z]=0 for arbitrary complex P. It does not require
each individual low-rank moment to vanish.

## Mixed positivity and partial transpose
With Q=I−P, every tensor word in P,Q is PSD. Its collective twirl is PSD.
Partial time reversal of one factor also preserves each such product's
positivity, although partial transpose is not positive on arbitrary entangled
operators. That product/separability premise is essential and is present here.

Expanding gives PPQ=Y12−Z, PQQ=(2/19)I−Y12−Y13+Z, and
QQQ=(1−6/19)I+Y12+Y13+Y23−Z. Their other placements follow by copy permutations.
After τ3 there are five inequivalent cases PPQ,PQP,PQQ,QQP,QQQ; none assumes
that τ3Z remains fully S3 invariant. Only its valid swap12 parity decomposition
is used. Time reversal intertwines the conjugate spin representation with the
original, so τ3Z remains collectively SU2 invariant and admits the recoupling
blocks used by the certificate.

## General local-Casimir formula, not only finite controls
Fix pair spins L,L′. Let E_J be the invariant intertwiner obtained by coupling
L with j to total J on the left and L′ with j to J on the right, summing over
magnetic index M. Its Hilbert–Schmidt norm is sqrt(2J+1). For normalized basis
E_J/sqrt(2J+1), the rank-one channel

 C(X) = 3/[(2j+1)j(j+1)] · Σ_a (I⊗J_a)X(I⊗J_a)

has matrix entries

 C_KJ = 3 sqrt((2K+1)(2J+1)) (−1)^(L+L′)
        {j K L; J j 1}{j K L′; J j 1}.

To derive this, insert coupled magnetic bases on both sides of X. Apply the
Wigner–Eckart formula to I⊗J_a. Each reduced matrix element contributes
sqrt((2K+1)(2J+1)) sqrt(j(j+1)(2j+1)) times its six-j; the two phase factors
multiply to (−1)^(L+L′). Summation over the magnetic indices and the three
spherical components gives the three-j orthogonality factor; division by the
intertwiner norms and the channel normalization leaves exactly the displayed
coefficient. Equivalently this follows by expanding the defining four-three-j
sum for the [six-j symbol](https://dlmf.nist.gov/34.4).

The local commutator Casimir is

 K = 2j(j+1)I − 2(2j+1)j(j+1) C/3.

On third-factor operator tensors of rank r it acts by r(r+1), since
End(V_j)=⊕_(r=0)^(2j) V_r under conjugation. In the invariant intertwiner space,
allowed ranks run from |L−L′| through min(L+L′,2j), each once. This proves the
general spectrum and low-rank interpretation used by both independent
certificate routes. The direct-CG small-spin tests check implementation phases
and normalization; they are not the sole proof of the formula.

## Finite minimum-length conclusion and remaining uncertainty
An eighteen-qubit exclusion alone would not imply exclusion at every shorter
length; symmetric padding is not assumed. The chain is instead:

1. General quantum Singleton bound excludes n≤8 for dimension2,distance5.
2. Separate exact intrinsic-LP/Farkas certificates exclude each n=9,…,17.
3. The current full-space interval dual excludes n=18 if its independent model
   and arithmetic checks pass.
4. The known n=19 construction has an independently replayed exact rational
   contraction proof of its algebraic root and all50 reduced-Gram KL relations
   (`advisor/code19_audit.json`). It is a replicated positive control, not a
   newly invented code.

Together these establish the finite statement n_min^PI(2)=19. They do **not**
settle the all-t conjecture3t²+3t+1, arbitrary qudit variants, or the broader
permutation-invariant-projector model.

Remaining uncertainty is now external validation/priority and ordinary software
trust, not a known mathematical gap in the checked model. Arb/FLINT's outward
rounding and the exact integer/rational parser are trusted computational
components; this is a computer-assisted proof, not a proof-assistant formalization.
The independent rewritten verifier passed at21:53UTC: `quantum-independent-audit/verify_full_certificate_independent.json` binds the same candidate SHA256, imports no worker code, and uses a separately certified Casimir eigenresidual defect below10^-40 rather than assuming the closed Racah projector formula. Its strict negative upper remains approximately−9.8385e−5.
Fresh targeted literature checks found no prior unrestricted n18 exclusion,
but absence of a search result is not a priority guarantee.
