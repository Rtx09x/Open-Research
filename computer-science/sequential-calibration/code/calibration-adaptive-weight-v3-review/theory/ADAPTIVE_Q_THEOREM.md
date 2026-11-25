# Candidate theorem: state-dependent continuation weights

**Status, 26 October 2026: uniform proof and full-domain inequalities independently checked within the research team. Two arithmetic backends passed. This is an internally verified theorem draft, not external peer review or comprehensive priority clearance.** This changes the algorithm, not the six numerical parameters of the published fixed-shift algorithm. The new choice is made from count ratios available at the trigger; it never uses future traffic.

## 0. The strengthened local trace domain

Only the ROOT is a standalone SPR game with mandatory full-board termination. Internal A instances are persistent labeling subroutines: local fullness does not terminate their counters or recursive state, and a later external erasure may permit another call.

For an instance J, a sign is J-owned exactly when it was placed in response to a request processed by J or a descendant. Its owned inventory starts empty; physical signs predating initialization are foreign and are not counted. Define E(I,w) to contain all finite owned-board traces that interleave arbitrary external erasures (no owned insertions) with local requests at cells EMPTY OF OWNED SIGNS. Each local request eagerly removes its eligible owned signs, executes the specified persistent subroutine, and inserts its returned sign. A full owned board permits no further request until an erasure frees a cell; unlike the original root game, there is no automatic local termination. This is an induction domain, not a replacement of the target game.

Every real global history projects into E for each instance: globally empty implies owned-empty; global eager deletion removes all eligible owned signs; requests handled elsewhere only erase owned signs or place foreign signs. The same projection holds recursively from a parent E-trace to every half child and continuation child. Each child's code and counters persist through external erasures. Hence the induction below is proved DIRECTLY for E, not inferred from ordinary SPR optimality or from an assertion that extra erasures can only help future play.

Cohort accounting remains disjoint within each parent: earlier-epoch signs, current phase-one child signs and continuation signs come from disjoint placement requests. A physical sign can be owned by several ancestors without being counted twice in one parent's decomposition. Full details and a stepwise induction-domain audit are in `EXTERNAL_ERASURE_INDUCTION.md`.

## 1. The algorithm

Use binary equal splits and epochs, including the exact pointer stop and full-board rules of SPR. Delete every eligible sign before every response. (The signed-subset dominance lemma justifies this restriction for optimal play, although only legality is needed for this upper-bound strategy.)

An instance `A(I,w)` has real weight `w>0`, total request count `count`, and a current epoch `B(I,w,tau=count_at_epoch_start)`. For one cell it returns `+` when `w>=1`, otherwise `-`. For more cells, an epoch initializes two half-interval instances with the SAME weight `w`, and counters `t0=t1=0`. A request is answered by the appropriate child, after incrementing its counter. Let `h=max(t0,t1)` and `l=min(t0,t1)`. At the FIRST request such that

    delta*l >= tau  and  l >= rho*h,

enter continuation, with `L=floor(kappa*h)`. The triggering request is answered by the old child, not by the continuation. Define the NOMINAL threshold ratio

    z=tau/h, r=max(rho,z/delta).

Necessarily `rho<=r<=1`, and either `r=rho` or `z=delta*r`. Define `q=q(z,r)` below. The next `L` requests are answered by a NEW same-interval instance whose weight is `w*q` for a right-half trigger, and `w/q` for a left-half trigger. The epoch returns exhausted on the next request, so the parent initializes its next epoch and answers that same request there. If `L=0`, no continuation instance is needed.

Weights are never reset globally; each new same-interval instance gets the specified weight. Old physical signs are NOT cleared on an algorithmic restart. External requests may clear signs but do not change an instance's counters.

## 2. Exact rational-decimal parameters and continuous obligations

Candidate constants:

    alpha = 0.0102, beta = 0.9475,
    rho = 0.0097, kappa = 0.6, delta = 14.8,
    Kp = 0.856, Kt = 0.902,
    P0 = 0.85599, Q0 = 0.9019, qmax = 0.76,
    F = 10^10, C = F^2/Kp.

Every displayed decimal means the exact terminating rational, not a binary float.

Put `H=2^alpha`, `U=H*kappa^beta`, and, on the compact trigger domain

    T = {(z,rho):0<=z<=delta*rho}
        union {(delta*r,r):rho<=r<=1},

put

    S=(z+1+r+kappa)^beta,
    B=Kp*z^beta+r^beta,
    P=Kp*z^beta+1,
    A=P+r^beta,
    q(z,r)=max(1/2, U/(P0*S-B)).

The interval verifier must prove uniformly on BOTH closed segments:

    P0*S-B > 0,
    q <= qmax,
    P + q*U <= P0*S,
    A + q*U <= Q0*S.                          (E)

**Pointwise bias-elimination lemma.** Among factors in `[1/2,qmax]` that meet the completed-minus budget `B+U/q<=P0*S`, this q is the smallest possible. Every plus envelope is increasing in q, so checking (E) at this q is necessary and sufficient for simultaneous endpoint feasibility within that interval. Thus the function is analytically selected, not fitted on sampled trigger states.

The formula for `q` then automatically gives `B+U/q<=P0*S`: if the fraction is >=1/2, equality holds; otherwise `B+2U<=P0*S`. Do not interval-divide before proving the denominator positive.

Let `s=1/(1-beta)` and

    x=min(1/delta, Kp^(-s)),
    M=max( (((Kp+x^beta)/(1+x)^beta)^s+1)^(1/s),
           (Kp^s+((1+rho^beta)/(1+rho)^beta)^s)^(1/s) ),
    D=max( (Kt^s+1)^(1/s), (M^s+(qmax*H)^s)^(1/s) ).

The scalar verifier must prove

    0<P0<Kp<1, P0<Q0<Kt, Kp<Kt, Kp<=M<=D,
    P0*(1+1/F)+F^(-beta) < Kp,
    Q0*(1+1/F)+F^(-beta) < Kt,
    D+F^(-beta) < H.                          (S)

These are sufficient obligations; none is only a finite-horizon test.

## 3. Claimed uniform induction, conditional on (E) and (S)

For every instance A on a power-of-two board of n cells, every weight w>0, every deletion-augmented owned-cohort trace in E(I,w), and every number t of requests answered by A,

    remaining_plus(A)  <= C*w*n^alpha*t^beta,
    remaining_minus(A) <= C/w*n^alpha*t^beta.    (I)

`remaining` counts only signs originally placed in response to requests handled by this instance or its descendants, not arbitrary preexisting signs unrelated to it. External deletions can only reduce these counts.

At the start of each epoch of A, with earlier request total tau, use the stronger inherited bounds, separately for sigma=+1,-1:

    persistent_sigma <= C*w^sigma*(n/2)^alpha*Kp*tau^beta,
    total_sigma      <= C*w^sigma*(n/2)^alpha*Kt*tau^beta. (J)

Persistent means plus in the left half or minus in the right half.

### 3.1 Well-founded induction and small executions

Induct on n, then strongly on t at fixed n, uniformly in positive real w and over the full trace class E. The recursive projection lemma above supplies the induction hypothesis for the actual child histories, including local full-and-resume histories. Half-interval children decrease n. A same-interval continuation answering c requests has parent count at least h+l+c, and `c<=L<=h`; thus parent count is at least `2c`. Hence any such call decreases t, and each weight change along a call chain consumes a factor of at least two in request count.

Each change multiplies weight by a number in `[1/2,2]`. If a chain returns sign sigma, its leaf satisfies `w_leaf^sigma>=1`. For j changes, `w^sigma>=2^(-j)>=1/t`. Consequently for `t<=F`, `C*w^sigma*n^alpha*t^beta>=C/t>=t`, and with the stronger inherited prefactor `C*Kp/t>=F^2/t>=t`. This handles arbitrarily small/large real weights and all small epochs. At n=1, at most one OWNED sign remains at any prefix and its type has `w^sigma>=1`, even if the cell has repeatedly been filled, externally erased and requested again. We do not assume a leaf receives at most one call. At t=0 the count is zero.

### 3.2 Trigger orientation and surviving inventories

At the first trigger, the half just requested is light (ties allowed): if it had been strictly heavy after the increment, the light count was unchanged and the heavy count only rose, so neither previously false condition could become true. For a right trigger, the left count is h and the right count is l. Both halves have been visited; therefore only persistent inherited signs remain. The right trigger deletes every minus placed by the left child. Throughout continuation of length c, normalize each sign by `C*w^sigma*(n/2)^alpha`. The exact upper envelopes are

    total_minus      <= Kp*tau^beta + l^beta + (H/q)*c^beta,
    persistent_plus  <= Kp*tau^beta + h^beta + (H*q)*c^beta,
    total_plus       <= Kp*tau^beta + h^beta+l^beta+(H*q)*c^beta. (R)

They count old signs plus newly placed signs, never resetting physical inventories. For a left trigger exchange plus/minus and replace w by 1/w in these expressions. The same q function applies because h,l,tau are unchanged by reflection.

### 3.3 Completed epochs and rounding

Let `l0=r*h=max(tau/delta,rho*h)`, `L0=kappa*h`,
`u=tau+h+l+L` and `u0=tau+h+l0+L0`.
First-trigger timing gives `l0<=l<l0+1`; floor gives `L<=L0<L+1`; hence `u0<u+1`.
For `0<beta<1`, `l^beta<=l0^beta+1`.
Using (E), the normalized two persistent envelopes in (R) are bounded by `P0*u0^beta+1`, and total-plus by `Q0*u0^beta+1`. Total-minus has the stronger persistent bound and therefore also fits the total bound because `P0<Q0` (verify this scalar range). For `u>F`,

    P0*u0^beta+1 <= [P0*(1+1/F)+F^(-beta)]*u^beta < Kp*u^beta,

and likewise with Q0,Kt. Here `(1+1/u)^beta<=1+1/F`. This reestablishes (J) at the next epoch. If u<=F the small-execution argument above establishes (J). Any deletion on the next epoch's first request can only help.

### 3.4 Every unfinished epoch

If only one half has been visited, total inherited coefficient Kt is needed. Weighted concavity gives

    Kt*tau^beta+h^beta <= D*(tau+h)^beta.

If both halves have been visited and phase 1 has not ended, either `delta*l<tau` or `l<rho*h`. The explicit expression for M bounds

    Kp*tau^beta+h^beta+l^beta <= M*(tau+h+l)^beta.

For completeness: when `l<tau/delta`, first combine the inherited and light contributions. Their normalized ratio is `(Kp+x^beta)/(1+x)^beta` with `x=l/tau<=1/delta`; its maximum occurs at `x=min(1/delta,Kp^(-1/(1-beta)))`. Then combine this bound with `h^beta` using weighted concavity. When `l<rho*h`, the ratio `(1+x^beta)/(1+x)^beta`, `x=l/h<=rho<=1`, is increasing, so replace x by rho and combine with `Kp*tau^beta`. These are exactly the two terms defining M. Cases of zero counters follow by continuity. At the triggering request the same bound holds with an additive 1, by applying the preceding inequality with l-1 and using `l^beta-(l-1)^beta<=1`.

During a right continuation, total-plus in (R), `q<=qmax`, and weighted concavity give

    total_plus_normalized <= D*(tau+h+l+c)^beta+1.

For total-minus, define

    f(c)=Kp*tau^beta+l^beta+(H/q)*c^beta
         -Kp*(tau+h+l+c)^beta.

For c>0 its derivative is positive: `H/q>1>Kp` and `beta-1<0`. Thus `f(c)<=f(L)`. If current total `t=tau+h+l+c>F`, then completed total `u>=t>F`, the endpoint **algebraic inequality** from Section 3.3 gives `f(L)<0`. This substitution does not assume that the remaining L-c requests can legally occur, and does not invoke the induction hypothesis at a hypothetical future time u: only the current continuation count c uses that hypothesis; f(L) is bounded directly from (E), integer counts and rounding. This proves the minus bound for EVERY c in `[0,L]`, including c=0 by continuity. For t<=F use the small-time case. Reflection treats left continuations.

All cases have envelope `D*t^beta+1` in the half-interval normalization. Since `t>F`, (S) gives `D+t^(-beta)<H=2^alpha`, proving (I). The E-domain claim holds at every local prefix, including after resumption following an external erasure. When restricted to the actual root game, a pointer stop uses exactly this bound at that prefix and a full ROOT board ends at such a prefix. No extension past a root-terminal board is assumed.

## 4. Conditional transfer and what remains to verify

At root w=1, sum the two signs. For arbitrary n, pad to a power of two N in `[n,2n)` and never request padded cells; if the original board fills, Pointer stops in the padded simulation. This gives `opt(n,t)<=2^(1+alpha)*C*n^alpha*t^beta` uniformly. If (E),(S) and the induction audit pass, Dai–Fishelson Theorem 5.1 yields epsilon=.0423 and theta=2.0423/3.0846 (about .66209557155).

Completed: independent reconstruction from the algorithm, outward-rounded certificates for (E),(S), a second exact-integer rational-power replay, and review that the cited transfer accepts any legal uniform SPR strategy. See `../certification/INDEPENDENT_AUDIT.md` and associated certificate scripts/results. The adaptive-q function changes the algorithm; absence from the inspected papers alone does not establish comprehensive priority.


## 5. Exact rational realization (same theorem)

The proof only needs a function q in `[1/2,qmax]` satisfying the three endpoint budgets; it does not require the minimal analytic formula. On every interval of the certified trigger cover, take the interval upper enclosure of q* and round it UP to a rational with denominator `2^48`. The compiled factor is at least q* everywhere on its interval, so the minus endpoint budget still holds; both plus budgets and q<=qmax are rechecked on that whole interval. `compile_rational_policy.py` constructs and checks the resulting 4,988-row table in `rational_q_policy.json`. The minimum certified plus margin remains positive.

At runtime z=tau/h is rational. If z<=delta*rho, locate z on the first segment; otherwise locate z/delta on the second. At a shared boundary choose the first containing closed interval. Coverage is exact and both endpoint choices are certified. The weights then remain rational products/quotients, and the leaf sign comparison w>=1 is exact. `adaptive_policy.py` implements this policy with `fractions.Fraction`. Its bounded-history checks exercise operational invariants only and are not a substitute for the uniform proof.
