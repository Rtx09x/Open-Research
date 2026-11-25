# Erratum: the recursive induction needs an explicit external-erasure interface

## What was incomplete in v2

The v2 draft quantified over “surrounding histories” but did not explicitly define the enlarged local trace class and prove its recursive closure. Reading its child induction as an application to an ordinary isolated SPR game is invalid: a globally legal request can revisit a child-owned cell after an external deletion that the isolated child history omits.

The hostile Extra High review identified this issue and supplied the following concrete legal transcript. We independently replayed it with the frozen exact-rational algorithm; it is a real interface counterexample, not a counterexample to the proposed sign bound.

## Exact 19-round witness

Use n=32 and root weight w=1. Request

    17,1,18,2,19,3,20,4,21,5,22,6,23,7,24,8,25,9,25.

During the first eight pairs, the root's earlier-epoch count is tau=0,2,...,14. Each pair has h=l=1; both trigger tests hold because delta=14.8. Every continuation has L=floor(.6)=0. The root starts a new epoch at the next request. All labels are plus. Each left request clears the preceding right plus, leaving pluses at 1,...,8 after round 16.

At round 17, the root's new epoch has tau=16 and inserts plus at 25. At round 18, request 9 removes that plus. But delta*l=14.8<16, so the root remains in the same phase-one epoch. Round 19 can legally request 25 again. The SAME right child, and the SAME leaf at 25, receive the address twice; the intervening root request 9 is external to them.

An isolated child game seeing only 25,25 cannot make its second request: its own history contains no deletion of the first sign. The deletion-augmented owned trace instead records request 25, external erasure, request 25 and is valid. The root never becomes full; all 19 physical requests are legal.

The replay and complete per-round boards are in `check_19_round_interface.py` and `19_round_interface_check.json`.

## v3 repair

The integrated manuscript now defines E(I,w), an extended OWNED-COHORT trace class:
- An instance starts with no owned signs, even if foreign signs physically exist in its interval.
- External events may erase owned signs but never insert owned signs.
- A local request must be empty of owned signs, performs the usual eager deletions on that owned board, and inserts the subroutine's returned sign.
- Internal counters and recursive states persist. A full local owned board is not a separately terminated game; it may resume after an external erasure frees a requested cell.

Every actual global history projects into this class, and the same projection holds recursively from a parent extended trace to its children. The proof is rerun DIRECTLY over E. It does not infer future-strategy monotonicity from the observation that an erasure lowers current inventory. Only the actual ROOT obeys the original game's mandatory full-board termination.

The one-cell base case bounds occupancy by one, not the number of calls by one. Small-time chains, inherited-cohort decompositions, trigger geometry, completed/unfinished inequalities and padding all remain valid on E. The strengthened domain and projection proof are explicit in `ADAPTIVE_Q_THEOREM.md` and `EXTERNAL_ERASURE_INDUCTION.md`.

The hostile reviewer proposed a different analysis-only repair using overwrite shadows and monotone signed-subboard coupling. The direct E-domain repair here does not require that auxiliary construction and does NOT permit physical overwrites. Both approaches address the same missing induction interface. We preserve the issue transparently rather than relabeling the original draft as already fully explicit.

## What changed—and what did not

**Changed:** the formal induction domain, projection lemma, base-case wording, and explanation of local versus root termination.

**Unchanged:** physical algorithm, rational continuation table, numeric constants, interval inequalities, exact-power certificates, uniform exponents, original calibration metric and published transfer invocation.

The claimed exponent remains 20423/30846. This semantic repair is not a new exponent improvement. The source v2 archive remains immutable for provenance. Internal and AI-assisted adversarial review are not external human peer review, formal proof-assistant verification, or comprehensive priority clearance.
