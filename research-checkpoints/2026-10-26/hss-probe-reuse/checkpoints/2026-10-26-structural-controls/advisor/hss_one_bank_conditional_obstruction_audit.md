# Independent audit: coherent phase-return conditional obstruction

2026-10-26 01:39 UTC. **PASS** for the restricted counterexample in `one_bank_conditional_obstruction.md`.

The physical swap sends x and D=x−z to −alpha, places the old D in the first passive-forward coordinate, and retains all unused passive coordinates. During the following row-rotation block, (D,w_first) rotates by exactly −I while x gains the scalar factor rho and passive-forward energy gains rho². Centering/isotropy of the fresh forward orientation yields precisely U_next=q[(1−1/d)U+A], A_next=U/d; no independence between the prior active amplitude and passive energy is required. The three stated cost terms follow from the actual coefficient extraction.

The rational unit-circle increments satisfy the exact pi product and 1−r_j≤8/m². For m≥64, q≥1−16/m, T_i=U_i+A_i≥q^i, and the first floor(m/32) periods give the stated positive multiple of m/d. The infinite geometric sum is correct but is not necessary for the finite-depth contradiction. Hierarchy depth is O(m²), giving an unbounded square-root-depth conditional cost at every fixed finite width.

`check_hss_one_bank_obstruction_independent.py/.json` is advisor-written and imports no worker code. It constructs the actual sample/coefficient/subtraction maps and propagates a full six-dimensional Fraction covariance over all eight forward signed-permutation orientations per step. Exact cycles at m=4,8,16 pass even with a nonzero initial active/passive cross covariance. Separately derived rational recurrence totals at m=16,32,64,128 give exact integer lower bounds5,8,14,26 at depths272,1056,4160,16512. These second-moment orientation controls match Haar isotropy; the analytic argument supplies all finite widths d≥2.

At fixed finite depth the conditional expected output is continuous in the fixed opposite-bank frames. Every strict finite lower bound therefore persists on an open positive-Haar-measure neighborhood of the identity bank. This refutes a single uniform almost-sure conditional constant, not merely an exceptional null-point formulation.

The neighborhood probability can shrink with depth. No unconditional lower bound, full-HSS impossibility, or contradiction to the audited scalar801 theorem follows. The correlated-anchor proof must retain opposite-bank averaging (as its fourth-moment argument does) or use a genuinely weaker conditional statement.
