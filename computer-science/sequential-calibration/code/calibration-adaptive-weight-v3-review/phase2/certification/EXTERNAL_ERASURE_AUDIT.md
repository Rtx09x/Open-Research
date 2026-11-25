# Independent hostile audit: external erasures and resumed local boards

**Verdict: PASS for the explicit extended-trace induction in the v3 draft.** No algorithm, parameter, numerical inequality, constant, or exponent changes are required. The clarification is necessary: applying only the ordinary standalone SPR theorem to a locally full child would be invalid. The stronger statement is instead proved directly below and in the audited addendum.

Audited files are `theory/phase2/v3_draft/ADAPTIVE_Q_THEOREM.md` and `EXTERNAL_ERASURE_INDUCTION.md`. Their exact hashes are recorded in `external_erasure_audit.json`. The frozen v2 release is not edited. This review concerns its existing factor-two/`kappa<=1` construction; later no-floor and oriented-startup research is separate.

## 1. Why the concern is real

Ordinary SPR on a one-cell board ends after its first placement. A persistent one-cell labeling subroutine may nevertheless be filled, erased by an outside request, and called again. Thus its local call sequence need not be a legal nonterminated standalone SPR play. Neither ordinary minimax optimality nor a claim that extra erasures strategically help a fixed history-dependent algorithm establishes the required child bound.

The draft now treats internal instances as persistent label oracles. Only the actual root game has mandatory full-board termination. This matches the existing runtime implementation: `A.label` has no local-full termination branch, and external deletion does not reset counters or weights.

## 2. Exact projection proof

Annotate each newly placed sign-token with all instances on the answer chain that produced it. A token is owned by each of those instances. Erasing a token removes it, including all its ownership annotations; an erasure does not merely remove one ancestor's ownership label.

For a fixed instance J, project the parent/global event sequence as follows.

1. A parent erasure removes the intersection of its erased tokens with J-owned tokens. It inserts none and changes no J controller state.
2. A parent request routed through J selects a parent-owned-empty cell. J-owned tokens form a subset of the parent's tokens, so the cell is J-owned-empty. The eager parent deletion, restricted to J's interval and owned tokens, removes exactly the eligible J-owned minuses/pluses. The returned sign is annotated as J-owned. This is one legal J local-request event.
3. A parent request not routed through J can delete J-owned tokens, but its new token lacks the J annotation. It is therefore only an external-erasure event in the J projection. The new sign is foreign to J and may be ignored by J's owned-board model.
4. A newly initialized half child or same-interval continuation starts with no tokens bearing its new identity, even when its interval contains surviving parent/ancestor tokens. Those foreign tokens do not enter its time-zero inventory.

These steps prove recursive closure from an arbitrary parent extended trace, not just from an ordinary root game. A child's projection may repeatedly become full and later be externally erased; its next request is still owned-empty. Any foreign occupancy that would prohibit a real request only restricts the actual global histories further. The enlarged local class may ignore that prohibition without weakening an upper bound proved over the entire enlarged class.

## 3. Direct induction in the enlarged class

The asserted bound is quantified over every finite extended trace, every positive weight, and every prefix with t answered local requests. Between requests, arbitrary external erasures remove owned tokens but do not create owned tokens or alter controller state. The proof is an outer induction on interval size and a strong inner induction on answered local requests, NOT an induction using ordinary child-game values.

### Base cases

- At t=0 there are no owned tokens, regardless of foreign occupancy.
- A one-cell instance has at most one owned token at any prefix. It may have answered many calls; the fixed leaf weight selects the same eligible sign type each time, with `w^sigma>=1`.
- For t<=F, choose a past request that returned the surviving sign type. Evaluate all answer-chain counts immediately after that request. Same-size continuation counts still halve along weight-changing edges because frozen v2 has `c<=L<=h`; neutral half-size edges do not increase counts. External erasures have not reset any counter. Hence `w^sigma>=1/s>=1/t`, where s is that past parent count. At most t owned placements exist, so `C>=F^2/Kp` gives both the ordinary and stronger inherited small-time bounds.

### Recursive hypotheses and epoch inventory

The projection lemma supplies a genuine extended trace for every half child and continuation child. Half children have smaller intervals. A same-size continuation has actual answered count `c<tau+h+l+c<=t`, since a trigger has visited both halves. Therefore its strong-time hypothesis is available even after prior local fullness or external erasure.

Within the parent, earlier-epoch tokens, tokens placed by the current half children, and tokens placed by the continuation are disjoint cohorts of placement events. Ancestor/descendant ownership of the same token does not cause double counting, because the parent sums only these disjoint top-level cohorts.

First visits and trigger deletions remove the same old cohort types as in the original algebra. No erased token can reappear: a later reused-cell placement is a new token in the new cohort. The three inherited/child/continuation envelopes therefore follow from the actual child hypotheses with precisely the old coefficients.

### Closing inherited and live bounds without circularity

Inherited budgets are propagated by induction over completed epochs. At a completed endpoint u, their proof uses the already established prior-epoch budget, smaller-space child hypotheses, and a same-space continuation count strictly below u. Even if u equals the parent t currently being proved, it does not use the desired parent bound at u. Small completed epochs use the separate chain base case.

The one-half, two-half waiting, and unfinished-continuation inequalities then use only these inventory envelopes and counters. None assumes that the local owned board has never been full. For the low sign in continuation, the comparison with `f(L)` is algebraic in frozen counts; the child hypothesis is invoked at the observed c only. It does not ask a full local or root board to continue illegally.

The same certified strict live inequality closes the request-prefix bound. An erasure-only prefix immediately afterward has no more owned tokens. If a later request becomes possible, its counter increment and recursive behavior are covered by the assertion for that larger t. This handles future consequences of erasure through universal quantification, rather than assuming they strategically help.

## 4. Root restriction and unchanged result

Actual root histories form a subclass of the extended traces and have no owned placements outside root responses. The root still terminates on its first full board, pointer stop, or horizon. The proved prefix bound therefore applies to every legal original stopping condition. No augmented-game payoff or calibration-model change is substituted.

The v3 draft needs exactly the existing v2 scalar/continuum certificate, `C=F^2/Kp`, and exponents `alpha=51/5000`, `beta=379/400`. The invoked transfer still yields `20423/30846`. No finite test is used to establish this uniform implication.

## 5. Independent operational controls

`check_augmented_projection.py` uses the actual exact-rational v2 runtime, annotates placements by their actual answer chains, and exhaustively explores every external-erasure subset and legal next empty cell to depths `(n,t)=(1,6),(2,6),(4,4)`.

- 3,111 augmented transitions checked.
- 9,063 local projected response events checked against exact eager owned deletion plus one insertion.
- 13,682 events outside a given instance checked to make no owned insertion and no counter change.
- 1,058 calls occurred after that same instance had previously been locally owned-full.
- 307 newly called instances had foreign surviving signs in their interval.

All checks passed in approximately 0.44 seconds. These are bounded semantic controls, not a replacement for the direct induction above. Full results are in `augmented_projection.json`.

## 6. Review boundary

The original phrase “allowed surrounding histories” did not formally supply the stronger interface and projection proof required by recursive reuse. Reading the child induction as ordinary standalone SPR gives a genuinely false inference, as the exact execution below demonstrates. This presentation/proof-interface gap existed and should not be erased from the provenance. The v3 addition supplies the extended quantifier and its missing recursive-closure justification. The theorem is not justified by merely assuming the stronger hypothesis; its base cases, epoch propagation, and live induction have been checked directly in that class. Priority clearance and formal proof-assistant verification remain separate from this internal sign-off.

## 7. Hostile review's actual 19-round counterexample: independently reproduced

Use n=32, root weight one, and request

    17,1,18,2,19,3,20,4,21,5,22,6,23,7,24,8,25,9,25.

`replay_hostile_transcript.py` runs the frozen exact-rational implementation. All 19 requests are globally legal, all return plus, and the root never fills. The first eight pairs end zero-length continuations, leaving pluses at cells 1 through 8. The new root epoch starts with tau=16.

At rounds 17 and 19, the SAME right-half child receives cell 25. Round 18's request at cell 9 erases the physical plus at 25 without advancing that child. Its counts after these three rounds are exactly `1,1,2`. The SAME one-cell descendant at cell 25, previously locally full, also resumes. The parent's phase remains one because `14.8*1<16`.

An isolated ordinary child receiving the address sequence `(25,25)` would reject its second request, because its first plus was never locally deleted. Thus the hostile review identified a real defect in the ordinary-child interpretation, not a counterexample to the claimed sign bound. Full round-by-round evidence is retained in `hostile_transcript_replay.json`.

## 8. Comparison with the reviewer's overwrite-shadow repair

For an overwrite shadow, every address is accepted, and its transition is

    T_(j,+)(P,M)=(P intersect {i<j} union {j}, M intersect {i>j}),
    T_(j,-)(P,M)=(P intersect {i<j}, M intersect {i>j} union {j}).

These operators preserve signed-subboard containment for a fixed address and sign. The label oracle depends on request counters/weights, not occupancy or erasures. Therefore an arbitrary E trace and an overwrite shadow fed the same addresses produce the same labels. Extra erasures remove only physical owned signs, and monotonicity of T then preserves physical-owned containment in the shadow. This is transition-level coupling for a fixed realized address sequence, not an unsupported strategic claim about arbitrary erasures.

Conversely, every overwrite address sequence is itself realized in E by externally erasing the requested cell immediately before its local request when occupied. That erasure does not change controller state. The owned board after the resulting E request equals the overwrite transition exactly. Hence our directly proved E theorem includes the reviewer's overwrite theorem as a special case; the shadow domination gives the converse guarantee for this occupancy-oblivious oracle.

The two repairs are compatible. E makes actual ownership/projection and arbitrary erasures explicit; overwrite shadows provide another convenient closed interface. Neither introduces overwriting into the physical target SPR game. No numerical recertification or exponent change is needed for either repair.
