# Attribution-only addendum for the theorem writeup

Prepared 25 October 2026. This text does not modify the frozen theorem, certificate, or verification artifacts.

## Suggested insertion

Multi-copy separability formulations and semidefinite hierarchies are established tools for code-existence and rank-constrained optimization problems. Yu et al. give a complete hierarchy for the pure-state marginal problem, including a formulation of general quantum-code existence, and subsequently extend the framework to rank-constrained optimization with polynomial constraints [YSMNG21, YSNG22]. The general quantum-code hierarchy of Anglès Munné, Nemec, and Huber provides a further direct antecedent [AMNH25]. Our contribution is the concrete, rigorously certified exclusion at n = 18, not the general hierarchy methodology.

Numerical evidence for the length sequence 7, 19, 37, 61, 91 appears already in Visnevskyi's 2025 MSc thesis [V25] and in the later numerical study of Bond et al. [BMO+26]. These works motivate a general conjecture but do not supply an unrestricted complex n = 18 nonexistence certificate in the materials we inspected. Aydin–Alekseyev–Barg's earlier discussion of minimality occurs alongside their real, odd-length PR-type equations [AAB24]. The present unrestricted exclusion, together with Okada's shorter-length bounds [O25] and the known nineteen-qubit construction [AAB24], establishes the two-error minimum without resolving the all-t conjecture.

## References to add or retain

- **[YSMNG21]** Xiao-Dong Yu, Timo Simnacher, Nikolai Wyderka, H. Chau Nguyen, and Otfried Gühne. *A complete hierarchy for the pure state marginal problem in quantum mechanics.* Nature Communications **12**, 1012 (2021). DOI [10.1038/s41467-020-20799-5](https://doi.org/10.1038/s41467-020-20799-5). [arXiv:2008.02124v2](https://arxiv.org/abs/2008.02124v2), 16 February 2021. Relevant: Theorem 2; Methods, Proposition 2; supplementary extension construction.
- **[YSNG22]** Xiao-Dong Yu, Timo Simnacher, H. Chau Nguyen, and Otfried Gühne. *Quantum-Inspired Hierarchy for Rank-Constrained Optimization.* PRX Quantum **3**, 010340 (2022). DOI [10.1103/PRXQuantum.3.010340](https://doi.org/10.1103/PRXQuantum.3.010340). [arXiv:2012.00554v2](https://arxiv.org/abs/2012.00554v2), 14 March 2022.
- **[V25]** Vladyslav Visnevskyi. *High-dimensional permutation-invariant quantum error-correcting codes.* MSc thesis, University of Amsterdam, title-page date 29 July 2025; repository addition 22 August 2025. Relevant: §3.2, Tables 1–2, Conjecture 3.2. [Pinned publicly accessible thesis PDF](https://raw.githubusercontent.com/Techtonick/PI-codes/e30da4371caa5608bf727705121abb4cc26d67c6/High_dimensional_PI_Error_correcting_codes.pdf).
- **[AMNH25]** Gerard Anglès Munné, Andrew Nemec, and Felix Huber. *SDP bounds on quantum codes.* [arXiv:2408.10323v2](https://arxiv.org/abs/2408.10323v2), 10 September 2025 (first posted 19 August 2024).
- **[BMO+26]** Liam J. Bond, Jiří Minář, Māris Ozols, Arghavan Safavi-Naini, and Vladyslav Visnevskyi. *Permutation-invariant codes: a numerical study and qudit constructions.* [arXiv:2603.10981v1](https://arxiv.org/abs/2603.10981v1), 11 March 2026. Relevant: §3.1 and Conjecture 3.1.
- **[AAB24]** Arda Aydin, Max A. Alekseyev, and Alexander Barg. *A family of permutationally invariant quantum codes.* Quantum **8**, 1321 (2024). DOI [10.22331/q-2024-04-30-1321](https://doi.org/10.22331/q-2024-04-30-1321). [arXiv:2310.05358v3](https://arxiv.org/abs/2310.05358v3). Relevant: §7 and Proposition 7.1.
- **[O25]** Rui Samuel Okada. *A Quantum Analog of Delsarte's Linear Programming Bounds.* UC Davis doctoral thesis (2023); corrected release [arXiv:2502.14165v1](https://arxiv.org/abs/2502.14165v1), 20 February 2025. Relevant: Chapter 3, Table 3.1.

## Classification for editorial accuracy

| Evidence | Classification |
|---|---|
| Yu 2021/2022; general SDP hierarchy | Rigorous methodological prior theorems, **not** a concrete n = 18 certificate. |
| Okada finite LP bounds; AAB nineteen-qubit construction | Prior lower-bound/existence ingredients; retain their attribution. |
| AAB shorter-than-19 remark; thesis homotopy nonexistence prose | Earlier computational/minimality assertions whose unrestricted scope and certification are **not established by the inspected materials**. Do not silently promote them to rigorous unrestricted results or claim no prior assertion exists. |
| Thesis Conjecture 3.2; Bond Conjecture 3.1 | Numerical conjecture/antecedent, **not** a general lower-bound theorem. |
| Internally verified three-copy finite witness | The concrete contribution under review; priority remains subject to the usual limits of a literature search. |
