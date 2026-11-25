"""Third-party terminal certificate audit, no worker or published-code imports."""
import ast,json,itertools,math,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; start=time.time()
d=json.loads((ROOT/'weighted_terminal_improvement.json').read_text())
# Parse only the literal published K4a string, not executable implementation.
astree=ast.parse((ROOT/'published/shannon/bpz.py').read_text())
node=next(a for a in astree.body if isinstance(a,ast.Assign) and any(isinstance(x,ast.Name)and x.id=='K4a' for x in a.targets))
s=ast.literal_eval(node.value.args[0]);K={tuple(w.strip('()').split(','))for w in s.split('),(')}
assert len(K)==49
letters='BNADHV';ix={x:i for i,x in enumerate(letters)}
edges=['BN','BA','BD','AV','DH','HV'];closed=[1<<i for i in range(6)]
for x,y in edges:closed[ix[x]]|=1<<ix[y];closed[ix[y]]|=1<<ix[x]
def encode(w):return tuple(ix[x]for x in w)
def conflict(u,v):return all(closed[a]>>b&1 for a,b in zip(encode(u),encode(v)))
assert all(not conflict(u,v)for u,v in itertools.combinations(K,2))
r,q=map(tuple,d['pair_words']);assert r in K and q not in K
assert [x for x in K if conflict(q,x)]==[r]
weights=dict(zip('BNADOHV',d['input_vector']));value=lambda w:math.prod(weights[x]for x in w)
assert value(r)==value(q)
perm=d['auxiliary_automorphism']['perm'];flags=d['auxiliary_automorphism']['reflect'];refl={'B':'B','N':'N','A':'D','D':'A','H':'V','V':'H'}
X={tuple(refl[w[perm[i]]]if flags[i]else w[perm[i]] for i in range(4))for w in K}
assert X==set(map(tuple,d['auxiliary_words']))
assert all(not conflict(u,v)for u,v in itertools.combinations(X,2))
XH={x for x in X if conflict(x,r)};XV={x for x in X if conflict(x,q)}
assert not XH&XV
X0=X-XH-XV;B=K-{r}
rectangles=[(B,B),({r},X0),({r},XH),({q},XV),(X0,{r}),(XH,{q}),(XV,{r})]
recipe={a+b for S,T in rectangles for a in S for b in T}
code=list(map(tuple,d['code']));assert len(code)==len(set(code))==2402 and recipe==set(code)
# Literal exhaustive pair check via six-vertex closed-neighbor bit masks.
coded=list(map(encode,code));pairs=0
for i,u in enumerate(coded):
 for v in coded[i+1:]:
  assert any(not(closed[a]>>b&1)for a,b in zip(u,v))
  pairs+=1
old=sum(value(w)for w in K);new=sum(value(w)for w in code);aux=sum(value(w)for w in X)
assert old==d['main_weight'] and new==d['new_M'] and aux==old
assert new==old**2+value(r)**2 and new>old**2
whole,frac=d['bound'].split('.');scale=10**len(frac);lo=int(whole+frac)
assert lo**1000<=new*scale**1000<(lo+1)**1000
out={'exact':True,'method':'AST literal K4a; independent six-edge graph; complete pair enumeration; integer roots','pairs_checked':pairs,'word_count':len(code),'private_pair':[''.join(r),''.join(q)],'auxiliary_map_verified':True,'rectangle_recipe_verified':True,'weight_sum_verified':True,'gain_formula':'M_new=M_old^2+(w_N^2*w_H^2)^2','gain':str(new-old**2),'certified_bound':d['bound'],'seconds':time.time()-start,'scope':'terminal improvement conditional on independently established published length125 family sizes/separation; novelty not established'}
Path(__file__).with_name('c7_terminal_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
