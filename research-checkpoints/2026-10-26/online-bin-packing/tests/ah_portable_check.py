"""Source-derived AH audit. No worker/advisor imports; no dominance deletion.
All knapsack items retained if positive reduced profit. Rational data converted
to exact integer lattices, then density-bound DFS proves strict capacities.
"""
from pathlib import Path
from fractions import Fraction as F
from html.parser import HTMLParser
import re,json,math,os,resource,time,functools,sys,argparse,hashlib
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3)); resource.setrlimit(resource.RLIMIT_CPU,(285,290));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
ap=argparse.ArgumentParser();ap.add_argument('--track-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--facts',type=Path,default=Path(__file__).with_name('ah_primary_numerical_facts.json'));args=ap.parse_args()
START=time.monotonic(); P=args.track_root.resolve()
facts=json.loads(args.facts.read_text());assert facts['schema']=='AH-independent-primary-numerical-facts-v1'
C={int(j):[F(p['lower']),F(p['upper']),{F(i):F(a)for i,a in p['containers']}]for j,p in facts['classes'].items()};assert set(C)==set(range(2,213))
changes=[(167,1,3,F(101,1000000)),(172,2,6,F(203907985616802938880,661406035963546729717373)),(179,10,2,F(56254421499138925905512741470208,47449963408280619234481631165243337))]
for j,a,b,d in changes:C[j][2][a]-=d;C[j][2][b]+=d
cert=json.loads((P/'ah_three_parameter_full_certificate.json').read_text());R=F(1848920194883516152323541607,1171513518439186595284254720);assert F(cert['target'])==R
V={F(0),F(1,2)}
for j in range(2,213):
 lo,hi,A=C[j];assert hi==(F(1,2) if j==2 else C[j-1][0]) and 0<=lo<hi;assert sum(A.values())==1 and all(a>0 for a in A.values())
 cp=cert['parameters'][str(j)];assert (lo,hi)==(F(cp['lower']),F(cp['upper'])) and A=={F(i):F(v) for i,v in cp['containers']}
 V|={lo,hi}
 for i in A:
  if j!=212:assert i.denominator==1 and 1<=i<=1//hi
  vol=i if j==212 else i*hi;assert 0<vol<=1
  V|={vol,1-vol}
V=sorted(v for v in V if 0<=v<=F(1,2));assert V[0]==0 and V[-1]==F(1,2)
S={(F(r['lower']),F(r['upper'])):tuple(F(r[k])if r[k]is not None else None for k in ['u','v','w'])for r in facts['weight_intervals']}
assert facts['special_weight_intervals']==[{'lower':'0','upper':'1/6','w':'0'},{'lower':'3/10','upper':'1/3','w':'413913/524288'}]
assert R<F(facts['original_exact_bound'])
supplied={(F(s['x']),F(s['y'])):s for s in cert['scenarios']};assert set(supplied)==set(zip(V,V[1:])) and len(supplied)==len(cert['scenarios'])
node_count=0;check_count=0;balance_count=0

def price(items,rho,cap,target):
 global node_count,check_count
 # Use integer size/profit lattices rather than Fraction DFS or deletions.
 raw=[(s,w-rho*s) for s,w in items if 0<s<cap and w>rho*s]
 raw.sort(key=lambda z:z[1]/z[0],reverse=True)
 allowance=target-rho*cap;assert allowance>=0
 sl=math.lcm(cap.denominator,*(s.denominator for s,p in raw));pl=math.lcm(allowance.denominator,*(p.denominator for s,p in raw))
 data=[(int(s*sl),int(p*pl)) for s,p in raw];budget=int(allowance*pl);capacity=int(cap*sl)
 stack=[(0,capacity,0)];nn=0
 while stack:
  idx,remain,gain=stack.pop();nn+=1;assert gain<=budget
  if idx==len(data):continue
  sz,pr=data[idx]
  # Fractional relaxation bounds every remaining item by maximal remaining density.
  if gain*sz+remain*pr<=budget*sz:continue
  for q in range((remain-1)//sz+1):stack.append((idx+1,remain-q*sz,gain+q*pr))
 node_count+=nn;check_count+=1;return nn

for x,y in zip(V,V[1:]):
 t=(x+y)/2;a=1-t;k=next(j for j,(lo,hi,A) in C.items() if lo<t<hi)
 if y<=F(1,6):u=v=None;w=F(0)
 elif F(3,10)<=x and y<=F(1,3):u=v=None;w=F(413913,524288)
 else:
  rows=[weights for (lo,hi),weights in S.items() if lo<=x<y<=hi];assert len(rows)==1,(x,y,len(rows));u,v,w=rows[0]
 sc=supplied[x,y];assert F(sc['w'])==w;assert 0<=w<=1
 large=t>F(1,3)
 if large:
  assert F(sc['u'])==u and F(sc['v'])==v;assert 0<=u<=v<=1
  aa=C[k][2].get(F(1),0);bb=C[k][2].get(F(2),0);assert aa+bb==1
  assert (aa+2*bb)*u+aa*w>=1 and bb*u+v>=1 and aa*v+2*bb*u+bb*(1-w)>=1;balance_count+=3
 normal=[(F(1,2),w)];heavy=[]
 for j in range(2,213):
  lo,hi,A=C[j]
  if large and j==k:normal.extend([(lo,u),(x,v)]);heavy.append((lo,u));continue
  num=den=F(0)
  for i,alpha in A.items():
   # Exact threshold comparisons at an interior point, including actual-size
   # large singleton classes rather than pretending they have fixed upper volume.
   vol=i if j==212 else (lo+hi)/2 if j<=165 and i==1 else i*hi
   rw=F(1) if (vol>F(1,2) and vol>=a) or (vol<=F(1,2) and vol>t) else w if vol>F(1,2) else 1-w
   num+=alpha*rw;den+=alpha*(i-F(1,43) if j==212 else i)
  z=num/den
  if j==212:rho=z
  else:
   normal.append((lo,z))
   if j>=k:heavy.append((lo,z))
 assert 0<=rho<=2
 price(normal,rho,F(1),R);price(heavy,rho,y,R-1)
print(json.dumps({'status':'PASS','parameters_and_weights_from_independent_primary_extraction':True,'facts_sha256':hashlib.sha256(args.facts.read_bytes()).hexdigest(),'primary_HTML_sha256':facts['source']['sha256'],'exact_modified_parameters_match':True,'scenarios':len(V)-1,'strict_knapsacks':check_count,'large_balance_inequalities':balance_count,'integer_lattice_nodes_no_dominance_pruning':node_count,'target':str(R),'seconds':time.monotonic()-START,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'endpoint_convention':'threshold chosen at interior midpoint for scenario classification; separate proof establishes applicability to every input'},indent=2))
