"""Dense small-instance reproduction of Levitt--Martinsson Algorithm 4.1.
Only oracle products consume A inside reused_hss; dense A is used by tests only.
No implementation is claimed as a novel algorithm. All ranks stay exactly k.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy.linalg import block_diag

def nullifier(x):
    return np.linalg.qr(x.T, mode='complete')[0][:,x.shape[0]:]
def topu(x,k):return np.linalg.svd(x,full_matrices=False)[0][:,:k]
def reused_hss(matvec,rmatvec,n,k,L,s,rng, fixed=None, trace=False, sketches=None):
    om,ps = sketches if sketches is not None else (rng.normal(size=(n,s)),rng.normal(size=(n,s)))
    y=matvec(om); z=rmatvec(ps)
    levels=[]; stats=[]
    for ell in range(L,0,-1):
        m=2*k; nb=2**ell
        us=[];vs=[];ds=[]
        for i in range(nb):
            sl=slice(i*m,(i+1)*m)
            oi=om[sl];pi=ps[sl];yi=y[sl];zi=z[sl]
            u,v=(fixed[L-ell][0][i],fixed[L-ell][1][i]) if fixed is not None else (topu(yi@nullifier(oi),k),topu(zi@nullifier(pi),k))
            pu=u@u.T;pv=v@v.T
            d=(np.eye(m)-pu)@yi@np.linalg.pinv(oi)+pu@((np.eye(m)-pv)@zi@np.linalg.pinv(pi)).T
            us.append(u);vs.append(v);ds.append(d)
        U=block_diag(*us);V=block_diag(*vs);D=block_diag(*ds)
        if trace:stats.append({'level':ell,'omega_norm2':float(np.linalg.norm(om)**2),'omega_rows':om.shape[0],'min_block_sval':float(min(np.linalg.svd(om[i*m:(i+1)*m],compute_uv=False)[-1] for i in range(nb)))})
        levels.append((U,V,D))
        y=U.T@(y-D@om);z=V.T@(z-D.T@ps)
        om=V.T@om;ps=U.T@ps
    B=y@np.linalg.pinv(om)
    for U,V,D in reversed(levels):B=U@B@V.T+D
    return B, {'queries':2*s,'trace':stats}

def make_hss(k,L,rng,scale=1):
    n=2**(L+1)*k;levels=[];fixed=[]
    for ell in range(L,0,-1):
        us=[np.linalg.qr(rng.normal(size=(2*k,k)))[0] for i in range(2**ell)]
        vs=[np.linalg.qr(rng.normal(size=(2*k,k)))[0] for i in range(2**ell)]
        U=block_diag(*us);V=block_diag(*vs)
        D=block_diag(*[rng.normal(size=(2*k,2*k))*scale for i in range(2**ell)])
        levels.append((U,V,D));fixed.append((us,vs))
    B=rng.normal(size=(2*k,2*k))*scale
    for U,V,D in reversed(levels):B=U@B@V.T+D
    return B,fixed

def hss_rank_check(B,k,L,tol=1e-8):
    n=B.shape[0];worst=0.
    for ell in range(1,L+1):
        m=n//2**ell
        for i in range(2**ell):
            sl=np.arange(i*m,(i+1)*m);other=np.r_[0:i*m,(i+1)*m:n]
            for x in [B[np.ix_(sl,other)],B[np.ix_(other,sl)]]:
                sv=np.linalg.svd(x,compute_uv=False)
                if len(sv)>k:worst=max(worst,float(sv[k]))
    return worst
