"""Literal-coordinate validation of fixed C30+8 fiber-pair upper certificate.
No worker imports; the matching is a supplied witness, not an optimality claim.
"""
import json,hashlib,itertools,time
from pathlib import Path
ROOT=Path('/workspace/shared/research-active')
BASE=ROOT/'seven-cycle-capacity/physical_iteration'
start=time.time()
raw=(BASE/'c30_fiber_pair_gate.json').read_bytes(); cert=json.loads(raw)
iraw=(BASE/'c30_plus_eight_port_instance.json').read_bytes(); inst=json.loads(iraw)
def digits(w):
 assert isinstance(w,int) and 0<=w<7**5
 return tuple((w//7**j)%7 for j in range(5))
D={w:digits(w) for k in ['B','H','V','X'] for w in inst[k]}
def close(x,y):
 return all((a-b)%7 in (0,1,6) for a,b in zip(D[x],D[y]))
def independent(a):
 assert len(a)==len(set(a))
 assert all(not close(x,y) for x,y in itertools.combinations(a,2))
B,H,V,X=(inst[k] for k in ['B','H','V','X'])
assert tuple(map(len,[B,H,V,X]))==(344,23,23,367)
for a in [B,H,V,X]:independent(a)
P=cert['port_order'];assert len(P)==46 and set(P)==set(H)|set(V)
assert set(H).isdisjoint(V) and set(P).isdisjoint(X) and set(P).isdisjoint(B)
masks={x:sum(1<<i for i,p in enumerate(P) if close(x,p)) for x in X}
cover={}
for row in cert['covers']:
 mask=row['mask']; assert 0<=mask<2**46 and mask not in cover
 allowed={p for i,p in enumerate(P) if not mask>>i&1}
 parts=row['clique_partition']; flat=[p for q in parts for p in q]
 assert len(flat)==len(set(flat)) and set(flat)==allowed
 assert all(q and all(close(a,b) for a,b in itertools.combinations(q,2)) for q in parts)
 assert row['upper']==len(parts)
 cover[mask]=len(parts)
a0=cover[0]; assert a0==23
ax={x:cover[masks[x]] for x in X}
base=len(B)**2+sum(a0+ax[x] for x in X)
assert base==cert['diagonal_upper']
used=set();deficit=0
for row in cert['selected_disjoint_pairs']:
 x,y=row['x'],row['y'];assert x in ax and y in ax and x!=y and x not in used and y not in used
 used|={x,y}; aa=[a0,ax[x],ax[y],cover[masks[x]|masks[y]]]
 assert aa==row['alpha_bounds']; vals=[]
 # Four bits encode which side avoids the opposite outer label.
 for orient in range(16):
  bans=[0,0,0,0] # F_x,F_y,G_x,G_y
  for i,j in itertools.product(range(2),repeat=2):
   if orient&(1<<(2*i+j)):bans[2+j]|=1<<i
   else:bans[i]|=1<<j
  vals.append(sum(aa[z] for z in bans))
 assert vals==row['orientation_upper_bounds'] and max(vals)==row['pair_upper']
 gain=2*a0+ax[x]+ax[y]-max(vals)
 assert gain==row['gain_over_diagonal'] and gain>=0
 deficit+=gain
upper=base-deficit
assert deficit==cert['additional_deficit']==78
assert upper==cert['dimension10_upper']==135060<cert['target']==135093
out=dict(verified=True,certificate_sha256=hashlib.sha256(raw).hexdigest(),instance_sha256=hashlib.sha256(iraw).hexdigest(),physical_dimension=10,base_cardinality=len(B)**2,self_crossing_upper=base,disjoint_pairs=len(used)//2,additional_deficit=deficit,upper=upper,target=cert['target'],cover_witnesses=len(cover),seconds=time.time()-start,scope='Fixed B,P,X two-direction variable fibers only; no unrestricted capacity upper and no optimality claim for the matching.')
Path(__file__).with_name('c7_fiber_pair_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
