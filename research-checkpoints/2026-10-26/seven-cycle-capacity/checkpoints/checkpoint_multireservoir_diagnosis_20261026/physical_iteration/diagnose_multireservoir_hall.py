"""Exact fixed-pairing Hall diagnosis of the280 residual core singleton gap.
This proves maximum attachment for the final pairing, not globally best cover.
"""
from physical_graph import *
def nh(S):
 return {encode(tuple((a+b)%7 for a,b in zip(digits(v),delta))) for v in S for delta in itertools.product((-1,0,1),repeat=5)}
from collections import defaultdict,deque,Counter
import gzip,time,resource,os
def run():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});start=time.monotonic()
 d=json.loads(BASE.read_text());I=set(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};B=I-R;xh=X&nh(H);xv=X&nh(V);x0=X-xh-xv
 blocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)];Z=sorted(set().union(*(set(itertools.product(a,b)) for a,b in blocks)));zs=set(Z);T={(transform(a),transform(b)) for a,b in Z};S=sorted(T-zs);C=sorted(set(itertools.product(I,I))-(T|zs));raw=(HERE/'multireservoir_repaired_cover_full.json.gz').read_bytes();cert=json.loads(gzip.decompress(raw));mt=cert['reservoir_matching_targets'];cm=cert['core_matching_targets'];partner=[None]*len(Z);matched_core={j:c for c,j in enumerate(cm) if j>=0}
 for p,j in zip(S,mt):assert partner[j] is None;partner[j]=p
 alphabet={a for p in zs|T|set(C) for a in p};near={a:nh([a]) for a in alphabet}
 def cf(a,b):return b[0] in near[a[0]] and b[1] in near[a[1]]
 index={p:j for j,p in enumerate(Z)};rows=defaultdict(set)
 for a,b in Z:rows[a].add(b)
 types=list({tuple(sorted(v)) for v in rows.values()});ids={x:i for i,x in enumerate(types)};rt={a:ids[tuple(sorted(v))] for a,v in rows.items()};ts=list(map(set,types));first=set(rows);an={a:sorted(near[a]&first) for a in alphabet};bn={b:[sorted(near[b]&t) for t in ts] for b in alphabet};adj=[];original=[];deleted=[];back=defaultdict(list)
 for c,(p,q) in enumerate(C):
  cand=sorted(index[(a,b)] for a in an[p] for b in bn[q][rt[a]]);ok=[j for j in cand if partner[j] is None or cf((p,q),partner[j])];original.append(cand);adj.append(ok);deleted.append([j for j in cand if j not in ok])
  for j in ok:back[j].append(c)
 assert all(j in adj[c] for c,j in enumerate(cm) if j>=0)
 L={c for c,j in enumerate(cm) if j<0};RR=set();queue=deque(L)
 while queue:
  c=queue.popleft()
  for j in adj[c]:
   if j not in RR:
    RR.add(j);assert j in matched_core,'Augmenting path contradicts maximal final attachment';v=matched_core[j]
    if v not in L:L.add(v);queue.append(v)
 assert RR==set().union(*(set(adj[c]) for c in L));assert len(L)-len(RR)==280
 # Each connected component contributes its exact matching deficiency.
 unseen=set(range(len(C)));components=[]
 while unseen:
  c=min(unseen);lc={c};rc=set();unseen.remove(c);queue=deque([c])
  while queue:
   c=queue.popleft()
   for j in adj[c]:
    if j in rc:continue
    rc.add(j)
    for v in back[j]:
     if v in unseen:unseen.remove(v);lc.add(v);queue.append(v)
  matched=sum(cm[c]>=0 for c in lc);components.append({'left':sorted(lc),'right':sorted(rc),'matching':matched,'deficiency':len(lc)-matched,'edge_count':sum(len(adj[c]) for c in lc)})
 histogram=Counter((len(r['left']),len(r['right']),r['deficiency']) for r in components)
 zero=[c for c,a in enumerate(adj) if not a]
 failures=Counter()
 for c in zero:
  p,q=C[c]
  for j in original[c]:
   t=partner[j];assert t is not None
   failures[(int(t[0] not in near[p]),int(t[1] not in near[q]))]+=1
 def classify(p):return ('R' if p[0] in R else 'B')+('R' if p[1] in R else 'B')
 out={'parent_certificate_sha256':hashlib.sha256(raw).hexdigest(),'core_words':C,'core_attachment_targets':cm,'compatible_cliques':adj,'unfiltered_cliques':original,'hall_left':sorted(L),'hall_right':sorted(RR),'maximum_attachment':len(C)-len(L)+len(RR),'hall_deficiency':len(L)-len(RR),'zero_attachment_core_indices':zero,'zero_attachment_type_counts':dict(Counter(classify(C[c]) for c in zero)),'zero_attachment_pair_blocking_halves':{str(k):v for k,v in failures.items()},'hall_type_counts':dict(Counter(classify(C[c]) for c in L)),'attachment_degree_histogram':dict(Counter(map(len,adj))),'unfiltered_degree_histogram':dict(Counter(map(len,original))),'components':components,'component_histogram':[[*k,v] for k,v in sorted(histogram.items())],'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Exact maximum core attachment for the fixed final Z-to-T(Z) pairing. Does not prove optimal clique cover or absence of an improving independent code.'}
 (HERE/'multireservoir_hall_diagnosis.json.gz').write_bytes(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0));print(json.dumps({k:v for k,v in out.items() if k not in ['core_words','core_attachment_targets','compatible_cliques','unfiltered_cliques','hall_left','hall_right','zero_attachment_core_indices','components','component_histogram']},indent=2));print('component_histogram',json.dumps(out['component_histogram']))
if __name__=='__main__':run()
