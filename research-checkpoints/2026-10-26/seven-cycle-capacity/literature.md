# Seven-cycle zero-error capacity: literature check

Checked 25 October 2026 against primary sources. No newer improvement was found in the targeted search; this is not an exhaustive priority/novelty certification.

- Polak and Schrijver, [arXiv:1808.07438v2](https://arxiv.org/html/1808.07438v2), later IPL (2019): explicit 367-word length-five independent code. The construction rounds a length-five circular code with 382 points, retains 327 isolated words, and extends them with 40 words. The paper reports no 3-for-4 improving trade. This supplies a finite starting point, not the present global lower bound.
- Itty, Rosin, Carstensen, Reichman, [arXiv:2607.21517v2](https://arxiv.org/html/2607.21517v2): a 134753-word length-ten construction using eight private pairs and complementary horizontal/vertical pieces; explicitly AI assisted.
- Gao, [arXiv:2607.27869](https://arxiv.org/abs/2607.27869): binary recursive propagation of the private-pair gadget.
- Buys, Polak, Zuiddam, [arXiv:2607.29681](https://arxiv.org/abs/2607.29681), [Lean source](https://github.com/spectra-research/shannon-capacity-lean): seven-family set representations and admissible finite combining rules. The relevant snapshot is aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65; its updated C7 bound is 3.258827985920007… .
- Ravi Tandon, [arXiv:2608.30273v1](https://arxiv.org/html/2608.30273v1), [exact artifacts](https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion): heterogeneous recursion, length 500, lower bound 3.25883262035326630912153905181047543760538759432195… . This work retains Python exact finite certificates but does not claim a full Lean formalization of the new heterogeneous theorem.

The general upper bound remains the Lovász value 7 cos(pi/7)/(1+cos(pi/7)) ≈ 3.317667207394. Any 368-word length-five independent code would give 368^(1/5) ≈ 3.25963943869, improving the lower bound but not solving capacity.

## Download and attribution

`published/` is an unmodified public-source snapshot downloaded as a GitHub archive (not a repository checkout). Its Apache-2.0 LICENSE, NOTICE, upstream attribution, and release manifest are retained. `august.html` and `august.txt` are reading copies of the arXiv page. Our scripts are outside `published/`.

## Mathematical convention

Words are confusable if every coordinate difference modulo7 is 0,1,or6. Independent words must differ by 2,3,4,or5 in at least one coordinate. Equality is included in closed confusability. Codeword integers use least-significant base7 digit as coordinate0.

## Snapshot integrity check

Downloaded upstream snapshot pinned to commit `c753408492dde92a239708986d16c15dbf6c3235`. All35 executable/data/other listed files match the bundled release-manifest hashes. The sole stale manifest entry is README.md; its downloaded bytes were separately verified against that exact current upstream commit. No computational source/data mismatch was found. See source_provenance.json.
