#!/usr/bin/env python3
"""Independent certificate checker: does not import published verifier/math code."""
import json,itertools,hashlib,time
from pathlib import Path
P=Path(__file__).resolve().parent;start=time.monotonic();x=json.load(open(P/'weighted_terminal_improvement.json'));labels='BNADOHV';weights=dict(zip(labels,x['input_vector']))
# Direct literal symmetric separation table from the seven-family definition.
sep={frozenset(pair) for pair in ['BO','BH','BV','NA','ND','NO','NH','NV','AD','AH','DV']}
code=[tuple(w) for w in x['code']];assert len(code)==2402 and len(set(code))==2402;assert all(len(w)==8 and set(w)<=set(labels) for w in code)
comparisons=0
for u,v in itertools.combinations(code,2):
 assert any(frozenset((a,b)) in sep for a,b in zip(u,v)),(u,v)
 comparisons+=1
M=0
for w in code:
 val=1
 for l in w:val*=weights[l]
 M+=val
assert M==x['new_M'];assert M>x['main_weight']**2
whole,frac=x['bound'].split('.');scale=10**len(frac);numerator=int(whole)*scale+int(frac)
assert numerator**1000<=M*scale**1000<(numerator+1)**1000
out={'valid':True,'label_words':len(code),'label_length':8,'original_channel_dimension':1000,'pair_comparisons':comparisons,'M':M,'strictly_exceeds_published_square':True,'certified_truncated_bound':x['bound'],'sha256_code':hashlib.sha256(json.dumps(sorted(code)).encode()).hexdigest(),'elapsed_seconds':time.monotonic()-start}
(P/'weighted_terminal_independent_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
