# HSS RE-02: substantive checkpoint, not a solution

## Full target status
Unresolved. No algorithm has been proved here to give rank-at-most-k HSS output with O(k) total forward plus transpose queries and O(L) expected squared error relative to the full HSS optimum for every fixed input.

## Independently checked exact arguments
1. **Minimal-width algorithm obstruction.** For k=1, L=1, s=3 Gaussian columns per direction, the reused Levitt–Martinsson algorithm has infinite expected squared error on [[0,I₂],[I₂,0]], while the exact HSS optimum is2. Larger constant oversampling remains possible.
2. **Actual dependence, at every width.** On that same input, for any s≥3, the squared compressed core coefficient has positive covariance E(λ₁−λ₂)/8 with the squared norm of the corresponding compressed Gaussian test row. Marginal Gaussianity does not imply independence from the compressed matrix. This defeats a specific proof shortcut, not the algorithm.
3. **Robust fixed block-tree theorem.** A known coordinate-nested block-tree subclass of rank-k HSS admits4k total queries and the exact off-support error formula weighted by tree distance. In particular expected squared error is at most(2L+2) times its **own fixed-support** optimum. This factor is sharp for the estimator. An off-tree rank-one input has full HSS optimum0 but nonzero output error, explicitly proving the limitation.
4. **Dense known-basis unbiasedness.** With arbitrary independently fixed dense nested bases,4k recursively orthonormal-frame queries and the coefficient decoder satisfy E R(A)=P_fixed(A) at every depth. This handles noisy inputs but does not yet control variance.

No novelty claim is attached to these results. Gaussian inverse moments, sparse coloring/substitution, and the general warning about reuse dependence are existing background. The exact witnesses and restricted random-sign identities were derived and checked here.

## Reproduction and exact checks
- Reused Gaussian baseline at exact rank k, k=1,2, depths through5; noisy known-competitor tests and rank checks.
- Heavy-tail Monte Carlo with finite-moment controls; divergence itself is proved analytically, not inferred from samples.
- Block-tree expectation identity checked over every256 sign assignments at N=4 and every65,536 assignments at N=8 using integer-valued data and integer equality.
- Sharp tree-distance examples checked through depth7.
- Dyadic/adversarial perturbation scan:270 configurations,30 trials each. s=4 is highly unstable near exactly HSS inputs at larger depths; s=6,10 behave better on tested families. No asymptotic claim follows.
- Dense fixed-basis frame tests, complete small mean-square operators, and analytically integrated sign checks identify a failed stronger variance shortcut. All computations use one CPU, bounded memory, checkpointed jobs under5 minutes.

## Precise next gap
For the fixed dense-basis frame decoder, lifted coefficient spaces at different levels are Frobenius-orthogonal. An O(L) variance bound would follow from a uniform bound on expected carried sketch energy, for example E(||Y_l||²+||Z_l||²)<=2||A−P_fixed(A)||². The stronger claim that a particular cross term is always nonnegative failed a depth3 exhaustive-sign numerical test. Direct energy contraction or a tree-path/scattering argument remains unproved.

Even an O(L) coefficient theorem cannot simply be multiplied by an O(L) basis-selection theorem without losing another factor L. A constant-factor coefficient theorem, or a shared optimum-level error charge, plus a robust unknown-basis learner would still be required for the full problem.

## Closest newly checked literature
- Amsel et al., SIMAX2026: O(kL) queries, O(L) error factor.
- Yesypenko, arXiv:2610.04574, October3: one-level reuse bound; global carried method empirical, global proved variant resketched.
- Gallmeier–Otto, arXiv:2610.07513, October5: predetermined row-space regression, not unknown HSS bases.
- Musco–Ramesh, ESA2026: degeneracy-based robust sparse approximation with logarithmic query factor; directly relevant to the tree subclass.

See `literature.md` for direct primary-source links and `pro_brief.md` for a self-contained consultation packet.

## Additional exact proof-route counterexample
`rational_potential_counterexample.md` supplies a rank-one three-entry input and rational nested bases for which expected carried sketch energy **increases** at one level by an explicitly positive rational number (about0.12825445). An independent standard-library-only verifier checks all4096 remaining sign assignments after analytic finest-sign elimination. This precisely rules out the monotone-potential proof shortcut; the uniform global-energy conjecture and RE-02 are not refuted.
