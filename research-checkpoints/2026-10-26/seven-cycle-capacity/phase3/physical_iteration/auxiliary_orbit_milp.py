"""Search changed physical auxiliary code, NOT the fixed n125 interface.

Uses T-orbit expansion (1288 original-channel words) filtered by the original
private endpoint neighborhood axiom. Any proposed improvement is rechecked
with integers and exact published construction arithmetic. Solver failure is
not an impossibility proof. SciPy/HiGHS is only a candidate proposer.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix,vstack
from physical_graph import *
import sys,time,resource,argparse
def nh(S):
 return {encode(tuple((a+b)%7 for a,b in zip(digits(v),delta))) for v in S for delta in itertools.product((-1,0,1),repeat=5)}
def run(gadget=None,local=0):
 start=time.monotonic();d=json.loads(BASE.read_text());i,x,*_=alphabets()
 if gadget:d.update(json.loads(Path(gadget).read_text()));i=set(d['main'])
 h=nh(d['PH']);v=nh(d['PV']);u=set();s=i|x
 for _ in range(4):u|=s;s=set(map(transform,s))
 if local:
  counts=[0]*16807
  for a in x:
   for b in nh([a]):counts[b]+=1
  u|={a for a,n in enumerate(counts) if 1<=n<=local}
 u-=h&v;vs,adj=graph(u);cl=maximal_cliques(adj)
 cls=[int(a in h)+2*int(a in v) for a in vs];assert all(c!=3 for c in cls)
 row=[];col=[]
 for j,c in enumerate(cl):
  for a in c:row.append(j);col.append(a)
 mat=coo_matrix((np.ones(len(row)),(row,col)),shape=(len(cl),len(vs))).tocsc()
 # Strong published role sensitivities: cardinality dominates boundary penalty.
 grad=json.loads((HERE.parent/'role_gradients.json').read_text())['leaves'][0]['auxiliary_weights_N_H_V']
 weights=np.array([grad[c]/grad[0] for c in cls]);oldscore=sum(grad[int(a in h)+2*int(a in v)] for a in x-(h&v))
 # A candidate must preserve >=367 auxiliary words; objective is role-sensitive.
 mat=vstack([mat,np.ones((1,len(vs))),weights.reshape(1,-1)]).tocsc()
 lb=np.array([-np.inf]*len(cl)+[367.,oldscore/grad[0]+.0001]);ub=np.array([1.]*len(cl)+[np.inf,np.inf])
 print('pool',len(vs),'cliques',len(cl),'baseline_weight',oldscore/grad[0],flush=True)
 res=milp(-weights,integrality=np.ones(len(vs)),bounds=Bounds(0,1),constraints=LinearConstraint(mat,lb,ub),options={'time_limit':240,'threads':1,'mip_rel_gap':0,'disp':True})
 out={'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,'pool':len(vs),'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'gadget':gadget,'local_neighborhood_limit':local,'scope':'T orbit plus bounded X-neighborhood physical words; private endpoint families fixed per supplied gadget'}
 if res.x is not None:
  cand={vs[j] for j,a in enumerate(res.x) if a>.5};assert independent(cand) and not cand&h&v
  score=sum(grad[int(a in h)+2*int(a in v)] for a in cand);out.update(X=sorted(cand),main=sorted(i),PH=d['PH'],PV=d['PV'],profile=[367,len(d['PH']),len(cand),len(cand-(h|v)),len((cand&h)-v),len((cand&v)-h)],exact_weight_improved=score>oldscore)
  if len(cand)>=368:out['new_length5_record']=True
  sys.path.insert(0,str(HERE.parent/'published'))
  from shannon.construction import baselines,load_certificates,nth_root_digits
  led=load_certificates();led['base_gadget']['profile']=out['profile'];M=baselines(led)['bpz2_M'];out['M500']=M;out['bound']=nth_root_digits(M,500,30)
 name='auxiliary_orbit' if not gadget else 'new_private_auxiliary'
 (HERE/f'{name}_local{local}_milp_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--gadget');p.add_argument('--local',type=int,default=0);a=p.parse_args();run(a.gadget,a.local)
