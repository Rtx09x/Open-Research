"""Independent stdlib exact proof-DAG dual checker, including rounded cap ancestors."""
import argparse,json,itertools,time
from pathlib import Path
if not __debug__:raise RuntimeError('Run without -O')
p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);args=p.parse_args();start=time.monotonic()
strings=[format(x,'012b') for x in range(4096)]
d=[{s[:i]+s[i+1:] for i in range(12)} for s in strings];recv={format(y,'011b'):[] for y in range(2048)}
for x,ys in enumerate(d):
 for y in ys:recv[y].append(x)
orbits=[];oid={}
for x,s in enumerate(strings):
 if x in oid:continue
 r=int(s[::-1],2);o=sorted({x,r,4095-x,4095-r})
 for y in o:oid[y]=len(orbits)
 orbits.append(o)
assert len(orbits)==1056
checked_cliques=set()
def clique(Q):
 t=tuple(Q)
 if t not in checked_cliques:
  assert len(Q)==len(set(Q)) and all(isinstance(x,int) and 0<=x<4096 for x in Q)
  assert all(d[x]&d[y] for x,y in itertools.combinations(Q,2));checked_cliques.add(t)
 return {x:1 for x in Q},1

def verify(cert,nesting=0):
 assert nesting<=4
 M=cert['scale'];assert isinstance(M,int) and M>0
 cap=None;cap_proof=None
 if 'cap_certificate' in cert:
  cap_proof=verify(cert['cap_certificate'],nesting+1);cap=cap_proof['numerator']//cap_proof['denominator']
 memo={};depth={}
 def expand(i):
  if i in memo:return memo[i]
  assert isinstance(i,int) and 0<=i<len(cert['nodes']);node=cert['nodes'][i]
  if 'cap' in node:
   assert cap is not None and node['cap']==cap
   memo[i]=({x:1 for x in range(4096)},cap);depth[i]=cap_proof['maximum_CG_rank']+1;return memo[i]
  dv=node['divisor'];assert isinstance(dv,int) and dv>=2
  aa={};bb=0;dep=0
  for t in node['parents']:
   m=t.get('m',1);assert isinstance(m,int) and m>0
   assert sum(k in t for k in ['receiver','clique','cut'])==1
   if 'receiver' in t:
    y=t['receiver'];assert isinstance(y,int) and 0<=y<2048;a={x:1 for x in recv[format(y,'011b')]};b=1
   elif 'clique' in t:a,b=clique(t['clique'])
   else:
    j=t['cut'];assert isinstance(j,int) and 0<=j<i;a,b=expand(j);dep=max(dep,depth[j])
   for x,v in a.items():aa[x]=aa.get(x,0)+m*v
   bb+=m*b
  memo[i]=({x:v//dv for x,v in aa.items() if v//dv},bb//dv);depth[i]=dep+1;return memo[i]
 cov=[0]*1056;num=0
 def add(lam,a,b):
  nonlocal num
  assert isinstance(lam,int) and lam>0
  for x,v in a.items():cov[oid[x]]+=lam*v*(4//len(orbits[oid[x]]))
  num+=lam*4*b
 for lam,Q in cert['cliques']:
  a,b=clique(Q);add(lam,a,b)
 for i,lam in cert['node_multipliers']:
  a,b=expand(i);add(lam,a,b)
 for i,lam in cert['orbit_upper']:
  assert isinstance(lam,int) and lam>0 and isinstance(i,int) and 0<=i<1056
  o=orbits[i];alpha=max(len(s) for k in range(len(o)+1) for s in itertools.combinations(o,k) if all(not(d[x]&d[y]) for x,y in itertools.combinations(s,2)))
  cov[i]+=lam;num+=alpha*lam
 assert min(cov)>=M and num==cert['numerator']
 return {'passed':True,'numerator':num,'denominator':M,'upper':num/M,'integer_upper':num//M,'dual_cliques':len(cert['cliques']),'dual_CG_nodes':len(cert['node_multipliers']),'expanded_ancestor_nodes':len(memo),'maximum_CG_rank':max(depth.values(),default=0),'coverage_checks':len(cov),'rounded_cap_ancestor':cap,'cap_proof':cap_proof}
result=verify(json.loads(args.certificate.read_text()));result['checked_cliques']=len(checked_cliques);result['seconds']=time.monotonic()-start;print(json.dumps(result,indent=2))
