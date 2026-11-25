# Explicit induction domain: externally erased owned-cohort traces

**Clarification of the frozen v2 proof domain, not a change to its algorithm, parameters, or calibration model.** The phrase “uniformly over allowed surrounding histories” must be interpreted and proved as below. It is NOT justified by asserting that arbitrary extra erasures can only help the entire future game, nor by invoking the ordinary SPR value on a child after that child was full.

## 1. Subroutines are not independently terminated SPR games

Only the ROOT is played in the original SPR game. That game stops when its whole board is full, when Pointer stops, or at its horizon. An internal A instance is a persistent labeling subroutine with counters and an interval, not a separately terminated SPR game. Its code contains no “terminate when locally full” step. It can receive another call after signs in its interval have been erased by activity outside that instance.

For an A instance J, call a physical sign J-owned if its placement was the returned answer to a request processed by J (including a descendant). A sign can be owned by every ancestor on its answer chain. Within one parent's analysis, its earlier-epoch cohort, the two current phase-one child cohorts, and the current continuation cohort are disjoint by their placement requests. A sign predating J's initialization is foreign to J, even if it lies in J's interval.

## 2. Extended local trace class E(I,w)

An instance starts with its normal initialized algorithmic state, weight w, zero answered requests, and NO owned signs. Foreign signs need not be absent physically.

A finite trace can interleave:

1. **External erasure:** remove any subset of the currently owned signs. This changes physical owned inventory but not the instance's internal counters, weights, or recursive state. It never creates an owned sign.
2. **Local request at j in I:** j must be empty of J-owned signs. Delete every J-owned minus left of j and every J-owned plus right of j, execute J.label(j), and insert its returned sign at j as J-owned. Increment the same internal counters as the algorithm specifies.

Every finite prefix is allowed, including a prefix with a full owned board. A full owned board admits no further request until an external erasure frees a cell. There is no mandatory local termination. Foreign signs may additionally prohibit requests in a real global execution, but that restriction is not needed in this enlarged class. We do NOT permit overwriting an occupied owned cell.

The strengthened inductive assertion is exactly:

    For every trace in E(I,w), at every prefix after t local requests,
    remaining_sigma(J) <= C*w^sigma*|I|^alpha*t^beta.

The inherited epoch invariants count only J-owned signs. They do not bound arbitrary foreign signs at time zero.

## 3. Projection lemma

The actual global execution projects into E(I,w) for every instance J.

- Every request sent to J selected a globally empty cell, hence a cell empty of J-owned signs.
- Global all-deletion removes every eligible J-owned sign before that placement. It is exactly the local request deletion operation on the owned subset; deletions already performed can be regarded as idempotent.
- A global request not handled by J can remove some J-owned signs, but cannot create a J-owned sign. Model this as an external erasure event. Foreign placements do not alter the J-owned board.
- J.label and its counters are persistent across these events. Local fullness is not an algorithmic termination condition.

The same projection holds from a parent trace in E(I,w) to any half child or continuation child: erase events of the parent and requests handled by other children become external erasures; each child-handled request is empty of its owned signs and has the required eager deletion. This recursive closure is what permits the induction. It is proved from the event definition, not from a standalone SPR theorem.

## 4. Direct induction over E, including full-and-resume traces

Run the frozen proof's outer induction on interval size and strong inner induction on LOCAL answered-request count over this extended class. No appeal to the minimax value of a child is made.

### Base cases

For t=0 there are no owned signs. For one cell, owned occupancy is at most one even if the cell has been filled, externally erased, and requested repeatedly. The returned sign is fixed by w, so any surviving type has w^sigma>=1. This uses occupancy at a prefix, NOT an assertion that a leaf gets at most one call.

For t<=F, the returning-chain weight/count argument uses all calls actually processed by each persistent instance. External erasures neither change its weights nor erase its counters. Half-child calls decrease size; same-size continuation calls have the frozen factor-two count reduction because kappa<=1 in v2. Thus the frozen w^sigma>=1/t small-time proof remains valid on E. Full-and-resume histories do not alter it.

### Inherited cohorts and epochs

At the first visit to the left half, all old right-half pluses are removed; at the first right visit, all old left-half minuses are removed. Additional erasures may remove more owned signs but cannot restore a removed cohort sign. Once both halves have been visited, inherited signs are therefore persistent. The right triggering request removes every minus placed by the left phase-one child, and the reflected assertion holds for a left trigger.

Apply the size induction to actual half-child traces in E, and the time induction to actual continuation-child traces in E. Earlier external erasures and later resumption are already among the quantified histories. Combine their owned counts with the disjoint old cohort to obtain precisely the three frozen inventory envelopes. Every algebraic inequality in the completed-epoch proof then applies unchanged, restoring inherited Kp/Kt budgets at the next epoch.

### Unfinished phases and terminal prefixes

One-half-only, both-half phase one, and continuation cases depend only on those inventory envelopes, request counts and trigger timing. They do not assume the local owned board was never previously full. Every resumed call is charged in the count t.

For the continuation's low sign, the hypothetical endpoint f(L)<0 is still a scalar consequence of the certificate and rounding. The induction hypothesis is used only at the actual child count c. No future extension of a full owned board is assumed.

The same strict live inequality closes the E-domain induction. Arbitrary erasures after a prefix can lower its owned count; if future requests follow, their count increments and recursive evolution are handled by the same proved assertion. This last statement is the conclusion of the induction, not a shortcut assuming erasures cannot benefit a future adversary.

## 5. Restriction back to the original game

The root actual history is a special case of E: no foreign placement is counted and no additional arbitrary erasure is required. Original root termination on a full board is preserved exactly. Since every actual root prefix satisfies the bound, Pointer's stop and horizon termination do as well. The extended child proof domain does not replace the user's calibration metric or allow illegal moves in the claimed original game.

## 6. Verification boundary

The frozen proof already states uniformity over surrounding histories and counts owned signs; the expanded definition above makes the required stronger domain explicit. It should be reviewed as a direct strengthening of the inductive quantifiers, not described as a result inherited from ordinary SPR optimality. No numerical certificate changes are needed. Independent review should check the projection lemma and every inventory envelope in this domain.
