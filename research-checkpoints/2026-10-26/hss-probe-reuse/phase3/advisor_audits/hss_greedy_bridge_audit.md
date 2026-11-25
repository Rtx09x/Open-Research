# Greedy-basis and exact4L coefficient audit

2026-10-25 22:26 UTC. Analytic audit: PASS, with the scope below.

The external family is A=xw^T+(3/2)e0z^T, x=sum_(j=0)^(L−1)e_(2^j), w=e_(2^L), z=e_(3*2^(L−1)), L>=3. The root off-diagonal block has singular values sqrt(L),3/2, so its rank-one tail is9/4. The globally rank-one xw^T attains this HSS optimum. At each bottom-up greedy stage the first block row compares orthogonal energies1 and9/4 and uniquely retains the latter. All other nonzero row blocks preserve their one active row. The two nonzero columns remain in separate blocks until the final stage, where the same strict comparison picks the noise column. Thus exactly one unit signal is discarded per level, greedy loss is L, and the proposed weighted ledger is10L^2+13L. Kronecker product with I_k gives loss kL and optimum9k/4; projector uniqueness is sufficient even when bases within the k-dimensional retained subspaces rotate.

Fresh primary-source check of [Amsel et al.,2505.16937v2,§3 Algorithm1](https://arxiv.org/html/2505.16937v2#S3) confirms that this is the specified explicit-entry greedy rule: current off-diagonal block-row and block-column subspaces are selected independently, followed by compression. It does not cover all learners or establish a query lower bound.

For the fresh square-frame coefficient decoder, the exact4L result requires the stated canonical coordinate completion in zero-data blocks. Here is a narrower, explicit normal form for its sign proof. Along the relevant paths, write Ω_w=σ e0. A source row2^j has transpose test row τ_j e1 at its unique row-detail birth, where τ_j are distinct independent birth signs. The source contributes one unit-magnitude D_da at that birth. At the final right block the D_ad coefficient is sum_j τ_j; the root coefficient is ±σ sum_j τ_j. All other coefficients vanish. Consequently the POINTWISE total coefficient energy is

`L + 2 (sum_j τ_j)^2`,

and its expectation is3L. Since the pure signal is orthogonal to the fixed class and the noise is recovered exactly, total expected approximation error is L+3L=4L. The note's wording about “all active left/right test rows” should be read only along these relevant paths: w is ultimately a right DETAIL coordinate, so Ω_w lies on e0, not e1. This clarification does not change the identity. Arbitrary zero-block completions need not have the same exact risk.

The conditional covariance-risk reduction is also correct: exact recovery on C and output in C give K_C=(I−P_C)(I+E R_C^*R_C)(I−P_C). A fresh independent coefficient bank permits conditioning on learned bases; this does not retroactively make reused training probes independent. Young's inequality yields the stated signal-risk sufficient condition, which remains unproved for a general learner.

The twelve-probe two-candidate validation lemma passes: the second moment factor is7/6, inverse-square moment factor9/5, and Cauchy–Schwarz with the two-candidate maximum gives sqrt(21/5). Dependence of the two validation scores is harmless. The validation bank must be independent of candidate construction, and this lemma does not supply a good candidate.

Thus the weighted common-OPT ledger is disproved for this exact greedy learner, but actual coefficient risk still has the desired O(L) scaling on this family. Neither this counterexample nor the4L identity resolves unrestricted RE-02. Correctness and literature priority remain separate.
