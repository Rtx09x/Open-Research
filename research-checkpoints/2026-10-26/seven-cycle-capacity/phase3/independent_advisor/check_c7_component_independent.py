import json,itertools,hashlib,time
from pathlib import Path
from collections import Counter
st=time.time();root=Path(__file__).resolve().parents[1];p=root/'physical_iteration/private_component_closure.json';d=json.loads(p.read_text());core=set(d['core']);cs=list(map(set,d['components']));alphabet=core|set.union(*cs)
D=[tuple((x//7**i)%7 for i in range(5))for x in range(16807)]
def conf(x,y):return all(abs(a-b)in(0,1,6)for a,b in zip(D[x],D[y]))
def indep(s):return all(not conf(a,b)for a,b in itertools.combinations(s,2))
assert len(core)==357 and indep(core)and len(alphabet)==377
assert set(d['alphabet'])==alphabet
assert all(not conf(a,b)for a in core for b in alphabet-core)
assert all(not conf(a,b)for i,c in enumerate(cs)for e in cs[i+1:]for a in c for b in e)
choices=[]
for c in cs:
 deg={x:sum(conf(x,y)for y in c-{x})for x in c};assert sorted(deg.values())==[1,1,2,2]
 choices.append([set(s)for s in itertools.combinations(sorted(c),2)if indep(s)])
assert all(len(x)==3 for x in choices)
assert choices==[[set(s)for s in ch]for ch in d['component_choices']]
base=set(json.loads((root/'published/data/base_c7.json').read_text())['I0']);target=(base-set(d['base_change']['remove']))|set(d['base_change']['add']);assert core<=target and len(target)==367 and target<=alphabet and indep(target)
# Factorized minimum over ALL243 codes, for each outside physical word.
# Counting core neighbors caps at2 since that alone suffices.
minimum=100;exceptions=0
for x in range(16807):
 if x in alphabet:continue
 c=0
 for y in core:
  c+=conf(x,y)
  if c>=2:break
 if c<2:
  exceptions+=1
  c+=sum(min(sum(conf(x,y)for y in ch)for ch in chs)for chs in choices)
 minimum=min(minimum,c);assert c>=2,x
hist=Counter();states=set()
for rec in d['records']:
 ix=tuple(rec['choices']);assert ix not in states;states.add(ix)
 code=core|set.union(*(choices[j][k]for j,k in enumerate(ix)))
 private=sorted(x for x in alphabet-code if sum(conf(x,y)for y in alphabet&code)==1)
 assert private==rec['private']and rec['unconfusable']==[];hist[len(private)]+=1
assert states==set(itertools.product(range(3),repeat=5))
assert {str(k):v for k,v in hist.items()}==d['private_count_histogram']
out={'passed':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'states':len(states),'outside_words':16807-377,'factorized_minimum_outside_conflicts':minimum,'outside_words_needing_component_test':exceptions,'private_histogram':dict(sorted(hist.items())),'seconds':time.time()-st,'scope':'Entire fixed-size single-word-exchange component; not global C7^5 optimality','proof':'Independent direct coordinate distance and separable minimum over five P4 choices; no worker imports'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
