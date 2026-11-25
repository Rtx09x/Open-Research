"""Bounded actual-matvec controls for scalar width3 LM; numerical only."""
import json,time
import numpy as np
from scipy.linalg import block_diag
from fixed_basis_algorithm import complement,project
from global_ls_probe import frames
from coordinate_observation_forest import structure


def reconstruct(A,fixed,s,rng):
 om,ps=frames(fixed,'v',1,s,rng),frames(fixed,'u',1,s,rng)
 counts=[0,0]
 def mv(v):counts[0]+=1;return A@v
 def rmv(v):counts[1]+=1;return A.T@v
 Y=np.column_stack([mv(om[:,j]) for j in range(s)])
 Z=np.column_stack([rmv(ps[:,j]) for j in range(s)])
 levels=[]
 for us,vs in fixed:
  U,V=block_diag(*us),block_diag(*vs);D=np.zeros((len(om),len(om)))
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu,pv=u@u.T,v@v.T
   D[sl,sl]=(np.eye(2)-pu)@Y[sl]@om[sl].T+pu@((np.eye(2)-pv)@Z[sl]@ps[sl].T).T
  levels.append((U,V,D));Y,Z=U.T@(Y-D@om),V.T@(Z-D.T@ps);om,ps=V.T@om,U.T@ps
 B=Y@om.T
 for U,V,D in reversed(levels):B=U@B@V.T+D
 assert counts==[s,s]
 return B


def main():
 rng=np.random.default_rng(197332);out=[];start=time.monotonic()
 for L in [1,2,3,4,5]:
  n=2**(L+1)
  for kind in ['coordinate','dense']:
   fixed=[tuple([np.eye(2)[:,:1] if kind=='coordinate' else np.linalg.qr(rng.normal(size=(2,1)))[0] for i in range(2**ell)] for bank in range(2)) for ell in range(L,0,-1)]
   A=rng.normal(size=(n,n));H=project(A,fixed);E=A-H;E/=np.linalg.norm(E)
   assert np.linalg.norm(reconstruct(H,fixed,3,rng)-H)<1e-9
   if kind=='coordinate':
    bases=[([0]*2**ell,[0]*2**ell) for ell in range(L,0,-1)]
    *_,edges,w=structure(bases);w=w.copy()
    for i,j,_ in edges:w[i,j]=-1
    i,j=np.unravel_index(w.argmax(),w.shape);E=np.zeros((n,n));E[i,j]=1
   for s in [2,3]:
    vals=[]
    for trial in range(80):
     B=reconstruct(E,fixed,s,rng);vals.append(float(np.linalg.norm(E-B)**2))
     if trial==0:assert np.linalg.norm(project(B,fixed)-B)<1e-9
    row=dict(L=L,n=n,bases=kind,width=s,matvecs_each_direction=s,trials=len(vals),mean_error_factor=float(np.mean(vals)),max_error_factor=float(max(vals)),standard_error=float(np.std(vals)/np.sqrt(len(vals))))
    if kind=='coordinate' and s==2:row['known_exact_width2_mean']=1+int(w.max());assert abs(np.mean(vals)-row['known_exact_width2_mean'])<1e-9
    out.append(row);print(json.dumps(row),flush=True)
    open('scalar_wide_reconstruction_results.json','w').write(json.dumps(dict(status='NUMERICAL_CONTROLS_NOT_PROOF',seconds=time.monotonic()-start,results=out),indent=2)+'\n')

if __name__=='__main__':main()
