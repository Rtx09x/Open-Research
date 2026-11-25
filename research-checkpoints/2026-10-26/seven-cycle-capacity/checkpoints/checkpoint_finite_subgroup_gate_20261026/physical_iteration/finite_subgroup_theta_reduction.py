"""Exact rational reduction |H|<402 for dimension-five distance2/7 codes."""
from fractions import Fraction as F
import json
from pathlib import Path
# Machin identity pi=16 atan(1/5)-4 atan(1/239).
# Eight terms ending negative give lower bound for first atan; first term
# gives upper bound for second atan. Alternating remainder has correct sign.
pilower=16*sum(((-1)**j*F(1,5)**(2*j+1)/ (2*j+1) for j in range(8)),F(0))-4*F(1,239)
assert pilower>F(314159,100000)
x=F(314159,700000)
c=1-x*x/2+x**4/24-x**6/720+x**8/40320
# cos(pi/7)<cos(x)<=c, using monotonicity on(0,pi) and alternating series.
t=7*c/(1+c)
assert t**5<402
out={'PASS':True,'pi_lower_bound':'314159/100000','theta_C7_upper_numerator':str(t.numerator),'theta_C7_upper_denominator':str(t.denominator),'theta_C7_fifth_power_strictly_below':402,'remaining_integer_orders':[368,401],'scope':'Dimension-five finite-subgroup torus construction with distance>=2/7; does not bound all independent codes by367.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
