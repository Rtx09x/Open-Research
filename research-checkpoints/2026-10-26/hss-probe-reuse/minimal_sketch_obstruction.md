# An exact obstruction to minimal-sketch LM, not to RE-02

**Status:** complete argument; independent algebra audit passed. No novelty claim: this is a concrete specialization of the Gaussian inverse-Wishart integrability threshold to the reused-sketch algorithm. It invalidates s=3k without oversampling, not every depth-independent-query algorithm.

## Statement
Use Algorithm 4.1 of Levitt–Martinsson, with rank exactly k=1, leaf size2, depth L=1, and s=3 Gaussian columns each in Ω and Ψ (six total queries). Its expected squared Frobenius error is infinite on

A = [[0₂, I₂], [I₂, 0₂]].

The optimal rank-1 HSS squared error is2. Hence no finite relative expectation guarantee holds for this parameter choice, already at depth1.

## Proof
Write G=Ω[first leaf,:] and H=Ω[second leaf,:], independent2×3 standardGaussian matrices. Almost surely G has rank2. Choose a measurable unit vector n spanning kerG; let R be a3×2 orthonormal basis of row(G). Write

H = (Hn)nᵀ + (HR)Rᵀ.

Conditional on G, Hn and HR are independent standardGaussian arrays. The algorithm chooses a unit u spanning Hn, so P=uuᵀ has rank1 and depends only on G,Hn. The first term in the leaf discrepancy block is

T=(I−P) H G†,

because A's diagonal leaf block is zero. The other discrepancy term has left range in span(u). The synthesized coarse contribution has the same left range in that leaf. Consequently the row-complement of the output's diagonal leaf is exactly T, and ||A−B||_F²≥||T||_F².

Since nᵀG†=0, the random part in T uses only HR, independent of P given G,Hn. Standard Gaussian second moments therefore give

E[||T||_F² | G,Hn] = tr(I−P) ||G†||_F² = ||G†||_F².

For a2×3 standardGaussian G, E tr((GGᵀ)⁻¹)=∞. An elementary proof avoids citing a moment formula: write G's rows g₁,g₂, decompose g₂ into its projection onto g₁ plus its orthogonal component z. The Schur-complement formula gives ((GGᵀ)⁻¹)₂₂ = 1/||z||². Conditional on g₁, ||z||² is χ² with2 degrees of freedom. Its density is (1/2)e^(−t/2), whose t⁻¹ integral diverges at0. Tonelli yields E||A−B||_F²=∞.

At L=1 the only HSS constraints are rank≤1 on each offdiagonal2×2 block, with unrestricted diagonal blocks. Each I₂ has optimal rank1 squared error1, so E_{1,1}(A)=2.

## Scope and repair
This does **not** refute RE-02. Taking s≥4 for k1 makes this particular inverse moment finite; s=6k in our main baseline is safely oversampled. The defect has nothing to do with depth reuse: it occurs at the leaves. It warns that observed small median error is insufficient to establish an expectation theorem, and that sample constants must be checked before attempting the dependency argument. The published robust algorithm uses a larger constant and is not contradicted.
