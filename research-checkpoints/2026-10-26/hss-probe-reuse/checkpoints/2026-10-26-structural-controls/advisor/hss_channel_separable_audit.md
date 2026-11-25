# Audit: channel-separable rank-k corollary

2026-10-26 01:39 UTC. Analytic PASS for `channel_separable_fixed_basis_corollary.md` under its explicit global no-interlevel-mixing hypothesis.

After the prescribed orthogonal changes, the fixed linear model is an orthogonal direct sum of k² scalar fixed-basis classes. Their coefficient freedoms are independent, so both Frobenius error and the fixed-class optimum sum over the blocks. Three probes supported in column channel b yield all k row-block forward sketches simultaneously; three transpose probes supported in row channel a yield all k column-block transpose sketches. Thus there are3k+3k actual matvecs, not6k².

Each block sees an independent forward/transpose bank pair with the scalar theorem's distribution. Sharing one bank across different block pairs causes no issue: their physical output supports are orthogonal, so expected squared errors sum without cross terms. Known pre/post orthogonal changes preserve query count and norm. The801 expected squared-error factor follows directly.

Arbitrary k-by-k coupling blocks are allowed. Arbitrary mixing of channels between levels is not. Local CS decompositions do not automatically produce a compatible global channel decomposition. This corollary does not solve the arbitrary-rank dense-basis or unknown-basis HSS problem.
