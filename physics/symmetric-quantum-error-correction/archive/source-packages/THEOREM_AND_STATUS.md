# An unrestricted dipole–quadrupole cubic moment inequality and a rational 35-qubit cut

**26 October 2026.** Scope: every complex rank-two projector on the fully symmetric spin-`j=n/2` representation. The original `n_min(3)` interval **remains `35 <= n_min(3) <= 37`**. No length-35 or length-36 impossibility certificate, and no new physical code, is claimed. Exact arithmetic validates the new inequality/cut *against saved numerical pseudo-moment data*; this does not certify these saved data as feasible points of all earlier cones. External priority and review are unestablished.

## Theorem 1 (unrestricted rank-two projector cubic constraint)

Let `N=n+1`, `j=n/2`, `c=j(j+1)`, `P=P*=P^2`, `Tr(P)=2`, and

`Z = integral_SU2 (U P U*)^(tensor 3) dU`.

The rank enumerators are `a_r=(N/4) sum_mu |Tr(P T_{r,mu})|^2`, with HS-orthonormal irreducible spin tensors, so `||Pi_r P||_HS^2=4a_r/N`.

On the spin representation define `Q_ab={J_a,J_b}/2 -(c/3) delta_ab I`, and

`O = sum_{a,b in {x,y,z}} Q_ab^(1) tensor J_a^(2) tensor J_b^(3)`.

Then the exact inequality is

`|Tr(Z O)|^2 <= (64/405)c^3(4c-3) a_1^2 a_2`.                      (1)

All logical amplitudes and phases may be complex; no code constraints or symmetry ansatz are assumed.

**Proof.** Define `d_a=Tr(PJ_a)` and `q_ab=Tr(PQ_ab)`. These are real, `q` is symmetric traceless, and `O` is SU2-invariant, so `Tr(ZO)=sum_ab q_ab d_a d_b`. The standard spin traces `Tr(J_z^2)=Nc/3` and `Tr(Q_zz^2)=Nc(4c-3)/45` give, by irreducibility and tensor-component orthogonality,

`sum_a d_a^2 = (4c/3)a_1` and `sum_ab q_ab^2 = [2c(4c-3)/15] a_2`.

Because `q` is traceless,

`sum_ab q_ab d_a d_b = Tr[q (dd^T-|d|^2 I/3)]`.

The second factor's squared Frobenius norm is `(2/3)|d|^4`. Cauchy–Schwarz gives the result exactly, including `64/405`. No positivity relaxation is involved. QED.

For independent normalization, `Tr(Q_ij Q_kl)=C [ (delta_ik delta_jl + delta_il delta_jk)/2 - delta_ij delta_kl/3 ]` with `C=Nc(4c-3)/30`. This proves the quadrupole formula with all five rank-two components.

## Theorem 2 (an exact rational linear 35-qubit necessary cut)

Every arbitrary complex code in `Sym^35(C^2)` correcting three arbitrary physical-qubit errors satisfies

`a_2 <= 574057297 / 2590000000 < 9/40`, and consequently

`-40000 a_1 <= Tr(Z O) <= 40000 a_1`.                             (2)

**Proof of the scalar inequality.** Use `n=35`, `N=36`, `t=3`, and the standard real Wigner-6j Racah convention

`M_{rk}=(-1)^(n+r+k)(2r+1){j j r; j j k}`, `H=2M-I`, `S_{rk}=(-1)^k M_{rk}`.

Every physical code obeys `a>=0`, `a_0=1`, `sum_r a_r=N/2`, `(Ha)_r=0` for `r=1..6`, `(Ha)_r>=0` for `r>=7`, and `S a>=0`. Construct the equality rows `E` and nonnegative inequality rows `G` exactly as in `check_a2_n35_dual.py`. The JSON `a2_n35_farkas_dual.json` gives 8 rational equality multipliers `lambda` and 28 nonnegative rational inequality multipliers `y`, with denominator `10^6`. For `e_2` the unit vector of coordinate 2, define

`res = e_2 - E^T lambda + G^T y`, `epsilon=||res||_infinity`.

The standalone standard-library exact checker proves `epsilon<1/900000` and, more tightly,

`a_2 <= lambda^T b +(N/2)epsilon = 574057297/2590000000 <9/40`.

Indeed `e_2^T a=lambda^T b-y^T G a+res^T a <=lambda^T b+(N/2)epsilon`, since `y,G a,a >=0`. This is a rigorous residual-Farkas dual, not a floating LP outcome.

At `j=35/2`, `c=1295/4`, exact integer arithmetic verifies

`[(64/405)c^3(4c-3)] * (9/40) < 40000^2`.

Combine this with (1) to obtain (2), also valid when `a_1=0`. QED.

### Exact rational coefficient matrices to append to a three-copy SDP

Use the packet's pair `(12)` spin-coupled basis and full block normalization

`Z = direct_sum_J I_(2J+1) tensor Z_J`, `X_J=(2J+1)Z_J`, `sum_J Tr(X_J)=8`.

Let `L` denote the pair spin, `x_L=[L(L+1)-2c]/2`, and `D_LL=(-1)^(n-L)`; `F_J` is the real orthogonal swap-(23) Racah matrix

`F_J[L,K]=(-1)^n sqrt((2L+1)(2K+1)){j j L; j J K}`.

With `X12=diag(x_L)`, `X13=F_J X12 F_J`, `X23=D X13 D`, the invariant operator is exactly

`O = (X12 X13+X13 X12)/2 -(c/3)X23`.

Hence

`O_J[L,L'] = [(x_L+x_L')/2 -(c/3)D_LL D_L'L'] * sum_K F_J[L,K] x_K F_J[L',K]`,

and `Tr(ZO)=sum_J Tr(X_J O_J)`.

`emit_rational_cut.py` produces **53 full-spin blocks** of rational approximants `O_J_hat` in `n35_rational_cubic_cut.json`. Each entry is an integer divided by `10^8`, generated using 6j Racah factorial fractions and integer-square-root enclosures of the swaps to `10^-24`. Its standard-library proof gives for every **actual** code

`|sum_J Tr(X_J O_J_hat)-Tr(Z O)| < 1/100000`.

Because `X_J` are PSD and sum of their traces is 8, the bound uses a uniform operator-norm error, not the correctness of any numerical saved `X_J`. Thus the following is an exact **rational-coefficient linear cut** usable directly with the old three-copy variables:

`-40000 a_1 - 1/100000 <= sum_J Tr(X_J O_J_hat) <= 40000 a_1 + 1/100000`.

For a real symmetric stored block `X_J`, the off-diagonal coefficient in `Tr(X_J O_J_hat)` is `2 O_J_hat[L,L']`. Do not use `Z_J` in its place without multiplying by `2J+1`. Do not impose S3 on `tau_3 Z`.

## Rigorous test against supplied numerical pseudo-moment records

The checker `check_cubic_cut.py` interprets every input decimal **exactly as a rational**, evaluates each Wigner 6j as an exact rational times a rigorously enclosed square root, bounds the total observable error, and squares the resulting rational intervals. Repeated results are **tests on the stored decimals**, not proof that they satisfy all relaxation cones exactly.

| Point from attached archive | Tr(ZO), interval center | RHS of (1), squared | `(Tr ZO)^2-RHS`, rigorous lower (approx) | Outcome |
|---|---:|---:|---:|---|
| `colab_direct_n35/direct_logical_point_n35_t3.json` | +25.931904810596 | 26.679209380163 | +645.784477725687 | FAIL |
| `physical_point_n35_t3.json` | +49.123645701125 | 2635.737581676910 | -222.605014707209 | no violation |
| `physical_point_n36_t3.json` | +95.328935944417 | 8269.885871204661 | +817.720157090134 | FAIL |

The first point's stored `a1=0.0005077407068497744`; the **rational** linear cut bounds its observable by `20.309638274` including slack `10^-5`. The checked rational observable is about `25.931904811`, so the gap exceeds **5.6222**. This is a substantial, rigorously certified separation **from that particular recorded pseudo point**. Earlier native *numerical* diagnostics found the point compatible with tested `R/D`, ordinary/mixed PPT, and their known faces to solver precision; none of those diagnostics is converted here into an exact feasibility claim.

The n=36 baseline violation is also real for its stored decimals, but that baseline already failed the stronger logical cones. Consequently it is not an independent n=36 exclusion.

The n=35 baseline is a deliberate nonseparating control: it passes the cubic test but is known to violate the logical cones. This prevents conflating the new inequality with the earlier exclusions.

## Independent applicability controls

`check_small_spin_controls.py` builds ordinary Clebsch–Gordan coupled bases **independently** of the large-spin Racah formula for `n=1,2,3,4`, checks `F_J` against the actual swap (23), and verifies the polynomial-in-Casimirs formula for `O_J` against a direct physical `J_x,J_y,J_z` tensor construction. The standard coupled basis and the packet's `F_J` basis differ by `diag((-1)^L)`; the checker explicitly applies this gauge change. It additionally verifies *all nine exact normalized two-erasure KL pairs* for the known seven-qubit Pollatsek–Ruskai code. The tetrahedral/octahedral 19- and 37-qubit codes are not falsely excluded: for 2O-invariant 37, the rank-one multipole is identically zero by group irreducibility, so both sides of (1) vanish.

## Exact commands

From this directory:

```bash
python check_a2_n35_dual.py       # stdlib exact rational Farkas check
python check_cubic_cut.py         # stdlib exact Racah/interval checks on three pseudo records
python emit_rational_cut.py       # stdlib, verifies and reproduces SDP-ready rational coefficients
python check_small_spin_controls.py  # optional numpy/sympy; independent CG and physical KL controls
```

**What remains open:** (2) is a **new valid necessary linear cut**, not a global infeasibility certificate for the original 35-qubit SDP, nor a code or nonexistence certificate at 36. The unrestricted `n_min(3)` bracket therefore remains 35–37. To close it, the whole joint cone plus new cut would need a global dual, or one would need a code with exact 49-pair physical KL. Absence of literature attribution here is not a priority guarantee.
