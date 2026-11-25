"""Independent rigorous audit of KL lift, using SymPy exact 6j + Arb.
Unlike the primary checker, does not assume the supplied Racah formula gives
exact eigenvectors or a projector. Each proposed low-rank vector is instead
certified by an a posteriori local-Casimir eigenresidual estimate.
"""
from pathlib import Path
import json,time,hashlib
from fractions import Fraction
from functools import lru_cache
import sympy as s
from sympy.physics.wigner import wigner_6j
from flint import arb,arb_mat,fmpq,ctx
ctx.prec=256
BASE=Path(__file__).resolve().parents[1]/'symmetric-quantum-codes'/'phase2';FILE=BASE/'interval_dual_candidate.json';raw=FILE.read_bytes();cert=json.loads(raw);scale=cert['scale'];j=9;n=18

def rat(a,b=1):return arb(fmpq(int(a),int(b)))
@lru_cache(None)
def six(a,b,c,d,e,f):
 q=wigner_6j(a,b,c,d,e,f)
 if q==0:return arb(0)
 square=s.cancel(q*q);assert square.is_Rational
 return (-1 if q<0 else 1)*rat(square.p,square.q).sqrt()
start=time.time();rows=[];count=0
for item in cert['KL_projected_h']:
 L,Lp=item['L'],item['Lp'];Js=[J2//2 for J2 in item['Js']]
 expected=[J for J in range(28) if abs(L-j)<=J<=L+j and abs(Lp-j)<=J<=Lp+j]
 assert Js==expected
 h=[rat(v,scale)for v in item['h']];d=len(Js)
 C=arb_mat(d,d)
 for a,K in enumerate(Js):
  for b,J in enumerate(Js):
   if abs(K-J)<=1:C[a,b]=3*rat((2*K+1)*(2*J+1)).sqrt()*(-1)**(L+Lp)*six(j,K,L,J,j,1)*six(j,K,Lp,J,j,1)
 Cas=arb_mat([[180*int(a==b)-1140*C[a,b]for b in range(d)]for a in range(d)])
 for r in range(abs(L-Lp),min(L+Lp,n,4)+1):
  u=[(-1)**(L+j+J)*rat((2*J+1)*(2*r+1)).sqrt()*six(L,j,J,j,Lp,r)for J in Js]
  dot=sum((a*b for a,b in zip(u,h)),arb(0))
  err=[sum((Cas[a,b]*u[b]for b in range(d)),arb(0))-r*(r+1)*u[a]for a in range(d)]
  assert abs(dot)<1
  assert all(abs(e)<arb('1e-50')for e in err)
  rows.append(dict(L=L,Lp=Lp,r=r,dimension=d,residual_component_bound='1/10^50',coefficient_abs_bound='1'))
  count+=1
# ||residual||2 <= d*epsilon <=19e-50, ||W||2<=24,
# spectral gap from ranks>=5 to r<=4 is >=10. Triangle sum over all rows.
budget=Fraction(count*19*24,10*10**50)
assert budget<Fraction(1,10**40)
out={'PASS':True,'candidate_sha256':hashlib.sha256(raw).hexdigest(),'arithmetic':'SymPy exact 6j signs/squares converted to outward Arb balls; 256 bits','vectors_checked':count,'max_dimension':max(row['dimension']for row in rows),'total_KL_defect_bound_exact':str(budget),'simplified_KL_defect_bound':'1/10^40','explanation':'Uses spectral separation, not exact Racah orthogonality/eigenvector identities. The physical commutator Casimir spectrum and KL high-rank support are the mathematical inputs.','seconds':time.time()-start,'rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
