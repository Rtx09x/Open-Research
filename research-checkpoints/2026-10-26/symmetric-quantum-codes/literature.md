# Literature audit (2026-10-25)

## Target
All rank-two subspaces of Sym^n(C^2), arbitrary complex coefficients and either parity, detecting Pauli weight up to four (distance >=5, correction of arbitrary two-site errors).

## Primary sources checked
- Bond et al., *Permutation-invariant codes: a numerical study and qudit constructions*, https://arxiv.org/html/2603.10981v1 (11 March 2026; current arXiv record has v1). Conjectured minimum 3t²+3t+1 rests on numerical searches, not an unrestricted nonexistence proof.
- Aydin, Alekseyev, Barg, *A family of permutationally invariant quantum codes*, https://arxiv.org/html/2310.05358v3 (15 April 2024). Section 7 gives nine quadratic PR equations and a 19-qubit solution certified by the authors using msolve intervals. Printed decimals alone are not an exact witness.
- Kubischta, Teixeira, *MacWilliams Identities for Intrinsic Quantum Codes*, https://arxiv.org/html/2604.16023v2 (26 August 2026). Theorem A1 gives the scalar intrinsic LP; Corollary A3 gives its SU(2) 6j matrix. Proposition B2 proves physical-distance equivalence. Appendix B treats distance-three optimality at n=7 but does not evaluate distance five. **Normalization caution:** the sentence after B18 says sum normalized A=K, inconsistent with its own B17 and examples. The correct value from definitions is N/K (N=n+1), used here.
- Teixeira, *Orthogonal Polynomials and the MacWilliams Transform for Permutation-Invariant Qudit Codes*, https://arxiv.org/html/2605.15372v1 (14 May 2026). Provides the equivalent terminating Racah formula, enabling an independently coded rational transform checker.

## Novelty status
Searches for PI 18 + MacWilliams, PI 17 + linear programming, and distance-five lower bounds did not locate this n>=18 evaluation. This is not a claim of exhaustive novelty; the bound is a small new application of established machinery unless prior art is located. Exact certificates are useful even if the evaluated bound is known.

## Prior-art correction
- Y. Okada, *A Quantum Analog of Delsarte's Linear Programming Bounds*, https://arxiv.org/abs/2502.14165 (20 February 2025), dissertation Table 3.1 (printed p89 / PDF p92), already evaluates the spin-code LP: distance-five excludes n<=17, while n=18 and n=19 allow dimension bounds about 2.019 and 2.096. Smaller entries were checked with exact GLPK arithmetic. Section 3.3 includes time-reversal shadow inequalities. **Therefore our n>=18 certificates and shadow test are replications, not new research results.** Advisor independently located this source. The new tentative contribution is a nondegeneracy lemma at n=18, not the n>=18 bound.

## Anticoherent-subspace cross-check
Pereira–Paul-Paddock, https://arxiv.org/pdf/1610.05841 (2017), supplies invariant constructions and numerical-range characterization, not an apparent spin9/order4 two-plane exclusion. Serrano-Ensástiga et al., https://arxiv.org/html/2404.15548v2 (later PRA111022435,2025), gives K≤floor((2j−t+1)/(t+1)); at j9,t4 this allows K=3. Their numerical table treats t1,2 only. These obvious antecedents do not subsume the restricted pure-complement obstruction, but novelty remains unconfirmed.
