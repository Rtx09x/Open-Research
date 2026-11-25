# A concrete next target, not part of the certified numerical claim

The present Best Fit theorem conservatively replaces every high-residual container's capacity by A_min. A future type-resolved conservation analysis could retain more information. This note records a finite mathematical target rather than starting another parameter sweep.

Let `a_i=A_i-d`, and let h_i count final high-residual containers of each type. The chronology lemma actually proves

`sum_i a_i h_i <= L_{>c}+O(1)`.

The fixed quotas also give `h_i<=alpha_i m+O(1)`. In the current two-type case, a1<a2. Consequently both of the following bounds hold:

```
h1+h2 <= L_{>c}/a1+O(1),
h1+h2 <= L_{>c}/a2 + alpha1*(1-a1/a2)*m+O(1).
```

The first is the certified theorem's inequality. Combining the second with the same waste bound would give

```
[B-c-(d-c)*alpha1*(1-a1/a2)] m
    <= T+(d-c)*L_{>c}/a2+O(1).
```

Its denominator stays positive since it is at least B-d>0. This suggests another valid step charge, or a properly justified convex combination of the two aggregate inequalities. Any improvement must still price the discontinuities exactly and recheck all402 scenarios; neither a pointwise minimum of charges nor optimization of active patterns alone is justified.

No new threshold was tested using this refinement, no new numerical bound is claimed, and the Best Fit algorithm's true ratio remains unknown. The current preferred bound stays frozen at1.5782281252210837. This is a sensible next structural proof target after parent/model/novelty review, not a reason to extend a blind tuning chain.
