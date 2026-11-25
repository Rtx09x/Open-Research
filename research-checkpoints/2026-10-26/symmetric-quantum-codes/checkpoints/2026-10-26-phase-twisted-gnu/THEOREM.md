# Phase-twisted gnu: an explicit all-t construction candidate

**Status:** internally independently audited theorem; advisor and root analytic checks passed. External review remains unresolved. No novelty, best-known, publication-priority, or full-minimum claim. This is a new route within this project, not a claim that complex phase constructions are new in the literature.

## Statement

For every integer t>=10, there is a complex rank-two code in Sym^n(C^2) correcting arbitrary t physical-qubit errors at

    n=4t^2+2t.

This is one qubit below the explicit uniform upper construction n=4t^2+2t+1 of Aydin–Alekseyev–Barg, arXiv2310.05358v3, Construction5.1 and Theorem5.3. It does not approach or prove the conjectured3t^2+3t+1 sharply. Other published constructions and priority must be checked separately. For t<=9 this particular phase-only family is impossible, as shown by the exact polygon controls; that does not exclude other families.

## 1. Family and all KL equations

Set m=2t+1, g=2t, n=gm, and p_i=binomial(m,i)/2^(m-1), i=0,...,m. Choose unit complex numbers zeta_i. Define

    |0_L> = sum_(i even) sqrt(p_i) zeta_i |D_(gi)^n>,
    |1_L> = sum_(i odd)  sqrt(p_i) zeta_i |D_(gi)^n>.

The two states are orthogonal and normalized. All diagonal spin polynomials of degree<=2t compress to scalars, because

    sum_i (-1)^i binomial(m,i) i^h=0,  0<=h<m.

A spin polynomial of degree<=2t has magnetic bandwidth<=2t=g. Distinct support nodes are separated by g. Therefore its only potentially nonzero off-diagonal matrix elements on the union support have shift g. The shift-g component of this operator space is one-dimensional, spanned by the ladder power J_+^g (or its adjoint). It remains to cancel, separately, its two directed logical cross entries.

Let

    a_i = sqrt(p_i p_(i+1) (n-gi)_g (gi+1)^(rising g)),
    eta_i = zeta_i conjugate(zeta_(i+1)),  i=0,...,2t,

where (x)_g is the falling factorial. The two requirements are exactly

    sum_(i even) a_i eta_i=0,
    sum_(i odd)  a_i eta_i=0.                         (1)

No logical diagonal off-shift entry exists: adjacent support nodes belong to different logical columns. Adjoints are automatic. Thus (1), together with the binomial identity, gives the full rank<=2t scalar compression, and hence physical t-error correction.

**Phase compatibility is explicit, not assumed:** for any assigned unit eta_i on the path, set zeta_0=1 and recursively

    zeta_(i+1)=zeta_i conjugate(eta_i).

Then the desired edge products hold exactly. There are no cycles, so the two directed edge families can indeed be assigned independently.

## 2. Symmetry and explicit phases

The positive amplitudes satisfy a_i=a_(2t-i). The parity class not containing the central index t has an even number of indices, paired by i<->2t-i. Set their paired phases to +1,-1, so they cancel.

For the class containing t, set eta_t=1. If t>=11, put b=a_(t-2) and choose

    c=a_t/(2b),   e=c+i sqrt(1-c^2),
    eta_(t-2)=-e, eta_(t+2)=-conjugate(e).

Provided c<=1, those three terms sum to zero. Assign all remaining mirrored pairs phases +1,-1. This is an explicit algebraic construction.

For t=10 use b=a_8+a_6, set c=a_10/(2b), and use phases -e on edges6,8 and -conjugate(e) on edges12,14. Again the central contribution cancels, and every other mirrored pair receives opposite phases.

The next section proves all required strict inequalities; hence every square root is real and all assigned phases have unit modulus.

## 3. Uniform inequality

Up to a positive factor independent of i, the squared amplitude is

    A_i = binomial(2t,i)^2
          product_(s=1)^(2t-1) (i+s/(2t))(2t-i+s/(2t)). (2)

This follows by cancelling the factors g(i+1), g(2t-i+1) in the ladder factorials against the two adjacent binomial coefficients. In particular

    (a_t/a_(t-2))^2
      = [((t+1)(t+2)/(t(t-1)))^2]
        product_(s=1)^(2t-1) [1-4/(t+s/(2t))^2]^-1.   (3)

For t>=13, log(1+x)<=x and -log(1-x)<=x/(1-x) give

    log(a_t/a_(t-2))
      <= 3/t + 1/(t-1) + 2(2t-1)/(t^2-4)
      <= 3/13+1/12+50/165 < 2/3 < log2.              (4)

Each term in the middle expression decreases for t>=13; for the last term its derivative has numerator -4t^2+4t-16<0. The final log2 inequality follows, for example, from log2=2 atanh(1/3)>2/3. Thus a_t<2a_(t-2) uniformly.

For t=11 and12, the exact rational expression (3) is <4. For t=10, exact rational comparison in (2) gives

    A_8/A_10 > (19/40)^2,
    A_6/A_10 > (1/40)^2,

so 2(a_8+a_6)>a_10. These are finite exact controls, not numerical extrapolation.

## 4. Direct all-t physical proof, exact checks, and negative controls

For k=g=2t erasures, a diagonal reduced-Gram coefficient is

    C(g,a) C(n-g,gi-a)/C(n,gi)
      = C(g,a)(gi)_a(n-gi)_(g-a)/(n)_g.

It is a polynomial of degree at most g in i, so the alternating binomial sum vanishes. Off-diagonal reduced-Gram entries require gi-a=gj-b. Since0<=a,b<=g, unequal support nodes can match only for |i-j|=1 and {a,b}={0,g}. Equal logical parities never match in this case. The four remaining cross entries are precisely the two edge sums, or their conjugates, times the common positive factor1/(n)_g. Thus the construction satisfies every physical g-erasure KL equation directly. Symmetry makes the condition identical for every g-qubit subset, which is equivalent to correcting arbitrary t errors. This proof does not require any assumption about intrinsic syndrome rank or time reversal.


`check_phase_twisted_gnu.py` constructs the exact squared physical coefficients using binomial partial trace, separately from the spin-ladder formula. At t=10,n420,k20 it verifies normalization, every diagonal reduced-Gram equality, the exact support zeroes of all other entries, the shared conversion factor for the two off-diagonal boundary entries, and the algebraic phase-closure conditions. It also verifies the factorial reduction(2), inequalities at10–12, and the rational bound in(4).

For t=1,...,9, the central amplitude exceeds the sum of all other amplitudes in its parity class, so (1) cannot close for any phases. The checker certifies each inequality by outward rational square-root intervals, not floating-point residuals. This is only a failure statement for the specified phase-twisted uniform support.

## 5. Implication and limitation

This construction improves the stated explicit AAB all-t upper formula by one for t>=10, while retaining leading constant4. More importantly, it exposes a reusable exact construction mechanism: support moments plus unit-phase closure on a transition graph. It also disproves any proposed universal assertion that a code with the minimum possible2t+2 axis-support nodes must have n>=4t^2+2t+1. The previously checked t2/t3 sparse thresholds cannot be extrapolated to all t.

For smaller gaps t<g<2t, only adjacent support transitions still occur, but each direction must now cancel polynomial moments through degree2t-g. This becomes a prescribed-modulus vector in a real Vandermonde nullspace. A univariate nonnegative-polynomial interpolation formulation is a possible next gate, not a proved all-t construction at leading constant3.
