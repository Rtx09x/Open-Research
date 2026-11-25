# Scalar constant-factor known-basis approximation from six queries

**Status:** complete restricted proof; independent advisor analytic audit PASS
(26 October 2026), with all four exact Fraction controls replayed separately.
This is NOT unrestricted RE02, not arbitrary rank k, and not a statement
about bases learned from the same queried sketches. No novelty is claimed.
It is outside the frozen00:20 addendum.

## Theorem

Fix arbitrary real scalar (k=1) orthonormal nested left/right bases on a
binary hierarchy. Let C be their prescribed linear HSS class. Generate two
independent generic Haar tree-frame banks of width3, using the explicit
full-complement construction already audited for this law. Run the fixed-
basis LM local coefficient decoder, with row-frame transposes as local
inverses and forward orthonormal root decoding.

For every deterministic A, the conclusion is

    E||R(A)||_F^2 <=800||A||_F^2,
    E||A-R(A)||_F^2 <=801 min_(B in C)||A-B||_F^2.          (1)

Exactly3 forward and3 transpose vector products are used, independent of
depth. The output stays in the prescribed scalar-rank HSS class. Arithmetic
is ideal exact arithmetic. Constants are intentionally conservative.

Dependencies: the audited scalar inverse-column mean-square bound<=5;
`wide_inverse_column_fourth_moment.md` (fourth norm<=50000, audited);
the standard deterministic-input tree-sketch fourth moment<=3; and the
exact central-sign sector identities already used in `fixed_basis_bound.md`.

## 1. A full-output one-bank rank-one input lemma

At any carried cut, let a be a deterministic spatial row-coordinate vector,
and let q be a unit row vector depending only on the entire forward bank.
It may depend on a finer forward detail frame as well. Initialize samples
Y=a q,Z=0 and apply the remaining fixed decoder. Then

    E||output(Y,0)||_F^2 <=5||a||^2.                       (2)

Decompose a in the prescribed orthonormal left hierarchical wavelet basis,
including the two root-active vectors. A detail component a_v at node v
creates no coefficients below v. At v it creates

    c_v=a_v <q,F_v>,       d_v=a_v <q,G_v>,

as its da and dd coefficients. Its entire output is exactly

    c_v V e_(da,v)+d_v e_(dd,v).

The inverse-column identification follows from the same original-sample
triangular system as before: the da coefficient causes the transpose carry
-c_v Q_v; dd causes no feedback. The two displayed vectors have orthogonal
coefficient supports because V e_(da,v) is supported at its own da coordinate
and strict ancestors, not its own dd coordinate. Moreover

    c_v^2+d_v^2<=a_v^2,       ||V e_(da,v)||^2>=1.

Therefore its squared output norm is pointwise at most
a_v^2||V e_(da,v)||^2, whose expectation is<=5a_v^2. This does NOT assume
c_v independent of the inverse column; the amplitude bound is pointwise.

Different wavelet births are orthogonal in expected TOTAL coefficient energy.
For two distinct births choose the deeper one if nested, or either if
disjoint. Its strict-ancestor output is linear in its own centered row detail
Q_v. Its coefficients c_v,d_v depend only on the forward bank. The other
birth's output never uses that chosen row detail. The chosen birth-coordinate
entries cannot overlap the other output (which is supported at its own birth
and ancestors). Hence the chosen independent central row sign kills all
possible overlaps. A root-active input is independent of all row-detail signs
and has no finer coefficient support; it is covered by the same cancellation.
Its root decoding norm is at most its input norm. Summing squared deterministic
wavelet amplitudes proves(2).

The symmetric input Z=a q,Y=0, with q depending only on the transpose bank,
has the same bound. At its column-wavelet birth it creates only c_v V e_(ad,v);
root transpose-only data are ignored by the specified forward root decoder.
The symmetric central-sign argument uses the forward detail signs.

This lemma is deliberately for a common unit q times a deterministic spatial
vector. It does not claim a conditional bound for arbitrary forward-dependent
sample arrays with random wavelet magnitudes.

## 2. One whole off-diagonal ad column, including its correlated anchor

At a fine cut express the physical input in local active/detail coordinates.
For an ad column j let a=A_ad[:,j] with a_j=0. Let P be the stacked inherited
row frame and P_j its jth unit row. The exact carry is

    Y=(a-e_j B_j)G_j,    Z=0,    B_j=P_j P^T a.            (3)

The first source a G_j satisfies(2), because G_j is a unit vector depending
only on the forward bank. Thus its full COARSER output energy is<=5||a||^2.

The second source is the strict-ancestor output of an ad inverse column born
at the eliminated node j, multiplied by B_j (up to an irrelevant sign).
This is a frame-adapted pure forward-detail source, not an independent
physical sample. Dropping the inverse column's unit birth coordinate only
reduces its norm. Cauchy–Schwarz and the two fourth moments give

    E[B_j^2 ||(V e_(ad,j))_strict ancestors||^2]
      <=sqrt(E B_j^4 E||V e_(ad,j)||^4)
      <=sqrt(150000)||a||^2.                             (4)

Here |B_j|<=||P^T a|| pointwise and E||P^T a||^4<=3||a||^4.
No independence of B_j and the inverse column is asserted.

The Hilbert-space triangle inequality, or the simpler two-term bound, yields

    E||coarser output of this ad sector||^2
      <=2(5+sqrt(150000))||a||^2 <785||a||^2.             (5)

The da row sector is symmetric and has the same conservative bound.

## 3. One off-diagonal dd entry

For scalar M=A_dd[i,j], i!=j, the exact carry is the sum of two pure detail
sources

    Y_j=-(P_j Q_i^T M)G_j,      Z_i=-(F_i G_j^T M)Q_i.

They are strict-ancestor parts of two corresponding inverse columns. Each
scalar amplitude is bounded by |M| pointwise, regardless of dependence.
The inverse-column second moment<=5 and the two-term squared-norm bound give

    E||coarser output of this dd sector||^2<=20|M|^2.       (6)

Diagonal ad,da,dd local terms have zero carry by local row orthogonality.

## 4. Recursive total-output energy ledger, without a depth sum

At the chosen fine cut extract independent central signs from each fresh
G_j and Q_i. Conditional on all coarser frames, carried aa data have character
1, ad column j has character sigma_j, da row i character tau_i, and off-
diagonal dd entry(i,j) character sigma_j tau_i. The entire subsequent decoder
uses only coarser frames, so these carried sectors are orthogonal in expected
TOTAL COARSER coefficient energy. The statements(5)–(6) bound whole ad columns
and da rows, not individual entries with uncontrolled cross terms.

The aa carry is exactly the consistent queried data of A_aa on the coarser
hierarchy with the same width3 probe law. Hence, assuming the bound800 at
the coarser hierarchy, its expected coarser output energy is<=800||A_aa||^2.

The fine coefficients have disjoint Frobenius support from all coarser
coefficients. They vanish for aa input. For arbitrary non-aa input, their
expected total squared energy is at most

    ||A_ad||^2+||A_da||^2+2||A_dd||^2
      <=2||A_non-aa||^2.                                (7)

Indeed da/dd are orthogonal projections of the forward detail samples onto
F_i,G_i, while ad is a contraction of transpose detail samples. Expected
tree-frame isotropy gives the displayed energies of those samples. This
does not require independence of the local frame and the samples.

Combining(5)–(7), the non-aa fine-plus-coarser contribution is less than
787||A_non-aa||^2, whereas aa contributes at most800||A_aa||^2. Their input
energies add orthogonally. Thus the induction takes the MAXIMUM constant800,
not a sum over depth. The root-only base case is an orthonormal contraction.
This proves the first inequality(1).

Finally R is linear, exact on C, and outputs in C. With E=A-P_C A,

    ||A-R(A)||_F^2=||E||_F^2+||R(E)||_F^2,

which yields the second inequality(1).

## Boundaries

This argument is scalar and depends on bases prescribed before both banks.
It cannot be combined with an unproved query-efficient unknown-basis learner
or declared relative to unrestricted HSS optimum. A rank-independent matrix
fourth-moment/inverse-column substitute would need a new proof. Nor is the
bound a finite-precision guarantee. The analytic proof audit is distinct
from formal verification, peer review, literature-priority assessment, and
the following finite implementation controls.

## Reproducible controls

* `verify_branch_doob_exact.py`:512 finite full-frame paths, exact conditional
  future mean/Doob differences/common-mode variation invariance.
* `verify_one_bank_output_signs_exact.py`:64 row-sign assignments and8
  deterministic row-wavelet inputs, exact zero off-diagonal full-output Gram.
* `verify_correlated_sector_signs_exact.py`:256 fine-sign assignments and21
  whole sectors under actual physical queries, with correlated anchors intact,
  coarser frames unchanged, and exact Walsh Gram256I.
* `verify_anchor_inverse_identity_exact.py`:8 complete ad columns matched to
  the independently built original22-by22 triangular inverse and coarse
  pure-detail decoder. These four controls use Fraction arithmetic only.
* `test_scalar_wide_reconstruction.py`: actual counted forward/transpose
  products, dense/coordinate bases throughL5, exact-on-class and output-class
  numerical checks. The known width2 long-route baseline reaches factor12
  atL5; width3 sample mean there was2.64. Numerical results are not the proof.
