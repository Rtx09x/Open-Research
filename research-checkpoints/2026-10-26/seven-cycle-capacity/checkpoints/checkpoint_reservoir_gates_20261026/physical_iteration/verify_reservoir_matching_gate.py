"""Independent standard-library matching + independent-set equality verifier.

No proposer imports or matching algorithm; checks literal physical coordinates,
the published rectangle recipe, each matching edge, and the exact removed
neighborhood of the selected outside reservoir. Pass --orbit for gzip bundle.
"""
import json,gzip,itertools,hashlib,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def word(a):return tuple((a//7**j)%7 for j in range(5))
def tr(a):
 a,b,c,d,e=word(a);return (2-b)%7+7*d+49*a+343*((2-c)%7)+2401*e
def main():
 start=time.monotonic();compact='--compact' in sys.argv;path=HERE/('reservoir_orbit_compact.json.gz' if compact else 'reservoir_orbit_matching_gate.json.gz' if '--orbit' in sys.argv else 'reservoir_matching_gate.json');raw=path.read_bytes();o=json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)
 base=HERE.parent/'published/data/base_c7.json';assert hashlib.sha256(base.read_bytes()).hexdigest()==o['source_base_sha256'];d=json.loads(base.read_text());I=sorted(d['I0']);X=set(d['X']);H=set(d['PH']);V=set(d['PV']);R={r for r,q in d['private_pairs']};assert o['base_order']==I and len(I)==len(X)==367
 alphabet=set(I)|X|H|V
 for r in o['records']:alphabet.update(w for p in r.get('reservoir',[]) for w in p);alphabet.update(r['main'])
 for _ in range(3):alphabet|=set(map(tr,alphabet))
 alphabet|={w for pair in d['exchanges']['pairs'] for p in pair for w in p}
 ws={a:word(a) for a in alphabet}
 def cf(a,b):return all((x-y)%7 in (0,1,6) for x,y in zip(ws[a],ws[b]))
 def ip(a):return len(a)==len(set(a)) and all(not cf(x,y) for x,y in itertools.combinations(a,2))
 def sep(a,b):return all(not cf(x,y) for x in a for y in b)
 assert ip(I) and ip(X);xh={x for x in X if any(cf(x,h) for h in H)};xv={x for x in X if any(cf(x,v) for v in V)};assert not xh&xv;x0=X-xh-xv
 near={a:[j for j,b in enumerate(I) if cf(a,b)] for a in alphabet};results=[]
 for r in o['records']:
  M=set(r['main']);assert len(M)==367 and ip(M) and R<=M;B=M-R
  blocks=[(B,B),(R,x0),(H,xh),(V,xv),(x0,R),(xh,V),(xv,H)]
  for _ in range(r.get('transform_power',0)):blocks=[(set(map(tr,a)),set(map(tr,b))) for a,b in blocks]
  assert all(ip(a) and ip(b) for a,b in blocks)
  assert all(sep(a,c) or sep(b,e) for (a,b),(c,e) in itertools.combinations(blocks,2))
  z=set().union(*(set(itertools.product(a,b)) for a,b in blocks));assert len(z)==134753
  if r.get('exchanged',False):
   inserted={tuple(e[1]) for e in d['exchanges']['pairs']};removed={tuple(e[0]) for e in d['exchanges']['pairs']}
   for a,b in d['exchanges']['pairs']:
    assert tuple(a) in z and tuple(b) not in z
    assert {p for p in z if cf(p[0],b[0]) and cf(p[1],b[1])}=={tuple(a)}
   assert all(not(cf(a[0],b[0]) and cf(a[1],b[1])) for a,b in itertools.combinations(inserted,2));z=(z-removed)|inserted
  iset=set(I);S=sorted(p for p in z if p[0] not in iset or p[1] not in iset)
  if not compact:assert S==[tuple(p) for p in r['reservoir']]
  assert len(S)==r['reservoir_count']
  if compact:assert len(r['matching_targets'])==len(S);mt=[(a,b) for a,b in enumerate(r['matching_targets']) if b>=0]
  else:mt=r['matching']
  assert len(mt)==r['matching_size']==len({a for a,b in mt})==len({b for a,b in mt})
  for a,b in mt:
   assert 0<=a<len(S) and 0<=b<367**2
   p,q=S[a];assert cf(p,I[b//367]) and cf(q,I[b%367])
  if compact:lower=len(z)
  else:
   chosen=r['selected_reservoir_indices'];deleted=r['deleted_base_indices'];assert len(chosen)==len(set(chosen)) and all(0<=j<len(S) for j in chosen)
   actual={a*367+b for j in chosen for a in near[S[j][0]] for b in near[S[j][1]]}
   assert sorted(actual)==deleted
   lower=367**2+len(chosen)-len(deleted)
  upper=367**2+len(S)-len(mt)
  assert lower==upper==r['maximum_code_size'] and len(S)-len(mt)==r['deficiency']
  results.append({'name':r['name'],'maximum_code_size':upper,'deficiency':r['deficiency'],'reservoir_count':len(S),'matching_size':len(mt)})
 out={'PASS':True,'certificate':path.name,'sha256':hashlib.sha256(raw).hexdigest(),'records':results,'seconds':time.monotonic()-start,'scope':o['scope']};target=HERE/('reservoir_compact_audit.json' if compact else 'reservoir_orbit_matching_audit.json' if '--orbit' in sys.argv else 'reservoir_matching_audit.json');target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
