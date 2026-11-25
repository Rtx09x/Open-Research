# Bounded two-coordinate successor after the ordered-suffix proof

## Preferred internally audited result

With the new ordered-suffix analysis and **exactly two revised small-class proportion pairs**, the deterministic online unit-bin algorithm has asymptotic upper bound

`R=96988842290419266162339453629607142739/61455140781288409357546665835971477504 ≈1.5782055179987482`.

Full integer pricing and a separate Fraction recursion pass402 scenarios /804 strict knapsacks. **Independent primary-derived advisor arithmetic and final prose audit also PASS**: only167/179 change, all positive supports and weights are verified against primary data, and all402/804 strict knapsacks and the physical G floor pass with42,813 Fraction nodes. See `advisor/phase2/check_packing_retune_two.py`, `packing_retune_two_audit.json`, and `packing_retune_two_audit.md`. The fully audited unchanged-algorithm bound1.5782187688512288 remains preserved. This is a revised algorithm, not just a changed proof of the frozen algorithm.

Only the following two proportions change relative to the ordered-suffix anchor; the companion proportion in each row is1 minus the displayed value:

| Class | Supported types | Revised first-type proportion |
|---|---|---|
|167|(1,3)|2443403469042275048800466661985715451963478233706047451683 /10391935267352565383103044400009949515480488221135948379842|
|179|(2,10)|27927345544998943473172174410059889328771995680602116851 /75741405378444607696070020526291572299375191317598061148|

All class endpoints, supported types, tiny capacities/proportions, Best Fit behavior, other algorithm parameters, published u,v,w and ordered-suffix cutoffs are unchanged. Both pairs remain strictly positive and sum to1. The affected classes are small, with upper endpoints271/960 and1/10, both below1/3; no large-class feasibility constraint changes.

This is a small all-input upper-bound improvement, **not full-gap closure**, a universal lower-bound improvement, or an actual-ratio tightness result. Publication priority and external human/formal review remain unestablished.

## 1. Exact affine coordinates

Set

`x=1/(2 alpha_(2,179)+10 alpha_(10,179))`,

`y=1/(alpha_(1,167)+3 alpha_(3,167))`.

Then

`alpha_(2,179)=(10-1/x)/8`,

`alpha_(1,167)=(3-1/y)/2`.

Positive support is equivalent to1/10<x<1/2 and1/3<y<1. Every fixed-scenario item weight of these two classes is affine in its reciprocal-count coordinate. Every other weight and tiny envelope is fixed. The complete fixed-analysis maximum is therefore a convex piecewise-affine function of(x,y).

The bounded test used a box of width1/1000 in each coordinate, starting at the prior class179-only result. All box corners and candidate active-plane intersections were checked by the complete402/804 pattern oracle. The small LP master was solved by exact enumeration of rational three-plane vertices, not a floating solver. It closed in three iterations. Parent explicitly limited this continuation to these two coordinates; no third/fourth-coordinate chain is pursued.

## 2. Three physical active rows and a parameter-independent floor

The final scenario is(3/7,1/2), with unchanged tiny charge c=997/2100120,g=11/500.

The active patterns are

1. `P=(1,165,179,205,208,211)`, residual997/2100120, weight

   `16937334239132566685351795707/10496187989852832684086132736 - x/4`.

2. `Z=(1,167,168,189)`, residual1/3360, weight

   `101960709481823113009047421167/57415045414579597588163461120 - y/2`.

3. `G=(1,165,172)`, residual1/60, weight **R independent of both x and y**.

The selected x,y solve P=Z=G exactly. One tiny item approaches each residual from below, with all non-tiny items strictly above their class lower endpoints, so these are genuine physical supremum rows rather than loose tiny-envelope artifacts. Full pricing checks every other pattern and scenario, not only these three.

The constant G row proves that no change of167 and179 alone can improve the bound **with these fixed analysis charges and all other parameters fixed**, anywhere in their positive-support domain. This strengthens the bounded-box optimization certificate to the whole two-coordinate fixed-charge family. It does not optimize charges jointly with proportions or other algorithm coordinates, and is not a lower bound on actual algorithm performance.

## 3. Source-proof applicability

The two classes keep their original container volumes and positive supports. The scenario partition therefore stays identical. Their quota rules permit arbitrary fixed positive proportions summing to1 and retain bounded discrepancy. The source large-case u,v conditions depend on the large threshold class, not on these small-class proportions, and the exact verifier rechecks all conditions.

Tiny capacities/proportions are unchanged, so every part of the ordered-suffix chronology and its explicit finite-prefix additive constant transfers unchanged. Matching and temporary/declared-large-container proofs are not altered. This change does not use advice, future information, repacking or extra capacity.

## 4. Artifacts and reproducibility

Stable full certificate: `retuned_certificate.json`, SHA256

`c8559b05ef4fd6373ad391504fc93d931651ea550ab61c998eb4f0ebe52868bd`.

`candidate.json` records the exact proportions, box, active planes and full-oracle history. `verify_independent.py` checks that only167 and179 change relative to the immutable ordered-suffix anchor, that every support/end point/analysis weight/charge stays fixed, and that all804 strict knapsacks satisfy R. `verify_active_face.py` recomputes the physical P/Z/G rows and parameter-independent floor.

From `online-bin-packing/`, use one CPU,1GiB,290-second timeouts and `PYTHONDONTWRITEBYTECODE=1`:

```sh
python phase4/retune_two/check_all.py
python phase4/retune_two/verify_independent.py
python phase4/retune_two/verify_active_face.py
```

All proof and verification code uses exact standard-library fractions. The integer oracle visits67,514 nodes and the separate Fraction target verifier30,422. The complete two-coordinate discovery took about18 seconds.

The next native task is the separately documented above-quarter **restricted lower-bound kill test**, not further decimal tuning. The blocked ChatGPT submission is not retried or routed through another agent; native mathematical work is independent of that browser action.
