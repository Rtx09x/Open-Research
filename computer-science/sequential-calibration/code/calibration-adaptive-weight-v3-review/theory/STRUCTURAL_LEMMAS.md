# Exact SPR groundwork and rejected three-way premise

These are structural checks, not claims to have resolved the calibration rate or established priority.

## Signed-subset monotonicity and deletion dominance

For boards B,A with B a signed subboard of A, `V_h(B)<=V_h(A)` for every remaining horizon h. Prove this by induction on h, with horizon monotonicity from the pointer's stop option.

For a request j that is empty in both boards, copy A's minimizing response in B, intersecting its deleted subset with B; the successors remain nested, so the induction applies. If j is empty in B but occupied in A, put A's sign at j and delete nothing; this gives B' subset A and

    V_(h-1)(B') <= V_(h-1)(A) <= V_h(A).

The stop alternative is bounded by `|B|<=|A|<=V_h(A)`; a full A has value n and is trivial. The horizon-zero case is sign count. Therefore the maximization over pointer responses preserves the inequality.

For each chosen sign, the successor deleting all eligible signs is a signed subboard of every partially deleting successor with that same sign. Hence all-delete is weakly optimal at every request and horizon. The exact solvers enumerated ALL subsets before this lemma was used.

## Normal form and one-sided erasure

After an all-delete response at j, every survivor to its left is plus and every survivor to its right is minus. Whichever sign is placed at j, all surviving pluses lie left of all surviving minuses. This holds after every move starting from the empty board.

Consequently an eligible minus left of j and an eligible plus right of j cannot coexist: their ordered positions would exhibit a minus left of a plus. **A request in normal form erases at most one sign type.** In particular, a middle-block request cannot simultaneously achieve the tempting two-sided clearance of left-block minuses and right-block pluses. The initial three-way prompt overlooked this joint-realizability restriction. The adaptive-binary theorem does not use it.

This does not say ternary recursion is impossible. It says a proof must track the frontier/visit-order state or exploit something other than that false simultaneous-erasure gain.

## A precise outer-only barrier for a naive ternary family

Consider a recursively ternary strategy on n=3^d cells with these restrictions:
- Each parent initially sends requests to three equal child intervals with the same weight/bias as the parent.
- Until the middle child has been visited, it performs no bias change, regrouping, or parent-level restart.
- The one-cell sign is a fixed function of the inherited weight/bias.

Pointer visits only leaves whose d ternary digits are 0 or 2. No middle child is ever visited at ANY scale. There are 2^d such leaves; all inherit the same bias and return the same sign. Visit them in increasing order if that sign is plus, decreasing order if minus. No sign is erased, and the board is not prematurely full. Pointer therefore retains 2^d signs in 2^d requests.

Any uniform guarantee `C*n^alpha*t^beta` for this restricted family must satisfy

    alpha*log(3)+beta*log(2) >= log(2),

or equivalently `alpha >= (1-beta)*log_3(2)`. This is an actual adversarial transcript family, not a finite exponent fit. It does NOT apply to strategies with an outer-only fallback, different inherited child weights, adaptive regrouping, or other excluded state changes.

Example for n=9: request cells 1,3,7,9 in that order when the fixed leaf sign is plus. Every response is plus, every cell remains occupied, and the middle child at each relevant scale is avoided.
