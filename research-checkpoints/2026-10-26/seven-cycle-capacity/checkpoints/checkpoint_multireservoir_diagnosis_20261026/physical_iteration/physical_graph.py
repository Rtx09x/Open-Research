"""Physical C7^5 alphabets, with published source data (see ../published/NOTICE).

All words use little-endian base seven. No abstract BPZ relation is used.
"""
import json,itertools,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'published/data/base_c7.json'
def digits(x): return tuple((x//7**j)%7 for j in range(5))
def encode(w): return sum(a*7**j for j,a in enumerate(w))
def transform(x):
 a,b,c,d,e=digits(x)
 return encode(((2-b)%7,d,a,(2-c)%7,e))
def confusable(x,y): return all((a-b)%7 in (0,1,6) for a,b in zip(digits(x),digits(y)))
def alphabets():
 d=json.loads(BASE.read_text());i=set(d['I0']);x=set(d['X'])
 return i,x,i|x,i|x|set(map(transform,i)),i|x|set(map(transform,i|x))
def graph(vertices):
 vs=sorted(vertices);ws=list(map(digits,vs));adj=[set() for _ in vs]
 for i,x in enumerate(ws):
  for j in range(i):
   if all((a-b)%7 in (0,1,6) for a,b in zip(x,ws[j])):
    adj[i].add(j);adj[j].add(i)
 return vs,adj
def maximal_cliques(adj):
 out=[]
 def rec(r,p,x):
  if not p and not x: out.append(sorted(r));return
  u=max(p|x,key=lambda t:len(p&adj[t]))
  for v in sorted(p-adj[u]):
   rec(r+[v],p&adj[v],x&adj[v]);p.remove(v);x.add(v)
 rec([],set(range(len(adj))),set())
 return out
def matching(left,right):
 left=sorted(left);right=set(right);arcs={a:[b for b in sorted(right) if confusable(a,b)] for a in left};match={}
 def dfs(a,seen):
  for b in arcs[a]:
   if b in seen:continue
   seen.add(b)
   if b not in match or dfs(match[b],seen):match[b]=a;return True
  return False
 for a in left: assert dfs(a,set()),('matching failure',a)
 return sorted([a,b] for b,a in match.items())
def independent(vs): return all(not confusable(a,b) for a,b in itertools.combinations(vs,2))
def audit_base_and_partition():
 i,x,u2,u3,u4=alphabets()
 assert len(i)==len(x)==367 and independent(i) and independent(x)
 assert (len(i&x),len(u2),len(u3),len(u4))==(32,702,704,1009)
 assert u3-u2=={6494,13358}
 cycles=[[6494,8888,6773,6828,4092],[13358,13065,11062,10677,13364]]
 used=set(sum(cycles,[]));pairs=matching(i-x-used,x-i-used)
 assert len(pairs)==331
 for c in cycles: assert len(c)==len(set(c))==5 and all(confusable(c[j],c[(j+1)%5]) for j in range(5))
 components=[[a] for a in sorted(i&x)]+pairs+cycles
 assert len(sum(components,[]))==len(set(sum(components,[])))==704
 assert set(sum(components,[]))==u3
 two_pairs=matching(i-x,x-i)
 assert len(two_pairs)==335
 vs,adj=graph(u4);cl=maximal_cliques(adj)
 assert sum(map(len,adj))//2==5394 and len(cl)==3698
 cert={'source_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'I0':sorted(i),'X':sorted(x),'U2_pairs':two_pairs,'singletons':sorted(i&x),'U3_pairs':pairs,'U3_cycles':cycles,'U4':vs,'U4_edges':[[a,b] for a in range(len(vs)) for b in sorted(adj[a]) if a<b],'U4_maximal_cliques':cl}
 (HERE/'independent_physical_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
 info={'I0':len(i),'X':len(x),'U2_size':len(u2),'U2_matching':len(two_pairs),'U3_size':len(u3),'U3_pairs':len(pairs),'U3_cycles':cycles,'U3_theta_upper':'363 + 2 sqrt(5)','U3_below_target':True,'U4_vertices':len(vs),'U4_edges':len(cert['U4_edges']),'U4_maximal_cliques':len(cl),'U4_max_clique_size':max(map(len,cl))}
 # Exact rational comparison: sqrt(5)<9/4, hence bound<367.5<target^5.
 assert 5*16<81 and 2*3258841**5>735*10**30
 (HERE/'independent_physical_audit.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__': audit_base_and_partition()
