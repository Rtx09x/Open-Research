# Independent finite-subgroup construction gate

**PASS, 2026-10-26 02:49 UTC.** There is no finite subgroup (or translate)
of (R/Z)^5 with at least368 elements and toroidal minimum coordinate-max
circular distance at least2/7. This is a restricted construction-principle
exclusion, not a bound on arbitrary independent sets or Shannon capacity of C7.

`check_c7_abelian_subgroups_independent.py` is a separate standard-library
implementation with no proposer imports. It independently generates the44
noncyclic invariant-factor types of orders368..401, tests surjective and
no-surjective coordinate cases (88 jobs), and checks every character-cover
possibility using exact integer masks. It completed in45.8 seconds, with18
theta cases,21 missing-difference cases and49 full pair-cover enumerations.
The separate earlier cyclic gate and zero/repeated-coordinate treatment remain
necessary dependencies; this checker does not silently replace them.

## Completeness and normalization

Rounding each coordinate by floor(7x) sends any separated pair to a
nonconfusable C7 pair and is injective. Hence order is at most theta(C7)^5.
The independent rational Machin/Taylor bound verifies theta(C7)^5<402.
Each finite subgroup of five circles has p-rank at most5 for every prime,
so invariant-factor rank>5 is impossible.

A surjective character onto the exponent-e cyclic group splits: choose an
element mapping to1, necessarily of order e, and use kernel direct sum that
cyclic factor. Cancellation of finite abelian invariant factors identifies
the kernel with the remaining invariant factors. Thus a DOMAIN isomorphism
normalizes that coordinate to the last projection; permuting the five
coordinates is metric-preserving. No unjustified codomain row operations,
invertible coordinate-pair assumption, or universal full-order coordinate
assumption is used. When no coordinate is surjective, all five nonsurjective
characters are enumerated.

For a character of image order d, d/ceil(2d/7) is a fractional clique-cover
bound for its image confusability graph. If at most3, that coordinate together
with four rounded C7 coordinates gives at most3 theta(C7)^4<368. Thus removing
such a character from every candidate is safe, including zero coordinates.
Duplicate masks and repeated characters are harmless for existence testing.

For the remaining exponents satisfying3e<=10 ceil(2e/7), the checker verifies
every pair for the floor(10x/e) cohomomorphism. It independently derives the
three Fourier-mode theta dual on E(10/3): trace-normalized circulant variables
at offsets3,4,5 have objective1+20x3+20x4+10x5. Modes1,2,5 with the stated
positive Q(sqrt5) multipliers cancel all three coefficients and give
theta<=30-12sqrt5<16/5, whose fifth power is below336. No floating theta result
is trusted.

The remaining finite cover test is exact: after one normalized coordinate,
four character masks are two unordered pairs with replacement. Without a
surjective coordinate, enumerate one mask and two pairs. An inverted bit index
tests all possible partner pairs for every missing difference. The independent
implementation uses the opposite representative ordering g>=-g; no difference
class or repeated-character possibility is omitted.

## Scope

This closes exact finite-subgroup torus packings in dimension5 at threshold2/7,
including noncyclic groups and arbitrary coordinate characters. It does not
exclude near-packings below that threshold followed by nonlinear rounding and
completion, nonlinear unions of cosets, higher-dimensional subgroup codes, or
arbitrary physical C7^5 codes. It produces no capacity lower-bound gain and
makes no novelty claim for this finite exclusion or the established subgroup
construction principle.
