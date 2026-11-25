#!/usr/bin/env python3
"""Exact operational/projection controls under arbitrary extra erasures.

Tests the existing v2 rational label oracle, including resuming locally full
instances. This is a semantic control, NOT a substitute for the uniform proof.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import importlib.util
import json
import time

root=Path(__file__).resolve().parents[2]
path=root/'theory'/'adaptive_policy.py'
spec=importlib.util.spec_from_file_location('v2_rational_runtime',path)
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
original=runtime.A.label
CURRENT_PATH=[]


def traced_label(self,j):
    before=self.count
    CURRENT_PATH.append((self,before))
    result=original(self,j)
    assert self.count==before+1
    return result


runtime.A.label=traced_label


def owned(board,instance):
    return {i:token[0] for i,token in enumerate(board)
            if token is not None and instance in token[1]}


def move(world,j,statistics):
    global CURRENT_PATH
    board,a,known,everfull=world
    assert board[j] is None
    before={x:owned(board,x) for x in known}
    counts={x:x.count for x in known}
    for i,token in enumerate(board):
        if token is not None and ((i<j and token[0]==-1) or (i>j and token[0]==1)):
            board[i]=None
    CURRENT_PATH=[]
    sign=a.label(j)
    responding={x for x,c in CURRENT_PATH}
    assert len(responding)==len(CURRENT_PATH)
    newinstances=responding-known
    for x in newinstances:
        before[x]={}
        if any(token is not None and x.l<=i<=x.r for i,token in enumerate(board)):
            statistics['new_instances_with_foreign_signs']+=1
    for x,c in CURRENT_PATH:
        assert j not in before[x]
        if x in everfull:
            statistics['calls_after_previous_owned_fullness']+=1
    board[j]=(sign,frozenset(responding))
    known |= responding
    for x in known:
        after=owned(board,x)
        assert all(x.l<=i<=x.r for i in after)
        if x in responding:
            expected={i:s for i,s in before[x].items()
                      if not((i<j and s==-1) or (i>j and s==1))}
            expected[j]=sign
            assert after==expected
            statistics['local_projected_responses']+=1
        else:
            assert all(before[x].get(i)==s for i,s in after.items())
            assert x.count==counts[x]
            statistics['external_erasure_projections']+=1
        if len(after)==x.r-x.l+1:
            everfull.add(x)
    return board,a,known,everfull


def main():
    start=time.perf_counter()
    reports=[]
    for n,depth in [(1,6),(2,6),(4,4)]:
        stats={'n':n,'depth':depth,'edges':0,'local_projected_responses':0,
               'external_erasure_projections':0,'calls_after_previous_owned_fullness':0,
               'new_instances_with_foreign_signs':0}
        a=runtime.A(0,n-1)
        def dfs(world,remaining):
            if not remaining:return
            board=world[0]
            occupied=[i for i,t in enumerate(board) if t is not None]
            for k in range(len(occupied)+1):
                for deleted in combinations(occupied,k):
                    for j in range(n):
                        if board[j] is not None and j not in deleted:continue
                        w=deepcopy(world)
                        for i in deleted:w[0][i]=None
                        # Deletion is an external event: no controller count or
                        # internal state changes, only owned-cohort removal.
                        w=move(w,j,stats)
                        stats['edges']+=1
                        dfs(w,remaining-1)
        dfs(([None]*n,a,{a},set()),depth)
        assert stats['calls_after_previous_owned_fullness']>0
        reports.append(stats)
    assert sum(r['new_instances_with_foreign_signs'] for r in reports)>0
    out={'all_checks_passed':True,'runs':reports,'wall_seconds':time.perf_counter()-start,
         'scope':'Complete arbitrary-erasure subsets and empty-cell requests to the stated bounded depths, with exact rational v2 runtime. Every instance projection is a valid extended owned-sign trace; full local instances may resume after erasure. Root ordinary SPR remains terminal-full.',
         'proof_caveat':'Operational controls only; deletion-robust uniform induction is documented separately.'}
    Path(__file__).with_name('augmented_projection.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
