# Explicit minimum fixed queries by opposite leaf pairing

This is an elementary construction within classical minimum 3-edge-connectivity augmentation, not a claim to have invented that problem or its optimal algorithms.

Let C be a nontrivial finite loopless bridgeless cactus, permitting parallel two-cycles. Let L denote both the set of degree-two nodes and, when used numerically, its cardinality. L≥2. Fix a cyclic orientation for each cycle. Root the cycle-node incidence tree at any cactus node. Traverse a cycle starting at its parent node, visit its other nodes in the fixed cyclic order, and recursively traverse each child cycle when its attaching node is visited. Record each degree-two node once. If the root has degree two, record it before its unique child cycle. Call the resulting circular sequence ℓ₀,…,ℓ_(L−1).

## Consecutive-shore lemma

Every two-edge-cut shore contains a nonempty proper circular interval of this leaf sequence.

Each two-edge cut consists of two edges of one cactus cycle Z. Deleting them separates the nodes of Z into two complementary node-containing arcs. Every subcactus attached at a node of Z remains on that node's side. In the recursive traversal, all descendants attached at a given cycle node occupy one consecutive segment, and the segments at successive nodes of Z occur in Z's cyclic order. If Z is not the root cycle, the part outside Z and its descendants attaches at its parent node; in the *circular* traversal this outside segment joins the segment at that node across the end/start boundary if necessary. Consequently the leaves on either arc, including all attached components, form complementary circular intervals.

Neither interval is empty. One way to see this without an embedding argument: the cycle-node incidence graph is a finite tree whose leaves are exactly the degree-two cactus nodes. Each side contains a node of Z; its attached branches either contain such a leaf, or the cycle node itself is degree two. Equivalently use the established fact that every two-cut shore contains a degree-two node. Each side therefore contains at least one leaf and neither contains all leaves.

## Antipodal matching lemma

In a circular list of even length 2h, join position i to i+h for 0≤i<h. Every nonempty proper circular interval has a matching edge crossing its boundary.

Take the smaller of the interval and its complementary interval; it has size at most h and is itself consecutive. No two positions in a consecutive interval of at most h positions are antipodal: after rotating its first position to 0, their integer difference is at most h−1. Every vertex of this smaller interval is therefore paired outside it. In particular at least one matching edge crosses the original boundary.

## Even and odd constructions

For even L, apply the matching lemma directly to the cyclic leaf order. For odd L, duplicate one leaf immediately next to itself, giving L+1 positions. Every shore includes either both copies or neither, so its membership remains a nonempty proper circular interval. Apply the matching lemma to this expanded sequence, then interpret duplicate positions as the same node.

No self-pair results: odd L≥3, hence the two duplicate positions are adjacent and their distance is 1, whereas opposite positions have distance (L+1)/2≥2. The only repeated node is the duplicated leaf; its two partners are distinct, so no query edge is duplicated either. Thus the result contains exactly ceil(L/2) distinct non-self query pairs in all cases.

Choose one accessible original vertex in each leaf blob. Every two-cut shore is a union of blobs, so the corresponding original query crosses it exactly when the cactus query does. All two-edge cuts are crossed, and hence the formal graph plus queries is 3-edge-connected. By the electrical structural theorem, these queries identify every edge deletion for generic weights.

For optimality, the L degree-two singleton cactus nodes lift to L disjoint two-cut shores. Each query has only two endpoints, so it can meet at most two of these disjoint shores. At least ceil(L/2) queries are necessary. The construction attains this bound.

If the cactus is a single node, there are no two-edge cuts and any one distinct-terminal query is generically identifying. The bound is then one, because there is more than one fault hypothesis.

This proof supplies a direct and easily verified optimal fixed design without invoking a general augmentation optimizer, while leaving the classical attribution boundary intact.
