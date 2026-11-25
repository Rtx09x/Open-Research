"""No-proposer-import, literal checker for the fixed Hall-core control.
Checks exact complete candidate filtering, a matching upper and Hall lower.
"""
import json,gzip,itertools,time,hashlib,resource,os
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
P=Path(__file__).resolve().parent
@lru_cache(None)
def ds(v):return tuple((v//7**i)%7 for i in range(5))
@lru_cache(None)
def cf(a,b):return all((x-y)%7 in (0,1,6) for x,y in zip(ds(a),ds(b)))
def c10(p,q):return cf(p[0],q[0]) and cf(p[1],q[1])
def tr(v):
 a,b,c,d,e=ds(v);return (2-b)%7+7*d+49*a+343*((2-c)%7)+2401*e
def ind(a):return all(not cf(x,y) for x,y in itertools.combinations(a,2))
def sep(a,b):return all(not cf(x,y) for x in a for y in b)
def run():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});start=time.monotonic()
 d=json.loads((P.parent/'published/data/base_c7.json').read_text());I=set(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};B=I-R;assert len(I)==367 and ind(I)
 xh={x for x in X if any(cf(x,h) for h in H)};xv={x for x in X if any(cf(x,v) for v in V)};assert not xh&xv;x0=X-xh-xv;blocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)]
 assert all(ind(a) and ind(b) for a,b in blocks);assert all(sep(a,c) or sep(b,e) for (a,b),(c,e) in itertools.combinations(blocks,2))
 Z=sorted(set().union(*(set(itertools.product(a,b)) for a,b in blocks)));zs=set(Z);T={(tr(a),tr(b)) for a,b in Z};index={p:i for i,p in enumerate(Z)};assert len(Z)==len(T)==134753
 raw=(P/'hall_shadow_seed_control.json.gz').read_bytes();o=json.loads(gzip.decompress(raw));hraw=(P/'multireservoir_hall_diagnosis.json.gz').read_bytes();assert hashlib.sha256(hraw).hexdigest()==o['hall_diagnosis_sha256'];h=json.loads(gzip.decompress(hraw));U={tuple(h['core_words'][i]) for i in h['hall_left']};assert len(U)==4272 and U<=set(itertools.product(I,I)) and not U&zs and not U&T
 # Complete five-coordinate factor-neighborhood intersections, not a sampled
 # outside graph. Reconstruct exact conflict neighborhoods of every U point.
 alphabet={v for p in zs|T|U for v in p};factors={frozenset(a) for rect in blocks for a in rect};near={(v,a):[w for w in a if cf(v,w)] for v in alphabet for a in factors}
 def nz(p):
  x,y=p;return {index[q] for a,b in blocks for q in itertools.product(near[x,frozenset(a)],near[y,frozenset(b)])}
 D=set().union(*(nz(p) for p in U));assert len(D)==5248
 rows=defaultdict(set)
 for x,y in U:rows[x].add(y)
 rowtypes={frozenset(y) for y in rows.values()};rown={v:[x for x in rows if cf(v,x)] for v in alphabet};second={(v,a):any(cf(v,y) for y in a) for v in alphabet for a in rowtypes}
 def admissible(p):return not any(second[p[1],frozenset(rows[x])] for x in rown[p[0]])
 outside=sorted(T-zs);S=[p for p in outside if admissible(p)];assert len(S)==112769 and len(outside)-len(S)==20960
 mt=o['matching_targets'];assert len(mt)==len(S);used=[j for j in mt if j>=0];assert len(used)==len(set(used))==112718
 assert all(j==-1 or (0<=j<len(Z) and j not in D and c10(p,Z[j])) for p,j in zip(S,mt))
 selected=set(o['hall_selected_reservoir_indices']);removed=set(o['hall_deleted_extra_Z_indices']);assert all(0<=i<len(S) for i in selected)
 complete_neighbors=set().union(*(nz(S[i])-D for i in selected));assert complete_neighbors==removed and len(selected)-len(removed)==51
 seed=len(Z)-len(D)+len(U);upper=seed+len(S)-len(used);lower=seed+len(selected)-len(removed);assert seed==133777 and upper==lower==o['exact_maximum_with_forced_core']==133828
 # All selected Q points are mutually separated, by the checked Z construction
 # and the explicit automorphism T; each is separated from U by full filtering.
 nonzero=[i for i in sorted(selected) if nz(S[i])-D];assert len(nonzero)==3
 out={'PASS':True,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'seed_size':seed,'admissible_reservoir_words':len(S),'matching_size':len(used),'hall_selected':len(selected),'hall_deleted':len(removed),'hall_surplus':51,'zero_cost_selected':len(selected)-len(nonzero),'nonzero_selected_words':[S[i] for i in nonzero],'deleted_Z_words':[Z[j] for j in sorted(removed)],'exact_forced_core_maximum':upper,'required_surplus':1316,'target_shortfall':1265,'seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Only codes retaining all prescribed4272 core words and using Z/T(Z) otherwise. Not the unconstrained joint alphabet or global C7.'};(P/'hall_shadow_seed_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
