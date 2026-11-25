# Independent audit: actual fixed-algorithm packing floor

**PASS, 2026-10-26 02:43 UTC.** This is an algorithm-specific asymptotic lower
bound, not a lower bound for all online bin-packing algorithms.

The fixed phase4 two-coordinate BF/AH variant has ratio at least
`1.5782054112079646...`, compared with its audited upper
`1.5782055179987482...`. The exact remaining window is
`244214804051211930109591/2286852816926276513629309223262`
(approximately `1.0679078349233566e-7`).

## Independent checks

`check_packing_actual_floor_independent.py` imports no worker code or analysis
weights. It reconstructs the six relevant parameter rows literally, compares
them with the frozen algorithm table (SHA256
`c8559b05ef4fd6373ad391504fc93d931651ea550ab61c998eb4f0ebe52868bd`), and derives
positive-container rates. The resulting exact lower bound agrees with the
worker certificate SHA256
`75eb8252024061302c16ce52a1f4faeefa4be626cb8875cc18e5c7a190b75dd6`.
Final prose including the four-hypothesis architecture corollary and explicit
parameter-change escape scope was read and approved at02:49 UTC, SHA256
`c89bb1a0427e6c0a3444197a3489f68780a8838a124c18ef98561f093f9b6d34`.

At fixed tau=1e-9, the seven rational item sizes lie in their claimed classes
and sum to exactly one. N copies therefore have total volume N and an explicit
N-bin offline packing: OPT=N, with no limiting perturbation argument.
The two tiny capacities hold at most596 and2106 identical tiny items.
Their quota-weighted mean is
`K=47899435362138/32568497273`.

The large class165 is handled separately: source Lemma5, Corollaries6 and8
give its positive-pair count at least
`(56035901/134217728)N-2`, including temporary/declared containers.
For every relevant small class, the quota discrepancies and cardinality
capacity give the stated positive-rate lower bound even if the last container
is unfinished. Huge items each contribute a positive container. The source
architecture places at most one advertised positive container per bin, so
unmatched negatives cannot invalidate the lower bound. These same source
invariants were independently checked in `packing_saturation_audit.md`;
the construction itself is different and does not transfer its one-open
execution assumption.

The independent checker also simulates all-prior-container Best Fit on every
prefix of120000 identical tiny arrivals, checking exact capacity, quota and
finite lower inequalities. This is a control, not the all-N proof. The proof
uses N<=K*m+1510 and n_positive>=beta*m-1; combined with the small/large-class
constants this gives the stated uniform additive constant. Taking arbitrary
N to infinity proves the asymptotic floor.

## Stronger, precisely conditional architecture consequence

For the lower inequality, Best Fit and chronological one-open behavior are
unnecessary. Any policy with these same fixed tiny capacities and bounded
type-count discrepancies has N<=596*n1+2106*n2=K*m+O(1), even with multiple
open containers. If it also retains the same positive-container proportions,
non-tiny positive-count invariants and at-most-one-positive-per-bin rule, the
same lower bound follows. Reordering, tie-breaking or changing eligibility
alone cannot beat this floor under those hypotheses. Altered capacities,
proportions, container accounting or non-tiny architecture are not covered.

Consequently, further analysis alone of this fixed algorithm can improve its
upper bound by at most the displayed window. This is not exact algorithm
tightness, a universal lower-bound improvement, or a full-gap solution.

Primary source for container invariants:
[Balogh et al., A New and Improved Algorithm for Online Bin Packing,
Sections3 and5](https://arxiv.org/html/1707.01728).
