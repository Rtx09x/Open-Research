"""Exploratory global fixed-class least squares, NOT the proved LM decoder.
One CPU, n<=32 default. Explicit atom matrices for a small-test implementation.
"""
import argparse, json, time
import numpy as np
from scipy.linalg import block_diag
from fixed_basis_algorithm import complement


def atoms(fixed, k):
    if not fixed:
        return np.eye(4*k*k).reshape(4*k*k,2*k,2*k)
    us,vs=fixed[0]; n=2*k*len(us)
    u,v=block_diag(*us),block_diag(*vs)
    out=[]
    for i,(ui,vi) in enumerate(zip(us,vs)):
        wu,wv=complement(ui),complement(vi)
        for left,right in [(wu,vi),(wu,wv),(ui,wv)]:
            for a in range(k):
                for b in range(k):
                    atom=np.zeros((n,n));sl=slice(2*k*i,2*k*(i+1))
                    atom[sl,sl]=np.outer(left[:,a],right[:,b]);out.append(atom)
    out.extend(u@c@v.T for c in atoms(fixed[1:],k))
    return np.array(out)


def frames(fixed,side,k,s,rng):
    rows=np.eye(s)[:2*k]
    for us,vs in reversed(fixed):
        out=[]
        for i,b in enumerate(us if side=='u' else vs):
            active=rows[k*i:k*(i+1)]
            ambient=complement(active.T)
            q,r=np.linalg.qr(rng.normal(size=(s-k,k)))
            q=q*np.where(np.diag(r)<0,-1,1)[None,:]
            detail=q.T@ambient.T
            out.append(b@active+complement(b)@detail)
        rows=np.vstack(out)
    return rows


def leakage(aa,om,ps):
    """Rows of J map off-class input to coefficient error; Gram is exact."""
    d,n,_=aa.shape
    gradients=aa@(om@om.T)+(ps@ps.T)@aa
    gram=gradients.reshape(d,-1)@aa.reshape(d,-1).T
    eig=np.linalg.eigvalsh(gram)
    h=np.linalg.solve(gram,gradients.reshape(d,-1))
    j=h-aa.reshape(d,-1)
    assert np.linalg.norm(j@aa.reshape(d,-1).T)<1e-9
    return j,eig


def main():
    p=argparse.ArgumentParser();p.add_argument('--trials',type=int,default=120)
    p.add_argument('--max-depth',type=int,default=3);p.add_argument('--output',default='global_ls_results.json')
    a=p.parse_args();rng=np.random.default_rng(10928);results=[];start=time.monotonic()
    for kind in ['coordinate','dense']:
      for L in range(1,a.max_depth+1):
        k=1;n=2**(L+1)
        fixed=[]
        for ell in range(L,0,-1):
          fixed.append(tuple([np.eye(2)[:,:1] if kind=='coordinate' else np.linalg.qr(rng.normal(size=(2,1)))[0]
                              for _ in range(2**ell)] for side in range(2)))
        aa=atoms(fixed,k);d=len(aa)
        assert np.linalg.norm(aa.reshape(d,-1)@aa.reshape(d,-1).T-np.eye(d))<1e-10
        for s in [2,3,4]:
          cov=np.zeros((n*n,n*n));mineig=[];traces=[]
          for trial in range(a.trials):
            om,ps=frames(fixed,'v',k,s,rng),frames(fixed,'u',k,s,rng)
            j,eig=leakage(aa,om,ps)
            cov+=j.T@j/a.trials;mineig.append(float(eig[0]));traces.append(float(np.linalg.norm(j)**2))
          lam=float(np.linalg.eigvalsh(cov)[-1])
          row=dict(kind=kind,L=L,n=n,k=k,s=s,total_queries=2*s,trials=a.trials,
                   empirical_worst_error_factor=1+lam,
                   mean_isotropic_error_factor=1+float(np.trace(cov))/(n*n-d),
                   minimum_observed_gram_eigenvalue=min(mineig),
                   mean_observed_gram_min_eigenvalue=float(np.mean(mineig)),
                   largest_observed_leakage_trace=max(traces))
          results.append(row);print(json.dumps(row),flush=True)
          with open(a.output,'w') as f:json.dump(dict(status='EXPLORATORY_NOT_PROOF',elapsed_seconds=time.monotonic()-start,results=results),f,indent=2)


if __name__=='__main__':main()
