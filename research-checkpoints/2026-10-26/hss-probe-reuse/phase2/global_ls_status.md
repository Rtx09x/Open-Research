# Wider global least squares: exploratory, separate from the proved decoder

Given an orthonormal coefficient basis C_1,...,C_d of the prescribed fixed
class, define the linear measurement map

    M(B)=(B Omega, B^T Psi).

Global least squares minimizes ||M(A-B)||^2 over B in the class. It is exact
on the class whenever its measurement Gram is positive definite. This is a
different decoder from the subtractive LM recursion; the latter's failures
do not transfer automatically.

A sufficient deterministic condition is coercivity

    ||M(B)||^2 >= c ||B||^2   for every B in the class.

Indeed, for E=A-P_C A and D=Bhat-P_C A, M(D) is the orthogonal projection of
M(E) onto the model measurement range, so ||D||^2<=||M(E)||^2/c. Isotropic
probes then give E||A-Bhat||^2 <=(1+2/c)||E||^2. This simple proof does not
require independence between the noise and the random inverse. Without
pointwise coercivity, an expected inverse bound must explicitly address that
correlation; replacing inverse expectation by inverse expected Gram is invalid.

`global_ls_probe.py` builds the complete off-class reconstruction operator
for small matrices, not merely a few random noise inputs. For k=1,L<=3,
120 samples, Haar width4 per bank gave empirical maximum error factors
1.48,1.69,1.84 on coordinate bases and1.47,1.62,1.81 on one dense hierarchy.
These are **finite-sample operator averages, not upper bounds or a theorem**.
The support of this Haar law contains arbitrarily near embedded-square
realizations, so it cannot give a uniform pointwise coercivity constant over
all depths and every realization.

`ordered_global_ls_probe.py` tests the earlier coordinate-faithful three-frame
construction with the new global decoder. Coordinate bases give minimum
measurement-Gram eigenvalue1 through L5, consistent with direct three-color
recovery. Dense45-degree bases with all-plus signs instead give minima
1,0.5858,0.3426,0.2061,0.1286 for L1,...,5. Thus the proposed c=1 extension
already fails at L2, and the apparent decay is a warning against an unproved
absolute constant. No asymptotic no-constant result is claimed from this
finite test. The global least-squares expected relative-error problem remains
open here.

The scripts use explicit dense coefficient atoms only as small reproducible
tests; production polynomial-time implementations could use implicit linear
operators, but none is required for these diagnostics. A minimum measurement-
Gram eigenvalue is not itself an expected approximation-error certificate.
