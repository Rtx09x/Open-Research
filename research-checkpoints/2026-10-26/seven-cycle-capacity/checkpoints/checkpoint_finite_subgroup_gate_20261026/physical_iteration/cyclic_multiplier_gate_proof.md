# Finite obstruction to direct rank-one circular constructions

**Scope:** for each integer368≤n≤401, no vector a∈Z_n^5 produces a rank-one
cyclic code `{t a : t∈Z_n}` with minimum cyclic L∞ distance at least
`k=ceil(2n/7)`. This is a finite computational statement, not an unrestricted
C7^5 upper bound. It does not exclude rounding followed by deletion and
completion, nonlinear circular codes, or general physical code constructions.
No publication priority is claimed.

The approach follows the circular-code motivation of Polak–Schrijver,
[arXiv:1808.07438v2](https://arxiv.org/html/1808.07438v2), while testing arbitrary
five multipliers rather than only geometric powers. The positive control
recovers their382-point/distance108 template up to coordinate signs and order.

## Exact reduction

For any vector a, all pair differences are `t a` for nonzero t modulo n.
Thus the required condition is

    for every 1≤t<n, some coordinate aj satisfies
    min(aj*t mod n, n-(aj*t mod n)) ≥ k.

Signs preserve these distances, so multipliers can be restricted to1,…,floor(n/2).
Likewise only1≤t≤floor(n/2) must be checked. Zero coordinates can be replaced
by duplicates of nonzero coordinates without reducing distance; duplicates
are allowed in the search. A feasible code necessarily has a nonzero coordinate.

If some coordinate is a unit modulo n, reparameterize t by its inverse and
permute coordinates so that the first multiplier is1. If no coordinate is a
unit, choose a nonzero coordinate with gcd g>1. Multiplication by a suitable
unit reparameterizes it to g. For every n and every possible nonunit residue,
the checker explicitly verifies existence of such a unit. All other coordinates
remain nonunits. Enumerating every proper divisor g arising from a nonzero
residue therefore covers all no-unit cases, even if this repeats some orbits.

Fix the first multiplier. Delete the t values it already separates, and for
each allowed remaining multiplier a form the bitset of residual t values it
separates. Four remaining coordinates suffice exactly when two unions of two
such bitsets cover the residual universe. Repeated choices are allowed.

## Two algorithms

`cyclic_multiplier_gate.cpp` tests all unit-normalized cases by direct
meet-in-the-middle pair-union comparison. Its complete34-case output is
`cyclic_multiplier_gate.jsonl`.

`check_cyclic_multiplier_gate.py` does not import or trust that output. For
each residual t, it forms the bitset of pair-unions covering t. For every first
pair-union, intersecting these bitsets for all still-uncovered t gives exactly
its possible partners. Every such intersection is empty in all target cases.

The Python run covers34 unit cases and177 no-unit normalization cases,211 total.
It also verifies a positive control at n=382,k=108, returning
`[1,7,39,49,109]`; thus it does not merely reject every instance. All finite
normalization checks pass. Runtime41.63seconds,13MiB, oneCPU.

Reproduce (Python standard library only):

    python check_cyclic_multiplier_gate.py

Result: `cyclic_multiplier_bitset_audit.json` has `complete_range=true` and
`all_target_cases_infeasible=true`. A separate advisor subsequently rewrote and
replayed all211 cases with no worker imports: PASS42.99seconds/14.6MiB. The
advisor also independently classified all382-point templates at distance107:
only(1,7,39,49,109), whose actual minimum distance is108; all no-unit cases are
empty. Advisor source files are check_c7_circular_range_independent.py and
check_c7_circular382_independent.py under advisor/phase2. Publication priority
remains unestablished; the scope does not expand beyond rank-one circular codes.

## Consequence and remaining route

Distance k≥2n/7 permits the direct map `i↦floor(2i/k)` into seven symbols,
preserving nonconfusability. The finite obstruction rules out this sufficient
direct construction in the stated cardinality range. It does **not** prove
that every successful rounding must have that global circular distance: phase
choices, nonuniform partitions, and subsequent deletion/completion may repair
short circular separations. Near-threshold arbitrary multiplier templates are
therefore still a legitimate constructive route.
