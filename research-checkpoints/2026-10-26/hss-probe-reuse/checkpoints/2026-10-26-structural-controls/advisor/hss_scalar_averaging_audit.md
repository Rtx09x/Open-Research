# Independent analytic audit: scalar fixed-basis averaging

2026-10-26 01:23 UTC. PASS for `hss-probe-reuse/phase2/scalar_near_optimal_averaging.md` as a separate standard corollary; this note does not modify the frozen scalar archive.

Rectangular row-orthonormal frames suffice for the unbiasedness induction. Conditional on inherited active frames, independent fine details are centered. The local da/dd/ad means recover the three projected diagonal blocks, while the averaged carried samples are exactly A_aa F and A_aa^T P. The coarser decoder is linear and depends only on the inherited frames. At the root only F0 F0^T=I2 is needed; the first two rows of I3 satisfy this. No inverse of the rectangular frame is invoked.

Thus E R(A)=P_C A for the prescribed scalar fixed linear class. Independent complete bank copies give independent centered reconstruction errors on A-P_C A. Their average stays in that same fixed linear class, so no rank inflation occurs. Orthogonality to the residual gives

    E||A-Bbar||_F² <= (1+800/t)||A-P_C A||_F²

using 3t forward plus3t transpose matrix-vector products. Choosing t=ceil(800/epsilon) proves the stated expected squared-Frobenius guarantee independently of depth. The parameter t here counts repetitions, not quantum error radius.

This is not an unknown-basis HSS theorem, an arbitrary-rank interlevel-mixing result, a claim about the error distribution of adaptively chosen bases, or a new general variance-reduction principle. It relies on independent full probe-bank repetitions, not reused samples.
