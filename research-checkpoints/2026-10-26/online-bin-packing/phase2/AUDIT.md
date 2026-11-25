# Phase 2 audit: delayed tiny closure and the Pro hypotheses

**Verdict:** the Pro algorithm modification, overflow lemma, nonlinear fill envelope, and claimed global upper certificate pass the checks described below. A later structural simplification and improved certificate are in `SINGLE_THRESHOLD_THEOREM.md`. No publication priority is established.

The initial frozen phase-1 certificate is unchanged. Code was read before execution; all phase-2 writes are confined here. All jobs used one CPU, a 1 GiB address-space limit, and a 290-second timeout. No additional Pro call was made.

## 1. What algorithm is actually certified

Use the frozen three-transfer AH parameters. Change only tiny-container closure: maintain at most one open tiny container of advertised capacity A; place a new tiny item s into it if its load L satisfies L+s≤A, otherwise close it and create the next quota-selected container using the original placement/matching rules. The item fits the new container because s≤d=1/43≤min A_i.

All original priority rules, including largest-temporary-singleton selection, are retained. Only genuinely unspecified ties receive a fixed deterministic tie-break. Advertised volumes never change while a tiny container fills. Consequently no bin exceeds capacity, no item moves, and no future information is used.

The advisor independently inspected the primary AH proof, not just Pro's narrative. Delaying closure preserves the all-but-one load>A_i−d invariant, the quota discrepancy, fixed-volume matching separation, and the temporary-singleton proofs. Open/closed tiny status is used only in tiny insertion and the tiny-load lemma; matching uses advertised volumes. Source proof audit: advisor's `phase2/packing_portability_audit.md`.

The retrospective threshold repair also passes: choose t in the strict interval between 1−minimum unmatched positive volume and the minimum unmatched negative volume, avoiding the finite breakpoints. This is an analysis choice, not online advice. The required unmatched-container separation holds and the charging proof does not require an unmatched positive exactly at 1−t.

The source's displayed threshold-class algebra has a possible O(1) sign issue; Pro's direct replacement argument and the advisor's independent algebra establish an input-independent additive constant. This is not an asymptotic counterexample to AH.

## 2. Overflow charge: direct proof check

For fixed tiny types, define B=Σα_i A_i, b=Σα_i r_i and d=1/43. For 0≤c≤d,

`rho_c=b/(B−c)`, `f_c(s)=rho_c[s+(s−c)_+]`.

Each failed insertion closes one container whose unused capacity is less than its distinct triggering item's size. The trigger fits its new container immediately. At most one final container remains unfinished. Type counts satisfy n_i=α_i m+e_i, e_i≤1, Σe_i=0; the positive and negative discrepancy masses are at most p−1. Therefore

`(B−c)m ≤ Σs + Σ(s−c)_+ + p`,

and total required tiny-container weight is at most

`Σf_c(s) + rho_c p + p−1`.

These statements hold for every finite input, not only sampled streams. All constants depend only on fixed parameters/scenario choices.

**Crucial distinction:** this stronger lemma does not apply to original AH's proactive closure. An exact counterexample was constructed with 1,000 proactively closed containers and all tiny items of size 1/2580. At c=1/60, the proposed charge including its additive constant is less than 1,000 by

`313260779032356/57291524611081 > 0`.

Thus attributing the improved bound to unchanged AH would be false. The delayed-closing algorithm change is essential.

## 3. Nonlinear offline fill and full arithmetic

For r=qd+e, q=floor(r/d), 0≤e<d, the exact maximum over tiny multisets of total size at most r is

`G_c(r)=r+q(d−c)+(e−c)_+`.

Counting the items larger than c proves the upper bound; q items of size d and a remainder e attain it. The envelope is continuous and increasing, including every endpoint. Strict-infimum non-tiny capacity remains correct; empty patterns cover tiny-only fills. A safe pruning bound is `G_c(r)≤(2−c/d)r`.

`verify_nonlinear_independent.py` uses the frozen phase-1 parameters, no Pro imports, and integer-scaled reduced profits with monotone nonlinear residual charge. It reconstructed all scenarios, checked all 804 cases, and verified the exact equality witness. Result: **PASS**, 402 scenarios, 22,986 search nodes, approximately 2.3 seconds.

Verified Pro target:

`87931323061219230147063794829048504459349/55715094120735551199336133222286481162240 ≈1.5782316165646344`.

The Pro source-free checker was also replayed after code inspection, but its PASS text is not treated as independent evidence. That replay reproduces all 804 cases in 29,867 Fraction-search nodes.

Supplementary falsification tests (`check_tiny_lemmas.py`) checked 250,000 exact published-parameter stream prefixes, 4,262 overflow events, and 13,758 exact grid-fill optimization cases. No delayed-rule counterexample was found. These finite tests supplement, not replace, the analytic proof.

## 4. Causal lower-history claim

The nine prefix masses agree with the previously checked t=3 witness. All 9 prefix and 34 suffix patterns fit uniformly at their upper adaptive-size bounds for 0<epsilon<2058^−3 and 0<gamma<epsilon/4. The supplied exact checker reproduces all eight costs and all refinement flow balances; source Lemmas 3–4 provide the constructive offline packings.

The chronology argument is sound for this particular tree: C3 slots are filled first, then C2 slots, then existing-bin A slots, then A-only bins. The first A in each A-only bin receives the large label; all other A-items receive the small label. Each branch is identifiable from its first arriving item or already revealed history. Every suffix schedule extends the actual first-stage packing. Uniform complete-word capacities imply all prefixes are feasible.

The base-volume dual is also valid here. All base sizes lie on (1/294)Z; actual items exceed 1/295, so a bin has at most 294 items. Each item is at least its base minus294epsilon. A base total above1 would force actual volume above `1+1/294−294^2 epsilon>1`. At integral scales the base totals match the constructive offline budgets, establishing genuine OPT equality at the eight specified stops.

The macroblock period is D=2,418,150,000,000 (or9D for the paper's stronger convenient divisibility). Repeated C3 macroblocks handle unknown N; an incomplete block and resulting affine suffix-count discrepancies cost O(D). Thus one causal deterministic policy has ratio1.5428+O(D/N) on this **original eight-stop t=3 family**.

This does not give a competitive algorithm on arbitrary inputs, does not handle arbitrary extra stopping times or new branches, and does not improve the universal lower bound. It closes chronology and size-spread loopholes only for the specific witness.

## 5. Outstanding limitations

Publication priority and independent human/formal review remain unresolved. At the initial Pro-audit stage, the finite exact certificates established only an upper analysis bound. The subsequent `SINGLE_THRESHOLD_THEOREM.md` improves that bound, and `coupled/SATURATION_THEOREM.md` now gives an independently audited explicit input family attaining it asymptotically for the fixed modified algorithm. This algorithm-specific tightness is not a universal lower-bound improvement. New algorithms and structural universal adversaries remain open. Source caches and Pro replay copies are not needed in the minimal final verification bundle.
