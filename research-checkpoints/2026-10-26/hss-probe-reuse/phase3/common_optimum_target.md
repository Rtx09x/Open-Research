# Precise remaining bridge to the unrestricted comparator

**Update22:24UTC:** the weighted sufficient condition below is now exactly
refuted for the full-entry local greedy-SVD learner, by the independently
audited family in `external_continuation_audit.md`. The bound(W) itself remains
valid. On that family its RHS isquadratic while actual fresh coefficient risk
is4L, so the failed certificate is not an algorithm lower bound. A more precise
remaining condition is the learner-aware PSD risk operator described there.


The independently audited theorem is conditional on supplied nested bases.
They may depend on A or on an earlier training transcript, provided the new
tree-frame orientations are drawn independently afterward. If training uses
q_train queries, the total is **q_train+4k**, not4k. No bound on q_train or on
the quality of those learned bases has been established here.

## A finer weighted oracle bound

Let E_ell be the orthogonal off-model ad/da/dd residual born at fine-to-coarse
level ell, with ell=1 finest and ell=L coarsest. The recursive aa component
contains later-born residuals. Fine-sign orthogonality applies to the entire
output, not just carried samples. At its birth, immediate coefficient energy
is at most2||E_ell||_F^2: an ad column costs at most its input energy; a da row
uses its complete forward-detail decomposition; a dd block costs at most one
copy from each bank. Every subsequent local coefficient stage and the root
cost at most20||E_ell||_F^2 by the sector argument. Hence

    E||A-B||_F^2
      <= sum_{ell=1}^L [3+20(L-ell+1)] ||E_ell||_F^2.       (W)

The unweighted theorem follows because sum||E_ell||^2 is the fixed-class
projection residual. Equation(W) makes a more specific common-OPT target:
find/learn bases for which this **weighted** residual is O(L) times the full
rank-k HSS optimum, rather than first bounding the unweighted residual by
O(L)OPT and then multiplying it by another O(L).

The known generic greedy proof bounds each level by a constant times the
original HSS optimum, using contraction of the optimum under block-diagonal
compression. Summing those bounds with the weights in(W) gives O(L^2), so it
does not establish the needed weighted statement. No shortcut around that
gap is claimed.

## Why merely improving the constant20 is insufficient

The square-frame coordinate subclass has examples with coefficient error
linear in depth, so this particular decoder cannot have an absolute constant
fixed-class factor just by tightening its analysis. A genuinely different
possibility is wider probes with a constant-factor coefficient decoder, or a
joint basis/estimation proof charging errors to one common optimal residual.

The advisor suggested s>=4k local frames. A complete analysis must track the
unused s-2k-dimensional channel; the square four-block state cannot be reused
unchanged. A possible transmission/dissipation mechanism uses the ratio
rho=k/(s-k), but neither a summable coefficient ledger nor a constant-factor
wide-frame theorem has been proved in this phase.
