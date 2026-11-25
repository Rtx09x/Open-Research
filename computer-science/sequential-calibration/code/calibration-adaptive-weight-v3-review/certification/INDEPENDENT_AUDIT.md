# Independent analytic and numerical audit

**Verdict (26 October 2026): PASS for the stated adaptive-weight SPR theorem and its application of the published transfer theorem, subject to the ordinary reliance on that published transfer theorem.** This is an internal mathematical verification, not external peer review or a proof of priority. It does not resolve the full minimax calibration problem and does not establish an efficient forecaster.

Audited manuscript: `../theory/ADAPTIVE_Q_THEOREM.md`, sections 1–5. The algorithm and induction were reconstructed from the definitions rather than inferred from finite game values. The independent game solver used disjoint masks; the lead used ternary states. The continuous parameter checker below was independently implemented.

## 1. Legal algorithm and induction domain

The labeler deletes only eligible signs and labels the currently selected empty cell. Global all-deletion is a legal choice; its optimality is not needed for this upper bound. An algorithmic restart does not clear physical signs. Counts and ownership distinguish the new instance's signs from preexisting signs placed by its ancestors or other instances. Arbitrary external deletions only reduce each owned inventory.

Each half-child has the parent's fixed positive weight. A right-trigger continuation has weight `w*q`; a left-trigger continuation has `w/q`. Its weight is fixed when initialized: later requests do not retrospectively alter it. The trigger uses only already observed counts. A new epoch answers the request that exhausted the preceding epoch; the triggering request itself is answered by the old half-child. A zero-length continuation is skipped. New-epoch first requests cannot immediately require an infinite restart chain, because `rho>0` and both children must be visited to trigger.

The outer induction decreases the power-of-two interval size; same-size continuation calls decrease the number of answered requests. Induction is uniform over all positive real weights and all legal surrounding histories. It does not claim a bound on arbitrary preexisting signs at zero local requests.

## 2. Trigger orientation and integer rounding

Let the requested half's count after a trigger be `l`, and the other count `h`. The requested half cannot be strictly heavier: in that case the minimum count did not change while the maximum only increased, so a failed trigger condition could not become true. Ties cause no problem: before the request the other half still had exactly the same value `h`, while the requested half had `l-1`.

Before triggering, either `delta*(l-1)<tau` or `l-1<rho*h`; after triggering, both non-strict reverse inequalities hold for `l`. Therefore

    l0=max(tau/delta,rho*h) <= l < l0+1.

This proof explicitly handles ties and changes in which child is called light. Both halves have been visited, and `h>=1`. Thus `z=tau/h`, `r=l0/h` lie on the two certified trigger segments. The policy evaluates `q` at these NOMINAL ratios, not at the slightly overshot `l/h`. No continuity or Lipschitz assumption about `q` is needed for rounding.

For `L=floor(kappa*h)`, the ideal endpoint `u0=tau+h+l0+kappa*h` satisfies `u0<u+1`, where `u=tau+h+l+L`. Because `0<beta<1`, replacing `l0` by `l` costs at most one in the corresponding power. Replacing `kappa*h` by `L` can only decrease the positive continuation terms. Consequently the manuscript's additive-one and `(1+1/F)` rounding factors are sufficient. The strict inequalities use the separate gaps `P0<Kp` and `Q0<Kt`; `P0<Q0` is explicitly checked.

## 3. Small-time bounds for all real weights

On the actual answer chain, a same-size continuation has answered `c>=1` requests, while its parent has answered at least `tau+h+l+c>=2c`, since `c<=L<=h`. A half-size call never increases the answered-request count. Prior epochs only increase the parent's count. Calls to an already exhausted epoch are not on the chain returning the sign and do not affect this argument.

If the chain has `j` weight changes, its leaf has answered at least one request, so `2^j<=t`. Each weight multiplier and its reciprocal is at most two because `1/2<=q<=qmax<1`. The returned leaf sign satisfies `w_leaf^sigma>=1`; hence the original instance satisfies `w^sigma>=2^-j>=1/t` for that sign. This justifies the small-time bound uniformly even when `w` is arbitrarily small or large. The same argument with `C*Kp=F^2` establishes the stronger inherited budgets for short completed epochs. The leaf and zero-request base cases are valid.

## 4. Inventories and completed epochs

The first visit to each half deletes all inherited nonpersistent signs in the other half. A right trigger additionally deletes every minus placed by the left child. The three manuscript envelopes therefore account for exactly the potentially surviving owned signs: inherited persistent inventory, frozen half-child contributions, and new continuation contributions. A left trigger is the reflected, sign-reversed case. No child is reset after only one sign type is wiped.

At a completed endpoint, the formula for `q` makes the minus envelope at most `P0*S` because its denominator is positive. The two independently certified plus inequalities give persistent-plus and total-plus budgets. Both sign types then meet the inherited `Kp,Kt` budgets after rounding. In particular, total-minus is first bounded by the stronger `P0` inequality and fits the `Q0` total budget since `P0<Q0`.

## 5. Every unfinished epoch, including terminal boards

For one-half-only traffic, the old TOTAL budget `Kt`, not `Kp`, is used. For both-half phase-one traffic, the two alternatives in the failed trigger yield the manuscript's `M`: combine inherited/light traffic with ratio `l/tau<=1/delta`, or combine the two half counts with ratio `l/h<=rho`. The weighted concavity exponent is `1/(1-beta)`, and the stated scalar maximizers follow by differentiation. Zero-count endpoints follow by continuity. The triggering request costs at most one.

For a live continuation, plus inventory uses `q<=qmax` and the certified weighted-concavity bound `D1`. For minus inventory, the scalar deficit

    f(c)=Kp*tau^beta+l^beta+(H/q)*c^beta
         -Kp*(tau+h+l+c)^beta

is increasing for `c>0`, since `H/q>Kp` and `beta-1<0`. It is continuous at `c=0`, because `beta>0`.

**Crucial terminal-board point:** `f(L)<0` is an algebraic endpoint inequality in the frozen numbers `tau,h,l,L`, obtained directly from the certified trigger inequalities and rounding. It does NOT require the pointer to have a legal way to continue until `L`. The child inductive hypothesis is used only at the ACTUAL observed continuation count `c`. Therefore `f(c)<=f(L)<0` is valid even if a full board, pointer stop, or horizon makes the hypothetical endpoint unplayable. If the current total exceeds `F`, the algebraic endpoint total also exceeds `F`; otherwise the small-time proof applies.

Thus every actual prefix obeys the claimed `D*t^beta+1` envelope. The strict scalar bound `D+F^-beta<2^alpha` closes the induction. Stops and full-board termination are included, not added afterward by extrapolation.

## 6. Parameter certificate and transfer

`certify_adaptive_bias.py` checks every point on BOTH closed trigger segments using a gap-free exact-rational dyadic partition and outward interval arithmetic. It separately proves denominator positivity before division. The `max(1/2,...)` enclosure is monotone and sound, including across its switching point. The partition has 4,988 leaves; it is retained in `results/adaptive_bias_certificate.json`. The numerical verifier asserts all scalar range conditions used above, including `P0<Q0`.

The verified parameters have `alpha=51/5000`, `beta=379/400`, and `epsilon=423/10000>0`. At weight one, adding the two sign bounds gives a uniform SPR estimate. Padding to the next power of two introduces only the stated constant factor; if the original board fills, the pointer stops at that prefix of the padded board.

[Dai–Fishelson v2, Theorem 5.1](https://arxiv.org/html/2610.07623v2#S5) requires a legal uniform `opt(n,t)=O(n^alpha*t^beta)` bound, `alpha,beta` in `(0,1)`, and positive `1-alpha-beta`. It places no fixed-bias or integer-weight restriction on the labeler. These hypotheses are met. The resulting exponent is exactly

    (2+epsilon)/(3+2*epsilon)=20423/30846
                               =0.6620955715489852... .

The original simultaneous-move, exact-forecast-value, unnormalized expected calibration metric is unchanged. The transfer is an existence/minimax statement, not a polynomial-time implementation. The lower bound and bidirectional SPR connection in [Dagan et al. v4](https://arxiv.org/html/2406.13668v4) remain distinct results; this audit does not reprove their theorems.

The optional rational realization also passed a separate standard-library exact-integer check of all 4,988 CLOSED cells: each constant rational factor satisfies the minus budget, both plus budgets, and the factor cap throughout its cell. The minimum certified minus slack is the positive rational `1329825/604462909807314587353088`. Exact coverage includes every interval endpoint. At the common segment endpoint the runtime chooses segment one; at internal endpoints it chooses the leftmost containing closed cell, which is certified there. An independent comparison of the actual `adaptive_policy.factor` with these endpoint rules passed all 14,964 endpoints/midpoints. Weights and comparisons are therefore computable using rational arithmetic without a hidden exact-real oracle. No efficient-forecaster complexity bound follows from this fact alone.

## 7. Verification limits

- No finite-state fit is used in the all-size proof.
- Internal independent checking is not external peer review.
- Novelty/priority is not certified by a mathematical checker; the lead's source comparison has a separate scope.
- The published transfer theorem is invoked with checked hypotheses, not independently reproved here in full.
- No matching minimax rate, efficient forecaster, or resolution of the full calibration problem is claimed.
- A second, standard-library exact-integer rational-power replay independently passed all 4,988 boxes with 80-bit dyadic endpoints and 29,972 certified root endpoint evaluations in 27.10 seconds (24 MiB peak RSS). See `replay_rational_certificate.py` and `results/rational_replay.json`. Floating point seeds its root iteration only; exact integer inequalities validate every returned root, so correctness does not depend on the seed's accuracy. The analytic verdict does not depend on calling a finite grid a continuum certificate.

