# A certified upper gate for the C30-plus-eight variable-fiber instance

This is a **restricted dimension10 upper bound**, not an upper bound on the
unrestricted Shannon capacity of C7. No numerical lower-bound improvement is
claimed, and publication priority has not been investigated.

The exact physical sets in `c30_plus_eight_port_instance.json` satisfy
|B|=344, |H|=|V|=23, H∩V=∅, P=H∪V, |X|=367, P∩X=∅. B,H,V,X are independent
and B is separated from P. P consists of the canonical C30 port cycle plus
the published eight private-pair ports.

Consider **arbitrary independent** fibers F_x,G_x⊆P indexed by x∈X, subject
only to the requirement that the following union is independent:

    C = B×B ∪ ⋃_{x∈X}(F_x×{x}) ∪ ⋃_{x∈X}({x}×G_x).

The construction allows point-dependent, unequal fibers and arbitrary subsets
of P. It does not impose the old seven-family blanket double-neighborhood
filter. The three parts are disjoint because B∩P=P∩X=∅.

For x,y∈X, independence forces

    F_x∩N(y)=∅  OR  G_y∩N(x)=∅.                         (1)

Otherwise choose a∈F_x∩N(y) and b∈G_y∩N(x). Then (a,x) and (y,b) are
confusable. They are distinct because P∩X=∅. This last condition is important:
without it, an identical-word overlap could invalidate this argument.

Let A(S) be any certified independence upper bound for P\N(S), where S is an
outer-label subset. Every A used below is the size of an explicitly verified
physical clique partition; no numerical SDP or solver infeasibility is used.
We have A(∅)=23. Applying (1) with x=y gives

    |F_x|+|G_x| ≤ A(∅)+A({x}).

Summing gives |C|≤135138. The per-label bounds are23 for297 outer labels,
22 for60 labels, and21 for10 labels.

For a pair {x,y}, there are four crossing constraints (1). Choose, for each
constraint, which side is forced to avoid its forbidden neighborhood. There
are2^4=16 possibilities. Each possibility forces each of F_x,F_y,G_x,G_y to
avoid none, one, or both outer labels, and hence bounds their combined size by
a sum of four entries from

    [A(∅), A({x}), A({y}), A({x,y})].

Taking the maximum of the16 sums is a valid upper bound for the four fibers:
every actual independent choice satisfies at least one of these orientations.

The certificate selects disjoint outer-label pairs. Summing their pair bounds
and the single-label bounds for all unpaired labels saves78 words over the
diagonal estimate. Therefore

    |C| ≤ 135138 − 78 = 135060 < 135093.

Thus this precise C30-plus-eight unpunctured-core family cannot reach the
desired dimension10 target, **even with arbitrary point-dependent fibers**.
Selective holes inside the full I0² core, additional port words, different
outer codes, or additional independent reservoirs are outside the theorem.

Reproduce the exact certificate verification (Python standard library only):

    python verify_c30_fiber_pair_gate.py

`c30_fiber_pair_gate.py` is only a proposal generator. Its optional NetworkX
matching merely chooses disjoint label pairs; optimality is unnecessary. The
verifier checks the chosen pairs, every clique partition, all16 orientations,
and all integer sums independently of NetworkX or any optimization solver.
