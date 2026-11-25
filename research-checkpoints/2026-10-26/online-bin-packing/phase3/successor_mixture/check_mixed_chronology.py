#!/usr/bin/env python3
"""Explicit nontrivial S/N birth-target control; finite evidence, not proof."""
from pathlib import Path
import json
sequence=[13,7,7,3,13,7,1,3,7,7,7,7,13,1,1,1,1,1,13,7,1,3,1,3,7,7,1,7,3,13,3,7,13,1,13,13,13,3,1,3,13,1,3,7,7,1,13,7,13,1,7,13,3,3,13,13,1,1,7,13,13,13,13,7,13,7,13,3,3,3,1,1,1,7,3,1,13,13,7,13]
capacities=[17,29];d=13;c=1;g=7;bins=[]
for index,size in enumerate(sequence):
    fit=[(C['gap'],j) for j,C in enumerate(bins) if C['gap']>=size]
    if fit:j=min(fit)[1]
    else:
        j=len(bins);A=capacities[j%2];bins.append({'A':A,'gap':A,'birth':index,'items':[]})
    bins[j]['gap']-=size;bins[j]['items'].append(size)
H=[j for j,C in enumerate(bins) if C['gap']>c];S=[j for j in H if min(bins[j]['items'])<=c];N=[j for j in H if j not in S]
assert S==[20] and H[0]!=S[0] and len(N)>1
targets=[]
for j in S:
    if j==H[0]:continue
    C=bins[j];target=C['birth'];targets.append({'case':'S-own','container':j,'birth_target':target})
    assert C['A']-g<=sum(s for s in C['items'] if s>c)+max(sequence[target]-g,0)
for j,nextj in zip(N,N[1:]):
    C=bins[j];target=bins[nextj]['birth'];targets.append({'case':'N-successor','container':j,'birth_target':target})
    assert C['A']-g<=sum(C['items'])+max(sequence[target]-g,0)
assert len(targets)==len(set(t['birth_target'] for t in targets))
out={'status':'PASS explicit mixed S/N chronology control','unit':'1/60','capacities':capacities,'d':d,'c':c,'g':g,'sequence':sequence,'H':H,'S':S,'N':N,'targets':targets,'bins':bins}
(Path(__file__).resolve().parent/'mixed_chronology_control.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['sequence','bins']})
