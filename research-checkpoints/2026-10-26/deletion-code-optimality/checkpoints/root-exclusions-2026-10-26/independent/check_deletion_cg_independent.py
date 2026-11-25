"""Independent insertion-first string geometry and full-word averaged CG dual."""
import json,sys,itertools,hashlib,time
from pathlib import Path
from fractions import Fraction as F
st=time.time();path=Path(sys.argv[1]);d=json.loads(path.read_text());scale=d['scale'];assert type(scale)==int and scale>0
# Reconstruct parent sets from insertion, not deletion bit arithmetic.
parents=[];desc=[set()for _ in range(4096)]
for y in range(2048):
 s=f'{y:011b}';p={int(s[:i]+b+s[i:],2)for i in range(12)for b in '01'};parents.append(p)
 for x in p:desc[x].add(y)
def orbit(x):
 s=f'{x:012b}';rev=int(s[::-1],2);return sorted({x,rev,4095-x,4095-rev})
orbits=[];seen=set()
for x in range(4096):
 if x not in seen:o=orbit(x);orbits.append(o);seen.update(o)
assert len(orbits)==1056
cliquecache={}
def clique(xs):
 key=tuple(sorted(xs));assert len(key)==len(set(key)) and all(type(x)==int and 0<=x<4096 for x in key)
 if key not in cliquecache:
  assert all(desc[x]&desc[y]for x,y in itertools.combinations(key,2));cliquecache[key]={x:1 for x in key}
 return cliquecache[key],1
cache={};ranks={};visiting=set()
def node(i):
 if i in cache:return cache[i]
 assert type(i)==int and 0<=i<len(d['nodes'])and i not in visiting;visiting.add(i)
 o=d['nodes'][i];div=o['divisor'];assert type(div)==int and div>=2
 a={};b=0;rank=0
 for p in o['parents']:
  m=p.get('m',1);assert type(m)==int and m>0
  keys=set(p)&{'receiver','clique','cut'};assert len(keys)==1
  if 'receiver'in p:
   y=p['receiver'];assert type(y)==int and 0<=y<2048;aa={x:1 for x in parents[y]};bb=1
  elif 'clique'in p:aa,bb=clique(p['clique'])
  else:assert p['cut']<i;aa,bb=node(p['cut']);rank=max(rank,ranks[p['cut']])
  for x,v in aa.items():a[x]=a.get(x,0)+m*v
  b+=m*bb
 ans=({x:v//div for x,v in a.items()if v//div},b//div);cache[i]=ans;ranks[i]=rank+1;visiting.remove(i);return ans
# Apply every dual term after averaging its four actual group transports.
coverage=[0]*4096;objective=0
def add(lam,a,b):
 global objective
 assert type(lam)==int and lam>0
 for x,v in a.items():
  s=f'{x:012b}';z=int(s[::-1],2)
  for y in (x,z,4095-x,4095-z):coverage[y]+=lam*v
 objective+=4*lam*b
for lam,xs in d['cliques']:a,b=clique(xs);add(lam,a,b)
for i,lam in d['node_multipliers']:a,b=node(i);add(lam,a,b)
for i,lam in d['orbit_upper']:
 assert type(lam)==int and lam>0 and 0<=i<len(orbits);o=orbits[i]
 alpha=max(len(s)for k in range(len(o)+1)for s in itertools.combinations(o,k)if all(not(desc[x]&desc[y])for x,y in itertools.combinations(s,2)))
 for x in o:coverage[x]+=lam
 objective+=lam*alpha
assert min(coverage)>=scale and objective==d['numerator']
out={'passed':True,'certificate':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'numerator':objective,'denominator':scale,'exact_upper':str(F(objective,scale)),'upper_float':objective/scale,'integer_upper':objective//scale,'full_word_coverage_checks':4096,'cliques_checked':len(cliquecache),'nodes_expanded':len(cache),'maximum_CG_rank':max(ranks.values()),'seconds':time.time()-st,'method':'independent insertion-first string geometry; explicit four group transports; no worker imports'}
Path(__file__).with_name('deletion_cg_'+path.stem+'_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
