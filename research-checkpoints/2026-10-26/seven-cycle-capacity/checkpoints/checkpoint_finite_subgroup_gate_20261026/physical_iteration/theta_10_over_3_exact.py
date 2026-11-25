"""Exact Q(sqrt5) dual certificate theta(E10/3)<=30-12sqrt5<16/5.
E20/6 maps to E10/3 by floor(t/2), so any fifth-power code in either has<368
words. No floating point or SDP solver is trusted.
"""
from fractions import Fraction as F
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def add(x,y):return(x[0]+y[0],x[1]+y[1])
def mul(x,y):return(x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,s):return(x[0]*s,x[1]*s)
def run():
 y=[(F(60),F(-20)),(F(140),F(-60)),(F(90),F(-40))]
 rows=[[(F(1,2),F(-1,2)),(F(-1,2),F(-1,2)),(F(-1),F(0))],[(F(-1,2),F(-1,2)),(F(-1,2),F(1,2)),(F(1),F(0))],[(F(-2),F(0)),(F(2),F(0)),(F(-1),F(0))]]
 for col,target in enumerate([-20,-20,-10]):
  total=(F(0),F(0))
  for yi,row in zip(y,rows):total=add(total,mul(yi,row[col]))
  assert total==(F(target),F(0))
 # sqrt5<9/4 proves each y>=0; sqrt5>67/30 proves theta<16/5.
 assert F(5)<F(9,4)**2 and all(a+b*F(9,4)>=0 for a,b in y)
 bound=add((F(1),F(0)),scale(tuple(map(sum,zip(*y))),F(1,10)));assert bound==(F(30),F(-12))
 assert F(5)>F(67,30)**2 and F(30)-12*F(67,30)==F(16,5)
 assert F(16,5)**5<368
 # Explicit cohomomorphism for the equivalent fraction20/6 ->10/3.
 assert all(min((a//2-b//2)%10,(b//2-a//2)%10)>=3 for a in range(20) for b in range(20) if min((a-b)%20,(b-a)%20)>=6)
 out={'PASS':True,'theta_upper_exact':'30-12sqrt(5)','theta_upper_rational_strict':'16/5','fifth_power_integer_upper':335,'fourier_dual_nonzero_modes':[1,2,5],'dual_weights':['60-20sqrt(5)','140-60sqrt(5)','90-40sqrt(5)'],'scope':'All codes in E(20/6)^5 or E(10/3)^5; not all finite-torus denominators or C7 codes.'};(P/'theta_10_over_3_exact.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
