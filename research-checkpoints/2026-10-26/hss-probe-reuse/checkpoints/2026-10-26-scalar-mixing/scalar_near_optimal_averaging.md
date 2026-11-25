# Standard near-optimal averaging corollary for prescribed scalar bases

**Status:** proved corollary of the independently audited scalar constant-risk
theorem; rectangular unbiasedness also passed advisor analytic review.
This is a standard variance-reduction corollary, not a new averaging method.
It remains outside the frozen00:20 addendum.

The fixed-basis coefficient decoder with rectangular row-orthonormal tree
frames is unbiased:

    E R(A)=P_C A.                                          (1)

The original square-frame induction needs only row orthonormality, not
square invertibility. Here is the precise rectangular argument. At a fine
cut use active/detail coordinates and write the inherited frames as F,P,
with independent conditionally centered fine details G_i,Q_i. The coefficient
formulas are da_i=Y_di F_i^T, dd_i=Y_di G_i^T, ad_i=P_i Z_di^T.
Expected tree-frame isotropy gives their means equal to the respective
diagonal blocks A_da,ii,A_dd,ii,A_ad,ii. Conditional on F,P, the carried
samples obey

    E[Y_next|F,P]=A_aa F,
    E[Z_next|F,P]=A_aa^T P.

Every subtracted term has a centered fine detail in its independent bank.
The remaining coarser decoder is linear and depends only on F,P, so induction
gives(1). At the root F_0 F_0^T=I ensures A_root F_0 F_0^T=A_root; a rectangular
root frame is therefore sufficient. In the six-query algorithm F_0 is the
first two rows of I_3, so is2-by3 with F_0 F_0^T=I_2. All bases are prescribed
independently of both banks throughout.

Now draw t independent complete probe-bank pairs and let Bbar be the average
of their decoder outputs. The fixed class C is linear, so Bbar remains in
exactly the same prescribed rank1 HSS class; averaging causes no rank inflation.
For E=A-P_C A, the independent vectors R_i(E) are centered. Therefore

    E||A-Bbar||_F^2
      =||E||_F^2+(1/t) E||R_1(E)||_F^2
      <=(1+800/t)||E||_F^2.

This uses3t forward and3t transpose products, hence6t TOTAL. Taking
t=ceil(800/epsilon) gives a (1+epsilon) expected squared-Frobenius factor
with O(1/epsilon) total queries independent of depth. This does not imply
the corresponding unknown-basis HSS guarantee or an arbitrary-k result.
