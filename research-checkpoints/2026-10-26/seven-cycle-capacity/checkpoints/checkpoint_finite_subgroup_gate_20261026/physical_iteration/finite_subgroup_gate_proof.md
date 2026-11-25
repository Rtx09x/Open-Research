# Dimension-five finite-subgroup torus gate

Status (2026-10-26): independent PASS: separate advisor standard-library implementation completed all44 types/88 jobs in45.8 seconds; cyclic gate separately independently audited. This is **not** an upper bound on alpha(C7^5), Shannon capacity, nonlinear rounding/completion, or higher-dimensional subgroup constructions. No capacity lower bound changes.

## Verified statement
There is no finite subgroup H of (R/Z)^5 with |H| >= 368 and with every nonzero h having a coordinate at circular distance at least 2/7 from zero. The same holds for a translate of such a subgroup because distances are translation invariant.

The group/lattice construction principle is existing work: Buys, Polak and Zuiddam, arXiv:2506.14654v1, Sections 1.3, 1.4 and 2.1. No novelty claim is made for the principle or this numerical exclusion pending literature review. Their Remark 1.4 already explains why subgroup independence can be weaker than ordinary independence.

## Finite reduction and permitted normalization
Coordinatewise rounding floor(7t) takes such an H injectively to an independent code in C7^5. Thus |H| <= theta(C7)^5 < 402. A rational check of this strict inequality is in `finite_subgroup_theta_reduction.py`; it proves the needed lower bound on pi using the alternating Machin series rather than trusting floating point. Only orders 368 through 401 remain.

Every finite abelian group has a unique invariant-factor decomposition Z_(d1) x ... x Z_(dr), with 2 <= d1 | ... | dr. Its exponent is e=dr. Every character into R/Z has image in e-th roots and has coefficients a_i(e/d_i) modulo e. A subgroup of five circles has at most five generators: the p-torsion dimension is at most five for every prime p. Thus r>5 is impossible.

If a coordinate character is surjective onto Z_e, choose g with character(g)=1. Then g has order e, splits the character, and H is isomorphic to ker(character) x Z_e. Finite abelian cancellation identifies the kernel with the other invariant factors. A DOMAIN isomorphism therefore normalizes that coordinate to the final projection. No mixing of codomain coordinates is permitted. If no coordinate is surjective, all five characters must have image order below e and are enumerated without that normalization. In particular, having a globally invertible coordinate pair is NOT assumed.

## Exact character screens
Write k=ceil(2e/7). A difference g is separated by a character if its residue has circular distance at least k. For a character whose image has order d, its actual one-coordinate induced confusability graph is E_(d/ceil(2d/7)). Consecutive ceil(2d/7) residues give a fractional clique cover of total d/ceil(2d/7). If this is at most 3, any five-coordinate code using the character has at most 3 theta(C7)^4 < 368 words. These characters can safely be discarded. The script verifies the last inequality with an elementary rational cosine upper bound.

If e/ceil(2e/7) <= 10/3, the script checks literally every pair for the map t -> floor(10t/e) into E_(10/3). `theta_10_over_3_exact.py` verifies a nonnegative Fourier dual with exact Q(sqrt(5)) arithmetic, proving theta(E_(10/3)) <= 30-12sqrt(5) < 16/5 and hence fifth-power independence <368. This screen applies even to nonlinear codes at those exponents.

## Enumeration
`abelian_torus_gate.py` generates all 44 noncyclic invariant-factor types with orders 368..401 and rank 2..5. It tests both surjective and no-surjective cases, for 88 jobs. Two higher-rank types of order384 are separately ruled out by the rank condition.

Each nonzero difference is identified with its negative, which does not change circular-distance separation. Each character becomes a bit mask of separated differences. Duplicate masks may retain one witness because only existence is in question. Repeated characters are allowed.

In the surjective case, the fixed projection already separates differences with |g_r|_e>=k. The remaining four masks cover the residual differences iff a union of two masks and a second union of two masks cover them. In the no-surjective case, enumerate one character plus two such pair unions. All unordered pairs with replacement are considered. An inverted bit index intersects exactly the candidate pair unions covering each missing difference; a zero intersection certifies no completion. No heuristic pruning, solver infeasibility, or floating point is used.

Results: 49 exact pair-mask enumeration jobs; 21 jobs where even the union of all allowed character masks misses a difference; 18 exact theta-screen jobs. No witness. Total proposer replay 47.58 seconds, peak14,784 KiB. The JSON records exact counts and missed differences.

Cyclic groups are covered by the previously independently audited `cyclic_multiplier_gate_proof.md`, `cyclic_multiplier_bitset_audit.json`, and advisor's separate implementation over all 211 unit/no-unit cases. That proof includes zero-coordinate replacement, signs, and repeated coordinates. Combining the two exhaustions and the finite reduction proves the stated construction-family exclusion with the independently completed replays.

## Reproduction and stopping boundary
Run `python physical_iteration/theta_10_over_3_exact.py`, `python physical_iteration/finite_subgroup_theta_reduction.py`, and `python physical_iteration/abelian_torus_gate.py` from the project directory. The general gate hard-limits one CPU, 1 GiB, 270 CPU seconds and checkpoints below five minutes.

A genuinely new remaining route is a near-packing subgroup at distance slightly BELOW 2/7 followed by nonlinear coordinate rounding, deletion and completion. Such a result is NOT ruled out here. Another is a higher-dimensional subgroup. A physical code must always be checked on literal C7 coordinates before reporting a gain.
