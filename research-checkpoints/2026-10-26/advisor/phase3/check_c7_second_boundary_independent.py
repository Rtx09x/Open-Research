"""Exact independent cover/arc-certificate/transversal audit; no worker imports."""
import json,hashlib,itertools,time
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parents[2]/'seven-cycle-capacity'/'phase3'/'physical_iteration'
T=Path(__file__).resolve().parent
start=time.monotonic()
cp=P/'second_core_boundary_capacity_cover.json'; dp=P/'second_boundary_maxima_classification.json'
c=json.loads(cp.read_text()); d=json.loads(dp.read_text())
def digits(x):
 a=[]
 for _ in range(5):a.append(x%7);x//=7
 return tuple(a)
D=[digits(x) for x in range(7**5)]
def adjacent(a,b):return all((x-y)%7 in {0,1,6} for x,y in zip(D[a],D[b]))
core=json.loads((P/'private_component_closure.json').read_text())['core']
U={v for v in range(7**5) if sum(adjacent(v,w) for w in core)<=2}
assert U==set(c['alphabet']) and len(U)==842
C=[set(x['vertices']) for x in c['terms']]
assert len(C)==367 and all(x['weight']==1 for x in c['terms']) and c['denominator']==1
assert set.union(*C)==U and all(adjacent(a,b) for S in C for a,b in itertools.combinations(S,2))
m=Counter(v for S in C for v in S); excluded={v for v in U if m[v]>1}
assert excluded==set(d['multi_covered_forbidden'])
A=[S-excluded for S in C]
for round in d['arc_consistency_trace']:
 bad=set()
 for row in round:
  v=row['word']; k=row['incompatible_entire_clique']
  assert v in set.union(*A) and v not in A[k] and A[k]
  assert all(adjacent(v,w) for w in A[k])
  bad.add(v)
 for S in A:S.difference_update(bad);assert S
left=set.union(*A)
adj={v:{w for w in left if w!=v and adjacent(v,w)} for v in left}
# Discover independent blocks from surviving clique domains and physical conflicts.
owner={v:i for i,S in enumerate(A) for v in S}; assert len(owner)==sum(map(len,A))
near=[set() for S in A]
for v in left:
 for w in adj[v]:
  if owner[v]!=owner[w]:near[owner[v]].add(owner[w])
parts=[];todo=set(range(len(A)))
while todo:
 seen={todo.pop()};stack=list(seen)
 while stack:
  i=stack.pop();new=near[i]&todo;todo-=new;seen|=new;stack.extend(new)
 parts.append(sorted(seen))
nodes=0
# Exhaustive independent transversals, with forward compatibility filtering.
def enumerate_part(ids):
 global nodes
 solutions=[]
 def rec(dom,picked):
  global nodes
  nodes+=1;assert nodes<100000
  if not dom:solutions.append(tuple(sorted(picked)));return
  i=min(dom,key=lambda j:len(dom[j]))
  for v in sorted(dom[i]):
   child={j:S-adj[v] for j,S in dom.items() if j!=i}
   if all(child.values()):rec(child,picked+[v])
 rec({j:set(A[j]) for j in ids},[])
 return solutions
count=1;support=set();sizes=[];counts=[]
for ids in parts:
 sols=enumerate_part(ids);assert sols
 assert len(set(sols))==len(sols)
 count*=len(sols);support.update(itertools.chain.from_iterable(sols));sizes.append(len(ids));counts.append(len(sols))
assert count==486 and len(support)==392 and support==set(d['support_of_all_maximum_codes'])
# Recover physical support graph, without trusting reported graph decomposition.
Sadj={v:adj[v]&support for v in support};todo=set(support);shapes=[]
while todo:
 seen={todo.pop()};stack=list(seen)
 while stack:
  v=stack.pop();new=Sadj[v]&todo;todo-=new;seen|=new;stack.extend(new)
 degrees=sorted(len(Sadj[v]) for v in seen);shapes.append((len(seen),tuple(degrees)))
assert Counter(n for n,_ in shapes)=={1:342,4:5,30:1}
assert all(deg==((0,) if n==1 else (1,1,2,2) if n==4 else (2,)*30) for n,deg in shapes)
out={'passed':True,'cover_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'classification_sha256':hashlib.sha256(dp.read_bytes()).hexdigest(),'alphabet_size':842,'maximum_size':367,'maximum_code_count':count,'maximum_support_size':392,'graph':'342 isolated vertices + five P4 + one C30','nodes':nodes,'seconds':time.monotonic()-start,'scope':'Exact within the core-conflict-at-most-two alphabet, not global C7^5 or capacity improvement.'}
(T/'c7_second_boundary_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
