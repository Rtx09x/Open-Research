# Frozen26-selected-binary relaxation obstruction

An exact fractional point has total mass
`32021514469/100000000 = 320.21514469`.

It satisfies every maximal word-conflict clique (all155496 independently
enumerated), all four transforms of783 specified globally valid CG cuts,
0<=X<=1, X_0=X_4095=1, and integrality on26 explicitly listed original-word
variables. Only selected variableX_1625 equals1; the other25 equal0.
It also satisfies the stated lex-prefix normalization.

Therefore this specific finite26-selected-binary relaxation **cannot prove
an upper bound319**. This is NOT a deletion code, NOT a construction above316,
NOT a new global upper bound, and NOT an obstruction to additional cuts or
integrality constraints. The actual problem remains316–320.

The26 words are the complement/reversal closure of the15-word partial-
integrality selection reported by No2019. This package does not claim that
No's original smaller model included these new CG cuts.

## Replay

Only Python standard library; no solver, external file, network or installed
package required. Run without-O:

```
python -I -S verify.py
python -I -S negative_controls.py
```

The verifier reconstructs the channel by insertion, checks its four group
automorphisms, checks all CG ancestors and all four transports, and performs
a full independent maximal-clique enumeration. Expected runtime~3s.

Allzero/allone normalization is WLOG for maximum codes by replacing the
unique possible weight1/11 codeword, or adding the missing constant. The
lex-prefix inequalities are WLOG representative-selection constraints, not
invariance assumptions: choose the complement/reversal image with maximal
binary score on the same fixed10-word prefix. Ties need no rule.

No branch tree, frontier, numerical basis, or live-search file is included.
This frozen mathematical witness remains valid after search resumes with a
strictly stronger model. It was also independently checked by the advisor
using literal deletion and a separate clique enumerator.
