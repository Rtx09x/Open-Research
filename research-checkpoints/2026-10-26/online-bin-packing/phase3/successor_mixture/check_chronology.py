#!/usr/bin/env python3
"""Finite integer-unit falsification control, NOT a substitute for the proof.

Tests all 4^9 size sequences for two synthetic capacities, explicit BF events,
disjoint S-own/N-successor birth targets, and the waste-excess injection.
"""
from itertools import product
from pathlib import Path
import json,time
HOME=Path(__file__).resolve().parent
# Units of1/60: capacities3/10 and1/2; d=1/4. All A_i>d.
capacities=[18,30];sizes=[3,6,12,15];d=15;length=9
cuts=[(0,0),(0,6),(3,6),(3,12),(6,12),(6,15),(12,15),(15,15)]
start=time.time();counts={'sequences':0,'cutoff_checks':0,'S_targets':0,'N_targets':0,'nontrivial_both_classes':0}
for sequence in product(sizes,repeat=length):
    bins=[]
    for index,size in enumerate(sequence):
        fit=[(C['gap'],j) for j,C in enumerate(bins) if C['gap']>=size]
        if fit:j=min(fit)[1]
        else:
            A=capacities[len(bins)%2];j=len(bins)
            bins.append({'A':A,'gap':A,'birth':index,'items':[]})
        C=bins[j];C['gap']-=size;C['items'].append(size)
    counts['sequences']+=1
    for c,g in cuts:
        counts['cutoff_checks']+=1
        H=[j for j,C in enumerate(bins) if C['gap']>c]
        S=[j for j in H if min(bins[j]['items'])<=c]
        N=[j for j in H if min(bins[j]['items'])>c]
        targets=[]
        for j in S:
            if j==H[0]:continue
            C=bins[j];target=C['birth'];targets.append(target);counts['S_targets']+=1
            assert C['A']-g<=sum(s for s in C['items'] if s>c)+max(sequence[target]-g,0)
        for j,nextj in zip(N,N[1:]):
            C=bins[j];target=bins[nextj]['birth'];targets.append(target);counts['N_targets']+=1
            assert C['A']-g<=sum(C['items'])+max(sequence[target]-g,0)
        assert len(targets)==len(set(targets))
        if len(S)>1 and len(N)>1:counts['nontrivial_both_classes']+=1
        L=sum(s for s in sequence if s>c);E=sum(max(s-g,0) for s in sequence)
        assert sum(bins[j]['A']-g for j in H)<=L+E+2*(max(capacities)-g)
        assert sum(max(C['gap']-g,0) for C in bins)<=E+max(capacities)
        assert sum(C['gap'] for C in bins)<=c*len(bins)+(g-c)*len(H)+E+max(capacities)
out={'status':'PASS finite falsification control only','size_unit':'1/60','capacities':capacities,'sizes':sizes,'maximum_item':d,'sequence_length':length,'cuts':cuts,**counts,'seconds':time.time()-start}
(HOME/'chronology_control.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
