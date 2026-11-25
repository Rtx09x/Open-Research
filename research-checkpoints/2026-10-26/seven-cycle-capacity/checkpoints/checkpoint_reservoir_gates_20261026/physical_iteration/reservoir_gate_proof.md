# Ten independently verified reservoir obstructions

For each of ten explicitly specified independent length10 codes Z of size134753,
the restricted physical macro-alphabet `I0² ∪ Z` has Shannon capacity exactly
134753. This is **not** an upper bound on C7, nor on the simultaneous union of
three or more reservoirs. No new numerical lower bound or priority is claimed.

## Independent physical codes

The pinned published data supply I0 and X, each367 independent length5 words,
the eight private centers R, and transversals H,V. Set B=A\R, where A is either
I0 or the literal C30-flipped367-word code recorded in the certificate. Partition
X into X0,XH,XV according to closed confusability with H,V; no X word conflicts
with both H and V. The seven disjoint independent rectangles are

    B×B, R×X0, H×XH, V×XV, X0×R, XH×V, XV×H.

Their union has `359² + 2·8·367 = 134753` words. The verifiers independently
check every factor's physical independence and separation of each rectangle
pair in at least one coordinate block. They do not infer admissibility solely
from cardinalities or a stored seven-profile.

For each A, four codes are formed by applying T^j to both five-coordinate
blocks, j=0,1,2,3, where

    T(a,b,c,d,e) = (2-b,d,a,2-c,e) mod7.

T is a coordinate permutation followed by coordinate reflections/translations,
so it preserves physical confusability. One additional code for each A applies
the eight published exchanges to its T image. Each inserted word's full
neighborhood in the pre-exchange code is checked to be exactly the prescribed
removed word; inserted words are checked mutually independent. Thus all ten
Z codes are physically independent, with no stale changed-base overlap counts.

The original data, rectangle construction, T map, and exchanges retain their
published attribution in `published/NOTICE` and `published/LICENSE`. The
C30-flipped physical seed and these matching witnesses are this iteration's
finite artifacts; publication novelty has not been established.

## Matching and clique partition

Fix one Z and let S=Z\I0². The certificate gives a matching of size `|S|-64`
between S and I0², where every matched pair is physically confusable. All
matching endpoints are checked unique, and every edge is checked directly in
ten coordinates. The unmatched words are singleton cliques. Hence the full
alphabet has a clique partition of size

    |I0²| + |S| - (|S|-64) = 367² +64 =134753.

It also contains the independent134753-word code Z. For every positive m,
the m-fold product of this clique partition bounds independence by134753^m;
Z^m attains that number. This proves the exact restricted macro-capacity.

## Reproduction and evidence

`reservoir_orbit_compact.json.gz` stores the two literal main codes, source hash,
the ten recipes, and all matching targets. The outside-reservoir order is
reconstructed deterministically from the physical rectangles; no millions of
duplicate words need be stored. The2,539,346-byte certificate has SHA256

    a7961fa477d3d4ad6bacb875de2568cc27741d38294850c4003683913c88bb61

Python standard library verification:

    python verify_reservoir_matching_gate.py --compact

The local verifier completed in7.93seconds. An independent advisor checker,
with no worker imports, separately passed all ten cases, physical conditions,
exchanges, matching edges, and clique partitions. Its original source and
result are retained in the frozen packet. No optimization solver or numerical
infeasibility assertion is trusted by either checker.

The earlier Hall-deficiency interpretation was useful for proposing the
matching: maximizing an independent code inside a union of two known independent
codes is bipartite matching. This standard reduction appeared in the partial
accepted Extra High response before that run timed out; it is not claimed new.
