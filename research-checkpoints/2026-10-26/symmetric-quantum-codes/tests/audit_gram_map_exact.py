"""Exact Gram-map constant audit using matrix commutators, no Wigner symbols."""
import sympy as s,json
N=19;n=18
Jp=s.zeros(N)
for i in range(n):Jp[i+1,i]=s.sqrt((n-i)*(i+1))
Jm=Jp.T

def tensors(r):
 x=Jp**r;out=[(r,x,(x.T*x).trace())]
 for q in range(r,-r,-1):
  x=Jm*x-x*Jm
  out.append((q-1,x,s.simplify((x.T*x).trace())))
 return out
E=[x for r in range(3) for x in tensors(r)]
c=[]
for r in range(5):
 _,t,nt=tensors(r)[r]
 value=0
 for qa,a,na in E:
  for qb,b,nb in E:
   if qa!=qb:continue
   tr=s.simplify((t*a.T*b).trace())
   value+=tr**2/(nt*na*nb)
 c.append(s.simplify(value))
expected=list(map(s.Rational,['9/19','91/285','288199/1187025','33176/237405','10120/142443']))
assert c==expected,(c,expected)
print(json.dumps({'n':n,'exact':True,'method':'unnormalized spin-ladder tensor operators, commutators and HS norms; no 6j/Racah formula','c':[str(x) for x in c],'matches_worker':True},indent=2))
