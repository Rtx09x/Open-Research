# Independent audit: bounded two-coordinate ordered-suffix successor

2026-10-26 00:19 UTC. PASS.

Certificate SHA256: `c8559b05ef4fd6373ad391504fc93d931651ea550ab61c998eb4f0ebe52868bd`.

Exact upper bound:
`96988842290419266162339453629607142739 / 61455140781288409357546665835971477504`
(approximately 1.5782055179987482).

`check_packing_retune_two.py` independently reparses the primary AH parameter/analysis tables through the advisor's previously frozen source parser. It confirms that relative to the independently audited ordered-suffix algorithm only class167 type1/type3 proportions and class179 type2/type10 proportions change. Every proportion is positive, each class sums to one, every support and advertised capacity stays unchanged, and all published u/v/w analysis weights and all tiny ordered-suffix charges remain unchanged. Therefore the prior algorithm-portability and chronological suffix proof continue to apply; this is not the unchanged-parameter algorithm.

The checker independently reconstructs every item weight and checks all402 scenario intervals /804 strict knapsacks with Fraction arithmetic, using a reduced-profit density recursion different from the worker's implementation. It visits42,813 nodes. No worker implementation imports or old printed scenario bounds are used.

The physical pattern huge+165+172 has residual1/60, strictly between the final scenario's c and g. Its limiting tiny weight is b/(B-g) times1/60 and the total equals the claimed upper. Neither class167 nor179 appears. Perturbing non-tiny sizes above their infima and decreasing that tiny item by the total perturbation preserves the charge branch. Thus this fixed physical row supplies the same floor for every admissible change of these two class proportions with the fixed remaining analysis. It proves the stated restricted coordinate optimum, not an actual execution lower bound, global algorithm-parameter optimum, or whole online bin-packing gap solution.

Correctness and novelty are separate. This audit establishes the exact arithmetic/model statement, not exhaustive literature priority.
