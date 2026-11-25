# Literature status — binary single-deletion optimality

Checked 2026-10-25. Scope is unrestricted binary length-12 one-deletion codes, not multiple deletions, systematic codes, or asymptotic redundancy.

## Primary sources

1. Weindel & Heckel, *LLM-Guided Search for Deletion-Correcting Codes*, TMLR June 2026, [arXiv v2](https://arxiv.org/html/2504.00613v2). Table 1 reports VT0(12)=316, LP floor 321, and ILP upper 320. The work discovers VT-equivalent priority rules, not a resolution. General MIS solvers and random greedy were tested, so repeating greedy priority tuning is not our research claim.
2. Nakasho, Hagiwara, Anderson & Nation, [*The Tight Upper Bound … Dimension 11*](https://arxiv.org/html/2309.14736v1), 2023 preprint / 2024 ISITA. Establishes 172 at n=11 using ILP. It explicitly reports inability to improve 320 at n=12. Reusable constraints: deletion incidence, all-zero/all-one dominance, Hamming-weight/run sums, fixed prefix/suffix subcodes. Source: https://github.com/aabaa/deletion_code . Their fastest n=11 result took about 36,181 seconds on a 12-core Ryzen with 128GB and Gurobi; our limited resources make blind repetition unattractive. The paper acknowledges lack of independent formal proof logging.
3. Albert No, [*Nonasymptotic Upper Bounds … via MILP*](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514547/), Entropy 2019, DOI 10.3390/e21121202. Partial integrality produces 320 at n=12. Its conjecture equivalence partitions by the **unreduced** weighted checksum, and allows a low-checksum improved packing to be completed using high-checksum VT layers. The first prefix sub-conjecture is already proved generally: do not claim it as new.
4. Kulkarni & Kiyavash, [*Non-asymptotic Upper Bounds for Deletion Correcting Codes*](https://arxiv.org/abs/1211.3128), foundational fractional packing/covering formulation. Need consult full source before novelty claim for any LP cut.

No newer primary-source resolution was found in focused searches for n=12, 316/317/320, finite-length VT optimality. This is a search result, not a guarantee of exhaustive coverage.

## Planned distinction

Use the fact that VT deletion balls perfectly partition received words to represent replacement trades by their exact conflict-neighborhood supports. Exhaustive connected-support enumeration can yield independently replayable **local** impossibility results, unlike randomized search failure. It cannot establish global optimality unless all supports are covered. Also test insertion-ball and known subcode cuts as bounds; these are valid, but not presumed novel.

## Additional checks during experimentation

- Sloane, [*On Single-Deletion-Correcting Codes*](https://neilsloane.com/doc/dijen.pdf), revised 2002, section 2, explicitly suggests replacing k VT words by k+1. Thus **the broad swap idea is not new**. Our distinction is a complete connected-support enumeration and proof-limited exclusion, not invention of swaps. Its n=6 replacement (001011→000111 and complementary replacement) is a regression test our implementation successfully reproduces.
- No's 2019 numerical prefix table already checks k=1,2,3,4 for n=12. Repeating the small checksum-prefix tests is not a new result.
- [Pandav & Bhat 2026](https://arxiv.org/html/2602.08952v1) uses penalty-guided clique search; no resolution of this n=12 target was found there. This further discourages relabeling generic local search as novelty.
