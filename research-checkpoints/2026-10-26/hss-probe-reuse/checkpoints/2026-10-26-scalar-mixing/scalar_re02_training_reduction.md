# Scalar RE02 reduction after the constant coefficient theorem

**Status:** elementary conditional-expectation reduction, not a proved
query-efficient learner and not full RE02.

Suppose a training procedure uses q forward-plus-transpose matvecs and returns
scalar orthonormal nested row/column bases, defining a fixed linear class C_T.
It may depend on A and its own training randomness. Suppose it satisfies the
ORDINARY, unweighted projection guarantee

    E_T min_(B in C_T)||A-B||_F²
        <= C L min_(H in HSS_rank1)||A-H||_F².                 (1)

Condition on the complete training transcript. Construct the prescribed-basis
width3 frame banks AFTER training, with independent new randomness, and take
three new forward and three new transpose queries. The audited coefficient
theorem is uniform over deterministic prescribed bases and deterministic A;
therefore

    E[||A-Bhat||_F² | T] <=801 min_(B in C_T)||A-B||_F².

Averaging over T gives801 C L times the unrestricted scalar HSS optimum, with
q+6 TOTAL products and no rank inflation. Thus q=O(1) would solve the scalar
version of RE02 (not arbitrary rank). The complex scalar corollary similarly
uses six complex A/A* products.

The extra hierarchy-depth factor in the older4k-query fixed-basis bound is
absent here. Accordingly, the old counterexample to a *weighted* greedy-basis
ledger is not an obstruction to THIS new composition: only(1) is needed.
This does not invalidate that counterexample or assert that its original
weighted argument was correct.

What remains unproved is a q=O(1) black-box learner satisfying(1). Exact-entry
greedy bases do not meet the query model. Existing fresh-probe-per-level
training still incurs depth-dependent query count. A cheap reused-sketch
learner cannot simply assume independent compressed Gaussian sketches, and
its basis quality has not been proved here. The independent coefficient
queries must be counted and cannot be presumed available before the bases
needed to construct their specialized probes are known.

The same reduction works for any stated training quality factor gamma, with
801 gamma in place of801 C L. It does not supply such a learner. For arbitrary
rank k, the constant coefficient theorem itself also remains open outside the
explicit nonmixing-channel subclass.
