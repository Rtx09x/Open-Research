from pathlib import Path
from itertools import combinations, product
import json, re, sys, hashlib, time, resource, os, math, argparse
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3)); resource.setrlimit(resource.RLIMIT_CPU,(285,290))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});sys.set_int_max_str_digits(0)
ap=argparse.ArgumentParser();ap.add_argument('--track-root',type=Path,default=Path(__file__).resolve().parents[1]);args=ap.parse_args()
T=time.monotonic(); P=args.track_root.resolve(); OUT=Path(__file__).parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(P/'published'))
from shannon.construction import load_certificates,theorem2
led=load_certificates(recomputed=True);original=theorem2(led)
base=json.loads((P/'terminal_recycled_base.json').read_text()); w=dict(zip('BNADOHV',base['input_vector']))
# Locate the upstream theorem's vector by value, not by assumed dictionary name.
assert base['input_vector']==list(original['n25'])
# Literal upstream Lean terminal list. The separation relation is Definition 4.
text=(P/'published/upstream/TerminalCodes.lean').read_text().split('def C4a :',1)[1].split('def K4a :',1)[0]
K={''.join(re.findall('[BNADOHV]',x)) for x in re.findall(r'!\[([^]]+)\]',text)}
assert len(K)==49
edges={'BO','BH','BV','NA','ND','NO','NH','NV','AD','AH','DV'}; E={frozenset(x) for x in edges}
def sep(x,y):return any(frozenset(z) in E for z in zip(x,y))
def independent(S):return all(sep(a,b) for a,b in combinations(S,2))
R={'NHNH','VNVN'};Q={'NVNV','HNHN'};X={x[:2]+x[3]+x[2] for x in K}
assert independent(K) and independent(X) and independent(Q)
assert R<=K and not Q&K
for r,q in [('NHNH','NVNV'),('VNVN','HNHN')]:assert {x for x in K if not sep(x,q)}=={r}
noQ={x for x in X if all(sep(x,q) for q in Q)};noR={x for x in X if all(sep(x,r) for r in R)}
assert noQ|noR==X
F={'B':K-R,'N':noQ&noR,'A':noQ-noR,'D':noR-noQ,'O':R,'H':Q,'V':R}
assert [len(F[a]) for a in 'BNADOHV']==[47,41,4,4,2,2,2]
checks=0
for a in F:
 assert independent(F[a]);assert F[a]=={''.join(x) for x in base['families'][a]}
 for b in F:
  if frozenset((a,b)) in E:
   for x,y in product(F[a],F[b]):assert sep(x,y);checks+=1
U={a:sum(math.prod(w[c] for c in word) for word in F[a]) for a in F}
assert list(U.values())==base['vector']
M=sum(math.prod(w[c] for c in word) for word in K);assert M==original['M']
rule={'B':['BB','HD','VA','DV','AH'],'N':['NN','AA','AD','DA','DD'],'A':['AN','ND'],'D':['DN','NA'],'O':['ON','NO'],'H':['HN','NV'],'V':['VN','NH']}
for a in rule:
 assert independent(rule[a])
 for b in rule:
  if frozenset((a,b)) in E:assert all(sep(x,y) for x,y in product(rule[a],rule[b]))
def f(v,z):return {a:sum(v[x]*z[y] for x,y in rule[a]) for a in rule}
U2=f(U,U);p=w['N']**2*w['H']**2
assert U2['B']+U2['O']==M*M+4*p*p
U8=U
for _ in range(8):U8=f(U8,U8)
M8=U8['B']+U8['O'];V=f(U,U2)
for _ in range(9):V=f(V,V)
Mopt=V['B']+V['O'];assert Mopt>M8**6>M**1536
for filename,vec,n,r,d in [('recycled_terminal_certificate.json',U8,128000,3258832624209610237867099424184,10**30),('optimized_recycle_certificate.json',V,768000,3258832624232849476,10**18)]:
 c=json.loads((P/filename).read_text());assert c['dimension']==n and c['M']==vec['B']+vec['O'];assert c['final_vector']==list(vec.values())
 assert pow(r,n)<=c['M']*pow(d,n)<pow(r+1,n)
print(json.dumps({'status':'PASS','upstream_five_certificates_recomputed':True,'primary_Lean_K4a':True,'family_cross_pairs_checked':checks,'fresh_recipe_integer_root_checks':[128000,768000],'strict_gain_checked':True,'source_theorem_dependency':'Tandon theorem2 implementation replayed, not a new independent proof or Lean kernel replay','seconds':time.monotonic()-T,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
