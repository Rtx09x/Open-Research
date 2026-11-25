# Actual fixed-algorithm tightness: independent audit

**Status: analytic audit PASS, 2026-10-25 21:30 UTC.** The audited object is
`online-bin-packing/phase2/coupled/SATURATION_THEOREM.md`, not a universal online
bin-packing lower bound. Together with the separately audited all-input upper
theorem, it fixes the delayed-tiny three-transfer variant's asymptotic ratio at

23211234258164394107066141961880719040528132151 /
14707121654123980930208343329037931077093556224
= 1.5782309281201736… .

## Checks independent of the upper-bound LP

1. The two offline patterns have exact residuals p=997/2100120 and q=29/1254.
   Their non-tiny sizes are perturbed above open class endpoints by rational
   τ>0, with pτ=p−6τ and qτ=q−4τ. All claimed classes persist for τ≤10^-6.
2. The tiny prefix starts each quota-selected container of capacity A with qτ,
   then adds fillers totaling A−2qτ+τ. Its final load A−qτ+τ is below A, but the
   next qτ exceeds A by τ. Thus the prefix realizes precisely the intended
   deterministic quota sequence; matching cannot change that sequence.
3. Common refinement of the online filler intervals with offline intervals of
   length pτ produces positive finite filler items, each at most pτ<1/43.
   With nP=ceil(F/pτ), the offline packing has N=nP+m bins and total volume
   N−σ, 0≤σ<pτ<1. Therefore OPT=N exactly, including σ=0.
4. A bin contains at most one advertised positive container. Small-class quota
   discrepancies and maximum items per container therefore give a lower bound
   on actual cost even if containers are unfinished. Class165 is not treated
   as a small class: source Lemma5/Corollaries6 and8 explicitly cover its
   temporary/declared type changes and imply positive count at least
   α2 N165/(1+α2)−2. Tiny positive count is at least bm−1; huge items each give
   one positive container. No assumption that negative containers all match
   is required.
5. Independently reparsed primary parameters give exact limiting identity
   R=((B−2q)Kp/p+Kq+b)/((B−2q)/p+1); see
   `packing_saturation_algebra.json`. It is not inferred from dual equality.
6. At each fixed rational τ, m can tend to infinity, suppressing quota and
   ceiling constants. Then rational τ→0 gives R. For every ε>0 this supplies
   arbitrarily large OPT with ratio at least R−ε, which defeats any fixed
   additive competitive constant. The instances need not be prefixes of one
   infinite input.

The worker's integer-scaled finite trace checker validates the tiny/refinement
execution, not a complete AH simulator. The cost conclusion rests on the
source's all-input container invariants. These are distinct evidence layers.

**Consequences:** stronger accounting alone cannot improve this fixed variant.
A new upper-bound improvement needs an algorithm change. This does not improve
the universal lower bound, solve the full gap, or establish literature priority.

Primary source: [Balogh et al., A New and Improved Algorithm for Online Bin
Packing, Sections 3 and 5](https://arxiv.org/html/1707.01728).

## Narrow architecture corollary
The construction also applies to deterministic causal tiny type-order policies
with the same capacities/proportions, bounded quota discrepancy, one open
delayed-closure container, and the same non-tiny positive-count invariants.
After inferring each selected type, the adversary chooses its filler total and
cuts against a running pτ budget. This adaptive description can be unrolled into
a fixed finite input for a deterministic algorithm. Thus merely changing matching
priorities or bounded-discrepancy type order cannot help if the stated invariants
are retained. Randomized policies, altered quotas/capacities, and multiple-open
tiny algorithms are outside this corollary.
