from sympy import Rational as Q,simplify
from sympy.physics.wigner import wigner_6j
from pathlib import Path
import json,time
st=time.monotonic();rows=0
for n in range(1,15):
 j=Q(n,2);N=n+1;D=n*(n+2)
 for a in range(min(5,n)+1):
  for r in range(min(5,n)+1):
   row=[]
   for b in range(n+1):
    if abs(a-r)<=b<=a+r:v=N*(2*b+1)*wigner_6j(a,b,r,j,j,j)**2
    else:v=Q(0)
    row.append(v)
   assert simplify(sum(row)-1)==0
   drift=sum(row[b]*(b*(b+1)-a*(a+1)) for b in range(n+1))
   assert simplify(drift-r*(r+1)*(1-Q(2*a*(a+1),D)))==0
   rows+=1
out={'passed':True,'rows':rows,'n_range':[1,14],'a_r_up_to':5,'method':'independent SymPy exact6j squared, both spin parities','scope':'finite normalization/drift controls supplement CP-channel and6j recoupling proof','seconds':time.monotonic()-st};Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
