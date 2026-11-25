# Frozen C7 physical checkpoint — 2026-10-25 23:18 UTC

**No capacity improvement.** The current previously audited lower bound remains
3.258832624235574872655; its certificate is outside this physical checkpoint.
Unrestricted Shannon capacity and whether C7^5 has a368-code remain open.

## Exact results

1. The complete one-word-exchange component of published I0 consists of243
   size367 codes. Its377-word alphabet is357 isolated vertices plus fiveP4s,
   with restricted all-length capacity367. Advisor independently checked the
   full-space closure through factorized conflict minima.
2. Adding all60 words with one common-core neighbor gives437 words, still with
   a367-clique partition. Adding all405 words with two common-core neighbors
   gives842 words, again with an exact367-clique cover. Both alphabets contain
   I0 and thus have restricted capacity exactly367.
3. All maximum codes in842 are classified: exactly486=2·3^5. Their total support
   induces342 isolated vertices, fiveP4s and oneC30. The C30's alternating
  15-subsets give two243-code single-exchange components. The independent
   advisor rebuilt the alphabet, checked every elimination witness, and
   independently enumerated all surviving transversals.
4. `new_367_core_escape.json` is a valid367-code in the second component.
   It is not a coordinate-permutation/dihedral image of either published I0 or
   X: pair-distance histograms differ. This is not a claim of publication novelty.

## Corrected negative overlap replay

The same15-cycle core flip can preserve the old8ports and auxiliaryX. All base
axioms and8published exchanges remain valid. Fresh full overlap counts are
C1=25352, C2=11698980, C3=13949685, C4=741685629224688, q15=11899740.
The500-use rate is3.25882526526239299780, **worse**, not an improvement.

An earlier verbal smaller-q intuition was reversed and is superseded:
the published HetGao formula is
`o = J0.o0*oR + JH.q*hR + JV.q*vR`, so larger q contributes more neutral mass.
All five constants were freshly recomputed; no stale certificate was reused.
Replay resources:41.54s,752164KiB peak, hard1.5GiB/oneCPU/285s limits.

## Minimal verification

Copy this checkpoint to an isolated scratch directory first (checkers regenerate
result JSON files), then from its `physical_iteration/`, with Python3 only:

```sh
python verify_core_boundary_covers.py
python classify_second_boundary_maxima.py
```

These recheck physical membership/adjacency, the exact covers and all486-code
classification without SciPy or upstream imports. The supplied unchanged
independent advisor scripts provide a second mathematical implementation;
for isolated execution relocate only their hardcoded source paths to this
checkpoint (preserve originals and hashes). They require only Python stdlib.

The heavy changed-base replay requires the unchanged attributed `published/`
Python package from the main research tree, not included wholesale here.
Its outputs/ledger/log/resources are frozen. Do not rerun it as ordinary QA
without the parent's separate resource clearance. Likewise the optional
search/generator imports are not necessary for the two minimal exact checks.

`manifest.json` pins every included input/script/output. Historical upstream
source attribution is preserved in `published/NOTICE` and `published/LICENSE`.
The public July18,2026 radius≤5 I0 exchange exclusion predates this work and
must not be presented as new. No publication or external outreach occurred.
