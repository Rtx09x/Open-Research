# Conditional complement geometry and the limit of endpoint counting

This note assumes a full-rank degree≤t syndrome Gram matrix. That hypothesis is **not** established in general (our t3 variance gate did not establish it). No unconditional length theorem is derived here.

Put s=t+1, d=s², M=2d, N=n+1, and c=N−M. The 2d error-image vectors give an M-dimensional syndrome subspace W⊂V_n if the Gram is nonsingular. Let W also denote an isometry from C^M into the spin-n/2 representation.

Using Schwinger annihilation maps a,b:V_n→V_(n−1), form

    T = [[j I−A_z, A_-], [A_+, j I+A_z]],
    A_i=W†J_iW,   j=n/2.

The full spinor matrix is [b,a]†[b,a]=N times an orthogonal projection of rank n=N−1 in dimension2N. Hence0≤T≤NI, TrT=nM, and compression deletes2c dimensions.

## Universal degree syzygies

The rectangular operator span {aE,bE : E has tensor rank≤t} lies in rectangular tensor ranks1/2,3/2,…,t+1/2. For n≥t+1 each component occurs and the span has dimension

    Σ_(r=0)^t 2(r+1) = (t+1)(t+2)=s(s+1).

There are therefore2s²−s(s+1)=t(t+1) coefficient syzygies before logical doubling, and2t(t+1) after doubling. These give universal nulls of T. Creation maps give the same number of universal nulls of NI−T. Since G>0, the coefficient-to-syndrome map is invertible; the two eigenspaces are independent. This generalizes the independently checked t2 decomposition12 zeros+12 eigenvaluesN leaving12 active dimensions.

Thus there are at least z=2t(t+1)=2s(s−1) eigenvalues0 and z eigenvaluesN, leaving only

    2M−2z =4(t+1)=4s

active eigenvalues.

## What raw rank/interlacing counts actually force

Because rankT≤N−1 and rank(NI−T)≤N+1, the active block must have at least

    max(0,2t+3−c) additional zeros,
    max(0,2t+1−c) additional N eigenvalues.

These are necessary endpoint counts, not sufficient moment conditions. Both become vacuous at c≥2t+3. The proposed minimum has c=t(t−1), and already for t≥4 the candidate one qubit below the conjecture has c=t(t−1)−1≥2t+3. Consequently these endpoint counts alone cannot force all of the proposed extra t(t−1) dimensions.

For a concrete spectral obstruction to over-interpreting the count, when c≥2t+3 the abstract list

    0 with multiplicity z,
    N with multiplicity z,
    (N−s)/2 with multiplicity4s

satisfies0≤T≤NI, TrT=nM and both rank bounds. It also admits a dilation to N times a projection of rankN−1 in dimension2N: each interior eigenvalue uses one extra dimension, with c−2s−1 remaining one-eigenvalue dimensions and c−2s+1 zero-eigenvalue dimensions. All counts are nonnegative at c≥2s+1. **This is not a code or a realization of the compressed-generator moment identities.** It only demonstrates that endpoint counts/global trace/projection-compression spectra cannot by themselves supply the desired contradiction.

The useful remaining route is stronger: exploit actual low-degree multiplication, su(2) commutators, partial spinor trace, or the all-t D/R PSD face. Alternatively use more than the degree t+1 boundary. The two-error certificate itself already required more than naive syndrome-volume counting.

Priority of these bookkeeping observations is unassessed. The all-t rectangular-span claim is standard Clebsch–Gordan reasoning; a separate independent symbolic audit has been requested.
