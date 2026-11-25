# Wider-frame follow-on: no constant-factor theorem yet

The main square-frame fixed-basis theorem is independently audited. The next
different target suggested by the advisor is a constant-factor fixed-basis
coefficient decoder with s>=4k columns per bank (8k total at s=4k). This would
be more useful for composing with an O(L) basis-quality estimate.

Any proof must include the unused s-2k probe directions. A full complement
of dimension d=s-k gives normalized state blocks X,Z of size k-by-k,
Y of size k-by-d and W of size d-by-k. The single-live-branch flux still has
energy `||X-Z||^2+||Y||^2+||W||^2`. With a full Haar completion, the same
retained covariance calculation suggests the sharper cap
`EZZ^T <= c^2 I/d`, and thus pure-branch sample energy at most
`[1+2rho+2sqrt(rho)]c^2`, rho=k/d. This is a **sample-energy** observation,
not a summable coefficient-error theorem.

To look for the missing summable ledger, small numerical cutting-plane
searches tested a common quadratic branch potential built from
`||X-Z||^2`, separate detail energies, `||Z||^2`, and their mixed term.
For k=1,s=4, a169-pair angle grid already makes this restricted ansatz
infeasible, both when averaging only one bank and when averaging both.
Scripts and logs are `wide_branch_potential_search.py`, its semidefinite-only
diagnostic copy, and `wide_both_bank_potential_search.py`.

These sub-second numerical feasibility tests refute neither a richer
history-dependent potential nor the wide-frame algorithm. In particular,
they are **not** a matrix counterexample and not an impossibility result.
The current proven result remains4k queries and O(L) fixed-class error.
