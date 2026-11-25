"""Independent literal-deletion geometry + exact conditional leaf dual audit."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json,gzip,itertools,hashlib,time
start=time.monotonic();P=Path(__file__).resolve().parents[2]/'deletion-code-optimality/continuation/barrier26_release_20261025/independent_inputs';outdir=Path(__file__).resolve().parent
model=json.loads((P/'model.json').read_text())
D=[];R=[set() for _ in range(2048)]
for w in range(4096):
 s=f'{w:012b}';ys={int(s[:i]+s[i+1:],2) for i in range(12)};D.append(ys)
 for y in ys:R[y].add(w)
def transform(w,t):return (int(f'{w:012b}'[::-1],2) if t&2 else w)^(4095 if t&1 else 0)
cache={}
def clique(xs):
 key=tuple(sorted(xs));assert len(key)==len(set(key)) and all(type(x)==int and 0<=x<4096 for x in key)
 if key not in cache:
  assert all(D[a]&D[b] for a,b in itertools.combinations(key,2));cache[key]=({x:1 for x in key},1)
 return cache[key]
rowsCG=[]
for i,obj in enumerate(model['nodes']):
 a=Counter();b=0
 for p in obj['parents']:
  assert len(set(p)&{'receiver','clique','cut'})==1
  m=p.get('m',1);assert type(m)==int and m>0
  if 'receiver' in p:aa={x:1 for x in R[p['receiver']]};bb=1
  elif 'clique' in p:aa,bb=clique(p['clique'])
  else:assert 0<=p['cut']<i;aa,bb=rowsCG[p['cut']]
  for x,v in aa.items():a[x]+=m*v
  b+=m*bb
 divisor=obj['divisor'];assert type(divisor)==int and divisor>=2
 rowsCG.append(({x:v//divisor for x,v in a.items() if v>=divisor},b//divisor))
rows=[]
for i,obj in enumerate(model['rows']):
 if 'clique' in obj:a,b=clique(obj['clique'])
 elif 'canonical_prefix' in obj:
  prefix=obj['canonical_prefix'];assert prefix==model['normalization']['prefix'] and len(prefix)==len(set(prefix))==10
  tr=obj['transform'];assert tr in(1,2,3);a=Counter();b=0
  for j,x in enumerate(prefix):a[transform(x,tr)]+=2**(9-j);a[x]-=2**(9-j)
 else:
  assert set(obj)=={'cut','transform'};a0,b=rowsCG[obj['cut']];a={transform(x,obj['transform']):v for x,v in a0.items()}
 assert b==model['rhs'][i];rows.append((a,b))
assert model['fixed_constants']==[0,4095]

c=json.loads((P/'barrier.json').read_text());M=c['scale'];x=c['values']
assert len(x)==4096 and all(type(v)==int and 0<=v<=M for v in x)
assert x[0]==x[4095]==M and sum(x)==c['numerator']>=320*M
assert all(x[v] in(0,M) for v in model['selected_words'])
assert sorted(o['transform'] for o in model['rows'] if 'canonical_prefix' in o)==[1,2,3]
assert all(sum(a[v]*x[v] for v in a)<=M*b for a,b in rows)
adj=[0]*4096
for receiver in R:
 mask=sum(1<<v for v in receiver)
 for v in receiver:adj[v]|=mask^(1<<v)
count=0;maxmass=0
def bk(P,X,mass):
 global count,maxmass
 if not(P|X):
  count+=1;maxmass=max(maxmass,mass);assert mass<=M;return
 options=P|X;pivot=-1;best=-1
 while options:
  low=options&-options;v=low.bit_length()-1;options-=low
  score=(adj[v]&P).bit_count()
  if score>best:best=score;pivot=v
 candidates=P&~adj[pivot]
 while candidates:
  low=candidates&-candidates;v=low.bit_length()-1;candidates-=low
  bk(P&adj[v],X&adj[v],mass+x[v]);P-=low;X|=low
bk((1<<4096)-1,0,0)
assert count==155496 and not all(v in(0,M) for v in x)
out={'passed':True,'barrier_sha256':hashlib.sha256((P/'barrier.json').read_bytes()).hexdigest(),'model_sha256':hashlib.sha256((P/'model.json').read_bytes()).hexdigest(),'exact_mass':str(Fraction(sum(x),M)),'mass_float':sum(x)/M,'binary_selected_words':len(model['selected_words']),'selected_ones':[v for v in model['selected_words']if x[v]==M],'CG_nodes':len(rowsCG),'model_rows':len(rows),'maximal_cliques_enumerated':count,'maximum_clique_mass':str(Fraction(maxmass,M)),'actual_code':False,'seconds':time.monotonic()-start,'scope':'Exact partial-integrality barrier, not a320-word code or a universal impossibility of branching.'}
(outdir/'deletion_branch26_barrier_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
