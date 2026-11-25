# Wider scalar deterministic coefficient inverse: analytic audit

2026-10-26 00:05 UTC. Analytic PASS for precisely the theorem in `hss-probe-reuse/phase2/wide_scalar_inverse_bound.md`.

The full-complement construction is the essential new point: child coordinates satisfy C_child=H_child C_child^0, with C_child^0 determined by the parent full frame and fixed physical plane rotation. Expressing both samples in normalized child/parent coordinates cancels the actual parent frame. Thus a pure passive inverse-column source has deterministic normalized coordinates, and its successive parent states depend only on already used deeper H variables. The next ancestor H remains independent. This is a valid reverse-coordinate induction, unlike the earlier false chronological-feedback independence argument for arbitrary noisy samples.

The four-moment cone (d−1)X≤U,(d−1)Z≤W is invariant. Bounding emission by [(2d−1)/(d(d−1))](pU+qW), and flux loss below by [(d−1)/d](pU+qW), gives the claimed C_d=(2d−1)/(d−1)^2. Adding the source coefficient and terminal root contraction gives C_d+2.

Distinct inverse-column cross terms vanish by choosing the deeper birth and conditioning on all ancestor frames: its own centered detail occurs exactly once, linearly, while the other column never uses it. Same-node da/ad use independent banks. The source coefficient cannot overlap an ancestor column at its birth because transport is strictly upward. Hence E[V^T V] is diagonal.

**Approved scope:** real scalar k=1 fixed nested bases, width s≥3, coefficient RHS deterministic and independent of probes. The actual off-model RHS is correlated with V; this proof does not control it. E[V^T V] cannot be replaced with E[VV^T], nor with a global-LS inverse bound. No arbitrary-k theorem or full RE02 result follows.

Worker exact finite-design checks are corroborating controls; the argument above, not Monte Carlo agreement, supplies the all-depth justification.

## Separately gauged finite-randomness corollary (00:19 UTC)

Analytic PASS for the explicitly stated full-complement recursion with independent uniform signed-permutation H_child in dimension d. This defines a different probe law; no claim of equality with the Haar-frame distribution is needed or made. Its zero mean, E[H^T M H]=(tr M/d)I, independence between nodes/banks, and central-sign symmetry give all moments used by the reverse-coordinate recurrence, source cancellation, and terminal isotropy. The quantitative proof therefore applies unchanged. The specified canonical child complement and randomized full-complement recursion are hypotheses: the result does not cover arbitrary externally chosen complementary gauges with signed permutations attached afterward. All scalar/deterministic-RHS and E[V^T V]-only limitations remain.
