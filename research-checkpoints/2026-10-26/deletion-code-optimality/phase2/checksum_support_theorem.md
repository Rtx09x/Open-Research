# Seven VT checksum classes are necessary for a 317-word code

For a binary length-12 word, define

    sigma(x) = sum(i*x_i, i=1..12) mod 13.

**Theorem.** Every single-deletion-correcting code of size at least 317 uses at least seven distinct values of `sigma`.

**Improving-trade corollary.** Any improvement over `VT0(12)` must introduce words from at least six nonzero checksum classes, regardless of how many baseline words are removed. Otherwise the new code would lie in class 0 plus at most five other classes, contradicting the theorem.

Neither statement assumes complement/reversal invariance or proximity to VT0. They do not settle the unrestricted optimum.

## Exact proof

Fix any six-element syndrome support S. The certificate assigns nonnegative integer weights to received-word packing rows, or to valid word-conflict clique rows, with denominator M = 10^9. Every allowed word receives total coverage at least M. The total weight is strictly below 317 M.

A valid code uses each received word at most once and meets each conflict clique at most once. Summing the weighted inequalities therefore gives

    M * |C| <= certificate_total < 317 M,

so its integer size is at most 316. Every smaller syndrome support extends to a six-element one.

There are 1,716 six-element supports. Complement sends a support S to -S, preserving deletion conflicts. The 868 canonical representatives cover the whole family. The verifier explicitly checks complement on all words and deletion sets, checks complete support coverage, and checks every representative certificate with integers.

| Quantity | Exact result |
|---|---:|
| Representative certificates | 868 |
| Supports covered | 1,716 |
| Received-word covers | 866 |
| Clique covers | 2 |
| Word-coverage checks | 1,640,916 |
| Distinct referenced word cliques | 2,352 |
| Largest cover cost | 316.999169717 |
| Strict margin below 317 | 0.000830283 |

The largest certificate cost occurs on `{0,2,4,6,9,11}`. It is a certificate cost, not a claim that this is the unique hardest support or that its fractional optimum has been proved exactly.

Every support containing 0 has restricted optimum exactly 316, since it contains VT0. For supports excluding 0, this proof gives an upper bound of 316; it does not establish whether 315 or 316 is attained.

## Two independent proof directions

The track's standalone verifier reconstructs deletion sets by string slicing. A separate advisor checker independently reconstructed insertion incidence and verified all 868 certificates, all coverage inequalities, and every used clique. Both passed. The archived proof also passed a clean extracted replay under `python -I -S`, without numerical packages or any discovery code.

## Earlier five-class refinement

The preceding five-class sweep checked all 1,287 supports directly. Its largest cover cost was 316.156626280. All five-class supports excluding 0 had cost at most 315.48715498. Thus a 316-word code using at most five classes must contain a VT0 word. This does not prove five-class uniqueness at size 316.

Indeed, the received-word LP has an exact fractional packing of mass 316.139124714 on `{0,1,2,3,12}`. This blocks the naive extension of the four-class uniqueness dual argument, but is not an actual code.

## Why clique fallback matters

On `{0,1,2,3,5,12}`, an exact fractional received-word packing has mass 317.002534076. Existing word-clique constraints close that gap: an exact clique cover costs 316.189729881, proving the restricted integer optimum is 316. The all-six proof uses clique fallback on only two representatives.

## Scope

The unrestricted interval remains 316–320. No 317-word construction or unrestricted upper bound below 320 is claimed. The new support exclusion is established relative to this investigation; literature priority remains unverified.
