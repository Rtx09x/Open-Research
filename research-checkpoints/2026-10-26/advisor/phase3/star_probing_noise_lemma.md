# Known-support star probing: a simple noise corollary

**Status:** analytic audit, not novelty claim. Known sparse matrix probing already uses star coloring. This is a useful fixed-coordinate control, not the dense nested-basis HSS problem.

Let a prescribed block support S be a bipartite graph between row and column block indices, with k×k blocks. Suppose the bipartite graph has a proper star coloring with c colors. For each two-color connected component, select the leaf endpoint of each edge (choose either endpoint for an isolated edge). A selected row endpoint identifies a forward observation (row index, column color); a selected column endpoint identifies a transpose observation (column index, row color). Each such observation is selected at most once: in its bichromatic star, a leaf has degree one.

Use independent row signs τ_i and column signs σ_j. Set Ω_j=σ_j I_k in the channel for the color of column j, and Ψ_i=τ_i I_k in the channel for the color of row i. These require ck forward plus ck transpose products. Recover each supported block from its selected observation, dividing by its sign. Set off-support blocks to zero.

For A=C+E, where C is its coordinate projection onto S, the decoder recovers C exactly. For a forward-selected coefficient (i,j), error is a signed sum of E_iℓ over columns ℓ of the same color as j. Independence of σ makes its expected squared Frobenius error the sum of the individual squared block norms. The analogous assertion holds for transpose-selected coefficients using τ. Coefficient supports are disjoint, so there are no cross terms between different recovered blocks in Frobenius norm.

Each off-support block E_iℓ enters at most one selected forward observation and at most one selected transpose observation. Consequently

    E ||A−B||_F² ≤ 3 ||E||_F² = 3 OPT_S².

No independence between a computed inverse and data is assumed; there is no inverse or recursive carry. The additive1 is the unrecovered off-support residual, and the factor2 is the possible double leakage.

For treewidth≤2, the established star-coloring bound c≤binomial(2+2,2)=6 gives12k total queries. The rectangular coordinate-HSS support must still be proved to have treewidth≤2; the worker's reverse construction adds a three-edge path parallel to an existing edge, starting from K2,2, which supplies that proof. This does not apply to dense fixed-basis coefficient atoms merely by taking their support envelope: those atoms have tied entries, and that envelope need not retain this graph structure.

Primary prior art: Albertson, Chappell, Kierstead, Kündgen, Ramamurthi, *Coloring with no2-coloredP4's*, EJC11(2004)R26, and Gebremedhin etal, *Efficient Computation of Sparse Hessians Using Coloring and Automatic Differentiation*, INFORMS J.Comput.21(2009),209–223. The exact recovery/coloring method is established; only the stated elementary noisy corollary is derived here, without a priority claim.
