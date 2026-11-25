#!/usr/bin/env python3
"""Exact replay of the hostile review's 19-round ordinary-child counterexample."""
from pathlib import Path
import hashlib
import importlib.util
import json

root=Path(__file__).resolve().parents[2]
source=root/'theory'/'adaptive_policy.py'
spec=importlib.util.spec_from_file_location('hostile_replay_runtime',source)
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)
base_label=runtime.A.label
path=[]
def label(self,j):
    path.append(self)
    return base_label(self,j)
runtime.A.label=label

requests=[x for i in range(8) for x in [17+i,1+i]]+[25,9,25]
board=[0]*32
a=runtime.A(0,31)
rows=[]
saved_child=saved_leaf=None
child_counts=[]
for round_no,cell in enumerate(requests,1):
    j=cell-1
    assert board[j]==0,(round_no,cell,'globally illegal request')
    assert any(s==0 for s in board)
    erased=[]
    for i,s in enumerate(board):
        if(i<j and s==-1)or(i>j and s==1):
            erased.append(i+1);board[i]=0
    path=[]
    sign=a.label(j)
    assert sign==1
    board[j]=sign
    if round_no==17:
        saved_child=next(x for x in path if x.l==16 and x.r==31)
        saved_leaf=next(x for x in path if x.l==24 and x.r==24)
        assert saved_child.count==saved_leaf.count==1
    if round_no in [17,18,19]:
        child_counts.append(saved_child.count)
    if round_no==18:
        assert 25 in erased and saved_child not in path and saved_leaf not in path
    if round_no==19:
        assert saved_child in path and saved_leaf in path
        assert saved_child.count==saved_leaf.count==2
    rows.append({'round':round_no,'request':cell,'label':'+','erased':erased,
                 'root_epoch_tau':a.epoch.tau,'root_phase':a.epoch.phase,
                 'root_half_counts':a.epoch.counts.copy(),
                 'occupied_plus_positions':[i+1 for i,s in enumerate(board) if s==1]})
assert child_counts==[1,1,2]
assert rows[15]['occupied_plus_positions']==list(range(1,9))
assert rows[16]['root_epoch_tau']==rows[17]['root_epoch_tau']==rows[18]['root_epoch_tau']==16
assert all(row['root_phase']==1 for row in rows[16:])
assert len([s for s in board if s])==10
out={'all_checks_passed':True,'requests_one_based':requests,'rounds':rows,
     'same_right_half_child_on_rounds_17_and_19':True,
     'same_previously_full_leaf_on_rounds_17_and_19':True,
     'right_child_counts_after_rounds_17_18_19':child_counts,
     'isolated_child_request_sequence':[25,25],
     'isolated_standalone_second_request_illegal':True,
     'scope':'Actual v2 rational runtime; all19 physical requests legal, no root full-board termination. Confirms proof-interface defect under ordinary-child interpretation, not failure of sign bound.',
     'runtime_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
Path(__file__).with_name('hostile_transcript_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rounds'},indent=2))
