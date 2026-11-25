# A depth-independent robust theorem for a restricted block-tree HSS class

**Classification:** restricted theorem, not RE-02. The support/bases are known; comparator is the fixed block-tree subspace. Graph-coloring substitution is an existing recovery idea; novelty of the randomized robust bound is not established.

## Class and query budget
Let M=2^(L+1), N=Mk, and partition coordinates into M consecutive k-blocks. On these blocks build a tree T by recursively joining the first block of the left child interval to the first block of the right child interval, including the finest pairs. Let F_T consist of all block matrices supported on the diagonal blocks and both orientations of T's edges. Its diameter D is at most2L+1.

Every H in F_T is rank-at-most-k HSS on the requested dyadic tree with2k leaves: for each nonroot dyadic interval I, every edge from I to its complement meets its single representative k-block inside I. Thus both the external block-row and block-column have rank≤k. Diagonal2k leaf blocks are unrestricted, since each leaf contains two diagonal k-blocks and the joining edge in both directions.

There is an algorithm using **2k forward plus2k transpose matvecs**, independent of L, producing B in F_T with

E||A−B||_F² ≤ (D+1)||A−P_T(A)||_F² ≤ (2L+2)||A−P_T(A)||_F²

for every fixed A, where P_T is support masking (the Frobenius-orthogonal projection onto F_T). The arithmetic is polynomial; the flow solve is O(Nk).

## Algorithm
Fix a proper bipartite color c(i) in{0,1} of T. Independently draw signs σ_i,τ_i in{−1,+1}, one pair per block vertex. Form Ω,Ψ in R^(N×2k) by putting σ_i I_k, respectively τ_i I_k, into the color-c(i) k-column slot of their ith block-row and zeros in the other slot. Query Y=AΩ and Z=AᵀΨ.

Estimate diagonal blocks from the same-color forward channel:

B_ii = σ_i Y_i,color(i).

For each c=0,1 solve an oriented tree divergence system. Vertices of color c are treated as row vertices; those of color1−c as column vertices. Let

d_i = τ_i Y_i,1−c(i) if c(i)=c,

d_j = −σ_j Z_j,1−c(j)ᵀ otherwise.

The unknown block on an edge oriented row i to column j is b_ij=τ_i σ_j B_ij. Tree substitution uniquely solves divergence(b)=d (root and repeatedly eliminate leaves), and then B_ij=τ_iσ_j b_ij. All unsupported blocks are zero.

Even for arbitrary A, the divergence is consistent: its sum is zero, since each opposite-color block A_ij contributes +τ_iσ_j A_ij at row vertex i and the negative at column vertex j. Same-color blocks do not enter these channels.

## Exact error identity
Write A=H+E, H=P_T(A). Linearity and exact recovery on F_T reduce the support error to E. Off-support E is Frobenius-orthogonal to B−H. For a diagonal block,

B_ii−H_ii = Σ_{j≠i,c(j)=c(i)} σ_iσ_j E_ij.

Independence makes its expected squared norm the sum of the corresponding ||E_ij||_F².

An off-support opposite-color block E_ij acts on the divergence system as a virtual directed edge from i to j, carrying τ_iσ_j E_ij. Its unique tree-flow reconstruction puts that block, with signs, along the path from i to j. Its total squared coefficient energy is dist_T(i,j)||E_ij||_F². For any distinct ordered pairs(i,j) and(i',j'),

E[τ_iσ_j τ_i'σ_j'] = δ_(i,i') δ_(j,j').

The final edgewise factors τ_tail σ_head have square1 and therefore disappear from each edge's squared norm. All cross terms between distinct perturbation blocks vanish. Consequently the **exact expectation formula** is

E||A−B||_F² = ||E||_F²
 + Σ_{off-support,c(i)=c(j)} ||E_ij||_F²
 + Σ_{off-support,c(i)≠c(j)} dist_T(i,j)||E_ij||_F².

Bounding each weight by D proves the theorem. This is arbitrary-noise robustness, not just exact recovery; it does not assume E random.

## What is still missing
F_T is a strict known-coordinate subclass of HSS. E_T(A) can be much larger than E_HSS(A); hence this theorem cannot be relabeled the requested result. Arbitrary known dense nested bases already require a more general network argument. Unknown adaptive bases from reused Gaussian sketches add the original dependency barrier.

## Sharpness for this estimator, and an explicit scope warning
For k=1 choose i=M/2−1 and j=M−1 (zero-based indexing). Their tree distance is2L+1, and their colors differ. For A=e_i e_jᵀ, support masking gives0, so the fixed-tree optimum is1. Every sign realization sends a unit-magnitude coefficient along every edge of their path; thus ||A−B||_F²=2L+2 exactly. The linear depth factor is sharp for this estimator.

Crucially, this same A is globally rank1 and hence is itself in the **full** rank-1 HSS class. Its full HSS optimum is0. This explicit example proves that the fixed-tree algorithm is not an algorithm for RE-02 without a separate valid basis-selection mechanism. The restriction is substantive, not just a proof artifact.
