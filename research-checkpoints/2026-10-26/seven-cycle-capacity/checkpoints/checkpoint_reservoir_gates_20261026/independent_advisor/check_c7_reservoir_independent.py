"""Independent literal-coordinate clique partition audit; no worker imports."""
from pathlib import Path
from itertools import combinations,product
from functools import lru_cache
import gzip,json,hashlib,time
start=time.time();W=Path('/workspace/shared/research-active/seven-cycle-capacity');p=W/'physical_iteration/reservoir_orbit_compact.json.gz';raw=p.read_bytes();o=json.loads(gzip.decompress(raw));base=W/'published/data/base_c7.json';assert hashlib.sha256(base.read_bytes()).hexdigest()==o['source_base_sha256'];baseData=json.loads(base.read_text())
@lru_cache(None)
def digits(x):
 r=[]
 for _ in range(5):x,z=divmod(x,7);r.append(z)
 assert x==0;return tuple(r)
@lru_cache(None)
def adjacent(x,y):return all(min((a-b)%7,(b-a)%7)<=1 for a,b in zip(digits(x),digits(y)))
def independent(A):assert len(A)==len(set(A)) and all(not adjacent(x,y)for x,y in combinations(A,2))
def crossclear(A,B):return not any(adjacent(x,y)for x,y in product(A,B))
def transform(x):
 a,b,c,d,e=digits(x);v=[2-b,d,a,2-c,e];return sum((z%7)*7**j for j,z in enumerate(v))
I=tuple(sorted(baseData['I0']));assert I==tuple(o['base_order']);independent(I)
X=set(baseData['X']);PH=set(baseData['PH']);PV=set(baseData['PV']);R={x[0]for x in baseData['private_pairs']};independent(X)
Xh={x for x in X if not crossclear([x],PH)};Xv={x for x in X if not crossclear([x],PV)};assert not Xh&Xv;Xn=X-Xh-Xv
logs=[];Iset=set(I)
for row in o['records']:
 A=set(row['main']);assert len(A)==367 and R<=A;independent(A)
 rectangles=[(A-R,A-R),(R,Xn),(PH,Xh),(PV,Xv),(Xn,R),(Xh,PV),(Xv,PH)]
 for _ in range(row['transform_power']):rectangles=[({transform(x)for x in a},{transform(x)for x in b})for a,b in rectangles]
 for a,b in rectangles:independent(a);independent(b)
 for (a,b),(c,d) in combinations(rectangles,2):assert crossclear(a,c) or crossclear(b,d)
 Z={p for a,b in rectangles for p in product(a,b)};assert len(Z)==134753
 if row['exchanged']:
  removed={tuple(x)for x,y in baseData['exchanges']['pairs']};added={tuple(y)for x,y in baseData['exchanges']['pairs']};assert len(added)==len(removed)==8 and removed<=Z and not added&Z
  for x,y in baseData['exchanges']['pairs']:
   assert {z for z in Z if adjacent(z[0],y[0]) and adjacent(z[1],y[1])}=={tuple(x)}
  for a,c in combinations(added,2):assert not(adjacent(a[0],c[0])and adjacent(a[1],c[1]))
  Z=(Z-removed)|added
 outside=sorted((x,y)for x,y in Z if x not in Iset or y not in Iset)
 assert len(outside)==row['reservoir_count']==len(row['matching_targets'])
 used=set();cnt=0
 for (x,y),target in zip(outside,row['matching_targets']):
  if target<0:assert target==-1;continue
  assert 0<=target<367**2 and target not in used;used.add(target);cnt+=1
  i,j=divmod(target,367);assert adjacent(x,I[i])and adjacent(y,I[j])
 upper=367**2+len(outside)-cnt;assert cnt==row['matching_size'] and upper==row['maximum_code_size']==134753
 # Matched two-vertex cliques, every remaining vertex singleton; any code Z witnesses equality.
 logs.append({'name':row['name'],'alphabet':367**2+len(outside),'matching':cnt,'clique_partition':upper,'independent_lower':len(Z)})
out={'status':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'cases':logs,'seconds':time.time()-start,'scope':'Each specified I0^2 union single reservoir has exact independence number and all-macro-length Shannon capacity134753; not simultaneous3+reservoir union or full C7 capacity'}
Path(__file__).with_name('c7_reservoir_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
