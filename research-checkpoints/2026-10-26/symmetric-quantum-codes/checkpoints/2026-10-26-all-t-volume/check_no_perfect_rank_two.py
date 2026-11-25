"""Exact finite arithmetic tail for a UNIFORM perfect-rank-two no-go.
The analytic premise is the independently audited equality Lloyd-root
condition; the all-t reduction is the symbolic integer polynomial identity
2P(t)+2025=(2t-1)Q(t), verified here with stdlib integer arithmetic.
No floating point, optimizer, SymPy, worker imports, or external data.
"""
from fractions import Fraction as F
from pathlib import Path
from math import prod,isqrt
import json,time
st=time.monotonic()
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 return c
def evaluate(a,x):
 y=0
 for v in reversed(a):y=y*x+v
 return y
# Positive factors except t-2 at small t; no sign assumption is needed.
factors=[[0,0,1],[-2,1],[1,-2,1],[1,1],[2,1],[5,2],[2,3,2],[3,3,2],[4,3,2],[1,5,2]]
P=[1]
for f in factors:P=mul(P,f)
Q=[-2025,-4050,-7140,-6936,2632,17452,22174,9674,-7596,-14048,-8842,-1750,1184,976,288,32]
assert add([2*x for x in P],[2025])==mul([-1,2],Q)
assert evaluate(P,F(1,2))==F(-2025,2)

def newton_ratio(t,k):
 N=2*(t+1)**2;v=F(1)
 for h in range(t,t-k,-1):v*=F(-h*(h+1)*(N*N-h*h),(t-h+1)*(t+h+1))
 return v
# Exact symbolic polynomial identity for the formula of the third ratio:
# product_{h=t,t-1,t-2} [-h(h+1)(N²-h²)/((t-h+1)(t+h+1))]
# cancellation gives -P/[12(2t-1)]. Verify the uncancelled integer-polynomial identity.
N=[2,4,2];N2=mul(N,N);num=[1];den=[1]
for d in range(3):
 h=[-d,1];hp1=[1-d,1]
 num=mul(num,mul(mul(h,hp1),add(N2,[-v for v in mul(h,h)])))
 den=mul(den,[ (d+1)*(1-d),2*(d+1)])
assert mul(num,[-12,24])==mul(P,den)

# All odd positive divisors of2025=3^4*5^2. There are exactly15.
assert 3**4*5**2==2025
divisors=sorted({3**a*5**b for a in range(5)for b in range(3)})
assert len(divisors)==15 and all(2025%d==0 for d in divisors)
candidates=[(d+1)//2 for d in divisors if (d+1)//2>=3]
expected=[3,5,8,13,14,23,38,41,68,113,203,338,1013]
assert candidates==expected
bad=[];survivors=[]
for t in candidates:
 assert newton_ratio(t,3)==-F(evaluate(P,t),12*(2*t-1))
 for k in range(1,min(t,5)+1):
  v=newton_ratio(t,k)
  if v.denominator!=1:
   bad.append({'t':t,'newton_depth':k,'coefficient':str(v),'denominator':v.denominator});break
 else:survivors.append(t)
assert survivors==[3,5,8,14]

def monic_lloyd(t):
 # Full polynomial from the independent Newton ratio formula, with monic B_t.
 poly=[F(0)]*(t+1);basis=[1]
 for h in range(t+1):
  v=newton_ratio(t,t-h)
  for i,c in enumerate(basis):poly[i]+=v*c
  if h<t:basis=mul(basis,[-h*(h+1),1])
 assert poly[-1]==1
 return poly

def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def divide_linear(f,r,p):
 # Monic synthetic division, ascending coefficients.
 q=[0]*(len(f)-1);q[-1]=f[-1]
 for i in range(len(q)-2,-1,-1):q[i]=(f[i+1]+r*q[i+1])%p
 remainder=(f[0]+r*q[0])%p
 return trim(q),remainder

modular=[]
for t,p in [(3,19),(5,23),(8,23),(14,3)]:
 f=monic_lloyd(t);assert all(x.denominator==1 for x in f)
 coeff=[int(x)%p for x in f];rem=coeff[:];linear=[1];roots=[]
 for r in range(p):
  multiplicity=0
  while len(rem)>1:
   q,z=divide_linear(rem,r,p)
   if z:break
   rem=q;linear=[x%p for x in mul(linear,[-r,1])];multiplicity+=1
  if multiplicity:roots.append([r,multiplicity])
 assert len(rem)>1 and all(evaluate(rem,r)%p!=0 for r in range(p))
 assert [x%p for x in mul(linear,rem)]==coeff
 modular.append({'t':t,'prime':p,'polynomial_mod_p':coeff,'linear_root_multiplicities':roots,'remaining_factor':rem,'remaining_values_mod_p':[evaluate(rem,r)%p for r in range(p)]})

# t=2 is split over Q, but fails the stronger integer r(r+1) condition.
f2=monic_lloyd(2);assert f2==list(map(F,[114*272,-386,1]))
disc=1+4*114;assert isqrt(disc)**2<disc<(isqrt(disc)+1)**2
# Known perfect t=1 control survives.
f1=monic_lloyd(1);assert f1==[F(-42),F(1)] and 6*7==42
out={'passed':True,'scope':'K=2, equality n+1=2(t+1)^2 only; excludes every integer t>=2 after analytic Lloyd-root premise','all_t_polynomial_identity':True,'P_coefficients_ascending':P,'Q_coefficients_ascending':Q,'complete_divisor_candidates':candidates,'nonintegral_newton_coefficients':bad,'modular_nonsplitting':modular,'t2_nontriangular_root':114,'t1_known_control_root':42,'seconds':time.monotonic()-st}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
