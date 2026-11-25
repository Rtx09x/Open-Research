# Next target outside the optimized successor-charge family

The final theorem optimizes every finite convex mixture of the disjoint-successor two-cutoff charges. Do not resume by sweeping their c,g,q parameters. The true Best Fit ratio remains unknown, so a stronger chronological conservation law is the relevant next question.

## Terminal creation epochs retain information discarded so far

Fix a threshold c in(0,d]. At the **last tiny-container creation whose incoming item is at most c**, every prior advertised container has residual strictly below that item, hence at most c forever. Consequently every final container with residual>c belongs to the later terminal creation epoch, **except possibly the container opened by that last<=c creation itself**. Every creation item in the later epoch is>c. If no<=c creation occurred, the epoch is the entire history and no such exception is needed.

If M is the epoch length and N_c is the total number of tiny items>c, then M<=N_c. Because cumulative type discrepancies are bounded at every time, subtracting quota relations at the two ends gives epoch type counts `M_i=alpha_i*M+O(1)`. In particular, final-high type counts satisfy both `h_i<=M_i+1` and the existing volume inequality

`sum_i (A_i-d)h_i <= L_c+2(Amax-d)`.

This is more information than the previous replacement `h_i<=alpha_i*m+O(1)`: the quota budget applies to an input-defined terminal epoch, not every container ever created.

## First exact reduction to test

For q>=0 and `kappa(q)=sum alpha_i*(1-q(A_i-d))_+`, the same elementary type inequality suggests

`h <= q L_c + kappa(q) N_c + O(1)`.

Combining it with the original waste bound produces the candidate valid charge

`f_(c,q)(s) = b/(B-c) * [s+(d-c)*(q*s+kappa(q))*1_(s>c)]`.

Unlike the optimized family, this has a **per-item jump intercept**, arising from the number of large birth items. It cannot be treated as a homogeneous density step. Its exact tiny-bin envelope must jointly maximize high-item count and high-item volume: for a residual r, admissible counts satisfy `n*c<r`, and each selected high item has size in(c,d]. Strict endpoints and count/volume coupling matter. The zero-threshold case needs separate treatment because a positive per-item intercept would be unbounded.

This displayed reduction is a next hypothesis/derivation to independently audit, not part of the current certified bound. Use the final P/G/Q patterns for cheap falsification, then exact all-pattern pricing; stop if an exact continuous-family dual shows no improvement. A negative result would still motivate preserving multiple nested terminal epochs or birth-type flow variables rather than more separable weights.

## Stronger variant if the first reduction fails

Retain several thresholds jointly. Final residuals obey `r_i < min_{j>i} s_birth(j)` for every non-last container, so the high-residual sets form nested suffix epochs. Their type quotas and birth-size budgets are coupled. Seek a finite potential/LP theorem over this nested state, or an explicit execution saturating the current P/G/Q mixture. This would directly answer whether the current per-bin maximum loses realizability information. A numerical LP on hypothetical counts alone is not enough: prove the causal invariant and a uniform additive constant, or construct a real input execution.

No new ChatGPT request is authorized by this note. Root owns the already accepted external lower-architecture run and the two-active-run allocation. Native continuation remains one CPU,1GiB and bounded checkpointed jobs.
