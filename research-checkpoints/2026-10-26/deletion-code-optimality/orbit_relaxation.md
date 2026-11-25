# Sound symmetry use — and what it does not prove

Complement and reversal preserve the deletion-conflict graph. Let G be their four-element automorphism group, and O its orbits on all words. For an arbitrary (not assumed invariant) code C define z_O=|C∩O|. Averaging its indicator over G gives y_x=z_O/|O| for x∈O.

For each deletion-output clique Q, every transformed code gC contains at most one element of Q. Averaging therefore yields

    sum_O (|Q∩O| / |O|) z_O <= 1.

The same argument applies to any universally valid inequality, including insertion cliques, maximal conflict cliques, subcode bounds, and integer odd-walk cuts. Thus requiring integer z_O between0 and|O| is a necessary condition for every code; its objective sum z_O is the original code size. It is not sufficient: different orbit counts may have no simultaneously compatible choices of actual words.

For n12 orbit sizes are2 or4. Multiplying every inequality by4 gives exact integer coefficients. The model has1,056 orbit variables. All-zero and all-one may be included in a maximum code by replacing a conflicting weight1/weight11 word with the corresponding constant word; this never decreases size. Their two-word orbit is consequently fixed to2 in our bounding relaxation.

Using real y is also a valid LP symmetry reduction. If the original row family is group-closed, averaging proves equality of original and quotient LP optima. We use all deletion rows, all insertion rows, and when selected all maximal clique rows, so this equality holds. For a single valid cut not accompanied by its transforms, its **averaged inequality** on z remains valid for every integer code by the argument above, although equality to an arbitrarily incomplete original LP need not hold.

Dangerous alternative explicitly avoided: forcing y_O binary, or z_O∈{0,|O|}, assumes C is invariant. Such a model can be used to find constructions or to prove a restricted-family result only, never an unrestricted upper bound.

## Exact dual verification

`certify_lp.py` eliminates the fixed constant orbit, rounds nonnegative row multipliers upward to denominator10^8, and repairs any remaining column shortfall with nonnegative upper-bound multipliers. An integer-only check verifies A^Tλ+μ≥1 and computes b^Tλ+u^Tμ plus the fixed2 words. This does not rely on solver optimality or feasibility tolerances. A bound321.13 is rigorous but weaker than published320; such a certificate is a reproducibility control, not a frontier advance.
