"""Separate exact-integer physical-block decoder control for external4L claim.
Checks the stronger pointwise formula L+2(sum tau_j)^2 for coefficient energy.
No imported consultation code. Random sign cases are controls, not the proof.
"""
import json
import numpy as np
from fractions import Fraction as F
from verify_greedy_bridge_independent import select


def basis(L):
 n=2**(L+1);a={(2**j,2**L):F(1) for j in range(L)};a[0,3*2**(L-1)]=F(3,2)
 out=[]
 for t in range(L):
  us,_=select(a,n);vs,_=select(a,n,True)
  out.append(([r%2 for r in us],[c%2 for c in vs]))
  u={r:i for i,r in enumerate(us)};v={c:i for i,c in enumerate(vs)}
  a={(u[r],v[c]):x for (r,c),x in a.items() if r in u and c in v};n//=2
 return out


def probe(bas,side,rng):
 rows=np.eye(2,dtype=np.int64)
 for pair in reversed(bas):
  chosen=pair[side];new=np.zeros((2*len(chosen),2),dtype=np.int64)
  for i,active in enumerate(chosen):
   f=rows[i];g=int(rng.choice([-1,1]))*np.array([-f[1],f[0]])
   new[2*i+active]=f;new[2*i+1-active]=g
  rows=new
 return rows


def run(L,rng):
 bas=basis(L);om=probe(bas,1,rng);ps=probe(bas,0,rng);n=len(om);w=2**L
 signals=[2**j for j in range(L)]
 assert np.all(ps[signals,0]==0) and abs(om[w,0])==1 and om[w,1]==0
 tau=ps[signals,1].copy();y=np.zeros_like(om);z=np.zeros_like(ps)
 y[signals]=om[w];z[w]=ps[signals].sum(axis=0)
 costs=[]
 for u,v in bas:
  ny=[];nz=[];no=[];np_=[];cost=0
  for i,(ua,va) in enumerate(zip(u,v)):
   yy,zz=y[2*i:2*i+2],z[2*i:2*i+2];oo,pp=om[2*i:2*i+2],ps[2*i:2*i+2]
   d=np.zeros((2,2),dtype=np.int64)
   for r in range(2):
    for c in range(2):
     if r!=ua:d[r,c]=yy[r]@oo[c]
     elif c!=va:d[r,c]=zz[c]@pp[r]
   cost+=int(np.sum(d*d));ny.append((yy-d@oo)[ua]);nz.append((zz-d.T@pp)[va]);no.append(oo[va]);np_.append(pp[ua])
  costs.append(cost);y,z,om,ps=map(np.array,(ny,nz,no,np_))
 root=y@om.T;costs.append(int(np.sum(root*root)))
 T=int(tau.sum());assert costs==[1]*(L-1)+[1+T*T,T*T]
 assert sum(costs)==L+2*T*T
 return costs


def main():
 rng=np.random.default_rng(842135);rows=[]
 for L in range(3,11):
  trials=80;costs=[run(L,rng) for _ in range(trials)]
  rows.append(dict(L=L,trials=trials,pointwise_identity_pass=True,
                   exact_expectation_by_independent_sign_identity=3*L,
                   numerical_mean_coefficient_energy=float(np.mean(np.sum(costs,axis=1)))))
 report=dict(status='PASS',arithmetic='int64; values far below overflow',
             numerical_sign_sampling_only=True,pointwise_formula='L+2(sum_j tau_j)^2',results=rows)
 with open('greedy_coefficient_independent_results.json','w') as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2))


if __name__=='__main__':main()
