"""Actual6k matvec numerical controls for the uniformly-mixing restricted theorem.
Both Haar and explicitly gauged signed-permutation full-complement laws.
"""
import numpy as np,json,time
from scipy.linalg import block_diag
from fixed_basis_algorithm import complement,project,haar

def make_bases(k,L,delta,rng):
 out=[]
 for ell in range(L,0,-1):
  pair=[]
  for bank in range(2):
   bb=[]
   for i in range(2**ell):
    cs=rng.uniform(delta,np.sqrt(1-delta**2),k);ss=np.sqrt(1-cs*cs)
    left,right,gauge=haar(k,rng),haar(k,rng),haar(k,rng)
    b=np.vstack([left@np.diag(cs),right@np.diag(ss)])@gauge
    assert np.linalg.norm(b.T@b-np.eye(k))<1e-10
    assert min(np.linalg.svd(b[:k],compute_uv=False).min(),np.linalg.svd(b[k:],compute_uv=False).min())>=delta-1e-12
    bb.append(b)
   pair.append(bb)
  out.append(tuple(pair))
 return out

def frames_complete(fixed,side,k,s,rng,law):
 E=np.eye(s);incoming=[(E[:k],E[k:]),(E[k:2*k],np.vstack([E[:k],E[2*k:]]))]
 for pair in reversed(fixed):
  nxt=[];rows=[]
  for b,(F,C0) in zip(pair[side],incoming):
   d=s-k;H=haar(d,rng) if law=='haar' else np.eye(d)[rng.permutation(d)]*rng.choice([-1.,1.],d)[:,None]
   C=H@C0;G,J=C[:k],C[k:];local=b@F+complement(b)@G;f0,f1=local[:k],local[k:]
   assert np.linalg.norm(local@local.T-np.eye(2*k))<1e-9
   rows.append(local);nxt.extend([(f0,np.vstack([f1,J])),(f1,np.vstack([f0,J]))])
  incoming=nxt
 return np.vstack(rows)

def reconstruct(A,fixed,k,rng,law):
 s=3*k;om,ps=frames_complete(fixed,1,k,s,rng,law),frames_complete(fixed,0,k,s,rng,law);counts=[0,0]
 def mv(x):counts[0]+=1;return A@x
 def tmv(x):counts[1]+=1;return A.T@x
 Y=np.column_stack([mv(om[:,i]) for i in range(s)]);Z=np.column_stack([tmv(ps[:,i]) for i in range(s)]);levels=[]
 for us,vs in fixed:
  U,V=block_diag(*us),block_diag(*vs);D=np.zeros((len(om),len(om)))
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*k*i,2*k*(i+1));pu,pv=u@u.T,v@v.T
   D[sl,sl]=(np.eye(2*k)-pu)@Y[sl]@om[sl].T+pu@((np.eye(2*k)-pv)@Z[sl]@ps[sl].T).T
  levels.append((U,V,D));Y,Z=U.T@(Y-D@om),V.T@(Z-D.T@ps);om,ps=V.T@om,U.T@ps
 B=Y@om.T
 for U,V,D in reversed(levels):B=U@B@V.T+D
 assert counts==[3*k,3*k]
 return B

def main():
 rng=np.random.default_rng(556024);rows=[];start=time.monotonic();delta=.5
 for k in [1,2,3,4]:
  for L in [1,2,3,4]:
   fixed=make_bases(k,L,delta,rng);n=2**(L+1)*k;A=rng.normal(size=(n,n));H=project(A,fixed);E=A-H;E/=np.linalg.norm(E)
   for law in ['haar','signed_permutation']:
    defect=np.linalg.norm(reconstruct(H,fixed,k,rng,law)-H);assert defect<1e-8
    vals=[];ranges=[]
    for trial in range(24):
     B=reconstruct(E,fixed,k,rng,law);vals.append(float(np.linalg.norm(E-B)**2))
     if trial==0:ranges.append(float(np.linalg.norm(B-project(B,fixed))));assert ranges[-1]<1e-8
    row=dict(k=k,L=L,n=n,delta=delta,law=law,forward_queries=3*k,transpose_queries=3*k,trials=len(vals),mean_error_factor=float(np.mean(vals)),standard_error=float(np.std(vals)/np.sqrt(len(vals))),max_error_factor=float(max(vals)),exact_on_model_defect=float(defect),range_defect=max(ranges))
    rows.append(row);print(json.dumps(row),flush=True)
    open('uniform_mixing_fixed_basis_results.json','w').write(json.dumps(dict(status='NUMERICAL_PHYSICAL_QUERY_CONTROLS_NOT_PROOF',elapsed_seconds=time.monotonic()-start,rows=rows),indent=2)+'\n')
if __name__=='__main__':main()
