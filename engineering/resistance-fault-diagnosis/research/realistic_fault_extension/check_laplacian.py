import sympy as s
import json
from check_partial import profiles
out=[]
for m in range(4,9):
 g,C,pairs,S=profiles(m)
 edges=[(0,i+2,s.Rational(1)) for i in range(m)]+[(1,i+2,s.Rational(2)+s.Rational(i+1,m+1)) for i in range(m)]
 def resistances(fault=None,amount=0):
  L=s.zeros(m+2)
  for j,(a,b,r) in enumerate(edges):
   c=1/(r+(amount if j==fault else 0)); L[a,a]+=c;L[b,b]+=c;L[a,b]-=c;L[b,a]-=c
  K=L[:-1,:-1].inv()
  def R(a,b):
   x=s.zeros(m+1,1)
   if a<m+1:x[a]+=1
   if b<m+1:x[b]-=1
   return (x.T*K*x)[0]
  return [R(0,1)]+[R(p+2,q+2) for p,q in pairs]
 base=resistances()
 n=0
 for f in range(2*m):
  for amount in [s.Rational(1,10),s.Rational(1),s.Rational(3),s.Rational(-1,4)]:
   vals=resistances(f,amount); delta=[x-y for x,y in zip(vals,base)]
   idx=2*f if f<m else 2*(f-m)+1
   assert all(s.cancel(delta[j+1]/delta[0])-s.Rational(a.numerator,a.denominator)==0 for j,a in enumerate(S[idx]))
   n+=1
 out.append({'m':m,'fault_magnitudes_checked':n,'exact_laplacian_ratio_identity':True})
print(json.dumps(out,indent=2))
