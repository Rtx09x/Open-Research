"""Independent exact optimum for one forced Hall-core seed, no worker imports."""
from pathlib import Path
from itertools import product
from functools import lru_cache
import json,gzip,hashlib,time
H=Path(__file__).resolve().parent
ns={'__file__':str(H/'check_c7_multireservoir_independent.py')};exec((H/'check_c7_multireservoir_independent.py').read_text().split("out={'PASS'")[0],ns)
start=time.monotonic();W=ns['W'];Z,C,rects,cf,cf10,I=[ns[k] for k in('Z','C','rects','cf','cf10','I')];T=ns['T'];Zset=set(Z)
hp=W/'physical_iteration/multireservoir_hall_diagnosis.json.gz';hj=json.loads(gzip.decompress(hp.read_bytes()))
p=W/'physical_iteration/hall_shadow_seed_control.json.gz';raw=p.read_bytes();j=json.loads(gzip.decompress(raw))
assert hashlib.sha256(hp.read_bytes()).hexdigest()==j['hall_diagnosis_sha256']==json.loads((H/'check_c7_attachment_hall_independent.json').read_text())['certificate_sha256']
U={C[i] for i in hj['hall_left']};assert len(U)==4272 and not U&Zset and not U&T
zi={q:i for i,q in enumerate(Z)}
@lru_cache(None)
def near(v,a):return [x for x in a if cf(v,x)]
def nz(p):return {zi[q] for a,b in rects for q in product(near(p[0],frozenset(a)),near(p[1],frozenset(b)))}
D=set().union(*(nz(p) for p in U));assert len(D)==5248
I=sorted(I);ii={x:i for i,x in enumerate(I)};rowmask={}
for x,y in U:rowmask[x]=rowmask.get(x,0)|(1<<ii[y])
@lru_cache(None)
def imask(v):return sum(1<<i for i,x in enumerate(I) if cf(v,x))
def admissible(p):
 a,b=p;mask=imask(a);bm=imask(b)
 while mask:
  bit=mask&-mask;mask-=bit
  if rowmask.get(I[bit.bit_length()-1],0)&bm:return False
 return True
S=[p for p in sorted(T-Zset) if admissible(p)];assert len(S)==112769
mt=j['matching_targets'];assert len(mt)==len(S)
used=[q for q in mt if q>=0];assert len(used)==len(set(used))==112718
assert all(q==-1 or (0<=q<len(Z) and q not in D and cf10(p,Z[q])) for p,q in zip(S,mt))
sel=set(j['hall_selected_reservoir_indices']);deleted=set(j['hall_deleted_extra_Z_indices']);assert len(sel)==53 and len(deleted)==2
assert set().union(*(nz(S[i])-D for i in sel))==deleted
seed=len(Z)-len(D)+len(U);upper=seed+len(S)-len(used);lower=seed+len(sel)-len(deleted)
assert seed==133777 and lower==upper==133828 and 135093-upper==1265
out={'PASS':True,'certificate_sha256':hashlib.sha256(raw).hexdigest(),'forced_core':len(U),'complete_removed_Z_neighborhood':len(D),'admissible_T_outsiders':len(S),'matching':len(used),'Hall_selected':len(sel),'complete_Hall_deleted':len(deleted),'exact_optimum_with_forced_core':upper,'target_shortfall':135093-upper,'seconds':time.monotonic()-start,'scope':'Must retain all4272 specified core words; only Z/T(Z) otherwise. No unrestricted alphabet/capacity or global bound.'}
(H/'check_c7_hall_seed_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
