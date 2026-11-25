# A causal obstruction for the shared marked-B / D-versus-E-then-half fork

## Result and scope

At the inherited nine-state t=3 prefix and r=3857/2500=1.5428, the proposed shared marked-B fork is defeated by a simple causal policy over an entire interval of B pair/quartet proportions. It survives every B-prefix stop, every E-prefix stop up to the proposed E count, every subsequent near-half C count, and every complementary D count.

This is a **restricted-family obstruction**, not an all-input competitive algorithm, not a new universal lower bound, and not a resolution of the full packing gap. The earlier upper-bound artifacts and all phase2 files remain unchanged.

The inherited prefix and the initial forced-mark proposal are from the audited external note in `extra-high/packing-round1/`. The primary adversarial separator and original eight-stop family are [Balogh et al., arXiv1807.05554, Sections2–4 and Theorem1](https://arxiv.org/html/1807.05554). We reuse those established constructions rather than infer causality from a fractional LP.

## 1. One shared causal policy

Let z=r/6 be the number of prefix bins per N and t=(2-r)/6 the mass of old bins that can receive a near-half item: types(0,0,2) and(0,6,1). Keep all old bins untouched by the new B and E streams.

For a rational paired-item fraction f, put fraction f of the B items into new pairs and the rest into new quartets. A fixed periodic schedule does this online, with only bounded incomplete-period error. Define

```
beta=(1+f)/4,       # new B bins per B item
alpha=(1-f)/4,      # quartet bins per B item
ready=f/2,         # B-pair bins per B item
lambda=(1+f)/6.
```

Mark B large iff it is inserted into a bin already containing at least two B items. Each quartet has two marks and each pair none, so

`h=(1-f)b/2+O(1/N)`.

The proposed E count is `(b-h)/3`, hence at most `lambda*b+O(1/N)`. Every E is placed in a **fresh double-E bin**. This is a causal decision independent of whether or how many C items later arrive. The old and B-pair near-half slots are all preserved.

On the D branch, or once C arrives after E, fill those preserved slots first and then use one new bin per remaining above-half item. The fork is identifiable from the arriving item sizes. The policy has committed to exactly the same B history before that revelation.

For the concrete choice f=1/5, repeat one pair and two quartets every ten B items. Thus beta=3/10, alpha=1/5, ready=1/10, h=2b/5 and the E cap is e<=b/5. No knowledge of the eventual B length or stopping time is used.

## 2. Leading-size costs and actual-OPT lower bounds

Write a=3/14 and s=5/14. At normalized lengths b,e,c,d, the online costs, up to O(1/N), are

```
A_B = z+beta*b,
A_E = z+beta*b+e/2,
A_C = max(A_E, z-t+alpha*b+e/2+c),
A_D = max(A_B, z-t+alpha*b+d).
```

Physical volume and the fact that C and D exceed1/2 give lower bounds on the **actual** offline optimum:

```
OPT_B >= 1/6+a*b,
OPT_E >= 1/6+a*b+s*e,
OPT_C >= max(c, 1/6+a*b+s*e+c/2),
OPT_D >= max(d, 1/6+a*b+(4/7)*d).
```

Only these lower bounds are used for survival. A constructive offline upper bound alone could not establish that a defender survives.

The B stop is safe if `r*a>=beta`. The E stop is then safe because `r*s>1/2`. The first expression in the C/D maxima is already covered by the corresponding earlier stop.

For fixed b,e, the second C expression has its worst comparison at the intersection

`c*=1/3+3b/7+5e/7`.

Before that intersection the difference using the volume bound decreases with c because r/2-1<0; after it, the difference using the C-count bound increases because r-1>0. At the intersection the exact slack is

\[
\left(\frac{3(r-1)}7-\alpha\right)b
-\left(\frac12-\frac{5(r-1)}7\right)e.
\]

The coefficient of e is negative. On the whole cone `0<=e<=lambda*b`, the worst comparison therefore has e=lambda*b. Solving the resulting linear inequality in f gives

\[
f\geq\frac{1263}{8095}.
\]

The B inequality gives f<=403/1250. Consequently the open interval

\[
\boxed{\frac{1263}{8095}<f<\frac{403}{1250}}
\]

has strictly positive margins and survives the full shared fork. It lies inside the earlier interval(304/4375,403/1250). These are sufficient surviving policies; failure of this particular lower-bound comparison outside the interval is not proof that those other policies lose.

At f=1/5 the exact B and C-cone coefficient margins are153/5000 and89/8750, respectively.

For D, the volume/count crossing is `d*=7/18+b/2`. The second expression's slack there is

\[
\frac{r-1}{18}+\left(\frac{r-1}2-\alpha\right)b.
\]

At f=1/5 these terms are1357/45000 and357b/5000, both positive. Thus this branch survives all nonnegative D lengths too, not merely the prescribed d=(b+h)/2.

## 3. Uniform finite perturbations and causal separation

Take the original C3,C2,A prefix, with A in its full published interval. Its actual volume per N is at least

`1/6-Delta`, where `Delta=(2053/7)*epsilon`.

Choose H=epsilon and B_i=3/14-H+d_i with0<d_i<epsilon^2. Apply the source separator theorem with SMALL meaning that B's destination has fewer than two previous B items. It produces gamma>0 such that every SMALL offset is at most gamma and every LARGE offset is greater than4gamma. No comparison between this new gamma and the old A-separator width is required.

After B, use

```
E=5/14+3epsilon-3gamma,
D=4/7+2epsilon-2gamma,
C=1/2+epsilon/4.
```

Then E+3smallB<=1, but any three-B online bin contains a marked B and cannot receive E. Also D+2smallB<=1 while a marked/small pair cannot receive D. The defender's B-pair items are both unmarked. Its quartets, E doubletons, and preserved old/B-pair half slots all satisfy the exact perturbed capacity inequalities. The source A spread is harmless because the online old-slot inequalities have fixed positive slack.

To avoid an error that grows with an arbitrarily long B stream, keep explicit slope margins. If B>=3/14-delta_B and E>=5/14-delta_E, the B coefficient decreases by r*delta_B; the C-cone coefficient decreases by

`2(r-1)*(delta_B+lambda*delta_E)`.

For f=1/5, even delta_B=delta_E=1/10000 leaves both positive, and `r*(5/14-delta_E)>1/2`. The prefix deficit contributes at most `r*Delta*N` after the crossing comparison. D can also be bounded using only its size>1/2, in which case the already positive direct-half comparison applies whenever D fits the preserved slots.

Thus the bound is uniform in b,e,c,d, not an unjustified O(epsilon*b*N) remainder. Choosing, for instance, `epsilon_N=1/(10^12*N^2)` makes the prefix deficit bounded independently of the continuation lengths. Fixed-period rounding and a possibly incomplete E pair add only O(1) bins. The inherited rational prefix macroperiod contributes its fixed O(period) additive term when N is not a multiple; this is independent of input length.

The exact verifier includes a genuine ten-arrival causal separator trace: each offset is chosen before the destination mark is observed, by binary search in an exponent interval. It verifies the observed marks and final multiplicative separation. The arbitrary-length existence is supplied by the primary theorem, not extrapolated from this trace.

## 4. Exact natural-length offline checks

At b=13643/15000 and f=1/5,

```
h=13643/37500,
e=13643/75000,
d=(b+h)/2=95501/150000.
```

The E stop admits e bins[E+3smallB], then the inherited B-stop packing for the remaining h large B; its cost is at most `1/6+b/3-5h/42` when the construction's count restrictions hold.

A valid final-C packing, avoiding the invalid below-base E+C+A pattern, uses:

* 1/2 bins[C+B+2A];
* y=(b-1/2)/2 bins[C+2B];
* e bins[C+E].

There are c=e+b/2+1/4=133001/150000 C items. All tiny pairs C3+C2 can be assigned because the last two classes accept respectively3 and6 pairs and `3y+6e>=1`. Every pattern's perturbed load is checked exactly. As C>1/2, this proves actualOPT=c at integral scales.

The defender's final cost is20107/15000, leaving exact margin

`r*c-ALG_C=3436619/125000000>0`.

This construction is supplementary: the all-length survival proof did not depend on obtaining a favorable offline construction.

## 5. The sign-reversal variant is also covered

An alternative B=3/14+H+d and E=5/14-3H-3gamma permits C+E+A, while losing the earlier4B+A offline pattern. That correct geometric change does not escape this obstruction. The defender's proof already allows either sign of sufficiently small B/E perturbations, every C length, and does not assume that C+E+A is forbidden. Its pairs/quartets, E doubletons and ready slots still fit. The complementary D=4/7-2H-2gamma remains above half and fits its two-small-B pairs.

Therefore another sign-reversed near-base fork with the same E cap cannot exclude this face. A successful successor must violate a genuine premise, such as forcing more E items than the unmarked-B/3 cap, changing the leading sizes/available pair structure, or introducing a further shared decision that makes the all-double-E policy untenable. Merely improving an offline packing after the same near-base stages is insufficient.

## 6. Reproduction and stopping conclusion

Run `python phase3/lower_shared/verify_shared_fork.py` from the worker root. It uses only exact standard-library fractions. It independently checks the full f inequality interval, finite perturbation margins, nine-state counts, causal separator trace, all geometry, natural offline counts and margins, and bounded incomplete-period errors. Output: `shared_fork_verification.json`.

This is the requested kill condition: one causal defender (in fact an interval) survives every stop of the proposed shared-history fork. No larger LP search is justified for this exact fork. The next native continuation returns to the separately documented type-resolved Best Fit conservation target, preserving the earlier upper theorem and its certificate unchanged.

## Independent audit checkpoint

Advisor independently checked the all-length algebra, perturbation hierarchy and causal rounding, and replayed the exact verifier in its own folder. PASS: `advisor/phase2/packing_shared_and_type_audit.md` and `packing_shared_replay/`. This remains a restricted-family obstruction.
