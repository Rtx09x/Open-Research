"""Independent literal triple-clique partition check; only base arrays and final certificate."""
from pathlib import Path
from itertools import combinations,product
from functools import lru_cache
import gzip,json,hashlib,time,resource
start=time.monotonic();W=Path('/workspace/shared/research-active/seven-cycle-capacity')
bp=W/'published/data/base_c7.json';cp=W/'physical_iteration/multireservoir_repaired_cover_full.json.gz'
b=json.loads(bp.read_text());raw=cp.read_bytes();c=json.loads(gzip.decompress(raw))
assert hashlib.sha256(raw).hexdigest()=='1560f166ec9f804319b1713c7f686b23d17d8fb91f5630db9abb96c6c079c4a3'
@lru_cache(None)
def digits(v):
 out=[]
 for _ in range(5):v,r=divmod(v,7);out.append(r)
 assert v==0;return out
@lru_cache(None)
def cf(a,b):return all((x-y)%7 in(0,1,6) for x,y in zip(digits(a),digits(b)))
def ind(a):assert all(not cf(x,y) for x,y in combinations(a,2))
def separated(a,b):return all(not cf(x,y) for x,y in product(a,b))
def tr(v):
 a,b,c,d,e=digits(v);return sum((x%7)*7**j for j,x in enumerate((2-b,d,a,2-c,e)))
def cf10(p,q):return cf(p[0],q[0]) and cf(p[1],q[1])
I=set(b['I0']);X=set(b['X']);H=set(b['PH']);V=set(b['PV']);R={r for r,q in b['private_pairs']}
assert len(I)==367 and R<=I;ind(I);ind(X)
xh={x for x in X if any(cf(x,h) for h in H)};xv={x for x in X if any(cf(x,v) for v in V)}
assert not xh&xv;xn=X-xh-xv
rects=[(I-R,I-R),(R,xn),(H,xh),(V,xv),(xn,R),(xh,V),(xv,H)]
for a,b in rects:ind(a);ind(b)
for (a,b),(d,e) in combinations(rects,2):assert separated(a,d) or separated(b,e)
Z=set().union(*(set(product(a,b)) for a,b in rects));assert len(Z)==134753
T={(tr(a),tr(b)) for a,b in Z};assert len(T)==len(Z)
# T is a coordinate permutation plus C7 reflections/translations, an automorphism.
core=set(product(I,I));S=sorted(T-Z);C=sorted(core-(Z|T));Z=sorted(Z)
assert len(S)==133729 and len(C)==5296 and len(core|set(Z)|T)==273778
mt=c['reservoir_matching_targets'];ct=c['core_matching_targets'];assert len(mt)==len(S) and len(ct)==len(C)
assert len(set(mt))==len(mt) and all(0<=j<len(Z) for j in mt)
second={}
for p,j in zip(S,mt):assert cf10(p,Z[j]);second[j]=p
attached=set();singletons=0;triples=0
for p,j in zip(C,ct):
 if j<0:assert j==-1;singletons+=1;continue
 assert 0<=j<len(Z) and j not in attached;attached.add(j)
 assert cf10(p,Z[j])
 if j in second:assert cf10(p,second[j]);triples+=1
assert len(attached)==5016 and singletons==280
upper=len(Z)+singletons;assert upper==c['cover_size']==135033
assert upper*10**60<3258841**10
out={'PASS':True,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'base_sha256':hashlib.sha256(bp.read_bytes()).hexdigest(),'alphabet':273778,'reservoir_outside':len(S),'core_outside':len(C),'core_attached':len(attached),'core_singletons':singletons,'triple_cliques':triples,'partition_size':upper,'known_independent_lower':134753,'all_macro_lengths_capacity_upper':upper,'target_3_258841_excluded':True,'scope':'Only alphabet I0^2 union Z union T(Z); no global capacity bound, no new lower bound, exactalpha not determined','seconds':time.monotonic()-start,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
