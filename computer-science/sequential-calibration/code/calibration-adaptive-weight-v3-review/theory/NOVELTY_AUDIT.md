# Focused primary-source comparison — 26 October 2026

## Finding

The adaptive continuation factor `q(z,r)` in `ADAPTIVE_Q_THEOREM.md` is **not the fixed-bias-shift algorithm specified in the inspected source versions**. The mathematical novelty supported by this comparison is the changed epoch transition and its uniform sufficient inequalities, not replacing integer notation by real weights alone. No comprehensive priority claim follows from this focused audit.

## Versions directly checked

The live arXiv abstract pages report Dai–Fishelson latest v2 (8 October 2026), Dagan et al. latest v4 (16 September 2026), and Zhang latest v1 (14 July 2026). Earlier complete HTML snapshots were directly downloaded and their algorithm/analysis sections inspected. The source versions and public links are listed in `../SOURCES.md`; full third-party source snapshots are intentionally not redistributed in this review package.

1. **Dai–Fishelson 2610.07623v1 and v2.** Both specify integer bias b, half children at the same b, and a same-interval continuation at b+1 or b-1 according to trigger orientation. A single global lambda converts those integer shifts into multiplicative type-wise bounds. The continuation length is floor(kappa*h), and the global six-tuple is optimized in Remark 6.2 of v2. Their per-trigger inequalities use the same lambda at every trigger. No state-dependent magnitude or function of z,r was found in the algorithm, admissibility definition, parameter optimization remark, or appendix verifier. Our q is not constant: at the chosen parameters it equals 1/2 on some trigger states but is about .754663 at (z,r)=(14.8,1). Thus no single lambda reproduces this transition rule.

2. **Dagan et al. 2406.13668v1.** This June 2024 version has the earlier title *Improved bounds for calibration via stronger sign preservation games*. Its abstract states the SPR equivalence and improved lower bound, but leaves improving the SPR upper bound as the route to beating 2/3. It does not contain the later recursive upper-bound algorithm whose bias could subsume the proposed rule.

3. **Dagan et al. 2406.13668v2,v3,v4.** Their four-phase recursive upper-bound algorithm uses integer b and a fixed unit shift when the relevant child is reinitialized (Algorithms 3–4 in the versions inspected). The analysis uses one global lambda and uniform type-wise bounds proportional to lambda^(±b). Their traffic-dependent *timing* of reinitialization is a precursor and must be credited; it does not choose the *magnitude* of the bias shift as our q(z,r) does. Direct searches for real/continuous/variable/state-dependent bias were supplemented by reading the displayed initialization, phase transitions, induction statement and parameter proof, not used as standalone absence evidence.

4. **Zhang 2607.12928v1.** Appendix/algorithm listing explicitly reproduces Dagan's A/B labeler with integer bias, fixed b±1 shifts, and combines SPR calibration with an outer correction algorithm. It is relevant to efficiency but does not state our adaptive continuation rule or the prospective explicit exponent. No claim is made here that our sharper nonconstructive minimax bound is automatically achieved by Zhang's efficient forecaster.

## Broader search limitation

A targeted web search for SPR with state-dependent, variable or real bias did not identify another primary source containing this rule. Search retrieval was noisy, and this is **not exhaustive literature clearance**. Other manuscripts, unindexed work, unpublished ideas, or independent discoveries could exist.

## Comparison and scope if the proof is accepted

The resulting exponent is `20423/30846 = .6620955715489852...`, compared with the printed `.662942288` upper bound, a reduction of about `.00084671645`. The classical 2/3 baseline is not the correct comparator for novelty. The lower bound `.54389` remains far below this upper bound; the minimax problem is not resolved. Constants are large (`F=10^10` in the clean certificate), so this is asymptotic existence work, not a demonstrated practical finite-horizon forecast improvement.

## Direct links

- https://arxiv.org/abs/2610.07623 ; https://arxiv.org/html/2610.07623v1 ; https://arxiv.org/html/2610.07623v2
- https://arxiv.org/abs/2406.13668 ; https://arxiv.org/html/2406.13668v1 ; https://arxiv.org/html/2406.13668v2 ; https://arxiv.org/html/2406.13668v3 ; https://arxiv.org/html/2406.13668v4
- https://arxiv.org/abs/2607.12928 ; https://arxiv.org/html/2607.12928v1
