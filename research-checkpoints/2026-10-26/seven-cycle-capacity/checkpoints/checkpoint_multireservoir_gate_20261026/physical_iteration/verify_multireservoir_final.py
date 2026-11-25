"""Minimal standard-library checker for the final135033-clique partition.

Inputs only the pinned literal base data and final matching certificate. No
other proof prelude, optimizer, proposer import or floating point is used.
"""
import json,gzip,itertools,hashlib,time,resource,os
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
BASE=P.parent/'published/data/base_c7.json'
CERT=P/'multireservoir_repaired_cover_full.json.gz'
def ds(a):return tuple((a//7**j)%7 for j in range(5))
def cf(a,b):return all((u-v)%7 in (0,1,6) for u,v in zip(ds(a),ds(b)))
def tr(a):
 a,b,c,d,e=ds(a);return (2-b)%7+7*d+49*a+343*((2-c)%7)+2401*e
def independent(a):return all(not cf(x,y) for x,y in itertools.combinations(a,2))
def separated(a,b):return all(not cf(x,y) for x in a for y in b)
def run():
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});t=time.monotonic()
 raw=BASE.read_bytes();assert hashlib.sha256(raw).hexdigest()=='2395d9ce16e068010a5f2a57f3fbfec5a607fa9272b02afd6c9e4a95fc70016b';d=json.loads(raw)
 I=set(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};B=I-R
 assert len(I)==len(X)==367 and independent(I) and independent(X)
 xh={x for x in X if any(cf(x,h) for h in H)};xv={x for x in X if any(cf(x,v) for v in V)};assert not xh&xv;x0=X-xh-xv
 blocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)]
 assert all(independent(a) and independent(b) for a,b in blocks)
 assert all(separated(a,c) or separated(b,e) for (a,b),(c,e) in itertools.combinations(blocks,2))
 Z=sorted(set().union(*(set(itertools.product(a,b)) for a,b in blocks)));zs=set(Z);assert len(Z)==134753
 tz={(tr(a),tr(b)) for a,b in Z};assert len(tz)==len(Z)
 core=set(itertools.product(I,I));S=sorted(tz-zs);C=sorted(core-(zs|tz));assert (len(core),len(S),len(C))==(134689,133729,5296)
 raw=CERT.read_bytes();o=json.loads(gzip.decompress(raw));assert o['base_recipe']=='T1'
 mt=o['reservoir_matching_targets'];ct=o['core_matching_targets'];assert len(mt)==len(S) and len(ct)==len(C)
 assert len(set(mt))==len(mt) and all(0<=j<len(Z) for j in mt)
 assert len({j for j in ct if j>=0})==sum(j>=0 for j in ct) and all(j==-1 or 0<=j<len(Z) for j in ct)
 # Cache the literal coordinate predicate, not any graph supplied by proposer.
 alphabet={a for p in core|zs|tz for a in p};near={a:{b for b in alphabet if cf(a,b)} for a in alphabet}
 def c10(a,b):return b[0] in near[a[0]] and b[1] in near[a[1]]
 cliques=[[p] for p in Z]
 for p,j in zip(S,mt):assert c10(p,Z[j]);cliques[j].append(p)
 for p,j in zip(C,ct):
  if j<0:cliques.append([p])
  else:assert all(c10(p,q) for q in cliques[j]);cliques[j].append(p)
 flat=[p for c in cliques for p in c];assert len(flat)==len(set(flat)) and set(flat)==core|zs|tz
 upper=len(cliques);assert upper==o['cover_size']==135033 and len(flat)==273778
 assert upper*10**60<3258698**10<3258841**10
 out={'PASS':True,'source_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'alphabet_size':len(flat),'clique_count':upper,'clique_size_histogram':dict(sorted(Counter(map(len,cliques)).items())),'independent_lower':len(Z),'restricted_macro_capacity_upper':upper,'normalized_rate_upper_strict':'3.258698','target135093_excluded':upper<135093,'seconds':time.monotonic()-t,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Only the simultaneous alphabet I0^2 union Z union T(Z); no global C7 upper bound and no new lower bound.'};(P/'multireservoir_final_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
