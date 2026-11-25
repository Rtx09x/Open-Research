# Exact reduction of dense fixed-basis robustness to a potential inequality

Scope: all bases are independently fixed before the4k orthonormal-frame probes. This is not yet proved for the full HSS problem or even for all fixed dense bases.

Let E=A−P_fixed(A). The decoder is linear, exact on the fixed class, and outputs that class. Hence its error is

    ||E||² + ||R(E)||².

The lifted local discrepancy factors and root factor occupy mutually Frobenius-orthogonal subspaces. Thus ||R(E)||² is exactly the sum of their squared norms, without a factor L from Cauchy–Schwarz.

At a level in active/detail coordinates, write the tests as [F;G] and [P;Q], with local [F_i;G_i] and [P_i;Q_i] square orthogonal. The coefficient estimates and carried products are

    D_da,i = Y_d,i F_iᵀ,   D_dd,i = Y_d,i G_iᵀ,
    D_ad,i = P_i Z_d,iᵀ,
    Y' = Y_a − diag(D_ad) G,
    Z' = Z_a − diag(D_da)ᵀ Q.

For S=||Y||²+||Z||² and

    C=<Y_a,diag(D_ad)G> + <Z_a,diag(D_da)ᵀQ>,

exact arithmetic gives

    S'=S−||Y_d||²−||Z_d||²+||D_ad||²+||D_da||²−2C <= S−2C.

Also ||D||²=||D_da||²+||D_dd||²+||D_ad||² <= S. At the root ||D_root||²<=S_root. Initial isotropy gives E S_initial=2||E||².

**Sufficient missing lemma:** for every fixed E orthogonal to the prescribed nested-basis class, the carried random arrays satisfy E C>=0 at every level.

If true, expected S never increases, and summing L nonroot levels plus the root proves

    E||A−R(A)||² <= [1+2(L+1)] ||A−P_fixed(A)||².

This is a clean O(L) fixed-basis result. The implication above is proved; the sufficient missing lemma is not.

At the finest level E C=0 follows directly by complement centering and the zero cross-block diagonals of E in active/detail coordinates. At later levels the carried arrays contain correlated lower-level errors, so the same conditioning argument cannot simply be repeated.

## Tests and their limits
`potential_operator.py` computes the full quadratic form in E of each C and S'−S. For one random k1,L2 basis system, exhaustive averaging over all4096 frame-sign choices makes C positive semidefinite up to roundoff and S'−S negative semidefinite on the fixed-model orthogonal complement. A depth3 sample average has small negative C eigenvalues; these can arise from sampling noise. `conditional_ledger.py` integrates finest signs analytically and enumerates coarse signs, checking selected putative bad directions without this selection bias. None of these numerical tests proves the general inequality.

## Correction: the stronger cross-term shortcut fails numerically
Depth3 exact-sign averaging after analytic elimination of finest signs produces a last-level cross mean approximately−0.002273546944 on a selected fixed-model residual. This is a counterexample candidate to E C>=0, not a Monte Carlo fluctuation. A rational/interval certificate is still needed before labeling the negative decimal an exact theorem. The potential nevertheless decreases from1.5457328657 to1.4371352319 because the omitted nonnegative discarded-energy terms dominate. The next candidate inequality is therefore the **weaker direct contraction** E(S'−S)<=0; its sufficiency for the same O(L) bound is unchanged.

## Correction: consecutive contraction also fails numerically
The complete depth3 quadratic-form calculation (`exact_conditional_operator.py`) analytically averages16 finest signs and exhaustively averages the remaining12 signs. At the last carried level, the largest residual-space eigenvalue of E(S'−S) is approximately0.128978207523. Its cross form has minimum approximately−0.077441282002. These non-tiny margins kill both proposed local monotonicity shortcuts numerically; no general theorem is claimed from floating-point spectra.

The actually sufficient remaining conjecture is **uniform rather than monotone**:

    for every level l, E S_l <= 2 ||A−P_fixed(A)||².

The full depth3 calculation returns maximum eigenvalue2 for each checked carried level, within roundoff. A proof would need an augmented energy ledger or global tree-path argument that allows observed energy to increase locally. It cannot simply repeat a local contraction assertion.
