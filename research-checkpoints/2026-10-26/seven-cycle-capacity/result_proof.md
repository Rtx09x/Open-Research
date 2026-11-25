# A verified terminal-code recycling improvement for C7

## Result and evidence status

The construction below, applied to the seven-family representation in Ravi Tandon's August 2026 paper, gives

**Theta(C7) ≥ 3.258832624232849476**

using a recursively specified independent set in the768,000th strong power. A simpler128,000-dimensional certificate gives3.258832624209610237867099424184. The displayed decimal is truncated and certified by integer powers, not rounded. This improves the reproduced published finite bound3.258832620353266309… by approximately3.87958×10^-9. It does **not** determine the Shannon capacity; the upper bound remains about3.317667207394.

A simpler one-pair version has 2,402 words over eight macro-symbol positions and gives the independently audited length 1,000 bound3.25883262052565726113… . The stronger result uses two pairs and ordinary, previously established BPZ seven-family substitutions.

Our contribution is the explicit terminal-recycling base, its exact checks, and the resulting numeric improvement relative to the checked published bound. Priority and literature novelty have not been conclusively established. No new universal combining theorem is required. The construction inherits the existing August seven-family representation and its mathematical proof; our finite checks do not constitute a full Lean formalization.

## 1. The seven-family interface

Write L={B,N,A,D,O,H,V}. The symmetric guaranteed-separation pairs are

BO, BH, BV, NA, ND, NO, NH, NV, AD, AH, DV.

Two label words are separated when at least one coordinate is one of these pairs. Each actual family F_l is independent; separated labels represent mutually separated sets in the original strong-power graph. Consequently, pairwise-separated label words define disjoint independent Cartesian blocks, and their union has cardinality equal to the sum of the products of the family sizes.

The published representation lives in C7^125 and has seven-vector w stored as `input_vector` in `terminal_recycled_base.json`. It is reproduced from the base367 code and the five finite neighborhood certificates by `published/verify_arithmetic.py --recomputed`. The terminal code K=K4a has 49 label words of length4. Substituting w into K gives the published independent-set cardinality M in C7^500.

## 2. Recycling K4a instead of stopping at it

All strings below are four-letter words over L. Set

- r1=NHNH, q1=NVNV;
- r2=VNVN, q2=HNHN;
- R={r1,r2}, Q={q1,q2};
- X={ (a,b,d,c) : (a,b,c,d) in K }, the swap of the third and fourth coordinates.

The exact finite checks establish:

1. K and X are pairwise separated.
2. R is a subset of K; Q is pairwise separated, disjoint from K, and every q_i is nonseparated from exactly r_i among K.
3. No member of X is nonseparated from both Q and R.

Partition X as X0, XH, XV according as it is nonseparated from neither Q nor R, from Q only, or from R only. Define a new seven-family label representation

B'=K\R, N'=X0, A'=XV, D'=XH, O'=R, H'=Q, V'=R.

The family word counts are47,41,4,4,2,2,2. They need not be disjoint across labels: O'=V' is permitted, because O and V are not a required separation pair.

Every family is independent. B' is separated from O',H',V' by K's independence and the private-block checks. N',A',D' are disjoint parts of X and hence mutually separated. N' is separated from O',H',V' by its definition. A' is separated from H', and D' from V', by the no-double-neighborhood condition. These are exactly all eleven required separation pairs. Therefore this is a valid BPZ seven-family representation after Cartesian substitution, now in C7^500.

This argument treats r_i,q_i as **blocks**, not as individual original-channel vertices. It makes no claim that a physical vertex in a q_i block has just one physical neighbor in an r_i block.

## 3. Cardinalities and the elementary strict gain

For a four-letter word u, define W(u)=product_j w[u_j]. The published vector has w_H=w_V. Thus all four endpoint blocks have the same positive weight

p = w_N^2 w_H^2.

Also W(X)=W(K)=M because X is a coordinate permutation. Let t=2p and let o,h,v be the total weights of X0,XH,XV. Then o+h+v=M, and the new seven-vector is

u0 = (M-t, o, v, h, t, t, t).

Applying BPZ's binary S2a rule to two copies and selecting output families B and O yields

(M-t)^2 + 2t(o+h+v) = M^2 + t^2 = M^2 + 4p^2 > M^2.

This alone gives a strict length 1,000 improvement, without any asymptotic argument.

## 4. The completely finite recursive recipe

Starting from the explicit seven-family u0, define

u_(k+1) = S2a(u_k,u_k), for k=0,…,7.

Here S2a is the existing admissible BPZ rule with output word lists:

- B: BB, HD, VA, DV, AH;
- N: NN, AA, AD, DA, DD;
- A: AN, ND;
- D: DN, NA;
- O: ON, NO;
- H: HN, NV;
- V: VN, NH.

Every rule word denotes the corresponding Cartesian product of input families. The rule's internal and cross-family separation conditions are finite and checked exactly. Induction therefore produces actual independent families at every stage. Each stage doubles the original-channel dimension.

After eight stages, select B and O, which are guaranteed separated. The resulting cardinality is

M8 = (u8)_B + (u8)_O

in dimension 500·2^8=128000. All arithmetic is nonnegative integer arithmetic. The exact final vector, M8, the base-file SHA256, operation sequence, and root bracket are recorded in `recycled_terminal_certificate.json`.

For the displayed bound b=r/10^30, the checker establishes

r^128000 ≤ M8·10^(30·128000) < (r+1)^128000.

It also establishes M8>M^256, independently certifying a strict rate increase over the published construction.


## 4b. Best finite binary tree found and independently audited

A numerical binary-tree screen through 4,096 recycled leaves suggested the following finite tree. No optimality assertion depends on the screen:

- v1=u0;
- v2=S2a(v1,v1);
- v3=S2a(v1,v2);
- v_(2n)=S2a(v_n,v_n), successively for n=3,6,12,24,48,96,192,384,768.

Thus there are 1,536 recycled leaves, each of dimension 500. Select terminal B∪O at dimension 768,000. The exact certificate is `optimized_recycle_certificate.json`; its 12-node DAG, integer arithmetic, strict comparison with the simpler certificate, and root bracket have all passed an independent advisor audit. The resulting interval is

3.258832624232849476 ≤ M_opt^(1/768000) < 3.258832624232849477.

In particular M_opt > M8^6, so its normalized rate strictly improves the 128,000-dimensional certificate. The construction is finite. Further iteration is not asserted to improve the rate or converge monotonically.

## 4c. Reusable rule, not merely a single weighted example

The seven lists from Section2 have lengths(47,41,4,4,2,2,2), totaling102 length-four label words. Their separation conditions do not depend on cardinalities or on C7. They therefore form a generic admissible **quaternary BPZ substitution**, recorded in `recycled_quaternary_rule.json`, applicable to arbitrary ordered seven-family inputs. Equal endpoint weights are needed for the particularly simple M²+4p² identity, not for the substitution's validity. Whether this exact substitution has appeared elsewhere remains a literature-priority question.

## 5. Reproduction

Run from this directory, with one CPU:

```bash
python verify_base.py
python replay_wrapper.py
python terminal_weighted_gadget.py
python verify_weighted_terminal_independent.py
python terminal_multi_pairs.py
python recycle_terminal.py --levels 8 --digits 30
```

The first full upstream replay used 41.85 seconds and734MiB peak resident memory. The final exact recycled arithmetic/root check used 8.88 seconds. Upstream source, Apache-2.0 licensing, NOTICE and attribution are preserved under `published/`.

An independent advisor audit of the initial one-pair certificate passed all 2,883,601 label-word pairs, the exact weighted sum, root bracket, the literal upstream K4a list, private-block checks and rectangle construction. A separate independent advisor audit also passed the two-pair base-family axioms and provenance, literal S2a admissibility, all eight exact recurrences, strict rate comparison, and the integer128000th-root bracket. Audit artifacts are bundled in `tests/`.

## Sources

- Tandon, [Strengthening Recursive Constructions for Zero-Error Shannon Capacity](https://arxiv.org/html/2608.30273v1), especially Definition5, Proposition1 and Theorem2.
- [Tandon's exact source and certificates](https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion).
- Buys, Polak, Zuiddam, [seven-family Lean source](https://github.com/spectra-research/shannon-capacity-lean), pinned upstream commit aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65, especially Substitutions.lean and TerminalCodes.lean.
- Polak and Schrijver, [367-word base construction](https://arxiv.org/html/1808.07438v2).
