"""One-CPU small controls for the analytic path inverse lemma, not its proof."""
import json, math
import numpy as np


def bank(n,s,rng):
    x=np.zeros((n,s));x[0,0]=1
    if n>1:x[1,1]=1
    for i in range(2,n):
        z=rng.normal(size=s);z-=x[i-1]*np.dot(z,x[i-1]);x[i]=z/np.linalg.norm(z)
    return x


def main():
    rng=np.random.default_rng(737519)
    physical=[]
    for n in [3,4,9,16]:
        om,ps=bank(n,4,rng),bank(n,4,rng)
        support=[(i,i) for i in range(n)] + [(i,i+1) for i in range(n-1)]+[(i+1,i) for i in range(n-1)]
        mm=[]
        for i,j in support:
            b=np.zeros((n,n));b[i,j]=1
            mm.append(np.r_[(b@om).ravel(),(b.T@ps).ravel()])
        mm=np.array(mm);g=mm@mm.T
        assert np.max(np.abs(np.diag(g)-2))<1e-12
        assert np.max(np.abs(g[:n,n:]))<1e-12
        expected=np.zeros_like(g)
        for a,(i,j) in enumerate(support):
          for b,(h,l) in enumerate(support):
            expected[a,b]=(np.dot(om[j],om[l]) if i==h else 0)+(np.dot(ps[i],ps[h]) if j==l else 0)
        assert np.max(np.abs(g-expected))<1e-12
        edgeg=g[n:,n:]
        degree=np.sum(np.abs(edgeg-np.diag(np.diag(edgeg)))>1e-12,axis=1)
        assert max(degree)<=2
        physical.append(dict(n=n,coefficient_count=len(support),gram_identity_error=float(np.max(np.abs(g-expected)))))
    trials=20000;rows=[]
    # Tridiagonal inverse diagonal via independent left/right Schur pivots.
    # This uses the analytically derived iid turn law, separate from physical check.
    for m in [2,4,8,32,128]:
        c=rng.uniform(-1,1,size=(trials,m-1));left=np.full((trials,m),2.0);right=left.copy()
        for i in range(1,m):left[:,i]=2-c[:,i-1]**2/left[:,i-1]
        for i in range(m-2,-1,-1):right[:,i]=2-c[:,i]**2/right[:,i+1]
        den=np.full((trials,m),2.0)
        den[:,1:]-=c*c/left[:,:-1];den[:,:-1]-=c*c/right[:,1:]
        invdiag=1/den
        rows.append(dict(chain_length=m,trials=trials,max_empirical_mean_inverse_diagonal=float(invdiag.mean(axis=0).max()),analytic_upper_bound=math.pi**2/8))
    result=dict(status='NUMERICAL_CONTROLS_NOT_PROOF',physical=physical,inverse_moments=rows)
    print(json.dumps(result,indent=2))
    with open('path_global_ls_inverse_results.json','w') as f:json.dump(result,f,indent=2)

if __name__=='__main__':main()
