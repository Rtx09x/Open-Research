# What the remaining cover gap does—and does not—mean

## Exact diagnosis: the280 is a triangle-assignment deficit

Fix the audited pairing of133729 words in T(Z)\Z to distinct words of the
134753-word code Z. A missing core word c in I0²\(Z∪T(Z)) can join the clique
at z only if c is confusable with **both** z and its paired T(Z) word t, when
that partner exists. These are two physical constraints, not one deletion cost.

The5296 core words have a maximum matching of5016 into those fixed cliques.
A complete Hall witness consists of4272 core words U with exactly3992 eligible
cliques. Its deficit280 certifies that135033 is the best attachment cover for
this **fixed pairing**. It does not prove that135033 is the best possible cover.

The compatibility graph has203 components. Only30 core words have no eligible
clique at all; the other250 deficit units come from shared-clique congestion.
Four large components contribute184,22,22,18; the remaining34 consist of30
isolated core words and four small congested components. All156 lost candidate
edges at the30 isolated words fail the additional T-partner test in exactly
one five-coordinate half (76 first-half failures and80 second-half failures).

Independent advisor replay checked **every** original and filtered neighborhood,
the Hall dual, matching and all203 components. Files:

- `multireservoir_hall_diagnosis.json.gz`, SHA256
  `3fbd8a228a1830b23a1097c7976e7ababd6f668f16df8d84cd142fe522253ec8`;
- `diagnose_multireservoir_hall.py`, proposer1.96s/147MiB;
- `../../advisor/phase2/check_c7_attachment_hall_independent.py` and JSON,
  independent Hall replay0.55s after its own base reconstruction.

## Why this is not a280-word construction opportunity

The4272 words U have **5248 actual neighbors in Z**, not3992. The extra
T-partner requirement removes1256 available clique slots from their attachment
graph. Thus the true unfiltered deletion cost has surplus5248−4272=976 in the
wrong direction. Treating the filtered Hall deficit as a code gain would reverse
the meaning of the test.

Two minimal examples make the distinction concrete:

| Core words competing for one pair-clique | Compatible cliques | Actual Z-neighbor union |
|---|---:|---:|
| (6110,15371), (6110,16064) |1|9|
| (9512,13677), (12263,13677) |1|7|

Replacing the one compatible clique is not legitimate: the other Z words are
still physically confusable with the proposed core words.

## A targeted construction test, not a reservoir sweep

Force all4272 words U and remove their5248 actual Z-neighbors D. The independent
seed K=(Z\D)∪U has133777 words. Filter T(Z)\Z to words separated from every
member of U. Exactly112769 survive and20960 fail. On the surviving reservoir,
the remaining deletion-cost graph has3244004 edges and a112718-edge matching.
An exact Hall witness has53 reservoir words and2 additional Z deletions.

Therefore the **exact maximum retaining all U**, and otherwise using Z/T(Z),
is133777+51=**133828**. Of the51 surplus,50 are zero-extra-cost words and one
is a3-for-2 trade. This is925 below the existing134753 baseline. Reaching135093
with this seed would require surplus1316, not51—a shortfall of1265.

This decisively rejects using this particular Hall witness as a promising seed.
It does **not** reject other forced core subsets, other reservoirs, or the whole
unconstrained joint alphabet.

Files: `test_hall_shadow_seed.py`, `hall_shadow_seed_control.json.gz`,
`verify_hall_shadow_seed.py`, `hall_shadow_seed_audit.json`. The proposer ran in
3.74s/180MiB; the no-proposer-import literal verifier passed in about3s/178MiB.
No solver/floating-point optimality verdict is trusted. The certificate SHA is
`1e6c0136787701aa8ac1fc5b73e8ad932a6be814c5549aaadfa00913b72a28c1`.
Separate-agent audit also **PASS**,1.31s after its own base reconstruction:
`../../advisor/phase2/check_c7_hall_seed_independent.py` and matching JSON.
The three nonzero-cost selected words are(13358,9676),(13358,11980),
(13358,14233), replacing(13065,11685),(13065,14177) in the already punctured
seed. This local3-for-2 trade does not recover the seed's much larger loss.

## One falsifiable construction criterion for a genuinely different reservoir

Supply a physically independent reservoir Q—not merely a vector of family
cardinalities. Put S=Q\Z and form the **unfiltered** physical conflict graph
between S and Z. Let ν be its maximum matching size and δ=|S|−ν.

**Criterion: δ≥340.** This is necessary and sufficient for the single union
Z∪Q to contain an independent135093-word code. It is a finite sufficient target
for the working C7 rate3.258841, not a claim about the full capacity.

Proof/certificate: a matching gives |Z|+|S|−ν cliques. Alternating reachability
from unmatched S vertices gives L⊆S with exact neighborhood N_Z(L) and
|L|−|N_Z(L)|=δ. The literal code

    (Z \ N_Z(L)) ∪ L

has134753+δ words and is independent. The upper and lower witnesses coincide.
The construction score is the **actual shared-neighbor cost**, never the
triangle-attachment graph's filtered deficit. A smaller positive δ would be a
finite length10 gain only; it would not automatically improve the global bound.

### Resource-bounded executable test

`reservoir_escape_gate.py` accepts one explicit JSON recipe:

    {"name":"candidate_name","rectangles":[[[five-word integers],[five-word integers]], ...]}

Each factor must be an independent physical five-coordinate code. The checker
requires disjoint rectangles and separation of each rectangle pair in at least
one factor, so their union Q is provably independent. Its proposal routine uses
factorized neighborhoods; a candidate outcome is represented by exact matching
and Hall arrays, not a numerical optimizer status.

    timeout 285s python reservoir_escape_gate.py --recipe /path/to/recipe.json --output candidate_gate.json.gz

Operational caps: one CPU,1GiB,270 CPU seconds,12 rectangles,150000 reservoir
words,6000000 edges. A cap hit is inconclusive, not a failed construction theorem.
The no-argument run is a **diagnostic negative control**, Q=I0²:5296 outside
words,31792 edges, matching5296 and δ=0, exact maximum134753. It passed in
1.23s/123MiB. This independently falsifies reading the triangle deficit280 as
an available physical gain; it is not advertised as a new reservoir discovery.

### An even cheaper necessary novelty gate

The existing135033 cover implies that adding at most59 new physical length10
words to A=I0²∪Z∪T(Z) cannot reach135093, even at arbitrary macro-lengths.
For a larger independent Q, matching Q\A into compatible existing cliques gives
an exact extension upper135033+δ_attach. A prospective target-reaching Q must
have δ_attach≥60; passing this test is **not sufficient** for a construction.
After adding J, the135039 cover similarly requires at least54 new words beyond
the covered four-way alphabet. Small eight-swap perturbations cannot evade this.

## What input is actually missing

No candidate Q satisfying the constructive δ≥340 condition has been supplied
by this diagnosis. The remaining cover gap is predominantly lost triangle
compatibility, not a low-cost reservoir. A justified next experiment needs an
explicit independent Q (or a new separated-rectangle rule) designed to create
large **unfiltered** shared neighborhoods while supplying physically new words.
The bounded gate above can then accept or reject that concrete claim exactly.

This is not a declaration that all other reservoir combinations are exhausted.
For example, simultaneous uses of T²(Z) or the C30-flipped construction are not
excluded by the135033/135039 certificates. But their mere availability is not
evidence that another near-identical cover sweep will produce a construction.
The current global lower bound remains3.258832624235574872655, all external and
upload holds remain in force, and no publication priority is claimed.
