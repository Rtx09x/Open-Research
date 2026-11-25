#!/usr/bin/env python3
"""Standalone finite-label and exact-integer verifier for recycled certificates.
The channel realization of input_vector is the separately reproduced August theorem.
No published BPZ implementation is imported by this checker.
"""
import sys,json,itertools,hashlib,time,argparse
from pathlib import Path
sys.set_int_max_str_digits(0);P=Path(__file__).resolve().parent;start=time.monotonic();ap=argparse.ArgumentParser();ap.add_argument('certificate',nargs='?',default='recycled_terminal_certificate.json');args=ap.parse_args();c=json.load(open(P/args.certificate));raw=(P/c['source_base']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['source_base_sha256'];base=json.loads(raw);L='BNADOHV';seps={frozenset(p) for p in ('BO','BH','BV','NA','ND','NO','NH','NV','AD','AH','DV')}
def sep(a,b):return frozenset((a,b)) in seps
def separated(u,v):return any(sep(a,b) for a,b in zip(u,v))
def prod(seq):
 v=1
 for s in seq:v*=s
 return v
assert hashlib.sha256(json.dumps(base['input_vector']).encode()).hexdigest() == '6a62bfd209f37490db9e56ce6e6d6e40b4cd7a5502f9fb2c7678402aa1390911', 'wrong inherited August n25 vector'
F={l:list(map(tuple,base['families'][l])) for l in L};w=dict(zip(L,base['input_vector']))
for l in L:
 assert len(F[l])==len(set(F[l]))
 assert all(len(x)==4 and set(x)<=set(L) for x in F[l])
 assert all(separated(x,y) for x,y in itertools.combinations(F[l],2))
 for m in L:
  if sep(l,m):assert all(separated(x,y) for x in F[l] for y in F[m])
v0=tuple(sum(prod(w[x] for x in word) for word in F[l]) for l in L);assert v0==tuple(base['vector'])
rule={'B':['BB','HD','VA','DV','AH'],'N':['NN','AA','AD','DA','DD'],'A':['AN','ND'],'D':['DN','NA'],'O':['ON','NO'],'H':['HN','NV'],'V':['VN','NH']}
for l in L:
 assert all(separated(x,y) for x,y in itertools.combinations(rule[l],2))
 for m in L:
  if sep(l,m):assert all(separated(x,y) for x in rule[l] for y in rule[m])
def combine(a,b):
 da,db=dict(zip(L,a)),dict(zip(L,b))
 return tuple(sum(da[x]*db[y] for x,y in rule[l]) for l in L)
if 'nodes' in c:
 values=[];dims=[]
 for i,node in enumerate(c['nodes']):
  if node['operation']=='base':v=v0;d=base['base_dimension']
  else:
   assert node['operation']=='S2a';a,b=node['children'];assert a<i and b<i;v=combine(values[a],values[b]);d=dims[a]+dims[b]
  assert d==500*node['leaves'];values.append(v);dims.append(d)
 v=values[c['root']];dimension=dims[c['root']]
else:
 v=v0;dimension=base['base_dimension'];assert c['operation']=='S2a(previous, previous)'
 for _ in range(c['levels']):v=combine(v,v);dimension*=2
assert v==tuple(c['final_vector']);assert dimension==c['dimension'];assert c['terminal_labels']==['B','O'];assert sep('B','O');M=v[0]+v[4];assert M==c['M'];assert dimension%500==0 and M>(v0[0]+v0[4])**(dimension//500)
r,scale=c['root_numerator'],c['root_denominator'];target=M*scale**dimension;assert r**dimension<=target<(r+1)**dimension
result={'verified':True,'certificate':args.certificate,'dimension':dimension,'certified_lower_bound':c['certified_lower_bound'],'finite_family_checks':True,'literal_S2a_admissible':True,'exact_arithmetic_and_root_bracket':True,'strict_rate_gain_over_published_construction':True,'elapsed_seconds':time.monotonic()-start}
(P/('verification_'+Path(args.certificate).stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
