"""Independent exact partial-integrality witness audit, stdlib only."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json,itertools,time,sys
if not __debug__:raise RuntimeError('Assertions required; do not use -O')
start=time.monotonic();p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('point.json');c=json.loads(p.read_text());M=c['scale'];q=c['values'];assert isinstance(M,int) and M>0 and len(q)==4096 and all(isinstance(v,int) and 0<=v<=M for v in q);assert sum(q)==c['numerator']>=320*M;selected=c['selected_binary_words'];assert len(selected)==len(set(selected))==26 and all(q[x] in [0,M] for x in selected);assert c['fixed_constants']==[0,4095] and q[0]==q[4095]==M
R=[];D=[set() for _ in range(4096)]
for y in range(2048):
 s=format(y,'011b');parents={int(s[:i]+b+s[i:],2) for i in range(12) for b in '01'};R.append(parents)
 for x in parents:D[x].add(y)
 assert sum(q[x] for x in parents)<=M

def tr(x,n,t):return (int(format(x,f'0{n}b')[::-1],2) if t&2 else x)^(((1<<n)-1) if t&1 else 0)
for x in range(4096):
 for t in range(4):assert D[tr(x,12,t)]=={tr(y,11,t) for y in D[x]}
assert all(tr(x,12,t) in selected for x in selected for t in range(4))
prefix=c['canonical_prefix'];assert len(prefix)==len(set(prefix))==10 and set(prefix)<=set(selected)
score=sum(2**(9-j)*q[x] for j,x in enumerate(prefix))
for t in [1,2,3]:assert score>=sum(2**(9-j)*q[tr(x,12,t)] for j,x in enumerate(prefix))
rows=[];checked=set()
for i,node in enumerate(c['CG_nodes']):
 assert 'cap' not in node;aa=Counter();bb=0
 for p in node['parents']:
  mult=p.get('m',1);assert isinstance(mult,int) and mult>0;assert sum(k in p for k in ['receiver','clique','cut'])==1
  if 'receiver' in p:
   y=p['receiver'];assert isinstance(y,int) and 0<=y<2048;a={x:1 for x in R[y]};b=1
  elif 'clique' in p:
   Q=tuple(p['clique']);assert len(Q)==len(set(Q)) and all(isinstance(x,int) and 0<=x<4096 for x in Q)
   if Q not in checked:assert all(D[x]&D[y] for x,y in itertools.combinations(Q,2));checked.add(Q)
   a={x:1 for x in Q};b=1
  else:j=p['cut'];assert isinstance(j,int) and 0<=j<i;a,b=rows[j]
  for x,v in a.items():aa[x]+=mult*v
  bb+=mult*b
 d=node['divisor'];assert isinstance(d,int) and d>=2;a={x:v//d for x,v in aa.items() if v//d};b=bb//d;rows.append((a,b))
 for t in range(4):assert sum(v*q[tr(x,12,t)] for x,v in a.items())<=b*M
adj=[0]*4096
for parents in R:
 mask=sum(1<<x for x in parents)
 for x in parents:adj[x]|=mask^(1<<x)
count=0

def bk(P,X,total):
 global count
 if not(P|X):count+=1;assert total<=M;return
 U=P|X;u=-1;score=-1
 while U:
  bit=U&-U;v=bit.bit_length()-1;U-=bit;d=(P&adj[v]).bit_count()
  if d>score:u,score=v,d
 C=P&~adj[u]
 while C:
  bit=C&-C;v=bit.bit_length()-1;C-=bit;bk(P&adj[v],X&adj[v],total+q[v]);P-=bit;X|=bit
bk((1<<4096)-1,0,0);assert count==155496 and len(rows)==783;fractional=sum(v not in [0,M] for v in q);assert fractional>0
print(json.dumps({'passed':True,'objective_exact':str(Fraction(sum(q),M)),'objective_decimal':sum(q)/M,'selected_binary_words':26,'selected_ones':[x for x in selected if q[x]==M],'fractional_word_coordinates':fractional,'CG_nodes':len(rows),'CG_transports_checked':4*len(rows),'maximal_cliques_enumerated':count,'not_a_code':True,'global_bound_improvement':False,'seconds':time.monotonic()-start},indent=2))
