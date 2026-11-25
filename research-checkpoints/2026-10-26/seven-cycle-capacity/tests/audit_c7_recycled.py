"""Independent recycled seven-family BPZ certificate audit, exact integers only."""
import ast,json,itertools,math,sys,time,hashlib
from pathlib import Path
sys.set_int_max_str_digits(0); start=time.time();ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'terminal_recycled_base.json').read_bytes();base=json.loads(raw);d=json.loads((ROOT/'recycled_terminal_certificate.json').read_text())
assert hashlib.sha256(raw).hexdigest()==d['source_base_sha256']
labels='BNADOHV'; sep={frozenset(e)for e in ['BO','BH','BV','NA','ND','NO','NH','NV','AD','AH','DV']}
def separated(u,v):return any(frozenset((a,b))in sep for a,b in zip(u,v))
fams={a:set(map(tuple,base['families'][a]))for a in labels}
weights=dict(zip(labels,base['input_vector']));val=lambda w:math.prod(weights[a]for a in w)
for a,F in fams.items():
 assert len(F)==len(base['families'][a]);assert all(len(w)==4 for w in F)
 assert all(separated(u,v)for u,v in itertools.combinations(F,2)),a
for pair in sep:
 a,b=pair;assert all(separated(u,v)for u in fams[a]for v in fams[b]),pair
v=[sum(map(val,fams[a]))for a in labels];assert v==base['vector']
# Verify provenance of main/auxiliary families from literal K4a.
tree=ast.parse((ROOT/'published/shannon/bpz.py').read_text());node=next(a for a in tree.body if isinstance(a,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='K4a'for x in a.targets));s=ast.literal_eval(node.value.args[0]);K={tuple(w.strip('()').split(','))for w in s.split('),(')}
assert fams['B'].isdisjoint(fams['O']) and fams['B']|fams['O']==K
p=base['auxiliary_automorphism']['perm'];flags=base['auxiliary_automorphism']['reflect'];refl={'B':'B','N':'N','A':'D','D':'A','O':'O','H':'V','V':'H'}
X={tuple(refl[w[p[i]]]if flags[i]else w[p[i]]for i in range(4))for w in K}
assert all(fams[a].isdisjoint(fams[b])for a,b in itertools.combinations('NAD',2));assert set.union(*(fams[a]for a in 'NAD'))==X
# Independently literal S2a, plus formal admissibility under the separation relation.
rule={'B':['BB','HD','VA','DV','AH'],'N':['NN','AA','AD','DA','DD'],'A':['AN','ND'],'D':['DN','NA'],'O':['ON','NO'],'H':['HN','NV'],'V':['VN','NH']}
for a,R in rule.items():assert all(separated(u,v)for u,v in itertools.combinations(R,2)),a
for pair in sep:
 a,b=pair;assert all(separated(u,v)for u in rule[a]for v in rule[b]),pair
old=v[0]+v[4];dimension=base['base_dimension'];assert dimension==500
for _ in range(d['levels']):
 w=dict(zip(labels,v));v=[sum(w[x]*w[y]for x,y in rule[a])for a in labels];dimension*=2
assert v==d['final_vector'];M=v[0]+v[4];assert M==d['M'] and dimension==d['dimension'];assert M>old**(2**d['levels'])
lo=d['root_numerator'];scale=d['root_denominator'];target=M*scale**dimension
assert lo**dimension<=target<(lo+1)**dimension
assert d['certified_lower_bound']==str(lo//scale)+'.'+str(lo%scale).zfill(len(str(scale))-1)
out={'exact':True,'base_family_axioms':True,'base_main_aux_provenance':True,'S2a_admissibility':True,'recurrences_replayed':d['levels'],'dimension':dimension,'M_sha256':hashlib.sha256(str(M).encode()).hexdigest(),'strictly_exceeds_published_bound':True,'certified_lower_bound':d['certified_lower_bound'],'seconds':time.time()-start,'scope':'exact finite code using independently established published125-dimensional inputs; literature novelty unconfirmed'}
Path(__file__).with_name('c7_recycled_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
