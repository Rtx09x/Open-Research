# Exact joint two-reservoir objective

Let C=I0², |C|=134689, and let S1,S2 be independently verified independent
outside reservoirs, each disjoint from C. Deduplicate U=S1∪S2. Use binary
selection x_u for u∈U and deletion y_c for c∈C. The exact objective is

    maximize 134689 + sum(x_u) - sum(y_c)
    x_u <= y_c whenever u and c are confusable;
    x_u+x_v <=1 for distinct confusable outside words u,v.

Within either reservoir there are no conflicts. Intersection words are
nonconfusable with all distinct words of U, but still have core deletion
costs. At an optimum the deleted core is exactly the union of selected outside
neighborhoods: shared neighbors are charged once. Conversely every independent
code in C∪U is bounded by and can be completed to this objective.

Gain404 gives135093 words. Single-reservoir optima have gain64. Gain65 would
strictly improve the finite134753 construction, but not automatically the
current asymptotic lower bound.

## Product structure

For u=(u0,u1), N_C(u)=N_I0(u0)×N_I0(u1). Each published134753 code is a union
of seven physical rectangles. Cross-reservoir neighborhoods are obtained by
intersecting five-coordinate neighborhoods with their factors and then applying
core/dedup masks. No unrestricted ten-coordinate graph is needed.

## Compact cover gate

Start from a certified134753-clique partition of C∪S2. Attach each new S1 word
to an existing clique with which it is fully confusable. Because S1 is
independent, at most one new S1 word can join a given clique. A matching in
this attachment graph yields a valid clique cover; unmatched words are
singletons. The resulting upper bound is134753 plus the matching deficit.

Only witness clique edges are needed. All additional cross-reservoir conflicts
can only reduce independence. A large attachment deficit is not an impossibility
result: another base partition or actual joint optimization may do better.
Exact comparisons with3.258841^10 decide whether the cover closes this alphabet.

The first tests use the small5360-word published reservoir and15905-word
C30-flipped reservoir, against T^j(Z) and exchanged J. Existing pinned physical
constructions/matching witnesses are reused; no giant core graph is built.
