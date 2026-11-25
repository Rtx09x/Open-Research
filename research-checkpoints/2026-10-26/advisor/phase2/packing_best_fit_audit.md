# Tiny all-container Best Fit: independent audit

**Status: analytic lemma/portability and exact pricing PASS,21:45 UTC.**
This is a new algorithm, not an improved analysis of the one-open variant whose
ratio was shown tight. All non-tiny rules and the three frozen quota transfers
are unchanged. Tiny items search every previously created tiny container and
choose the fitting one with least remaining advertised capacity. A new
quota-selected container is created only if no old one fits. Advertised
capacities never change, so existing bin partners remain physically safe.

## Residual lemma
Let d=1/43, Amin=17/60, and 0≤c≤d. Let H be the final containers with residual
strictly greater than c, and let L_>c be the total size of tiny items larger than
c. Except for the earliest member of H and possibly the last-created container,
each member contains more than Amin−d volume of >c items:

- An earlier final-high container remains above c at every preceding time.
  When the later container was created, that earlier residual was smaller than
  the creation item, hence below d.
- At the later container's first item of size≤c, the earlier container still
  fits. Best Fit can select the later container only if its pre-arrival residual
  is no larger, hence below d. Its prior load exceeds its capacity minus d and
  consists entirely of >c items.
- If no small item enters it, any subsequent creation already forces its
  residual below d; this covers every such container except the last-created.

Thus |H|≤L_>c/(Amin−d)+2. All but the last-created container have final residual
below d. If m is the number of containers, quota capacity sum is Bm+O(1), and
total tiny volume is T, then

    (B−c)m ≤ T + (d−c)L_>c/(Amin−d) + O(1).

For scenario required-weight mean b this proves the valid item charge

    f_c(s)=b/(B−c) · s · [1+(d−c)/(Amin−d)·1_(s>c)].

With p supported tiny types, capacities≤1 and quota discrepancies summing to
zero, an explicit additive constant is
ρ[p+2(d−c)]+p−1, where ρ=b/(B−c). Capacity discrepancy costs p−1, the possible
last residual costs1, the two high-residual exceptions cost2(d−c), and required
weight discrepancy costs p−1. The full worker theorem's finite-input constant
and quantifiers pass this additional audit.

This proof uses the strict condition s>c. It is not the old continuous hinge.

## Source portability
Reread the primary AH text, especially Lemmas3,5,9,10,19,20. Matching and large
temporary/declared transitions use advertised volumes and creation/type-change
events, not tiny eligibility flags. Quota Lemma19 uses only counts at creation.
The tiny conclusion of Lemma10 survives with a new proof: at every creation all
old residuals are below the new item≤d, and residuals only decrease thereafter.
The new residual charge replaces the tiny weight argument. Small/large class
proofs and the previously audited scenario endpoint repair remain unchanged.

Primary: [Balogh et al., Sections3 and5](https://arxiv.org/html/1707.01728).

## Exact offline pricing
For 0<c<d and residual capacity r>0, let n be the largest integer with nc<r.
The supremum volume assignable to >c tiny items is min(r,nd), zero when r≤c.
At c=d the extra coefficient vanishes; c=0 can be treated separately. This
handles threshold discontinuities and strict non-tiny lower endpoints.

`check_packing_best_fit.py` independently reparses primary parameters using the
advisor's frozen source parser, checks every published analysis weight, and uses
a reduced-profit-density exact Fraction recursion. No worker or Pro imports.
All402 scenarios/804 strict knapsacks pass,23,108 nodes,2.72 seconds, proving

    R ≤ 174191383514152461065273968497444592350661 /
        110371486054812972793114744355465098952704
      = 1.5782281252210837… .

Certificate SHA256:
efd98b3ab6c17d81ad14da565410c47de2490b99c8c4742c9e3ebde183a8e315.
Thresholds are3/200 on(49/320,1/6),1/60 on(533/1600,1/3) and(3/7,1/2), and d
elsewhere. The algorithm itself does not know the retrospective scenario.

No tightness, universal lower-bound improvement, or publication priority is
claimed for this Best-Fit variant.
