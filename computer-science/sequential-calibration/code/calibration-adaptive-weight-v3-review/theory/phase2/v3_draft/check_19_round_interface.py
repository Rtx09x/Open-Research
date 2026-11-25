#!/usr/bin/env python3
"""Replay the hostile audit's concrete child-history counterexample exactly.
Uses the frozen v2 rational implementation without changing its algorithm.
"""
from pathlib import Path
import sys,json,hashlib
here=Path(__file__).parent
frozen=here if (here/'adaptive_policy.py').exists() else here.parent
assert (frozen/'adaptive_policy.py').exists()
assert hashlib.sha256((frozen/'adaptive_policy.py').read_bytes()).hexdigest()=='511b5d1f5a0eaad2fe4cd21a22efa498bac06b36a91598c6fcc4b5aa09d2a40e'
sys.path.insert(0,str(frozen))
from adaptive_policy import A,step
requests=[x for k in range(8) for x in (17+k,1+k)]+[25,9,25]
a=A(0,31);board=[0]*32;rows=[];right=None;leaf=None

def leaf_for(node,j):
 while node.l<node.r:
  b=node.epoch
  assert b.phase==1
  node=b.children[int(j>b.m)]
 return node

for t,j in enumerate(requests,1):
 before=board.copy();assert before[j-1]==0
 board=step(board,a,j-1)
 assert board[j-1]==1
 rows.append({'round':t,'request_1based':j,'sign':'+','erased_plus_cells':[i+1 for i in range(32) if before[i]==1 and board[i]!=1], 'occupied_after':[i+1 for i,s in enumerate(board) if s], 'root_tau':a.epoch.tau,'root_phase':a.epoch.phase,'root_half_counts':a.epoch.counts.copy(),'root_continuation_cap':a.epoch.L})
 if t==17:
  right=a.epoch.children[1];leaf=leaf_for(right,j-1)
  assert right.count==1 and leaf.count==1
 if t==19:
  assert right is a.epoch.children[1]
  assert leaf is leaf_for(right,j-1)
  assert right.count==2 and leaf.count==2
assert rows[15]['occupied_after']==list(range(1,9))
assert rows[17]['occupied_after']==list(range(1,10))
assert rows[18]['occupied_after']==list(range(1,10))+[25]
# Isolated child history ignores the root request at9; it is25,25 with plus labels.
assert requests[16:]==[25,9,25]
result={'all_checks_passed':True,'requests_1based':requests,'rounds':19,'board_size':32,'same_right_child_and_same_leaf_receive_25_twice':True,'isolated_child_second_request_illegal':True,'deletion_augmented_projection_legal':True,'root_full_board_never_reached':all(len(r['occupied_after'])<32 for r in rows),'algorithm_source_sha256':hashlib.sha256((frozen/'adaptive_policy.py').read_bytes()).hexdigest(),'scope':'Confirms an induction-interface defect, not a counterexample to the sign bound. Root requests are all legal; the child needs its external-erasure history.','rows':rows}
out=Path(__file__).with_name('19_round_interface_check.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
