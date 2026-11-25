# Exact replacement-trade reduction

Let B be any finite single-deletion code and let D(x) be the set of distinct one-deletion descendants of x. Define N_B(x)={b in B: D(x) intersects D(b)}. For any subset S of B, every word in a replacement T outside B must satisfy N_B(x) subset S. Conversely, if this containment holds for every x in T and the deletion balls of T are pairwise disjoint, then (B minus S) union T is a valid code. It is larger exactly when |T|>|S|.

**Connected-support lemma.** If an improving trade exists removing at most k words, then an improving trade exists whose removed set is the union of the neighborhoods N_B(x) of its added words, and whose neighborhood hypergraph is connected.

Proof: discard removed words not in that union, which cannot decrease the gain. Partition the incidence graph (added words on one side, their baseline neighbors on the other) into connected components. The total gain is the sum over components of (added vertices minus baseline vertices), so some component has positive gain. Each component alone is a valid replacement. A connected finite hypergraph can be built by starting from one edge and successively adjoining an edge that intersects the current union. This follows by traversing a spanning tree of its incidence graph. Thus enumerating every union obtainable this way, of size at most k, covers every possible smallest improving trade. QED.

`trades.py` implements precisely this exhaustive union closure, then tests all eligible added words by exact integer bitset packing DFS. No assumptions of complement or reversal symmetry are imposed. The finite-radius conclusion is **not** unrestricted optimality. The lemma is an elementary reduction; novelty is not asserted.

Implementation specialization: the mathematical lemma holds for any baseline B, including imperfect codes, if N_B(x) is computed from actual intersections. The current scripts deliberately specialize to perfect VT baselines and therefore build a unique `owner` for **every** received word; baseline verification proves this coverage. This owner lookup must not be reused unchanged for an imperfect switched code.

If exhaustive search finds neither positive nor neutral connected components through radius k, then there is no nonempty cardinality-preserving trade through radius k either. A disconnected neutral trade decomposes into integer-gain components; absent positive components, its zero total gain requires a neutral component. This explains the neutral-barrier claim; it is not unrestricted uniqueness.
