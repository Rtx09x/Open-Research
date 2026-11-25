# Phase-two prior-art check (2026-10-25)

## Closest ingredients to the six-k forest theorem

* [Montoison, Dalle and Gebremedhin, *Revisiting sparse matrix coloring and
  bicoloring* (2025), Sections 1.3, 2 and Appendix A.3](https://arxiv.org/html/2505.07308v1):
  direct star bicoloring recovers entries using either forward or reverse
  compressed measurements. Star coloring forbids a two-colored four-vertex
  path, so two-color components are stars. The forest depth-mod-three rule
  is an elementary instance, and the direct recovery mechanism is not new.
* [Amsel et al., *Fixed-sparsity matrix approximation from matrix-vector
  products* (2024), Section 4.1](https://arxiv.org/html/2402.09379v3):
  explicitly analyzes Rademacher-signed coloring, with exact Frobenius variance
  controlled by off-pattern energy for a banded/unidirectional setting, and
  variance reduction by averaging independent copies. Consequently the general
  random-sign principle and the averaging corollary are also established.
* [Musco and Ramesh, *Nearly Instance Optimal Sparse Matrix Approximation from
  Matrix-Vector Products*, ESA 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.85):
  Theorem 2 gives O(degen(S) log(m+n)/(epsilon delta)) queries for a relative-error
  approximation with probability 1-delta; exact recovery needs 2 degen(S).
  Section 5 asks whether the logarithm can be removed. This does not directly
  give the exact six-k, factor-two forest guarantee. **Parameter correction:**
  a scalar forest adjacency pattern has degeneracy one, but the diagonal-plus-
  bidirectional-forest pattern used here has degeneracy at most two (and dense
  k-block expansion at most 2k), not one.

The precise forest-specific calculation here is that a single off-pattern
block can contaminate **at most one** decoded coefficient: its color difference
chooses diagonal, forward-parent, or reverse-parent, exclusively. This is a
clean combination/extension of existing ingredients. We did not locate an
identical theorem in the checked primary sources, but that is not evidence
enough for a novelty claim. The consultation supplied the candidate; this
phase independently proved and exhaustively checked it.

## Relevance to RE-02

The fixed-support comparator is strictly weaker than the best unknown-basis
HSS comparator. The constant-factor tree result does not eliminate either
unknown-basis sketch dependence or dense nested-basis coupling. Existing
RE-02 literature and the one-level-versus-multilevel distinction remain as
recorded in the frozen parent-directory `literature.md`.

## Further checks after the fixed-basis theorem

[Amsel et al., *Query Efficient Structured Matrix Learning*, COLT2026,
Section3/Corollary1](https://arxiv.org/html/2507.19290v2#S3) handles general
q-dimensional linear families using approximately sqrt(q) two-sided queries,
with an additive alpha||A||_F term in its approximation guarantee. For a fixed
HSS basis q is proportional toNk, so this is not the depth-independent O(k)
purely multiplicative guarantee established in `fixed_basis_bound.md`. The
paper's general-family result does not directly subsume this restricted bound.

[Persson et al., *A recursive butterfly factorization with optimality
guarantees* (August2026)](https://arxiv.org/html/2607.29361) concerns a different
complementary-low-rank class and uses approximately sqrt(N) matvecs. Its
conditional-sketch analyses may be useful techniques, but it is not an
O(k)-query HSS result.

Additional targeted searches for known/fixed HSS bases did not locate an
identical four-k/fixed-class O(L) theorem. This is only a limited prior-art
check, not evidence sufficient to claim priority. The proof deliberately
attributes the reused flux and sign-sector identities to the supplied Pro
consultation and treats star bicoloring/signed probing as existing methods.

Implementation note: the new phase-two Haar generator corrects Gaussian QR
by the signs of diag(R). The frozen exploratory `tree_frames.py` did not do
this and should not be treated as a faithful full-Haar sampler. The signed
exhaustive scripts and exact arguments are unaffected; none of the theorem
depends on the old exploratory Monte Carlo output.
