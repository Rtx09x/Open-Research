# Exact flagged-erasure obstruction for stabilizer shields at total Pauli error 41/200

**Status (26 October 2026).** Proved, subject to standard finite-dimensional quantum-channel facts and elementary random-isotropic-subspace counting. Does **not** prove Q(D_{41/200})=0 or supply a positive-capacity witness. The bound applies to a full [[m,2]] stabilizer encoding subspace and **arbitrary** CPTP receiver decoders, including all erasure flags and postselection outcomes. A second result excludes uniformly random such stabilizer encoders with explicit probability at m=8192. The numeric check is integer-only and executable as `shield_stabilizer_obstruction_checker.py`.

## Model and exact prescribed target

D_p(X)=(1-p)X + (p/3)\sum_{P=X,Y,Z} PXP, p=41/200. Bloch multiplier eta=109/150. Shield input C is 4 dimensional, output C ⊕ span{|e>}, and ideal half erasure is E_{1/2}. Let the activation purification |Psi>_{RAC} have Schmidt weights (3/8,1/8,1/8,3/8) across RA:C. Define epsilon_Psi by the **half** trace norm of the difference after id_R ⊗ D_p ⊗ (S−E_{1/2}). Let epsilon_Phi be the **half** trace norm of the normalized 4×4 Choi-output difference between S and E_{1/2}.

Because |Psi>=(F⊗I)|Phi_4>, where F=2diag(sqrt(3/8),sqrt(1/8),sqrt(1/8),sqrt(3/8)), and ||F^{-1}||^2=2, we have epsilon_Phi ≤2 epsilon_preD. The linear inverse of D_eta obeys (id⊗D_eta^{-1})(X) = eta^{-1}[X−(1−eta)(id⊗replacer)(X)] and ||(id⊗D_eta^{-1})(X)||_1 ≤ [(2−eta)/eta] ||X||_1 on Hermitian operators (spectators allowed). Thus

    epsilon_Phi ≤ (382/109) epsilon_Psi.

Normalized Choi-to-diamond gives (1/2)||S−E_{1/2}||_diamond ≤4 epsilon_Phi ≤(1528/109) epsilon_Psi.

## Exact optimum for *every fixed* full [[m,2]] stabilizer code

Let V=F_2^{2m} label Pauli errors modulo phase, and let T⊂V be a symplectic-isotropic stabilizer subspace of dimension m−2. Define mu(e)=(159/200)^{m−wt(e)}(41/600)^{wt(e)}. The Pauli cosets V/T are indexed by a stabilizer syndrome s∈F_2^{m−2} and logical Pauli label ell∈F_2^4. Write

    P_{s,ell} = sum_{e in coset(s,ell)} mu(e),
    p_s=sum_ell P_{s,ell},     M_s=max_ell P_{s,ell}.

Define the fractional-knapsack optimum

    C_*(T) = max_{0≤u_s≤1, sum_s p_s u_s=1/2} sum_s M_s u_s.

Sort syndrome sectors in decreasing order of reliability M_s/p_s; accept the most reliable until their total probability is exactly 1/2, partially accepting the last sector if necessary. This defines deterministic sender encoding and receiver syndrome measurement, maximum-likelihood logical Pauli correction, and receiver-local random erasure; all operations CPTP, with the failure branch retained.

**Theorem 1 (exact optimal Choi approximation).** For every isometric encoding *onto the entire [[m,2]] stabilizer sector*, and every CPTP decoder to C^4 ⊕ |e>,

    epsilon_Phi(S_m,E_{1/2}) ≥ 1/2 − C_*(T).

Equality is attained by the syndrome-reliability rule above. Thus this is the **exact** minimum normalized Choi half-trace distance across arbitrary decoders, not just Pauli corrections or stabilizer decoders. In particular, if the prescribed activation test epsilon_Psi≤1/20000, necessarily

    C_*(T) ≥ 1/2 − 382/(109*20000) ≈ 0.49982477,

and hence the accepted half of all syndrome probability must have conditional logical-error probability ≤2*382/(109*20000) ≈0.00035046.

**Proof.** Error-pattern averaging decomposes the physical output into orthogonal syndrome sectors and within each into the 16 logical Pauli Bell states. This holds on the normalized maximally entangled input even if the receiver decoder is completely arbitrary. WLOG measure syndrome first. For syndrome s and its trace-nonincreasing logical **success** map R_s, put u_s=Tr R_s(I_4/4). Each of the 16 possible logical Pauli errors has reduced receiver state I_4/4 and therefore the same success probability u_s. Define f_ell as its overlap with target Bell state after R_s. The Bell-resolution-of-identity identity gives sum_ell f_ell = u_s, f_ell≥0. Hence successful target-Bell probability t≤sum_s M_s u_s and total success mass a=sum_s p_s u_s.

Measuring the receiver output with three orthogonal effects (target Bell success, other logical success, erasure flag) yields actual distribution (t,a−t,1−a), versus ideal (1/2,0,1/2). Data processing gives

    epsilon_Phi ≥ (|t−1/2|+(a−t)+|a−1/2|)/2.

For a≤1/2, increase some acceptance u_s to total 1/2; target mass can only increase, hence the displayed bound is ≥1/2−C_*. For a≥1/2, trim acceptance to exactly 1/2: this discards mass a−1/2 but target-Bell mass drops by no more than the same amount, hence the displayed bound is again ≥1/2−C_*. Conversely accept probability 1/2 using the optimum fractional knapsack, correct the most probable logical Pauli in each accepted syndrome, and erase otherwise. Its successful Choi output is Bell diagonal, with target-Bell probability C_* and wrong-Bell probability 1/2−C_*; its exact Choi half distance equals 1/2−C_*.

## Deterministic uniform-quotient obstruction

Let q_T denote the induced distribution on V/T (syndrome and logical Pauli together), and U the uniform distribution on V/T, whose cardinality is d=2^{m+2}. Put δ_T=TV(q_T,U)=(1/2)||q_T−U||_1. For any fractional acceptance u_s of total mass 1/2, choose ell_s achieving M_s and set f(s,ell)=u_s 1[ell=ell_s]. Then

    sum_s M_s u_s = E_{q_T} f ≤ E_U f + δ_T
                    = (1/16) E_{U_s}u_s + δ_T
                    ≤ (1/16)(1/2 + δ_T)+δ_T
                    = 1/32 + (17/16)δ_T.

It follows that

    epsilon_Phi ≥ [15/32 − (17/16)δ_T]_+,
    epsilon_Psi ≥ (109/382)[15/32 − (17/16)δ_T]_+.

In the hypothetical exact-uniform quotient case, the optimal Choi half distance is exactly 15/32. This follows from matching P_{s,ell}=p_s/16 and accepting half the mass. The bound is not an unrestricted no-go: highly nonuniform specially structured stabilizer cosets may evade it.

## Uniformly random [[m,2]] stabilizers: certified finite result

Sample T uniformly from all (m−2)-dimensional totally isotropic subspaces of V. Because the binary symplectic group is transitive on nonzero vectors, for e≠e',

    Pr_T(e+e'∈T)=(2^{m−2}−1)/(2^{2m}−1) ≤1/2^{m+2}.

Thus the quotient map e↦[e]∈V/T is a 2-universal hash family. Let A_t be the retained set of error strings of Pauli weight≥t; let b=mu(A_t^c), c=sum_{e∈A_t}mu(e)^2. A second-moment expansion, Cauchy–Schwarz, and the triangle inequality (including the discarded total mass b) establish

    E_T[δ_T] ≤ b + (1/2)sqrt(2^{m+2}c).

Both terms are exactly finite binomial sums at this rational p:

    b=sum_{w=0}^{t−1} binom(m,w)(123/600)^w(477/600)^{m−w},
    c=sum_{w=t}^m binom(m,w)3^w(477/600)^{2(m−w)}(41/600)^{2w}.

**Theorem 2 (finite exact random-code failure).** At m=8192 and t=1553, the integer-only checker proves

    E_T[δ_T] < 1/4000.

The prescribed activation test epsilon_Psi≤1/20000 requires

    δ_T≥(16/17)(15/32−382/(109*20000))
        =1021493/2316250 > 0.441.

Markov's inequality therefore gives the following bound simultaneously over **all encoding bases** of a sampled stabilizer sector and **all CPTP decoders**:

    Pr_T[there exists a qualifying shield decoder]
      < (1/4000)/(1021493/2316250)
      = 9265/16343888 < 0.000567.

The same exact script shows E δ_T<1/100 at m=4096, t=777. The m=8192 computation took less than 0.5 seconds in a standard CPU container; all assertions use Python integers and strict inequalities after cross-multiplication. The proof does not execute or trust any third-party code.

## Explicit four-qubit control

Take m=4 and T=span{XXXX,ZZZZ}, the [[4,2,2]] code, with four syndrome values. Let a=159/200, b=41/600, eta=109/150. Direct enumeration of the 256 Pauli strings gives:

    p_0=(1+3 eta^4)/4,       M_0=a^4+3b^4,
    p_1=(1−eta^4)/4,        M_1=a^3b+ab^3+2b^4

for each of three nonzero syndromes. The zero-syndrome reliability M_0/p_0 exceeds M_1/p_1, but p_0<1/2. Accept all zero-syndrome outcomes and enough of one nonzero syndrome to reach 1/2. Therefore

    epsilon_Phi^* = 1/2 − M_0 − (1/2−p_0)(M_1/p_1)
                  = 7165372619/77357250000
                  ≈ 0.09262703391,
    epsilon_Psi ≥ (109/382) epsilon_Phi^* > 0.02643.

The exact 256-pattern enumerator and fractional knapsack assertions run inside the same checker. This is a concrete code rejected by the theorem, independently of decoder ingenuity.

## Scope and boundary

- All statements use p=41/200 TOTAL nonidentity Pauli error, not p/3 as total. The only physical channel is D_p repeated m times.
- The exact knapsack theorem covers arbitrary CPTP decoders and all syndrome/flag failures, but **only isometric encoders onto an entire full [[m,2]] stabilizer sector**. It does not cover arbitrary non-stabilizer, smaller-subspace, mixed/CPTP encoders, multiuse exotic codes, or hand-designed rare stabilizer exceptions.
- The random-code theorem gives a probability over uniformly random stabilizer groups; it is **not a universal bound over all stabilizer codes**.
- The result is based on entanglement fidelity/Choi erasure simulation. It neither upgrades private information to coherent information nor assumes Q(D_p)>0 to build the shield.
- The maximum-likelihood fidelity formula is established in Tomamichel arXiv:2607.23450v1 Proposition 3.1; stabilizer syndrome/logical probability transforms are standard, including Kann et al. arXiv:2601.15505. We do not claim priority for those ingredients or the generic leftover-hash argument. Novelty of the combined shield-specific knapsack/no-go formulation remains to be checked.
- Below the hashing point H(1−p,p/3,p/3,p/3)=1 (p≈0.189289624915), random stabilizer codes of fixed logical dimension transmit accurately, so a receiver can deliberately erase with independent probability 1/2 and approximate the desired shield. This is a consistency control and a known achievability regime, not a threshold improvement at p=.205.

## One decisive next verification

For any explicit **structured**, possibly highly degenerate [[m,2]] stabilizer design proposed as a shield at p=.205, calculate the 16 coset probabilities P_{s,ell} per syndrome. Sort reliabilities M_s/p_s, accept total probability 1/2, and compute the *exact* rational C_*(T). If C_*<1/2−382/(109*20000), that entire stabilizer encoder is ruled out for the prescribed activation test, **for every possible decoder**, with no entropy diagonalization. A candidate clearing this necessary hurdle still needs a full quantum-state/entropy certificate for positive coherent information.
