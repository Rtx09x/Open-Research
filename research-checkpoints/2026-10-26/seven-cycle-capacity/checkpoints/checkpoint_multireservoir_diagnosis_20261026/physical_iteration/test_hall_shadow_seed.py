"""One exact diagnostic: force the audited Hall core set, then optimize T(Z).
This is a fixed-seed construction test, not a reservoir sweep or global bound.
"""
from physical_graph import *
def nh(S):
 return {encode(tuple((a+b)%7 for a,b in zip(digits(v),delta))) for v in S for delta in itertools.product((-1,0,1),repeat=5)}
from collections import defaultdict,deque
import gzip,time,resource,os,sys
def run():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});sys.setrecursionlimit(300000);start=time.monotonic()
 d=json.loads(BASE.read_text());I=set(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};B=I-R;xh=X&nh(H);xv=X&nh(V);x0=X-xh-xv;blocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)]
 Z=sorted(set().union(*(set(itertools.product(a,b)) for a,b in blocks)));zs=set(Z);T={(transform(a),transform(b)) for a,b in Z};raw=(HERE/'multireservoir_hall_diagnosis.json.gz').read_bytes();diag=json.loads(gzip.decompress(raw));U={tuple(diag['core_words'][c]) for c in diag['hall_left']};assert len(U)==4272 and U<=set(itertools.product(I,I)) and not U&zs and not U&T
 alphabet={a for p in zs|T|U for a in p};near={a:nh([a]) for a in alphabet};index={p:j for j,p in enumerate(Z)}
 def structure(points):
  rows=defaultdict(set)
  for a,b in points:rows[a].add(b)
  types=list({tuple(sorted(v)) for v in rows.values()});ids={x:i for i,x in enumerate(types)};rt={a:ids[tuple(sorted(v))] for a,v in rows.items()};ts=list(map(set,types));first=set(rows);an={a:sorted(near[a]&first) for a in alphabet};bn={b:[sorted(near[b]&t) for t in ts] for b in alphabet};return an,bn,rt
 za,zb,zr=structure(zs);ua,ub,ur=structure(U)
 def nz(p):
  a,b=p;return [index[(x,y)] for x in za[a] for y in zb[b][zr[x]]]
 D={j for p in U for j in nz(p)};assert len(D)==5248 and D==set().union(*(set(diag['unfiltered_cliques'][c]) for c in diag['hall_left']))
 # Literal separability from U, generated through its exact row-factor sets.
 def separated_U(p):
  a,b=p;return not any(ub[b][ur[x]] for x in ua[a])
 outside=sorted(T-zs);S=[p for p in outside if separated_U(p)];adj=[];edges=0
 for p in S:
  adj.append([j for j in nz(p) if j not in D]);edges+=len(adj[-1])
  assert edges<=6000000,'Explicit operational graph budget exceeded'
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
  assert time.monotonic()-start<245,'Operational time budget reached; no optimality result'
 L={u for u in range(nl) if ml[u]<0};RR=set();q=deque(L)
 while q:
  u=q.popleft()
  for v in adj[u]:
   if v not in RR:
    RR.add(v);w=mr[v];assert w>=0
    if w not in L:L.add(w);q.append(w)
 matched=sum(j>=0 for j in ml);assert len({j for j in ml if j>=0})==matched and all(j in adj[u] for u,j in enumerate(ml) if j>=0)
 assert RR==set().union(*(set(adj[u]) for u in L));assert not RR&D
 delta=nl-matched;assert delta==len(L)-len(RR)
 seed=len(Z)-len(D)+len(U);assert seed==133777;size=seed+delta
 out={'hall_diagnosis_sha256':hashlib.sha256(raw).hexdigest(),'reservoir':'T(Z)','forced_core_count':len(U),'removed_Z_count':len(D),'seed_size':seed,'outside_reservoir_before_filter':len(outside),'outside_separated_from_forced_core':len(S),'conflicting_with_forced_core':len(outside)-len(S),'additional_conflict_edges':edges,'zero_additional_cost_words':sum(not a for a in adj),'matching_targets':ml,'hall_selected_reservoir_indices':sorted(L),'hall_deleted_extra_Z_indices':sorted(RR),'matching_size':matched,'additional_hall_surplus':delta,'required_surplus_for135093':135093-seed,'shortfall':135093-size,'exact_maximum_with_forced_core':size,'target_reached':size>=135093,'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Exact optimum with all4272 prescribed core words forced, using only Z and T(Z) otherwise. Not alpha of the unrestricted simultaneous alphabet or a global capacity statement.'};(HERE/'hall_shadow_seed_control.json.gz').write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0));print(json.dumps({k:v for k,v in out.items() if k not in ['matching_targets','hall_selected_reservoir_indices','hall_deleted_extra_Z_indices']},indent=2))
if __name__=='__main__':run()
