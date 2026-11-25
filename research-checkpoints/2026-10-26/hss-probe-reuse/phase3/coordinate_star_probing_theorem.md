# Constant-factor recovery for unrelated block-coordinate HSS bases

**Status:** corollary of established star coloring/direct probing machinery,
with an explicit signed-noise ledger. No new coloring method or priority
claim. This is a known-coordinate fixed-class theorem, not unrestricted RE02.

## Statement

Suppose prescribed row and column nested bases each select an entire k-row
child block as active at every binary node. Row and column choices may be
unrelated. The resulting fixed HSS class C is exactly the class of matrices
supported on a known set of free kxk blocks. There is an exact-arithmetic
randomized decoder using at most6k forward and6k transpose products such that

    E||A−B||_F^2 <= 3 min_(H in C)||A−H||_F^2,   B in C.       (1)

The total query count is12k, independent of depth and number of blocks.

## 1. The physical bipartite support graph has treewidth at most2

Use a row vertex R_i and column vertex C_j for each physical block, with an
edge for each supported block(i,j). Start with the four root-core edges K2,2.
When a hierarchy node is refined, its old active-row/active-column edge(rc)
already exists. Add a new detail-row vertex r' and detail-column vertex c',
and the three edges r'c,r'c',rc'. Thus refinement adds a length-three path
parallel to an existing edge.

Here is a direct width-two tree decomposition, so no unverified graph-class
identification is needed. Root K2,2 has bags {r0,r1,c0},{r0,r1,c1}. For each
refinement attach bag {r,c,r'} to an existing bag containing r,c, then attach
bag {r,r',c'} to it. Every bag has at most three vertices. Every new edge is
covered, and the running-intersection property is preserved. Every child
active-active edge needed at the next refinement is one of its parent's
four existing support edges.

## 2. Use a known six-color star coloring

A proper star coloring has no bichromatic four-vertex path; equivalently,
each two color classes induce a star forest. The established treewidth-t
bound is binomial(t+2,2), hence six colors for our width-two graph. A primary
published proof and attribution to the earlier Fertin--Raspaud--Reed result
are in Albertson et al., *Coloring with no 2-Colored P4's*, EJC11(2004)R26:
https://www.combinatorics.org/ojs/index.php/eljc/article/view/v11i1r26 .
The coloring is computed from the known support, not from entries of A.

For each supported edge(i,j), inspect its bichromatic star component. At least
one endpoint is a leaf. If its row endpoint is a leaf, recover that block from
the forward observation in row i and column color color(C_j). Otherwise
recover from the transpose observation in column j and row color color(R_i).
Make one deterministic choice if both endpoints are leaves. The selected
observation contains exactly one supported target, and no selected scalar-
block observation is reused for another coefficient. This is standard direct
star-coloring recovery, not a newly proposed exact-recovery principle; see
also the sparse Jacobian/Hessian discussion in https://arxiv.org/abs/2505.07308 .

## 3. Signed probes and exact off-support ledger

Choose independent Rademacher signs sigma_j for column blocks and tau_i for
row blocks. For each color c, use k forward columns whose block j is
sigma_j I_k if color(C_j)=c and zero otherwise. Use analogous transpose
probes with tau_i and row colors. Six colors cost6k products per direction.

Let E=A−P_C A, so E vanishes on support. The recovered coefficient error at a
forward-selected edge(i,j) is

    sigma_j sum_(l:color(C_l)=color(C_j)) sigma_l E_il;

the transpose-selected formula is the analogous signed sum in column j.
Distinct source blocks in one coefficient have zero cross expectation.
Define w_ij on off-support blocks to be the number of selected observations
among (forward row i,column color C_j) and
(transpose column j,row color R_i). Since each observation is selected at most
once, w_ij belongs to{0,1,2}. Therefore the exact error identity is

    E||A−B||_F^2 = sum_(off support i,j) (1+w_ij)||E_ij||_F^2.

The off-support residual and supported coefficient error are Frobenius
orthogonal. This proves(1) for arbitrary real blocks. No independence between
different output coefficients is required. The same argument handles complex
blocks with real signs and conjugate-transpose queries.

## What composition does and does not establish

If an exact-entry learner produces such coordinate bases with fixed-class
loss at most2L times unrestricted HSS optimum squared, then independent
coefficient probes above give at most6L times that optimum. Entry-access
learning is not an O(k)-query learner; this composition is not RE02. A general
greedy SVD learner produces dense bases and need not lie in this subclass.

## Reproducibility and scope

`coordinate_star_probing.py` constructs/checks the width-two bag certificate,
finds a star coloring by a small-instance search, checks every bichromatic
P4 and every selected-observation uniqueness condition, and verifies the
exact signed-noise identity. Its coloring search is a test implementation,
not a claimed efficient implementation of the published general theorem.

The stronger6k/factor2 theorem for diagonal-plus-bidirectional physical
forests remains preferable for that narrower subclass. The present12k/factor3
corollary covers unrelated coordinate row/column hierarchies. Dense mixing
produces tied coefficients, not a free block support of this form; the next
note gives an explicit depth-growing obstacle to probing its free envelope.
