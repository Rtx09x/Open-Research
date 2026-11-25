# Six-query forest lemma: independent audit

For known rooted forest support with k×k blocks, diagonal and both edge directions, let c(i)=depth(i) mod3. Query AΩ and AᵀΨ with3k columns each, using signed I_k blocks in channel c(i).

Recover diagonal(i,i) from forward channelc(i); child→parent(i,p(i)) from forward channelc(i)−1; parent→child(p(j),j) from transpose channelc(j)−1. Each selected channel contains exactly one supported block: children have the other residue. This holds for arbitrary directed real or complex matrices, disconnected forests, roots and arbitrary degrees.

For off-support residualE, orthogonality of output block positions and pairwise sign cancellation give the exact expected error

    ||E||² + Σ_(i,j offsupport) w_ij ||Eij||²,
    w_ij=1[cj=ci]+1[i nonroot,cj=ci−1]+1[j nonroot,ci=cj−1]≤1.

The three cases are disjoint modulo3. Hence expected squared error≤2 times the fixed-forest optimum, with6k products. The same sign family can be reused for forward/transpose because their recovered coefficient supports are disjoint. This is not general HSS approximation.

Prior art: exact direct recovery through star bicoloring is classical; see [Montoison–Dalle–Gebremedhin §1.3/Table1/§2](https://arxiv.org/html/2505.07308v1). Random-sign coloring variance analysis and independent averaging are explicit for banded/unidirectional patterns in [Amsel et al. §4.1](https://arxiv.org/html/2402.09379v3). The forest-specific two-sided leakage ledger is a useful extension/composition, not a new coloring or random-sign principle. [Musco–Ramesh ESA2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.85), §4, retains a log-dimension factor for general degeneracy; its§5 asks about removing it. No exact matching forest theorem found; novelty is unestablished.

Two proposed dense-basis bridges were falsified by the worker: nonbacktracking3k frames have coordinate error growing asL+2 on an explicit bichromatic path; an ordered frame variant reproduces the correct popcount-mod3 colors but LM's carried subtraction still creates an extra spurious coefficient already atL2 (error3 instead of2). These kill probe-only transfer through that decoder, not all6k methods. Next target must change decoding or prove a different covariance ledger.
