# Independent audit of the completed Pro consultation

Read-only source: `../../pro-results/hss/HSS_research_results/`; parent supplied
the archive. This phase did not make another Pro request or upload anything.

## 1. Gaussian innovation obstruction: algebra audit passes

The actual observer basis projector satisfies the spectral-invariance equation
`(I-Pi) D H P H^T D^T Pi=0`. If, after conditioning on the observers' Gaussian
blocks and learned projectors, an additive full-row Gaussian innovation
`X Q^T` survives, substitution gives a polynomial vanishing under a full-support
density. Its homogeneous quadratic coefficient must vanish identically.
Choosing `X=D^{-1}(u+v)a^T`, with u in range(Pi) and v in its complement, forces
`a^T Q^T P Q a=0` for every a. Positivity yields `P Q=0`. Intersect over
observers. Independent Gaussian row spaces have intersection dimension
`max(0, 2km-(m-1)s)`, zero with two observers when s>=4k.

The construction's exact HSS optimum `mk epsilon^2` is also correct: truncating
the shared source block gives a globally rank-k competitor, and each disjoint
observer leaf imposes its own rank-k tail lower bound. The near-class limit
epsilon->0 is therefore substantive.

For the minimal stated conditioning field, the common row-space component is
independent of the learned projectors because every observer null projector
annihilates it, establishing sharpness of the surviving-dimension statement.
The one-projector covariance formula is consistent with right orthogonal
invariance and conditional Wishart spectral averaging; at s=3k the factors
are exactly 4/3 on the learned subspace and 2/3 on its complement.

**Scope:** this destroys that particular full-row additive Gaussian-column
decoupling under the specified field. It does not remove all conditional
randomness, rule out weaker conditioning, prove algorithmic failure, or prove
a matvec lower bound for RE-02.

## 2. Six-k tree theorem: independent derivation and stronger finite tests

The proof is reproduced independently in `three_color_forest_theorem.md` and
extended to arbitrary forests. Our implementation is independent of the Pro
code and tested every rooted four-vertex forest and arbitrary blocks through
k=3 in selected five-vertex cases. Direct star bicoloring and signed probing
are established ingredients; novelty of this precise forest ledger remains
unestablished. See `literature_phase2.md`.

## 3. Flux and isolated-branch statements: algebra and conditioning audit

The identities

    X'=Pi X-Pi W(I-Gamma),
    W'=W Gamma-(I-Pi)X Gamma,
    K'=K-(I-Pi)K(I-Gamma)

follow by expanding the coefficient formulas and the orthogonality of retained
and detail frames. The final map is an orthogonal projection on the space of
probe-space matrices, so its squared norm loss is exact. This holds even for
width s>2k; arbitrary incoming data outside the two local frame row spaces do
not invalidate it. At sibling merges the mixed-channel cross term remains
and is not sign-definite by the local calculation alone.

The arbitrary-k branch formulas match the coefficient update after expressing
one live child's data in complete square boundary frames. Independent centered
row/column complement orientations kill the mixed additions. Tracking mixed
covariance against arbitrary linear operators, rather than only scalar inner
products, justifies composing different noncommuting transfer contractions.
This gives the factor-two bound against exit energy along one ancestor branch.

The freshness qualification is essential and appears justified for a source
supported inside one subtree: square boundary frames admit an equivariant
factorization of all descendant probes; separate right rotations of the two
probe banks leave coefficient estimates invariant. Normalized exit data are
then functions of descendant randomness only. This argument is not valid for
arbitrary globally contaminated carried data, which depend on sibling and
ancestor orientations.

## 4. Sign sectors: expansion audit passes; inequality still open

The fine central-sign characters are constant (aa), sigma_j (ad column j),
tau_i (da row i), and sigma_j tau_i (offdiagonal dd block ij). They are distinct.
The later decoder is linear and independent of these fine signs, so their
output cross terms vanish exactly. For immediate coefficients, different ad
columns and da rows occupy orthogonal output blocks; the remaining da/dd and
dd/dd cross terms vanish under fine signs. This verifies the sector reduction
for the complete expected output-energy operator, not only the initial carry.

What remains is a uniform bound for the operator on **each whole ad-column or
da-row sector**, not merely on each individual matrix entry. Different source
rows inside one sector have the same fine sign and may interfere. The isolated
branch theorem does not alone control their initial compression and merging.

## Replayed checks

The three supplied exact-verifier sources were inspected before execution.
They use standard-library arithmetic and print results; no filesystem writes
or network operations are needed. Replayed with bytecode generation disabled,
and output saved only to `pro_verifier_replay.log` in this phase. This is a
replay of Pro's code plus the algebra audit above, not another independently
coded universal proof.
