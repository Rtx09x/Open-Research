r"""Exact, bounded falsification/construction test for one supplied reservoir.

Input: JSON with disjoint independent rectangles [[fivewordset,fivewordset],...].
All coordinates use literal little-endian base7. The input is a construction,
not a requested search. Let Z be the pinned134753 code and S=Q\Z. Compute the
physical bipartite conflicts S--Z. By Konig, alpha(Z union Q)=|Z|+|S|-nu.
A Hall deficiency >=340 gives an explicit135093-or-larger physical code.

Hard limits: one CPU/1GiB/270CPU seconds, <=12 rectangles, <=150000 reservoir
words, <=6000000 edges. A stopped test is explicitly inconclusive. The default
I0-square input is a negative control diagnosing the misleading triangle gap,
not a new reservoir search.
"""
from physical_graph import *
def nh(S):
 return {encode(tuple((a+b)%7 for a,b in zip(digits(v),delta))) for v in S for delta in itertools.product((-1,0,1),repeat=5)}
from collections import defaultdict,deque
import gzip,time,resource,os,sys,argparse
def run():
 ap=argparse.ArgumentParser();ap.add_argument('--recipe');ap.add_argument('--output',default='reservoir_escape_control.json.gz');args=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});sys.setrecursionlimit(300000);start=time.monotonic()
 d=json.loads(BASE.read_text());I=set(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};B=I-R;xh=X&nh(H);xv=X&nh(V);x0=X-xh-xv
 zblocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)]
 recipe=json.loads(Path(args.recipe).read_text()) if args.recipe else {'name':'I0_square_negative_control','rectangles':[[sorted(I),sorted(I)]]}
 assert 1<=len(recipe['rectangles'])<=12
 blocks=[]
 for a,b in recipe['rectangles']:
  assert len(a)==len(set(a)) and len(b)==len(set(b)) and len(a)<=367 and len(b)<=367
  assert all(isinstance(v,int) and 0<=v<16807 for v in a+b);blocks.append((set(a),set(b)))
 # Verify factor independence and rectangle separation, without trusting labels.
 factors={tuple(sorted(a)) for pair in blocks+zblocks for a in pair}
 for a in factors:assert independent(a)
 def sep(a,b):return all(not confusable(x,y) for x in a for y in b)
 for rects in [blocks,zblocks]:
  assert all(sep(a,c) or sep(b,e) for (a,b),(c,e) in itertools.combinations(rects,2))
 Z=sorted(set().union(*(set(itertools.product(a,b)) for a,b in zblocks)));zs=set(Z);assert len(Z)==134753
 Q=set().union(*(set(itertools.product(a,b)) for a,b in blocks));assert len(Q)<=150000;S=sorted(Q-zs)
 alphabet={a for p in Q|zs for a in p};near={a:nh([a]) for a in alphabet};index={p:j for j,p in enumerate(Z)};rows=defaultdict(set)
 for a,b in Z:rows[a].add(b)
 types=list({tuple(sorted(v)) for v in rows.values()});ids={x:i for i,x in enumerate(types)};rt={a:ids[tuple(sorted(v))] for a,v in rows.items()};ts=list(map(set,types));first=set(rows);an={a:sorted(near[a]&first) for a in alphabet};bn={b:[sorted(near[b]&t) for t in ts] for b in alphabet};adj=[];edges=0
 def save(out):
  out.update({'recipe':recipe,'source_base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss});(HERE/args.output).write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0));print(json.dumps({k:v for k,v in out.items() if k not in ['recipe','matching_targets','selected_outside_indices','deleted_Z_indices']},indent=2))
 for p,q in S:
  nb=[index[(a,b)] for a in an[p] for b in bn[q][rt[a]]];edges+=len(nb)
  if edges>6000000 or time.monotonic()-start>230:
   save({'complete':False,'reason':'edge/time construction budget reached','reservoir_size':len(Q),'outside_size':len(S),'materialized_left':len(adj),'edges_at_stop':edges,'scope':'No impossibility or construction conclusion.'});return
  adj.append(nb)
 nl=len(S);nr=len(Z);ml=[-1]*nl;mr=[-1]*nr;dist=[]
 def bfs():
  nonlocal dist
  dist=[-1]*nl;q=deque()
  for u in range(nl):
   if ml[u]<0:dist[u]=0;q.append(u)
  found=False
  while q:
   u=q.popleft()
   for v in adj[u]:
    w=mr[v]
    if w<0:found=True
    elif dist[w]<0:dist[w]=dist[u]+1;q.append(w)
  return found
 def dfs(u):
  for v in adj[u]:
   w=mr[v]
   if w<0 or (dist[w]==dist[u]+1 and dfs(w)):ml[u]=v;mr[v]=u;return True
  dist[u]=-1;return False
 while bfs():
  for u in range(nl):
   if ml[u]<0:dfs(u)
  if time.monotonic()-start>240:
   save({'complete':False,'reason':'matching time budget reached','reservoir_size':len(Q),'outside_size':nl,'edges':edges,'matching_targets':ml,'scope':'Partial matching is only an upper-bound witness, no optimality claim.'});return
 # Exact complementary Hall witness and matching certify optimality, not floats.
 L={u for u in range(nl) if ml[u]<0};RR=set();q=deque(L)
 while q:
  u=q.popleft()
  for v in adj[u]:
   if v not in RR:
    RR.add(v);w=mr[v];assert w>=0
    if w not in L:L.add(w);q.append(w)
 matched=sum(v>=0 for v in ml);assert len({v for v in ml if v>=0})==matched
 assert all(v in adj[u] for u,v in enumerate(ml) if v>=0)
 assert (RR==set().union(*(set(adj[u]) for u in L))) if L else not RR
 delta=nl-matched;assert delta==len(L)-len(RR)
 # Q and Z are independently checked; deleting all neighbors of selected S
 # proves the resulting code is independent without quadratic10-word replay.
 maximum=nr+delta
 save({'complete':True,'reservoir_size':len(Q),'outside_size':nl,'edges':edges,'matching_targets':ml,'selected_outside_indices':sorted(L),'deleted_Z_indices':sorted(RR),'matching_size':matched,'hall_deficiency':delta,'maximum_code_size_in_union':maximum,'target135093_reached':maximum>=135093,'scope':'Exact independent-set size and clique-cover capacity in Z union this single supplied independent reservoir. No claim about other reservoirs or global C7.'})
if __name__=='__main__':run()
