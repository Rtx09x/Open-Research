# Unbiased reconstruction with independently known dense nested bases

**Status:** complete induction argument; independent algebra audit passed. This establishes unbiasedness, not the required O(L) second-moment theorem. The bases must be fixed independently before these probes are acquired.

## Construction
At each node use prescribed orthonormal active bases U_i,V_i of dimension k, and orthogonal complements. Generate the forward test Ω top-down: begin with an orthonormal2k-by-2k root frame. At each local split, inherit a k-by-2k active frame F_i and draw a centered orthonormal complement frame G_i in its orthogonal complement, independently over nodes conditional on frames above. For example, multiply any fixed complement by an independent Haar orthogonal k-by-k matrix (a random sign when k=1). Expand through the known V_i and its complement. Generate Ψ independently using the U_i hierarchy.

Every compressed2k-by-2k local test block is orthogonal. Inductively EΩΩᵀ=I: the active-active covariance is inherited; active-detail cross terms vanish by centered complements; distinct detail blocks have zero covariance; each detail block has identity self-covariance. The same holds for Ψ. Query AΩ,AᵀΨ (4k vector products total), then run the Levitt–Martinsson coefficient recursion with prescribed bases, without estimating them. All local pseudoinverses are transposes.

## Fixed linear class
Apply the finest block-diagonal orthogonal changes of coordinates [U_i,U_i-perp] and [V_i,V_i-perp], then group active coordinates a and details d. The class with these fixed nested bases is the orthogonal direct sum of:
- the coarser fixed-basis HSS class in the aa block;
- arbitrary block-diagonal ad, da, and dd blocks.

Consequently its Frobenius projection P is obtained by projecting aa recursively and keeping only the block diagonals in the other three blocks.

## Induction
Write Ω=[F;G] and Ψ=[P;Q] in these coordinates. Here F,P are the coarser tree frames, and G_i,Q_i are independently centered complements conditional on F,P. The two families are independent. Products decompose as

Y_a=A_aa F+A_ad G,       Y_d=A_da F+A_dd G,
Z_a=A_aaᵀ P+A_daᵀ Q,    Z_d=A_adᵀ P+A_ddᵀ Q.

The local coefficient formulas are

D_da,i=Y_d,i F_iᵀ,
D_dd,i=Y_d,i G_iᵀ,
D_ad,i=P_i Z_d,iᵀ.

Taking expectations gives E D_da,i=A_da,ii and E D_ad,i=A_ad,ii from EFFᵀ=EPPᵀ=I and complement centering. For dd, conditional centering gives E(F_j G_iᵀ)=0, E(G_j G_iᵀ)=0 for j≠i, while G_i G_iᵀ=I. Thus E D_dd,i=A_dd,ii.

The carried products are

Y'=Y_a−diag(D_ad)G,
Z'=Z_a−diag(D_da)ᵀQ.

Condition on F,P. Each term of D_ad depends only on P,Q; each term of D_da depends only on F,G. Averaging the independent centered fine-level complements G,Q gives

E[Y'|F,P]=A_aa F,     E[Z'|F,P]=A_aaᵀ P.

The coarser decoder is linear in its two product arrays and depends on the tests F,P and the prescribed bases, not on the discarded fine complements G,Q. Hence its conditional mean is exactly its output on the true coarser products. Induction proves

    E R(A) = P(A).

The root is exact because its square orthogonal test is invertible. Frames and decoder matrices are bounded for fixed N, so all expectations and conditioning are legitimate; no inverse-Wishart tail issue occurs. Exact recovery on the fixed class also follows.

## What remains
Unbiasedness does not imply small variance. Orthogonal coefficient subspaces give

E||A−R(A)||² = ||A−P(A)||² + E||R(A−P(A))||².

The unresolved requirement is a depth-linear bound on the final term. An expected sketch-energy potential is being tested; its cross term has not yet been proved nonnegative at all carried levels. No claim for unknown adaptive bases follows from this lemma.
