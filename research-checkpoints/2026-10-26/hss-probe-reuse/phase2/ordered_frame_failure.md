# Correct forest colors alone do not repair the subtractive LM decoder

The ordered-frame experiment maintains (F,G,H). After a local basis rotation
produces child active frames F1,F2, the first child's detail uses an independent
sign times F2 and the second child's detail uses an independent sign times H.
For coordinate bases the physical colors are correctly popcount(index) mod3,
the representative forest's depth-mod-three coloring.

Nevertheless, at k=1,L=2,N=8, all-plus signs and A=e_7 e_1^T, the old LM
subtractive decoder returns B_0,1=1 and B_0,4=-1, hence squared error3 against
fixed-tree optimum1. The direct three-color forest decoder returns only the
first coefficient and has error2. The extra coefficient comes from subtraction.

Exhaustive4096-sign error-operator tests give maximum eigenvalue3 for coordinate
bases and3.91848669117 for one dense case. See `ordered_three_frame.py` and its
JSON/operator outputs. This refutes factor two for this decoder, not every
constant bound and not the direct forest theorem.
