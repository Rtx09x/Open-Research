# Two outside reservoirs plus retained core: exact target obstruction

## Result and scope

Let `I0` be the pinned published367-word code, let `Z` be the published
seven-rectangle134753-word length10 construction, and apply
`T(a,b,c,d,e)=(2-b,d,a,2-c,e) mod7` to each five-coordinate half of Z.
The **simultaneous** physical alphabet

    A = I0² ∪ Z ∪ T(Z)

has273778 distinct length10 words and an explicitly verified partition into
**135033 confusability cliques**. Consequently every independent code of
macro-length m over A has at most135033^m words. In particular its normalized
rate is at most135033^(1/10), approximately3.25869708137, strictly below
3.258698 and the working target3.258841. Both strict comparisons are integer
checks:135033*10^60 <3258698^10 <3258841^10.

This is a restricted-alphabet upper bound, **not** an upper bound for all C7,
and not a new lower-bound construction. The independent Z witness still gives
the lower bound134753. Thus the optimal selective-hole gain above|I0²|=134689
lies between64 and344 for this alphabet; gains65…344 have not been excluded.
The target135093 (gain404) is excluded, even using arbitrary macro-lengths.
Other reservoir pairs, larger unions and changed physical constructions are not
excluded by this certificate.

## Exact joint objective

See `multireservoir_model.md`. With S1=Z\I0² and S2=T(Z)\I0²,
the objective is134689 + selected outside words − deleted core words. Every
outside/core conflict forces deletion; every cross-reservoir conflict forbids
selecting both endpoints. Shared core neighbors are charged once. This is
exact, unlike simply adding two single-reservoir Hall deficiencies.

## Physical construction and partition

The source data are `../published/data/base_c7.json`, SHA256
`2395d9ce16e068010a5f2a57f3fbfec5a607fa9272b02afd6c9e4a95fc70016b`.
Use the published I0, X, PH=H, PV=V, private first endpoints R, B=I0\R,
Xh=X∩N(H), Xv=X∩N(V), and X0=X\(Xh∪Xv). The seven rectangles are

    B×B, R×X0, H×Xh, V×Xv, X0×R, Xh×V, Xv×H.

Each factor is independent and every pair of rectangles is separated in at
least one factor. Their union Z has134753 words. T is a coordinate permutation
with C7 rotations/reflections, so T(Z) is also independent.

The final certificate stores two explicit arrays:

1. `reservoir_matching_targets`: each of133729 sorted words of T(Z)\Z maps
   injectively to a confusable word of sorted Z. These give134753 disjoint
   singleton/pair cliques covering Z∪T(Z).
2. `core_matching_targets`: each of5296 sorted words of I0²\(Z∪T(Z)) either
   maps to a distinct one of those cliques and is confusable with **every**
   member, or has target−1 and is made a singleton. Exactly5016 attach and280
   remain singletons. Therefore the final partition has134753+280=135033 parts.

Literal confusability means every coordinate difference is0,1,or6 mod7.
The checker uses the actual ten coordinates, not abstract BPZ labels. These
cliques cover the entire deduplicated alphabet once; no favorable subset is
silently substituted. Products of their clique labels give at most135033^m
cliques at macro-length m, proving the all-length restricted upper bound.

## Reproduction and evidence

Final certificate:
`multireservoir_repaired_cover_full.json.gz`, SHA256
`1560f166ec9f804319b1713c7f686b23d17d8fb91f5630db9abb96c6c079c4a3`.

`python verify_multireservoir_covers.py` checks source factor independence,
rectangle separation, T/exchanges, all matching/clique edges and all counts
using the standard library and no proposer or published algorithm imports.
It also audits the preceding alternative covers. PASS10.47s/377MiB, saved in
`multireservoir_cover_audit.json`. The smaller
`python verify_multireservoir_final.py` needs only the pinned base and final
certificate, with no prelude dependencies.

Separate-agent audit **PASS**: the advisor independently rebuilt only the
literal base and final certificate, with no worker imports, and checked all
133729 pair attachments,5016 triple cliques,280 additional singletons, and the
entire273778-word partition. Runtime1.08s/105MiB. Files:
`../../advisor/phase2/check_c7_multireservoir_independent.py` and matching JSON.
The final size histogram is1304 singleton,128713 pair and5016 triple cliques.

The proposer used only factorized five-coordinate neighborhoods and lazily
generated alternating paths. Initial fixed-core covers were insufficient
(best135284). Starting instead from Z∪T(Z) gave135142. Constrained alternating
path repairs, preserving every already attached core point, then gave135122
with a20000-reached-vertex cap. A single resumed untruncated bounded pass
reached135033 in126.6s. The whole210.3s job used235MiB and one CPU, with a hard
1GiB address-space cap. A later deadline caused two incomplete repair attempts;
these are irrelevant to the explicit upper witness and confer no optimality.

Other tested alphabets have valid but insufficient covers; the current result
does not combine these into an unproved larger-union bound. A tiny exact
one/two-removal search about Z found no improving trade in A (72 relevant
neighborhood sets,4.66s); this is supplementary, not needed for the cover proof.

## Provenance and current status

Published arrays/recipes are reused with their original attribution and
LICENSE/NOTICE (Tandon pinned commitc753408492dde92a239708986d16c15dbf6c3235;
Polak–Schrijver base construction and later private-pair/BPZ/Gao methods).
The failed external continuation suggested an independent-reservoir Hall
formulation; the simultaneous-reservoir partition and its repairs were computed
locally. Publication priority is not established. The July18,2026 public
radius≤5 exchange exclusion around I0 remains prior work, not ours.

The global internal lower bound remains3.258832624235574872655. All artifacts
remain local under the parent's packaging hold. No upload, new model request,
paid compute or publication was used.
