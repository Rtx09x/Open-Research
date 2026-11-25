# Precise new one-bank transport target and remaining anchor correction

**LATEST UPDATE:** `fixed_basis_bound.md` proves one-bank constant5 and the
full prescribed-basis two-bank sector bound20 for arbitraryk with Haar
complements; the independent advisor audit passed. Thus this file is a
historical failed-shortcut record, not the current unresolved fixed-basis target.
Unknown bases, the full-HSS comparator, and sharp constant2 remain unresolved.

**UPDATE: the proposed one-bank <=1 lemma below is now exactly REFUTED.**
The independent rational verifier `verify_one_bank_counterexample.py` constructs
L=4,N=32 with initial energy one and final energy 913/625 for **every** transpose
sign assignment. See `one_bank_counterexample.md`. Retain the original target
below only as a record of a failed shortcut, not as a consultation request.
The complete correlated-sector uniform bound remains open.

## Candidate one-bank lemma

Fix known left/right nested bases and **fix a realization of the complete
forward square tree frame Omega** (2k columns). Draw only the transpose square
tree frame Psi with independent Haar complement orientations. Start with
arbitrary forward sample array `Y0` **independent of Psi** and `Z0=0`; no
assumption that these are consistent products of the same matrix is made.
Run only the fixed-basis coefficient/carry recursion:

    D_da,i = Y_d,i F_i^T,
    D_ad,i = P_i Z_d,i^T,
    Y_next = Y_a - diag(D_ad,i) G,
    Z_next = Z_a - diag(D_da,i)^T Q.

Here F_i,G_i are the fixed local active/detail forward frames; P_i,Q_i are the
random transpose frames. Candidate conclusion, at every cut t:

    E_Psi [||Y_t||_F^2+||Z_t||_F^2] <= ||Y0||_F^2.

An even stronger candidate is expectation-monotonicity across cuts **under
this independent-bank initialization only**. Exhaustive k=1 tests through
L=3 support it: fixed arbitrary forward frames, the entire quadratic operator
on all `N*2` initial data coordinates, and all transpose signs. At L=3 this
enumerates 16,384 assignments. Largest eigenvalues at every cut are 1 within
4.4e-13; all consecutive expected energy differences are nonpositive within
roundoff. This is evidence, not proof. Pointwise contraction is false: tested
fixed-sign examples exceed factor 5 at L=4.

Files: `one_bank_transport.py`, `one_bank_transport_results.json`, and optional
saved Gram matrices. The candidate is symmetric upon exchanging query banks.

## Why this could help, and exactly what it does not handle

The exact fine-sign decomposition reduces a whole ad-column sector j to

    Y = (a - e_j b) g_j,       Z=0,
    a_j=0,                    b=P_j P^T a,

for k=1; the block formula uses an injection J_j and block matrices. Here g_j
is the forward detail frame. After conditioning on the forward bank, the
direct term `a g_j` is independent of the transpose bank and fits the candidate
lemma. The correction `-e_j(P_j P^T a)g_j` does **not**: its amplitude is a
function of the transpose frames at many nodes. Neither one-bank contraction
nor the Pro isolated-subtree theorem may simply be applied to that term while
conditioning away its dependence on ancestor orientations.

The original whole sector has initial expected energy at most `2||a||^2`,
since `a_j=0` and `E||P_j P^T a||^2 <= E||P^T a||^2=||a||^2`. Later energies
can increase (the exact rational counterexample in the frozen dossier is such
an ad sector), so an arbitrary-state monotonicity induction is unavailable.

A useful next deliverable is a direct uniform bound for the complete ad/da
sector, including the
   correlated anchor correction, together with dd sectors.

For the full fixed-basis target the relevant conclusion is a depth-independent
bound at each cut; no consecutive monotonicity is required. Even completing
that fixed-basis analysis leaves unknown-basis selection and the O(L^2)
composition caveat for unrestricted RE-02.
