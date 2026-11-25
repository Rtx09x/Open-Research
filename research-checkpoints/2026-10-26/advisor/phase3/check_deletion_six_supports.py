"""Independent exact six-syndrome certificate audit via insertion incidence.
No worker imports and no optimizer. All output stays in advisor/phase2.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import gzip,json,time,hashlib,sys
t0=time.time()
root=Path(sys.argv[1])
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
# Generate incidence in the opposite direction from the worker's deletion
# slices: insert either bit into every11-bit received string at every slot.
inc=[set()for _ in range(4096)]
for y in range(2048):
    w=f'{y:011b}'
    for slot in range(12):
        for bit in '01':inc[int(w[:slot]+bit+w[slot:],2)].add(y)
assert all(inc)
synd=[sum((12-i)*((x>>i)&1)for i in range(12))%13 for x in range(4096)]
for x in range(4096):
    assert synd[4095-x]==(-synd[x])%13
    assert inc[4095-x]=={2047-y for y in inc[x]}
supports=set(combinations(range(13),6))
neg=lambda a:tuple(sorted((-v)%13 for v in a))
representatives=sorted(a for a in supports if a<=neg(a))
assert len(supports)==1716 and len(representatives)==868
cliques={int(k):v for k,v in read(root/'used_word_cliques.json.gz')['cliques'].items()}
for vertices in cliques.values():
    assert len(vertices)==len(set(vertices))and all(type(x)==int and 0<=x<4096 for x in vertices)
    assert all(inc[x]&inc[y]for x,y in combinations(vertices,2))
covered=set();costs=[];kinds={};checks=0;hashes={}
for i,S in enumerate(representatives):
    path=root/f'{i:04d}.json.gz';c=read(path)
    assert c['index']==i and tuple(c['support'])==S
    den=c['denominator'];assert type(den)==int and den>0
    chosen=[x for x in range(4096)if synd[x]in S]
    coverage={x:0 for x in chosen};rows=c['weights'];assert len(rows)==len({a for a,b in rows})
    assert all(type(a)==int and type(b)==int and b>0 for a,b in rows)
    total=sum(b for a,b in rows)
    if c['kind']=='received':
        weights=dict(rows);assert all(0<=y<2048 for y in weights)
        for x in chosen:coverage[x]=sum(weights.get(y,0)for y in inc[x])
    else:
        assert c['kind']=='cliques'
        for a,b in rows:
            for x in cliques[a]:
                if x in coverage:coverage[x]+=b
        singles=c['singletons'];assert len(singles)==len({x for x,b in singles})
        for x,b in singles:
            assert x in coverage and type(b)==int and b>0
            coverage[x]+=b;total+=b
    assert min(coverage.values())>=den and total==c['total_numerator']and total<317*den
    covered|={S,neg(S)};costs.append(Fraction(total,den));checks+=len(chosen)
    kinds[c['kind']]=kinds.get(c['kind'],0)+1
    hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
assert covered==supports
out={'PASS':True,'independent_insertion_incidence':True,'worker_imports':False,
     'representatives':len(representatives),'all_six_supports':len(covered),
     'integer_coverage_checks':checks,'kinds':kinds,'checked_cliques':len(cliques),
     'largest_exact_cover_cost':str(max(costs)),'seconds':time.time()-t0,
     'scope':'Every length12 binary one-deletion code with>=317 words uses at least7 VT classes; not a global upper bound improvement.',
     'certificate_hashes':hashes}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='certificate_hashes'},indent=2))
