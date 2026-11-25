# Sparse conductance recovery

## Question

How can changes in a known electrical network be recovered from pairwise effective-resistance measurements?

## Results and scope

The research develops a rank-adaptive way to reconstruct a changed network from exact effective-resistance measurements, and shows how radically the answer changes when conductance changes can cancel.

- **Same-direction changes:** for a connected target with Laplacian-change rank $r$, the stated adaptive algorithm reconstructs the network using $(r+1)(n-1)-r(r+1)/2$ distinct pair queries. It infers the direction and stopping rank within the monotone promise, without prior knowledge of the changed locations.
- **Mixed-sign lower bounds:** six changes among existing edges of a unit complete graph can require quadratically many randomized queries and nearly all pairs deterministically, even though only four pair readings change. A separate construction with a new edge gives a three-change marked-pair reduction.
- **Structured networks:** for product-weight complete baselines with at most $K\geq1$ changes, the manuscript gives the class-wide minimax order $\Theta(\min\{n^2,n+K^2\})$ under its monotone exact-oracle assumptions.

The manuscript also treats disconnected weakening and weighted class-structured networks. The exact recovery and composition test suites passed in the release replay; the different recovery and lower-bound models should not be conflated.

## Materials

[Sparse conductance manuscript](paper/sparse_conductance_changes.pdf) · [LaTeX source](paper/sparse_conductance_changes.tex) · [Additional studies](paper/)

## Verification and limitations

The manuscript and supporting studies are internally checked research, with independent expert review and peer review pending. The model assumes a known baseline network and an exact oracle where stated; noisy and joint-uncertainty variants are separate studies.

## Reproduce

See `code/` and the source manuscripts; the bundled compositional-diagnosis archive has its own README and checks.

The research used AI assistance in development and internal checking. The author is responsible for the claims. Prior work and detailed assumptions are cited in the underlying documents.

[Supplementary source packages](archive/source-packages/) preserve additional proofs, certificates and historical work.
