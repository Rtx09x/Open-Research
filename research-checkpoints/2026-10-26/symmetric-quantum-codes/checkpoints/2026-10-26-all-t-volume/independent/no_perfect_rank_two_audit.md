# Independent audit: no higher-radius perfect rank-two spin code

Date: 2026-10-26 01:16 UTC. Verdict: **analytic applicability and exact arithmetic PASS**, conditional only on the separately audited unrestricted volume theorem and its equality/quadrature corollary. This is not an external review or a publication-priority determination.

## Statement
A complex rank-two code in Sym^n(C²) detecting tensor ranks through 2t cannot attain n+1=2(t+1)² for any integer t≥2. Consequently the audited volume theorem strengthens to n≥2t²+4t+2 for t≥2. This does not settle the conjectured minimum 3t²+3t+1, nor the current distance-seven 35–37 interval.

## Independently checked bridge and arithmetic
- Equality rigidity forces purity, with enumerator support above rank 2t confined to zeros of the degree-t Lloyd polynomial. The quadrature measure argument forces exactly t positive support nodes, so all t roots must have the form r(r+1), r an integer greater than 2t. This is an equality-only conclusion, not assumed nondegeneracy away from equality.
- The monic integer Newton basis B_h(x)=product_{i<h}(x-i(i+1)) is unitriangular over Z. Integral roots therefore require every Newton coefficient to be integral.
- Starting directly from the finite hypergeometric coefficients, the independent checker derives beta_(h-1)/beta_h=-h(h+1)(N²-h²)/[(t-h+1)(t+h+1)]. Three steps give the displayed third-from-top coefficient -P(t)/[12(2t-1)].
- Independent symbolic expansion finds P(1/2)=-2025/2. Clearing powers of two modulo the odd number 2t-1 proves that integrality requires 2t-1 to divide 2025. A separate exact multiplication also verifies the worker's cleaner integer identity 2P+2025=(2t-1)Q with every displayed coefficient of Q.
- All 15 positive divisors of 2025 were generated independently. Removing the t=1,2 cases leaves exactly the 13 stated candidates, with no finite cutoff assumption.
- Exact Fraction recurrence eliminates nine candidates by a nonintegral coefficient within five steps. Independently constructed monomial polynomials for t=3,5,8,14 fail complete splitting over F_19,F_23,F_23,F_3, respectively. All repeated linear factors are removed and the nonconstant remainder is checked at every field element.
- At t=2 the roots 114 and 272 are exact; 114 fails the spin-index condition. At t=1 the root 42=6·7 survives, consistent with the known seven-qubit perfect code.

## Evidence and prose review
`check_perfect_spin_codes_independent.py` and its JSON are advisor-written and import no worker code. They use exact SymPy symbolic algebra and Fraction/integer arithmetic, not numerical root finding. The worker's separate standard-library checker provides an additional implementation, not the basis of the independent result.

The complete `symmetric-quantum-codes/phase3/no_perfect_rank_two_candidate.md` was read line by line. No mathematical or scope omission was found. Its status can now say independent internal audit PASS while retaining external-review/priority caveats. The frozen main volume package need not be changed; this is a separate addendum.
