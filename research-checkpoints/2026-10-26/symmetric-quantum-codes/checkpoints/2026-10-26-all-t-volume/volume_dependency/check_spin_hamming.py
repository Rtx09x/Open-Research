"""Exact convention/algebra controls for the all-t proof.
Finite 6j tests are controls, not a replacement for the analytic channel proof.
The Bernstein identity is symbolic in t and therefore not an interpolation.
"""
from pathlib import Path
from math import comb
import json,time
import sympy as S
from sympy.physics.wigner import wigner_6j
from racah_coefficients import racah
ROOT=Path(__file__).parent;start=time.time()

def R(n,a,r):return S.Rational(n+1)*(-1)**(n+a+r)*racah(n,a,r)
def P(n,a,r,b):
 if not abs(a-r)<=b<=min(n,a+r):return S.S(0)
 j=S.Rational(n,2)
 return (n+1)*(2*b+1)*wigner_6j(a,r,b,j,j,j)**2

drift_count=0;product_count=0
for n in range(1,9):
 for a in range(n+1):
  for r in range(n+1):
   pp=[P(n,a,r,b)for b in range(n+1)]
   assert sum(pp)==1
   assert sum(pp[b]*(b*(b+1)-a*(a+1))for b in range(n+1))==r*(r+1)*(1-S.Rational(2*a*(a+1),n*(n+2)))
   assert all((2*a+1)*pp[b]==(2*b+1)*P(n,b,r,a)for b in range(n+1))
   drift_count+=1
   if n<=5:
    for x in range(n+1):
     assert R(n,a,x)*R(n,r,x)==sum(pp[b]*R(n,b,x)for b in range(n+1))
     product_count+=1

# Exact symbolic positivity certificate for the r>=t branch.
t,r,x=S.symbols('t r x');m=(t+1)**2;s=r-t
escape=s*s/m+(r+1)/(2*t+r+1)*(m-s*s)/m*(1-(m+s*s-1)/(4*m*(m-1)))
den=4*t*(t+1)**4*(t+2)*(r+2*t+1)
poly=S.cancel(den*(escape-r*(r+1)/(4*m)))
Bs=[t*(t+1)**3*(t+2)*(t*t+7*t+3),
 t*(t+1)**2*(t+2)*(2*t**3+42*t*t+52*t+15)/5,
 t*(t+1)*(t**5+89*t**4+368*t**3+526*t*t+305*t+60)/10,
 t*(86*t**5+456*t**4+908*t**3+848*t*t+371*t+60)/10,
 t*(42*t**5+227*t**4+458*t**3+429*t*t+188*t+30)/5,
 2*t*(t+1)*(4*t**4+19*t**3+27*t*t+16*t+3)]
assert S.expand(poly.subs(r,t*(1+x))-sum(comb(5,i)*Bs[i]*x**i*(1-x)**(5-i)for i in range(6)))==0
assert all(all(c>=0 for c in S.Poly(b,t).all_coeffs())and b.subs(t,1)>0 for b in Bs)
escape_low=(r+1)/(2*t+r+1)*(1-S.Rational(1,4)/m)
assert S.cancel(escape_low-r*(r+1)/(4*m)-(r+1)*(4*m-1-r*(2*t+r+1))/(4*m*(r+2*t+1)))==0

cases=[]
for K,tt in [(2,t)for t in range(1,7)]+[(3,1),(3,2),(3,3)]:
 mm=(tt+1)**2;N=K*mm-1;n=N-1;j=S.Rational(n,2);mins=[]
 for rr in range(2*tt+1):
  ll=sum((2*a+1)*R(n,a,rr)for a in range(tt+1))
  cc=sum((2*a+1)*(2*b+1)*wigner_6j(a,b,rr,j,j,j)**2 for a in range(tt+1)for b in range(tt+1)if abs(a-b)<=rr<=a+b)
  hyp=sum(S.rf(-tt,h)*S.rf(tt+2,h)*S.rf(-rr,h)*S.rf(rr+1,h)/(S.rf(2,h)*S.rf(-n,h)*S.rf(n+2,h)*S.factorial(h))for h in range(min(tt,rr)+1))
  assert ll==mm*hyp and K*ll*ll-N*N*cc>0
  if rr:
   assert ll/mm>=1-S.Rational(rr*(rr+1),8*mm)
   assert cc*N/mm<1-S.Rational(rr*(rr+1),4*mm)
  else:assert cc==S.Rational(mm,N)and K*ll*ll-N*N*cc==mm
  mins.append(K*ll*ll-N*N*cc)
 cases.append({'K':K,'t':tt,'n':n,'minimum_low_coefficient':str(min(mins))})

# Saturating known7 control: its LP enumerator must survive, not be excluded.
a=[S.S(1)]+[S.S(0)]*5+[S.S(3),S.S(0)];n=7;N=8;tt=1
assert sum(a)==4
for r in range(3):assert 2*sum(S.Rational(2*r+1,N)*R(n,r,k)*a[k]for k in range(N))==a[r]
assert sum((2*b+1)*R(n,b,6)for b in range(2))==0
out={'status':'exact symbolic algebra and finite normalization controls PASS; full analytic audit separate',
 'stochastic_drift_reversibility_cases':drift_count,'full_linearization_cases':product_count,
 'bernstein_identity_symbolic':True,'positive_coefficient_polynomials':list(map(str,Bs)),
 'critical_cases':cases,'saturating_n7_control':True,'seconds':time.time()-start}
(ROOT/'spin_hamming_candidate_controls.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
