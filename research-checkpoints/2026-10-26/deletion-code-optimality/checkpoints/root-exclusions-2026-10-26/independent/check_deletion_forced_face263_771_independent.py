"""Independent literal deletion and exact dual-gap/Farkas chain; no worker imports."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,hashlib,time
start=time.monotonic();H=Path(__file__).resolve().parent
P=Path('/workspace/shared/research-active/deletion-code-optimality/continuation/evidence/dual_slack_gate263_771_frozen')
model=json.loads((P/'model.json').read_text());scope=model['conditional_target320']
reqroot=P.parent/'required_receivers320';reqraw=(reqroot/'certificate.json').read_bytes();req=json.loads(reqraw)
prior=json.loads((H/'check_deletion_forced_receivers_independent.json').read_text())
assert prior['PASS'] and prior['certificate_sha256']==hashlib.sha256(reqraw).hexdigest()==scope['required_certificate_sha256']
assert hashlib.sha256((reqroot/'global_dual.json').read_bytes()).hexdigest()==req['global_dual_sha256']
D=[];R=[set() for _ in range(2048)]
for w in range(4096):
 s=f'{w:012b}';ys={int(s[:i]+s[i+1:],2) for i in range(12)};D.append(ys)
 for y in ys:R[y].add(w)
def tr(w,g):return (int(f'{w:012b}'[::-1],2) if g&2 else w)^(4095 if g&1 else 0)
cache={}
def clique(xs):
 key=tuple(sorted(xs));assert len(key)==len(set(key)) and all(type(x)==int and 0<=x<4096 for x in key)
 if key not in cache:assert all(D[x]&D[y] for x,y in combinations(key,2));cache[key]=({x:1 for x in key},1)
 return cache[key]
cg=[]
for i,node in enumerate(model['nodes']):
 a=Counter();b=0
 for p in node['parents']:
  m=p.get('m',1);assert type(m)==int and m>0
  if 'receiver' in p:aa={x:1 for x in R[p['receiver']]};bb=1
  elif 'clique' in p:aa,bb=clique(p['clique'])
  else:assert 0<=p['cut']<i;aa,bb=cg[p['cut']]
  for x,v in aa.items():a[x]+=m*v
  b+=m*bb
 q=node['divisor'];assert type(q)==int and q>=2
 cg.append(({x:v//q for x,v in a.items() if v>=q},b//q))
rows=[];required=[];canon=[]
for i,r in enumerate(model['rows']):
 if 'clique' in r:a,b=clique(r['clique'])
 elif 'required_receiver' in r:
  y=r['required_receiver'];assert y in req['required_receivers'];required.append(y);a={x:-1 for x in R[y]};b=-1
 elif 'canonical_prefix' in r:
  pf=r['canonical_prefix'];g=r['transform'];assert 1<=len(pf)<=10 and len(pf)==len(set(pf)) and pf==model['normalization']['prefix'][:len(pf)] and g in(1,2,3)
  a=Counter();b=0;canon.append((len(pf),g))
  for j,w in enumerate(pf):a[tr(w,g)]+=2**(len(pf)-j-1);a[w]-=2**(len(pf)-j-1)
  a={x:v for x,v in a.items() if v}
 else:
  assert set(r)=={'cut','transform'} and r['transform'] in range(4)
  aa,b=cg[r['cut']];a={tr(x,r['transform']):v for x,v in aa.items()}
 assert b==model['rhs'][i];rows.append((a,b))
assert sorted(required)==sorted(req['required_receivers'])==sorted(scope['required_receivers'])
assert sorted(canon)==[(i,g) for i in range(1,11) for g in(1,2,3)]
assert model['selected_words']==[] and scope['all58_zero_restriction'] is False
assert scope['cover_path']==[[3,5],[7,263]]
assert scope['extra_fixed_ones']==[771]
ones=[0,4095]+[v for y,v in scope['cover_path']]+scope['extra_fixed_ones']
assert ones==scope['fixed_ones'] and all(v in R[y] for y,v in scope['cover_path'])
assert all(not D[x]&D[y] for x,y in combinations(ones,2))
zeros={x for x in range(4096) if x not in ones and any(D[x]&D[y] for y in ones)}
c=json.loads((P/'dual.json').read_text());M=c['scale'];assert type(M)==int and M>0
assert c['fixed_ones']==ones and set(c['conflict_zero_words'])==zeros
cov=[0]*4096;cost=0
for label in('lambda','upper','lower'):
 assert len(dict(c[label]))==len(c[label]) and all(type(v)==int and v>0 for _,v in c[label])
for i,v in c['lambda']:
 a,b=rows[i];cost+=v*b
 for x,z in a.items():cov[x]+=v*z
for x,v in c['upper']:cov[x]+=v;cost+=v*(x not in zeros)
for x,v in c['lower']:cov[x]-=v;cost-=v*(x in ones)
assert min(cov)>=M and cost==c['numerator'];gap=cost-320*M;assert gap==1053258
lam,mu,nu=map(dict,(c['lambda'],c['upper'],c['lower']))
fixed={x:1 for x in ones};fixed.update({x:0 for x in zeros})
def put(x,v):
 assert x not in fixed or fixed[x]==v
 fixed[x]=v
for x in range(4096):
 if mu.get(x,0)>gap:put(x,int(x not in zeros))
 if nu.get(x,0)>gap:put(x,int(x in ones))
 if cov[x]-M>gap:put(x,0)
eq=[]
for i,(a,b) in enumerate(rows):
 if lam.get(i,0)>gap or 'required_receiver' in model['rows'][i]:eq.append(({x:v for x,v in a.items() if x not in fixed},b-sum(v*fixed[x] for x,v in a.items() if x in fixed)))
eq.append(({x:1 for x in range(4096) if x not in fixed},320-sum(fixed.values())))
saved=json.loads((P/'equations.json').read_text())
assert saved['fixed_values']==[list(v) for v in sorted(fixed.items())]
assert saved['equations']==[[[list(v) for v in sorted(a.items())],b] for a,b in eq]
f=json.loads((P/'face_farkas.json').read_text());free=set(range(4096))-set(fixed);assert f['free_words']==sorted(free)
coef=Counter();rhs=0
for idx,m in f['lambda']:
 assert type(m)==int and m>0;desc=f['row_descriptors'][idx]
 if 'forced_equation' in desc:
  sign=desc['sign'];assert sign in(-1,1);aa,bb=eq[desc['forced_equation']];a={x:sign*v for x,v in aa.items()};b=sign*bb
 else:
  if 'global_row' in desc:aa,bb=rows[desc['global_row']]
  else:aa,bb=clique(desc['added_clique'])
  a={x:v for x,v in aa.items() if x not in fixed};b=bb-sum(v*fixed[x] for x,v in aa.items() if x in fixed)
 rhs+=m*b
 for x,v in a.items():assert x in free;coef[x]+=m*v
minimum=sum(min(0,coef[x]) for x in free)
assert minimum==f['minimum']==-8316 and rhs==f['rhs']==-1500979 and minimum>rhs
out={'PASS':True,'geometry':'independent literal deletion, no worker imports','root_required_receiver_dependency_sha256':prior['certificate_sha256'],'conditional_path':scope['cover_path'],'extra_fixed_ones':scope['extra_fixed_ones'],'conditional_dual_numerator':cost,'scale':M,'gap':gap,'forced_words':len(fixed),'forced_equalities':len(eq),'CG_nodes':len(cg),'global_rows':len(rows),'minimum':minimum,'rhs':rhs,'strict_Farkas_margin':minimum-rhs,'files_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in('model.json','dual.json','equations.json','face_farkas.json')},'seconds':time.monotonic()-start,'scope':'Excludes320 only for normalized codes on receiver-parent path[(3,5),(7,263)] plus selected771; no global319 proof'}
(H/'check_deletion_forced_face263_771_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
