# Final successor-mixture audit

2026-10-25 23:02UTC. **PASS** for the all-input asymptotic upper bound and the stated fixed-parameter analysis-family optimum.

R =17309229457317341044853136044527531250227952497 /10967548450040323523815819160873924866844131328 ≈1.5782222924443705.
Certificate SHA256 `48d1e32cefcb5f2c999de480684332a4c2b2b411c4912ffb7e8754ea9f56d64d`.

Independent source-derived pricing in `check_packing_successor_mixture.py` checks all402scenarios/804strict knapsacks,42956Fractionnodes. It imports no worker code, uses the advisor's frozen primary AH parser and a reduced-profit density recursion, and independently reconstructs the P/G/Q physical patterns, positive dual and all30 endpoint inequalities.

The complete `SUCCESSOR_MIXTURE_THEOREM.md` was read. The crucial new chronology argument is valid: final-high containers with a small item charge their own birth; those without one charge the next no-small container's birth. These target sets are disjoint and the second map is injective. Only earliest-high-if-small and last-no-small are exceptions. Thus the excess coefficient drops from2 to1, with unchanged finite additive constant. Final classification is ex-post proof bookkeeping, not an online information assumption.

The finite continuum reduction is also valid. q outside its two type endpoints is pointwise dominated. For fixed g, dependence on c is fractional-linear between row residuals and jumps downward at exact thresholds. At an endpoint q=1/(A−g), multiplying numerator/denominator by(A−g) cancels apparent quadratic terms: for row residualr>c the numerator is b(A−c)[r+(r−g)+], while forr≤c it is br(A−g). For fixed c these are affine in g on residual intervals; c=g is the hinge family. All30 endpoint checks therefore bound the entire continuum. There are four dual-flat endpoint columns, not a unique three-column optimum; this does not affect the selected mixture's optimality.

All three residuals are below d, so one tiny item tending to each residual realizes all selected components' limiting weights simultaneously. The family floor is not caused by incompatible separate envelope maxima. The upper bound nevertheless uses conservative summed envelopes for arbitrary patterns, which is safe.

The result keeps algorithm parameters and non-tiny weights fixed. It is not a matching lower bound for actual Best Fit performance, an optimum among all algorithms/potentials, or a solution of the classic packing gap. Publication priority and external review remain separate.
