"""Exact phase-twisted gnu construction: stdlib only, no optimization.
Physical partial trace is rebuilt from binomial Kraus coefficients.
The algebraic phase uses e=c+i*sqrt(1-c*c); only exact identities/inequalities
are required, not numerical approximations to amplitudes or phases.
"""
from fractions import Fraction as F
from math import comb,prod,isqrt,factorial
from collections import defaultdict
from pathlib import Path
import json,time,resource
ROOT=Path(__file__).parent

def simple_A(t,i):
 g=2*t
 return F(comb(2*t,i)**2)*prod(F((g*i+s)*(g*(2*t-i)+s),g*g)for s in range(1,g))
def actual_A(t,i):
 m=2*t+1;g=2*t;n=g*m;w=g*i
 return F(comb(m,i)*comb(m,i+1),2**(2*m-2))*prod(range(n-w-g+1,n-w+1))*prod(range(w+1,w+g+1))
def sqrtbox(x):
 if x==0:return F(0),F(0)
 scale=10**30;a=isqrt(x.numerator*x.denominator*scale**2)
 lo=F(a,x.denominator*scale);hi=F(a+1,x.denominator*scale)
 assert lo*lo<=x<=hi*hi
 return lo,hi

def phase_labels(t):
 # Each eta is sign * e**exponent, with |e|=1.
 chosen=[t-2,t-4]if t==10 else[t-2]
 eta={t:(1,0)}
 for i in range(t):
  if i in chosen:eta[i]=(-1,1);eta[2*t-i]=(-1,-1)
  else:eta[i]=(1,0);eta[2*t-i]=(-1,0)
 zeta=[(1,0)]
 for i in range(2*t+1):
  s,k=zeta[-1];a,b=eta[i];zeta.append((s*a,k-b))
 for i in range(2*t+1):
  si,ki=zeta[i];sj,kj=zeta[i+1];assert(si*sj,ki-kj)==eta[i]
 return chosen,eta,zeta

def construction(t,physical=False):
 m=2*t+1;g=2*t;n=m*g
 actual=[actual_A(t,i)for i in range(m)];simple=[simple_A(t,i)for i in range(m)];center=actual[t]
 assert all(actual[i]*simple[t]==simple[i]*center for i in range(m))
 assert all(actual[i]==actual[2*t-i]for i in range(m))
 ratios=[a/center for a in actual]
 if t==10:
  assert ratios[8]>F(19,40)**2 and ratios[6]>F(1,40)**2
 else:assert ratios[t-2]>F(1,4)
 chosen,eta,zeta=phase_labels(t)
 # Exact radical dictionaries prove both phase sums. A key r means sqrt(r).
 sums={c:{k:defaultdict(int)for k in [-1,0,1]}for c in [0,1]}
 for i in range(m):
  s,k=eta[i];sums[i%2][k][ratios[i]]+=s
 clean=lambda d:{r:s for r,s in d.items()if s}
 for c in [0,1]:
  for k in [-1,0,1]:sums[c][k]=clean(sums[c][k])
 assert all(not sums[1-t%2][k]for k in [-1,0,1])
 assert sums[t%2][0]=={F(1):1}
 expected=defaultdict(int)
 for i in chosen:expected[ratios[i]]-=1
 assert sums[t%2][1]==sums[t%2][-1]==dict(expected)
 # Hence center-normalized sum is 1-b*(e+conj(e))=1-2bc=0.
 out={'t':t,'n':n,'support_size':m+1,'chosen_left_edges':chosen,'phase_definition':'b=sum sqrt(ratio[i]) over chosen; c=1/(2b); e=c+i sqrt(1-c^2); zeta path recurrence','ratios_selected':{str(i):str(ratios[i])for i in chosen},'eta_labels':[[*eta[i]]for i in range(m)],'zeta_labels':zeta,'exact_phase_closure':True}
 if physical:
  p=[F(comb(m,i),2**(m-1))for i in range(m+1)]
  assert sum(p[::2])==sum(p[1::2])==1
  k=g;diagonal=[];cross=[];zero_entries=0
  for a in range(k+1):
   # Full diagonal reduced-Gram difference, with binomial weights retained.
   vals=[]
   for color in [0,1]:
    value=sum((p[i]*comb(k,a)*F(comb(n-k,g*i-a),comb(n,g*i)) for i in range(color,m+1,2)if 0<=g*i-a<=n-k),F(0))
    vals.append(value)
   assert vals[0]==vals[1];diagonal.append(str(vals[0]))
  # Enumerate every off-diagonal logical reduced-Gram entry and every
  # off-diagonal entry inside either diagonal logical block.
  for ca in [0,1]:
   for cb in [0,1]:
    for a in range(k+1):
     for b in range(k+1):
      if ca==cb and a==b:continue
      terms=[]
      for i in range(ca,m+1,2):
       l=g*i-a
       if not 0<=l<=n-k:continue
       wj=l+b
       if wj%g:continue
       j=wj//g
       if not(0<=j<=m and j%2==cb):continue
       weight2=p[i]*p[j]*comb(k,a)*comb(k,b)*F(comb(n-k,l)**2,comb(n,g*i)*comb(n,g*j))
       terms.append((i,j,weight2))
      if not terms:zero_entries+=1;continue
      assert ca!=cb and abs(a-b)==g
      for i,j,w2 in terms:
       edge=min(i,j)
       assert abs(i-j)==1
       assert w2*F(factorial(n),factorial(n-k))**2==actual[edge]
      assert {min(i,j)%2 for i,j,w2 in terms}=={min(i,j)%2 for i,j,w2 in terms[:1]}
      cross.append({'logical':[ca,cb],'reduced_entry':[a,b],'edges':[min(i,j)for i,j,w2 in terms]})
  assert len(cross)==4
  assert sum(F(x)for x in diagonal)==1
  out['physical_check']={'all_diagonal_reduced_Gram_equalities':len(diagonal),'diagonal_trace':1,'offdiagonal_nonzero_support_entries':cross,'other_entries_exact_zero':zero_entries,'cross_weights_exact_common_factor':'1/(n falling k) relative to ladder amplitudes','all_KL_pass':True}
 return out

st=time.monotonic();negative=[]
for t in range(1,10):
 a=[simple_A(t,i)for i in range(2*t+1)];bounds=[sqrtbox(v/a[t])for v in a]
 gap=F(1)-sum(bounds[i][1]for i in range(t%2,2*t+1,2)if i!=t)
 assert gap>0
 negative.append({'t':t,'n':2*t*(2*t+1),'central_minus_others_lower':str(gap)})
controls=[construction(t,physical=t==10)for t in [10,11,12,13]]
endpoint=F(3,13)+F(1,12)+F(50,165);assert endpoint<F(2,3)
result={'status':'exact controls PASS; all-t proof is analytic in companion document','controls':controls,'family_impossible_t1_to9':negative,'uniform_log_bound_at13':str(endpoint),'seconds':time.monotonic()-st,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(ROOT/'phase_twisted_gnu_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'physical_t10':controls[0]['physical_check'],'uniform_bound_at13':str(endpoint),'seconds':result['seconds'],'peak_rss_KiB':result['peak_rss_KiB']},indent=2))
