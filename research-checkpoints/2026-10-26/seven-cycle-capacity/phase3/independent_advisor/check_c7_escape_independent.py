import json,itertools,hashlib,time
from pathlib import Path
from collections import Counter
st=time.time();root=Path(__file__).resolve().parents[1];path=root/'physical_iteration/new_367_core_escape.json';raw=path.read_bytes();d=json.loads(raw);code=d['code'];base=json.loads((root/'published/data/base_c7.json').read_text());closure=json.loads((root/'physical_iteration/private_component_closure.json').read_text());boundary=json.loads((root/'physical_iteration/first_core_boundary_certificate.json').read_text())
D=[tuple(x//7**i%7 for i in range(5))for x in range(16807)]
def profile(c):
 assert len(c)==len(set(c))==367
 hist=Counter()
 for a,b in itertools.combinations(c,2):
  v=tuple(sorted(min((x-y)%7,(y-x)%7)for x,y in zip(D[a],D[b])));assert max(v)>=2
  hist[v]+=1
 return hist
h=profile(code);H0=profile(base['I0']);HX=profile(base['X'])
assert h!=H0 and h!=HX
core=set(closure['core']);alphabet=set(closure['alphabet']);assert len(set(code)&core)==342 and len(set(code)-alphabet)==15
out={'passed':True,'sha256':hashlib.sha256(raw).hexdigest(),'size':367,'pair_checks':367*366//2,'common_core_retained':342,'outside_old377':15,'not_coordinate_dihedral_permutation_equivalent_to_I0':True,'not_coordinate_dihedral_permutation_equivalent_to_X':True,'witness_I0':next([list(k),h[k],H0[k]]for k in h.keys()|H0.keys()if h[k]!=H0[k]),'witness_X':next([list(k),h[k],HX[k]]for k in h.keys()|HX.keys()if h[k]!=HX[k]),'scope':'New physical seed, not cardinality/capacity improvement','seconds':time.time()-st}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));print('boundarykeys',boundary.keys())
