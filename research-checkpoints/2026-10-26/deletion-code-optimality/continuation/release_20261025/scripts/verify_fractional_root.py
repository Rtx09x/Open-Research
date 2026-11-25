"""Stdlib-only insertion graph, independent clique enumeration, exact CG primal."""
import json,itertools,time,subprocess,sys,tempfile
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')
E=Path(__file__).resolve().parents[1]/'evidence';start=time.monotonic();c=json.loads((E/'exact_fractional_root.json').read_text())
R=[];D=[set() for _ in range(4096)]
for y in range(2048):
 s=format(y,'011b');P={int(s[:j]+a+s[j:],2) for j in range(12) for a in '01'};R.append(P)
 for x in P:D[x].add(y)
O=[];oid={}
for x in range(4096):
 if x in oid:continue
 v=int(format(x,'012b')[::-1],2);o=sorted({x,v,4095-x,4095-v})
 for y in o:oid[y]=len(O)
 O.append(o)
assert O==c['orbits'] and len(O)==1056
M=c['scale'];q=c['z_numerators'];assert len(q)==1056 and all(isinstance(v,int) and v>=0 for v in q);Q=sum(q);assert Q==c['numerator']>320*M
w=[(4//len(O[oid[x]]))*q[oid[x]] for x in range(4096)]
for i,o in enumerate(O):
 alpha=max(len(s) for k in range(len(o)+1) for s in itertools.combinations(o,k) if all(not(D[x]&D[y]) for x,y in itertools.combinations(s,2)))
 assert q[i]<=alpha*M
rows=[];checked_cliques=set()
for i,node in enumerate(c['nodes']):
 if 'cap' in node:assert node['cap']==320;rows.append(({x:1 for x in range(4096)},320));continue
 aa={};bb=0
 for p in node['parents']:
  if 'receiver' in p:a={x:1 for x in R[p['receiver']]};b=1
  elif 'clique' in p:
   clique=tuple(p['clique'])
   if clique not in checked_cliques:assert len(clique)==len(set(clique)) and all(D[x]&D[y] for x,y in itertools.combinations(clique,2));checked_cliques.add(clique)
   a={x:1 for x in clique};b=1
  else:assert 0<=p['cut']<i;a,b=rows[p['cut']]
  mult=p.get('m',1);assert isinstance(mult,int) and mult>0
  for x,v in a.items():aa[x]=aa.get(x,0)+mult*v
  bb+=mult*b
 div=node['divisor'];assert isinstance(div,int) and div>=2;rows.append(({x:v//div for x,v in aa.items() if v//div},bb//div))
for i,(a,b) in enumerate(rows):
 value=sum(v*w[x] for x,v in a.items())
 if 'cap' not in c['nodes'][i]:assert value<=4*M*b
 assert 320*value<=4*Q*b # scaled point, objective exactly320, includes cap
adj=[0]*4096
for parents in R:
 mask=sum(1<<x for x in parents)
 for x in parents:adj[x]|=mask^(1<<x)
count=0

def bk(P,X,total):
 global count
 if not(P|X):count+=1;assert total<=4*M;return
 U=P|X;u=-1;score=-1
 while U:
  bit=U&-U;v=bit.bit_length()-1;U-=bit;s=(P&adj[v]).bit_count()
  if s>score:u,score=v,s
 C=P&~adj[u]
 while C:
  bit=C&-C;v=bit.bit_length()-1;C-=bit;bk(P&adj[v],X&adj[v],total+w[v]);P-=bit;X|=bit
bk((1<<4096)-1,0,0);assert count==155496
# Replay the independent global bound proving cap320, not an untrusted axiom.
with tempfile.TemporaryDirectory() as t:
 f=Path(t)/'cap.json';f.write_text(json.dumps(c['cap_certificate']));rr=subprocess.run([sys.executable,'-I','-S',str(Path(__file__).with_name('verify_cg_hierarchy.py')),str(f)],text=True,capture_output=True,check=True);cap=json.loads(rr.stdout);assert cap['passed'] and cap['integer_upper']==320
print(json.dumps({'passed':True,'uncapped_fractional_lower_numerator':Q,'uncapped_fractional_lower_denominator':M,'uncapped_fractional_lower':Q/M,'certified_upper':cap['upper'],'scaled_fractional_feasible_size_exact':320,'all_maximal_cliques_independently_enumerated':count,'CG_nodes_checked':len(rows),'cap_in_scaled_model':True,'not_a_code':True,'seconds':time.monotonic()-start},indent=2))
