"""Independent exact physical erasure audit; no worker imports."""
from fractions import Fraction as Q
from math import comb, factorial, isqrt
from pathlib import Path
import json, hashlib

def choose(n,k):return comb(n,k) if 0<=k<=n else 0

def ladder_square(t,i):
 g=2*t; m=g+1;n=g*m;w=g*i
 return Q(comb(m,i)*comb(m,i+1),4**(m-1))*Q(factorial(n-w),factorial(n-w-g))*Q(factorial(w+g),factorial(w))

def sqrt_bounds(x):
 # Rational absolute bounds via floor sqrt(num*10^80/den), distinct formula.
 scale=10**40
 b=isqrt(x.numerator*scale*scale//x.denominator)
 lo,hi=Q(b,scale),Q(b+1,scale)
 assert lo*lo<=x<hi*hi
 return lo,hi

def finite_inequality(t):
 a=[ladder_square(t,i) for i in range(2*t+1)];mid=a[t]
 assert a==list(reversed(a))
 # Direct factorial versus the reduced product and ratio identity.
 reduced=[]
 for i in range(2*t+1):
  val=Q(comb(2*t,i)**2)
  for s in range(1,2*t):val*=Q((2*t*i+s)*(2*t*(2*t-i)+s),(2*t)**2)
  reduced.append(val)
 assert all(a[i]*reduced[t]==mid*reduced[i] for i in range(2*t+1))
 if t>=2:
  ratio=Q((t+1)*(t+2),t*(t-1))**2
  for s in range(1,2*t):ratio/=1-Q(4)/(t+Q(s,2*t))**2
  assert ratio==mid/a[t-2]
 if t<=9:
  gap=1-sum(sqrt_bounds(a[i]/mid)[1] for i in range(t%2,2*t+1,2) if i!=t)
  assert gap>0
  return {'t':t,'impossible_family_gap':str(gap)}
 if t==10:
  assert a[8]/mid>Q(19,40)**2 and a[6]/mid>Q(1,40)**2
 else:assert 4*a[t-2]>mid
 return {'t':t,'construction_inequality':True}

def physical(t):
 k=2*t;m=k+1;n=k*m
 p=[Q(comb(m,i),2**(m-1)) for i in range(m+1)]
 assert sum(p[::2])==sum(p[1::2])==1
 # Decompose actual Dicke Schmidt maps; enumerate all 4(k+1)^2 Gram entries.
 erasure={}
 for i in range(m+1):
  w=k*i
  for a in range(k+1):
   c=choose(n-k,w-a)
   if c: erasure[i,a]=(w-a,p[i]*Q(comb(k,a)*c,comb(n,w)))
 diag=0;zero=0;cross=0;edges={}
 for ca in range(2):
  for cb in range(2):
   for a in range(k+1):
    for b in range(k+1):
     terms=[]
     for i in range(ca,m+1,2):
      ei=erasure.get((i,a))
      if ei is None:continue
      for j in range(cb,m+1,2):
       ej=erasure.get((j,b))
       if ej is not None and ei[0]==ej[0]:terms.append((i,j,ei[1]*ej[1]))
     if ca==cb and a==b:
      assert all(i==j for i,j,_ in terms)
      value=sum(erasure[i,a][1] for i,j,_ in terms)
      if ca==0:edges[a]=value
      else:assert value==edges[a]
      diag+=1
     elif not terms:zero+=1
     else:
      assert ca!=cb and abs(a-b)==k
      cross+=1
      expected=[]
      for i,j,v in terms:
       edge=min(i,j);assert abs(i-j)==1
       assert v*Q(factorial(n),factorial(n-k))**2==ladder_square(t,edge)
       expected.append(edge)
      assert expected==list(range(min(expected)%2,m,2))
 assert cross==4 and sum(edges.values())==1
 # Algebraic unit phases: all mirrored equal magnitudes cancel except chosen pairs.
 selected={t-2,t-4} if t==10 else {t-2}
 labels={t:(1,0)}
 for i in range(t):labels[i]=(-1,1) if i in selected else (1,0);labels[2*t-i]=(-1,-1) if i in selected else (-1,0)
 states=[(1,0)]
 for i in range(m):
  s,e=states[-1];u,v=labels[i];states.append((s*u,e-v))
  assert (states[i][0]*states[i+1][0],states[i][1]-states[i+1][1])==labels[i]
 for parity in (0,1):
  symbolic={}
  for i in range(parity,m,2):
   key=(min(i,2*t-i),labels[i][1]);symbolic[key]=symbolic.get(key,0)+labels[i][0]
  symbolic={key:v for key,v in symbolic.items() if v}
  expected={} if parity!=t%2 else {(t,0):1,**{(i,e):-1 for i in selected for e in (-1,1)}}
  assert symbolic==expected
 # Remaining identity is a_t-(sum selected a_i)*(e+e^-1)=0 with e+e^-1=a_t/sum a_i.
 return {'t':t,'n':n,'diagonal_entries':diag,'zero_entries':zero,'cross_entries':cross,'path_phase_identity':True}

finite=[finite_inequality(t) for t in range(1,14)]
assert Q(3,13)+Q(1,12)+Q(50,165)==Q(353,572)<Q(2,3)
# Each bound term decreases for t>=13; the last derivative numerator is -4t²+4t-16.
controls=[physical(t) for t in (10,11,12,13)]
source=Path(__file__).resolve().parents[1]/'provenance/audited_source.md'
result={'status':'PASS','scope':'Independent exact physical 2t-erasure coefficients and symbolic phase closure; analytic uniform log bound audited separately','finite_inequalities':finite,'physical_controls':controls,'uniform_log_endpoint':'353/572','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':controls,'source_sha256':result['source_sha256']},indent=2))
