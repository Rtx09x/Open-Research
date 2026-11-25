"""Exact completeness/Hall audit, reusing only own literal reservoir reconstruction."""
from pathlib import Path
from collections import defaultdict,Counter
from itertools import product
import json,gzip,hashlib,time
H=Path(__file__).resolve().parent
ns={'__file__':str(H/'check_c7_multireservoir_independent.py')}
exec((H/'check_c7_multireservoir_independent.py').read_text().split("out={'PASS'")[0],ns)
start=time.monotonic();W=ns['W'];cp=W/'physical_iteration/multireservoir_hall_diagnosis.json.gz';raw=cp.read_bytes();j=json.loads(gzip.decompress(raw))
Z,C,rects,cf,cf10,second,ct,I=[ns[k] for k in ('Z','C','rects','cf','cf10','second','ct','I')]
assert j['parent_certificate_sha256']==hashlib.sha256(ns['raw']).hexdigest()
assert j['core_words']==[list(p) for p in C] and j['core_attachment_targets']==ct
zindex={p:i for i,p in enumerate(Z)}
# Enumerate EVERY Z neighbor from the seven exact rectangles, avoiding graph-size quadratic scanning.
sets={frozenset(a) for rect in rects for a in rect}
near={(u,a):[v for v in a if cf(u,v)] for u in I for a in sets}
N=[];back=defaultdict(set)
for i,(x,y) in enumerate(C):
 candidates={zindex[p] for a,b in rects for p in product(near[x,frozenset(a)],near[y,frozenset(b)])}
 eligible={q for q in candidates if q not in second or cf10((x,y),second[q])}
 assert sorted(candidates)==j['unfiltered_cliques'][i] and sorted(eligible)==j['compatible_cliques'][i]
 N.append(eligible)
 for q in eligible:back[q].add(i)
left=set(j['hall_left']);right=set(j['hall_right']);assert len(left)==4272 and len(right)==3992
assert set().union(*(N[i] for i in left))==right
assert len(C)-(len(left)-len(right))==5016==sum(q>=0 for q in ct)
zeros=[i for i,a in enumerate(N) if not a];assert zeros==j['zero_attachment_core_indices'] and len(zeros)==30
# Independent connected-component traversal on the exact bipartite graph.
remaining=set(range(len(C)));components=[]
while remaining:
 L={min(remaining)};Q=set();front=set(L)
 while front:
  qq=set().union(*(N[i] for i in front))-Q;Q|=qq
  ll=set().union(*(back[q] for q in qq))-L if qq else set();L|=ll;front=ll
 remaining-=L
 matches=sum(ct[i]>=0 for i in L)
 components.append((frozenset(L),frozenset(Q),matches,len(L)-matches))
assert len(components)==203
stored={(frozenset(r['left']),frozenset(r['right']),r['matching'],r['deficiency']) for r in j['components']}
assert set(components)==stored
large=sorted((de for l,r,m,de in components if len(l)>10),reverse=True)
assert large==[184,22,22,18]
out={'PASS':True,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'left':len(C),'matching':5016,'hall_left':len(left),'complete_hall_neighbors':len(right),'deficiency':280,'isolated_left':30,'nonisolated_deficit':250,'components':203,'large_component_deficiencies':large,'seconds':time.monotonic()-start,'scope':'Optimal core attachment only for the fixed Z/T(Z) pairing; not optimal global clique cover or actual independence number'}
(H/'check_c7_attachment_hall_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
