# Prior-art refresh —25 October2026,21:09UTC

Correctness and novelty are separate. This targeted refresh is not an exhaustive literature review and does not establish priority.

## HSS / structured learning
[Amsel et al., Query Efficient Structured Matrix Learning, COLT2026](https://proceedings.mlr.press/v336/amsel26a.html), [arXiv v2 §3](https://arxiv.org/html/2507.19290v2#S3), Corollary1 gives a general q-dimensional linear-family approximation with approximately sqrt(q log(1/alpha))/epsilon² two-sided matvecs, up to logarithms, and error (3+epsilon)OPT+alpha||A||F. The paper explicitly distinguishes this from a pure relative-error result. For the forest and dense fixed-nested-basis classes, q scales with Nk, so this is not an O(k), N-independent, exact-on-model guarantee. It therefore does not directly subsume our restricted constructions or the current scalar fixed-basis target.

[Persson et al., A recursive butterfly factorization with optimality guarantees, v2](https://arxiv.org/html/2607.29361) treats a different complementary-low-rank family. Its main matrix-free result uses about sqrt(N) queries and an N^(1/4) Frobenius error factor; AppendixD improves the factor to sqrt(L), still using sqrt(N) queries. It builds on HSS/BLR² analysis but does not resolve RE02 or give the fixed-basis O(k) result. This is relevant technique/background, not an immediate shortcut.

The earlier graph-probing and stochastic-coloring sources in `hss_forest_audit.md` remain the more direct prior art for the coordinate forest lemma. No claim that the random-sign principle or coloring recovery is new.

## Quantum
[Aydin, Albert and Barg, PRXQuantum7,010341](https://doi.org/10.1103/kx3b-4nrp) explicitly relates spin, Fock and permutation-invariant codes using Jordan–Schwinger operators. The oscillator mapping is therefore established background. The specific codimension-one completion/gauge elimination must be assessed separately; no novelty claim is made.

[Elimelech, Aydin and Barg, Quantum10,2240,20October2026](https://doi.org/10.22331/q-2026-10-20-2240) gives asymptotically good multimode Fock families and related qudit PI families. Its asymptotic/growing-mode scope is not a resolution of the fixed eighteen-qubit distance-five problem.

## Deletion and C7
The fresh primary [TMLR submission search result](https://openreview.net/pdf/fc33f565559c14809d73e3d34147e9c1038dcfdc.pdf) still reports316 versus320 at length12. [Sloane's survey](https://neilsloane.com/doc/dijen.pdf) supplies established VT background, not the new restricted certificates' priority. Targeted searches did not locate the exact four-syndrome or whole-cell theorem, but this is weak negative evidence only.

The [Tandon companion repository](https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion) still reports its length500 lower bound3.258832620353... and cites the inherited BPZ/Gao line. Component unions, weighted Lovasz arguments and multilinear expansions are standard mechanisms. The particular finite deflation, exact all-tree envelope and rigidity realization require separate novelty review.

## Packing
Fresh searches did not locate a primary improvement superseding the supplied AH framework or the new exact value, but a rounded-decimal search cannot establish a record. Delayed NextFit closure, threshold charges, convexity and amortized quota offsets are familiar ingredients. The precise ported algorithm, constants and restricted charge-family optimality are the checked contributions to this investigation, not yet a literature-priority claim.
# Additional fixed-basis check,21:33 UTC

The published [COLT2026 paper page](https://proceedings.mlr.press/v336/amsel26a.html)
confirms the general roughly square-root-of-linear-family-dimension query bound.
The primary [Gallmeier–Otto paper, Theorem1](https://arxiv.org/html/2610.07513#S2)
gives expected projection-error factor d/(q−d−1) for maximum prescribed full
row-space dimension d. This is not automatically the local HSS rank k, and its
independent-row family need not enforce tied nested-basis coefficients. Hence
neither theorem immediately subsumes the audited 4k fixed-nested-basis result.
Targeted fresh searches found no direct match; this is not a priority proof.

