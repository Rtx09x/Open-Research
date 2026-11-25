"""Standalone exact, standard-library verifier for the variable-fiber upper gate.

Crossing fibers force an entire-neighborhood avoidance on at least one side.
P and X are disjoint, so a confusable crossing cannot be an identical word.
All local independence upper bounds are explicit physical clique partitions.
"""
import json,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent
def conf(a,b):return all(((a//7**j)-(b//7**j))%7 in (0,1,6) for j in range(5))
def indep(c):return len(c)==len(set(c)) and all(not conf(a,b) for a,b in itertools.combinations(c,2))
def run():
 d=json.loads((HERE/'c30_fiber_pair_gate.json').read_text());z=json.loads((HERE/d['instance_file']).read_text());P=d['port_order'];B=z['B'];X=z['X'];assert len(P)==46 and len(set(P))==46 and set(P)==set(z['H'])|set(z['V'])
 assert len(B)==344 and len(X)==367 and all(indep(c) for c in [B,X,z['H'],z['V']]);assert set(P).isdisjoint(X)
 assert all(not conf(a,b) for a in B for b in P)
 cover={}
 for r in d['covers']:
  mask=r['mask'];assert 0<=mask<(1<<len(P));parts=r['clique_partition'];wanted={p for j,p in enumerate(P) if not mask>>j&1};flat=sum(parts,[])
  assert len(flat)==len(set(flat))==len(wanted) and set(flat)==wanted
  assert all(conf(a,b) for c in parts for a,b in itertools.combinations(c,2))
  assert r['upper']==len(parts);cover[mask]=len(parts)
 masks={x:sum(1<<j for j,p in enumerate(P) if conf(p,x)) for x in X};a0=cover[0];assert a0==23;ax={x:cover[masks[x]] for x in X}
 diagonal=len(B)**2+sum(a0+ax[x] for x in X);assert diagonal==d['diagonal_upper']==135138
 used=set();pairtotal=0;gain=0
 for r in d['selected_disjoint_pairs']:
  x,y=r['x'],r['y'];assert x!=y and x in X and y in X and x not in used and y not in used;used|={x,y};union=masks[x]|masks[y];assert union==r['union_forbidden_mask'];aa=[a0,ax[x],ax[y],cover[union]];assert aa==r['alpha_bounds'];values=[]
  for o in range(16):
   forced=[0]*4
   for i in range(2):
    for j in range(2):
     if o>>(2*i+j)&1:forced[2+j]|=1<<i
     else:forced[i]|=1<<j
   values.append(sum(aa[m] for m in forced))
  assert values==r['orientation_upper_bounds'];v=max(values);assert v==r['pair_upper'];g=2*a0+ax[x]+ax[y]-v;assert g==r['gain_over_diagonal'] and g>=0;gain+=g;pairtotal+=v
 upper=len(B)**2+pairtotal+sum(a0+ax[x] for x in X if x not in used);assert upper==diagonal-gain==d['dimension10_upper']==135060 and gain==78
 assert upper<135093
 out={'PASS':True,'port_vertices':46,'outer_labels':367,'base_square':344**2,'selected_outer_pairs':len(d['selected_disjoint_pairs']),'diagonal_bound':135138,'additional_pair_deficit':78,'final_dimension10_upper':upper,'target':135093,'target_excluded':True,'P_intersection_X_empty':True,'scope':d['scope']}
 (HERE/'c30_fiber_pair_gate_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
