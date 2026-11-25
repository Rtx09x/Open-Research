# A standard martingale fourth-moment bound for a fixed physical input

**Status:** elementary proved lemma; not a correlated reconstruction bound.
The scalar anchor consequence was independently analytically audited.
This is a standard martingale-moment argument, not a novelty claim.

Fix prescribed real nested bases, independent of a top-down Haar tree-frame
bank Psi of width s>=2k. Let B be any deterministic matrix with the physical
row dimension as its column dimension. Then

    E||B Psi||_F^2 = ||B||_F^2,
    E||B Psi||_F^4 <= 3 ||B||_F^4.

The deterministic root frame has orthonormal rows. Let H_0 and J_v be the
physical root-active and detail embeddings, a complete orthogonal wavelet
basis. Write

    B Psi = (B H_0) P_0 + sum_v (B J_v) Q_v.

The coefficient matrices B H_0,B J_v are deterministic, with squared
Frobenius norms summing to ||B||_F^2. Reveal all node orientations in a
topological order, including any prerequisite ancestor frames. Each new
increment Delta_v=(B J_v)Q_v is conditionally centrally symmetric, has zero
conditional mean, and has **deterministic** squared norm
a_v^2=||B J_v||_F^2 because Q_v Q_v^T=I_k. Root term norm is a_0.

For the partial sum S, symmetry kills both odd terms in the fourth-power
expansion. Pointwise Cauchy–Schwarz therefore gives

    E[||S+Delta_v||_F^4 | past]
      <= ||S||_F^4 + 6 a_v^2 ||S||_F^2 + a_v^4.

Expected squared norms add exactly. Telescoping from the deterministic root
term proves the sharper upper bound
3(sum a_i^2)^2-2 sum a_i^4, and hence the asserted inequality. No independence
between different detail frames was assumed; conditional centering suffices.

For scalar k=1 and deterministic physical vector a, an inherited active row
P_j is a unit vector even though it depends on Psi. Thus pointwise

    |P_j Psi^T a| <= ||Psi^T a||,

and E|P_j Psi^T a|^4<=3||a||^4. This does not use independence of P_j and Psi.
The same statement applies to a deterministic coarse-coordinate vector after
lifting it through its prescribed orthonormal physical active embedding.

## Remaining correlation gate

If a pure-source inverse column v_j had a depth-independent bound on
E||v_j||^4, Cauchy–Schwarz would control a single product
E[||v_j||^2 |P_j Psi^T a|^2] without an independence shortcut. The currently
proved deterministic-coefficient inverse theorem gives only E||v_j||^2;
it does not supply this fourth moment. Moreover, controlling individual
products does not by itself bound their summed cross terms or establish a
full off-model relative-error theorem. Those remain separate obligations.
