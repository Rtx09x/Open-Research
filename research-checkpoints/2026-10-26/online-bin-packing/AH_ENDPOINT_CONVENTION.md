# Advanced Harmonic: an explicit interior-threshold convention

Audit date: 2026-10-25. This note records a boundary clarification found by independently reading the primary proof. It is an analytical repair, not a change to the online algorithm or its rational parameters. It does not assert that the published numerical result is false.

## Why say this explicitly?

The [primary full paper, §4.2](https://arxiv.org/html/1707.01728#S4.SS2) labels scenarios by `1−a ∈ (x,y]`. In [§4.3.1](https://arxiv.org/html/1707.01728#S4.SS3.SSS1), the exact-threshold description assigns required weight 1 to a positive container of volume at least `a`, while its scenario-level formula assigns weight `w` when volume is at most `1−y`. At `1−a=y`, a container of volume `1−y=a` falls into both descriptions, with different values if `w<1`. Merely confirming that the closed interval endpoints are listed does not resolve this convention issue. The two numerical checkers use the scenario-level formulas.

The following choice removes that ambiguity and also makes the negative-container endpoint convention unambiguous.

## Interior-threshold lemma

Fix any finite nonempty input and run the stated AH algorithm. A positive or negative container is *unmatched* when it is alone in its bin. Let

- `p` be the smallest unmatched positive-container volume, or 1 if none exists;
- `n` be the smallest unmatched negative-container volume, or 1/2 if none exists.

Set `L=max(0,1−p)` and `U=min(1/2,n)`. Then `L<U`.

If both kinds exist, this follows from `p+n>1`, the strict invariant in [Lemma 3](https://arxiv.org/html/1707.01728#Thmtheorem3), together with `p>1/2` and `n>0`. If either kind is absent, it follows immediately from the chosen default and positivity. Choose any `t` in the nonempty open interval `(L,U)` that is not in the paper's finite breakpoint set `V`, and define `a=1−t`. Such a choice always exists; no algorithmic computation of it is needed.

Consequently:

1. `0<t<1/2` and `1/2<a<1`.
2. Every unmatched positive container has volume **strictly greater** than `a`.
3. Every unmatched negative container has volume **strictly greater** than `t=1−a`.
4. There are consecutive breakpoints `x<y` with `x<t<y`. In particular `1−y<a<1−x`.

The fixed container-volume comparisons in the certificate now agree exactly with the threshold definitions: a positive fixed volume at most `1−y` is below `a`; one at least `1−x` is above `a`. A negative fixed volume at most `x` is below `t`; one at least `y` is above `t`. Exact sizes of singleton huge items and threshold-class large items remain handled by the source's size-dependent rules.

## Why the source weight argument still works

This uses the *proof* of [Theorem 24](https://arxiv.org/html/1707.01728#Thmtheorem24), not a claim that the newly chosen `a` is literally the minimum unmatched positive volume in its opening definition.

The basic-class argument in [Lemma 17](https://arxiv.org/html/1707.01728#Thmtheorem17) only needs unmatched positive/negative containers to be on the appropriate sides of the threshold; (2)–(3) provide stronger statements. In the large threshold-class proof, smaller temporary singletons are those of volume at most `t`. None can remain unmatched at termination by (3). [Lemma 11](https://arxiv.org/html/1707.01728#Thmtheorem11) then uses the algorithm's largest-temporary-singleton selection rule. [Lemma 12](https://arxiv.org/html/1707.01728#Thmtheorem12) uses that same rule and the definition of the last time without a bigger temporary singleton. Neither requires the existence of an unmatched positive container with volume exactly `a`. The counting estimates and subsequent algebra in Lemmas 13–16 are unchanged. Thus the same feasible `u,v,w` inequalities yield `ALG(I)≤W(I)+Ψ`.

The [two offline-bin knapsacks in §4.4](https://arxiv.org/html/1707.01728#S4.SS4) remain valid: their capacities 1 and `y` overestimate the relevant infimum-size patterns, and `t<y` strengthens the residual-capacity condition for a weight-one huge item. The tiny-only pattern is included by zero non-tiny items and sand. These remain **strict** knapsacks; they should not be changed to allow non-tiny infimum sizes summing exactly to capacity.

There are finitely many scenario/threshold classes. Their additive constants depend only on the fixed parameters, not the chosen interior point or input size, so one may take their maximum. Therefore complete certification of the existing 402 open interiors and both knapsack cases per interior suffices for the asymptotic upper bound, including actual inputs whose original minimum-volume threshold happens to hit a breakpoint. The empty input is trivial.

## Suggested short addition to the result proof

> For endpoint clarity we choose the analysis threshold `t=1−a` strictly between `max(0,1−p)` and `min(1/2,n)`, avoiding the finite breakpoint set, where `p,n` are the smallest unmatched positive and negative container volumes (defaults 1 and 1/2). Lemma 3 makes this interval nonempty. Every unmatched positive has volume above `a`, and every unmatched negative has volume above `t`; the proof of Theorem 24 therefore applies unchanged. This selects an interior scenario and removes endpoint ambiguity without altering AH or its parameters.

Status: mathematical boundary clarification checked against the cited proof; not formalized in a proof assistant or externally reviewed.
