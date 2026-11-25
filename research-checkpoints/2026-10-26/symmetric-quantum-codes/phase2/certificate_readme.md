# Rigorous 18-qubit exclusion certificate

**Status:** the worker and a separately implemented independent rigorous verifier pass for the identical witness hash. Separate mathematical applicability audits and parent review also pass. This is an internally established computer-assisted result, not externally peer-reviewed or accepted; priority remains unconfirmed. See [the full theorem and necessity proof](theorem_and_necessity.md).

## What must be checked
The physical premise is a rank-two complex code projector P in spin9 satisfying Knill–Laflamme detection through tensor rank4. This implies the three-copy constraints in `three_copy_relaxation.md`. All partial-transpose, complement, and lifted-KL constraints used here are necessary for the unrestricted complex code, not a real/parity ansatz.

The finite witness is `interval_dual_candidate.json`, SHA256

    201e1acd2e8616807d98d07038174559cc4480aba1cca8b2d736997e251c7a79

Every PSD multiplier is stored as a rational Gram factor with denominator10^12. Its PSD property is exact by construction, without trusting numerical eigenvalues. The unstructured matrices `basis_U` are also rational: they only define compressions of a genuine PSD Z block, so they do not need to be exact S3 eigenvectors or orthonormal bases.

## Full-spin residual identity
Use weighted full multiplicity blocks Ztilde_J=(2J+1)Z_J. They are PSD and

    Σ_J Tr Ztilde_J = Tr twirl(P^⊗3) = 8.

The intrinsic enumerators satisfy a>=0 and Σa=19/2. The rational Gram multipliers give a nonnegative linear combination L(a,Z) of valid scalar/PSD inequalities. Subtracting exact equality multiples and using the code identities writes it as

    L(a,Z) = c + r·a + Σ_J Tr(R_J Ztilde_J),

where

    c = -1930688571530266893851 / 19000000000000000000000000
      < -1/10000.

The checker computes r and R using the factorial Racah formula with rigorous outward-rounded Arb balls. It does not import the optimizer, the floating S3 bases, or any worker model code.

The KL multipliers are first lifted to fixed-pair-spin vectors. Each supplied rational vector h is projected onto the **exact** detected-rank subspace using the closed Racah eigenvectors

    U_Jr=(-1)^(L+9+J) sqrt((2J+1)(2r+1)) {L 9 J;9 L' r}, r<=4.

Thus the corresponding equality is exact independently of the numerical eigensolver that suggested the multiplier. The full residual is averaged over the exact S3 representation, and its absent wedge³ component is removed. These operations preserve its pairing with every genuine code's Z.

At256-bit ball precision the checker proves every scalar entry of r and every entry of every R_J has absolute value less than10^-8. The largest multiplicity is19, so a conservative exact bound is

    |r·a + Σ_J Tr(R_J Ztilde_J)|
       <= (19/2 + 8·19)·10^-8
        = 323/200000000.

Therefore the nonnegative combination would obey

    L(a,Z) < -1/10000 + 323/200000000
            = -19677/200000000 <0,

a contradiction. The diagnostic floating residuals are substantially smaller, but are not used in the proof.

## Reproduction
The isolated environment contains python-flint0.9.0, obtained from official PyPI. Run

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      python phase2/check_interval_dual.py

from the parent problem directory. The checker typically takes under2 seconds. It uses only the standard library, python-flint, and the witness JSON. `interval_dual_verification.json` records the result. `extract_interval_dual.py` documents the numerical search/rounding provenance, but is not needed to verify the finite witness.

## Controls and scope
- The actual known19 projector's three-copy twirl, not merely some compatible SDP point, was reconstructed from numerical Clebsch–Gordan matrices. Its lifted-KL residual is1.56e-15 and PPT minimum eigenvalue about-1e-17. The independent auditor checked every mixed cone as well.
- Independent exact small-spin tests cover partial-time-reversal crossing and local-Casimir coefficients; random complex non-time-reversal-invariant controls check the full map, including imaginary moments.
- Independent confirmation of the finite witness, every necessary constraint, the exact n=9,…,17 exclusions, and the known19 construction is complete. Combined with the elementary n≤8 no-cloning obstruction, the result establishes the two-error minimum n=19 within the stated symmetric-code class. It does not prove the all-t conjecture n_min=3t²+3t+1; external review and priority checking remain outstanding.
