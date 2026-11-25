# Independent analytic audit: known dense nested bases

## Result and scope
The proposed proof in `hss-probe-reuse/phase2/fixed_basis_bound.md` passes this independent analytic audit. For fixed real orthonormal nested row/column bases specified independently of the probes, the square-frame coefficient decoder uses2k forward plus2k transpose queries and satisfies

    E||A−B||F² <= (20L+3) min_{H∈C_fixed}||A−H||F².

Here C_fixed is the associated linear HSS class. This is not the unrestricted unknown-basis RE02 statement. In particular, adaptive bases learned from the same probes cannot be treated as fixed/independent, and multiplying thisO(L) factor by anO(L) basis-selection factor givesO(L²).

## Key checks
1. **Single-branch flux:** embed the live child samples in the two complete boundary frames. The difference flux is mapped by K↦K−(I−Π)K(I−Γ), an orthogonal projection. With the sibling zero its squared norm J decreases pointwise, independently of random-sign claims.
2. **Covariance, not scalar commutation:** with fixed forward bank, retained transpose coordinate satisfies Z′=RᵀZA+R_perpᵀHᵀWA. Fresh HaarH has zero mean and isotropizes WAAᵀWᵀ. The invariant EZZᵀ≼c²I/k closes because AAᵀ≼I, ||W||F²≤J≤c² and RᵀR+R_perpᵀR_perp=I. R_perp is the lower-left block of the complete orthogonal transfer, not the upper-right same-child blockT.
3. **Freshness:** the pure-detail source is frame-adapted with normalized amplitude fixed independently of the randomized bank. In the equivariant complement gauge, normalized coordinates depend on already traversed orientations only. Fixing the opposite complete bank does not condition the new Haar orientation. This does not justify arbitrary globally contaminated source conditioning.
4. **Branch factor5:** S=J+2||Z||F²+2<X−Z,Z>; pointwiseJ≤c², expected||Z||F²≤c² and Cauchy–Schwarz yield5c². No consecutive observed-energy monotonicity is claimed. The scalar rotation example approaches5, so the previously found energy gain is compatible with this bound.
5. **Arbitrary one-bank data:** decompose spatial rows into fixed hierarchical wavelet blocks. A block emits only at its birth, with a unique fresh central sign. Pick the deeper birth sign for nested blocks, or either sign for disjoint blocks: it is absent from the other contribution and kills the cross term. Unemitted/root-active components remain orthogonal. Thus the5 bound sums over input squared norms.
6. **Correlated anchors:** an ad block-column is split into its direct source and anchor. The direct source invokes the arbitrary-input lemma conditional on forward probes. The anchor instead invokes the pure-detail branch lemma conditional on transpose probes, where its amplitude is fixed. It is not falsely treated as independent of its own bank. Isotropy bounds its mean squared amplitude by the input column norm.
7. **dd and sector induction:** each dd source splits into two pure-detail terms, each with a contraction amplitude under opposite-bank conditioning. Hilbert-space triangle gives20. Distinct fine Walsh characters are orthogonal under every later carry map, so aa recursion takes the maximum sector constant rather than accumulating another depth factor.
8. **Output error:** local discrepancy subspaces and the root core are Frobenius-orthogonal. The decoder is linear and exact on C_fixed. Each level's coefficient energy is bounded by incoming sample energy. The root uses B_root=Y_root Ω_rootᵀ with square orthogonal Ω_root, so its norm is at most root sample energy. Summing gives20L+3.

## Randomness caveat and possible finite variant
For arbitraryk, central signs alone do not imply isotropic matrix covariance. HaarO(k) suffices. Uniform signed-permutation orientations also have the two required moments EH=0 and E(HᵀMH)=Tr(M)I/k, so an explicitly equivariant parent-frame construction should admit a finite-randomness variant. That extension should be stated with its gauge construction, not assumed for arbitrary deterministic complement choices.

**21:32 update: explicit finite variant audited.** In the worker's
`finite_orientation_variant.md`, sibling active frames F0,F1 are complementary
rows of the parent's full orthogonal transfer. Set Gi=Hi F_(1−i), with independent
uniform signed-permutation Hi, and retain that gauge recursively. The normalized
next boundary orientation is then literally Hi, so no unproved invariance under
arbitrary orthogonal gauge changes is invoked. The same zero mean, conjugation
isotropy, and extracted central sign prove every step above. This explicit finite
construction passes the analytic audit; arbitrary signed-permutation complement
implementations are not covered.

## Prior art
The general COLT2026 linear-family theorem has approximately sqrt(q) query dependence and an additive norm error; it does not subsume thisO(k) pure-relative fixed-basis result. Classical probing and the existing HSS coefficient algorithm are inherited ingredients. The new covariance/wavelet/sector proof's publication priority remains unestablished. See `prior_art_refresh.md`.
