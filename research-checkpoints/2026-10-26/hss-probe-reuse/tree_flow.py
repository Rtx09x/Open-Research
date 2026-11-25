"""Four-k-query robust reconstruction in a KNOWN block-tree HSS subclass.
Not a full HSS approximation algorithm: the comparator is fixed tree support.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np

def dyadic_tree(L):
    m=2**(L+1);edges=[]
    for width in [2**p for p in range(1,L+2)]:
        for lo in range(0,m,width):edges.append((lo,lo+width//2))
    adj=[[] for _ in range(m)]
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    parent=np.full(m,-1,dtype=int);color=np.zeros(m,dtype=int);order=[0]
    for a in order:
        for b in adj[a]:
            if b!=parent[a]:parent[b]=a;color[b]=1-color[a];order.append(b)
    return edges,adj,parent,color,order

def reconstruct(matvec,rmatvec,k,L,rng,signs=None):
    edges,adj,parent,color,order=dyadic_tree(L);m=len(color);n=m*k
    sig,tau = signs if signs is not None else (rng.choice([-1.,1.],m),rng.choice([-1.,1.],m))
    om=np.zeros((n,2*k));ps=om.copy()
    for i in range(m):
        om[i*k:(i+1)*k,color[i]*k:(color[i]+1)*k]=sig[i]*np.eye(k)
        ps[i*k:(i+1)*k,color[i]*k:(color[i]+1)*k]=tau[i]*np.eye(k)
    y=matvec(om);z=rmatvec(ps);B=np.zeros((n,n))
    for i in range(m):B[i*k:(i+1)*k,i*k:(i+1)*k]=y[i*k:(i+1)*k,color[i]*k:(color[i]+1)*k]/sig[i]
    # Each directed half-tree: row vertices of color c, column vertices color1-c.
    # Signed divergence is +row sums, -column sums.
    for c in [0,1]:
        d=np.zeros((m,k,k))
        for i in range(m):
            if color[i]==c:d[i]=tau[i]*y[i*k:(i+1)*k,(1-color[i])*k:(2-color[i])*k]
            else:d[i]=-sig[i]*z[i*k:(i+1)*k,(1-color[i])*k:(2-color[i])*k].T
        for child in reversed(order[1:]):
            par=parent[child]
            # Edge variable is oriented from row(color c) to column(color1-c).
            tail,head=(child,par) if color[child]==c else (par,child)
            b=d[child] if color[child]==c else -d[child]
            B[tail*k:(tail+1)*k,head*k:(head+1)*k]=b/(tau[tail]*sig[head])
            d[par]+=d[child]
        assert np.linalg.norm(d[0])<1e-8*(1+np.linalg.norm(y)+np.linalg.norm(z)), 'inconsistent data'
    return B

def support_mask(k,L):
    edges,adj,parent,color,order=dyadic_tree(L);m=len(color)
    small=np.eye(m,dtype=bool)
    for a,b in edges:small[a,b]=small[b,a]=True
    return np.kron(small,np.ones((k,k),dtype=bool))

def predicted_error(A,k,L):
    edges,adj,parent,color,order=dyadic_tree(L);m=len(color)
    mask=support_mask(k,L);E=np.where(mask,0.,A);total=np.linalg.norm(E)**2
    for i in range(m):
        dist=np.full(m,-1);dist[i]=0;q=[i]
        for a in q:
            for b in adj[a]:
                if dist[b]<0:dist[b]=dist[a]+1;q.append(b)
        for j in range(m):
            if not mask[i*k,j*k]:total+=(1 if color[i]==color[j] else dist[j])*np.linalg.norm(E[i*k:(i+1)*k,j*k:(j+1)*k])**2
    return float(total)

if __name__=='__main__':
 import json,itertools
 from baseline import hss_rank_check
 rng=np.random.default_rng(6718);out=[]
 for k,L,reps in [(1,1,256),(1,2,65536),(2,2,1024),(1,4,1024),(2,4,512),(1,7,128)]:
  n=2**(L+1)*k;A=rng.normal(size=(n,n));mask=support_mask(k,L);H=np.where(mask,A,0)
  E=A-H;vals=[];mxrank=0;exact=0
  # Monte Carlo independent sign pairs; analytic formula is checked separately.
  for r in range(reps):
   B=reconstruct(lambda x:A@x,lambda x:A.T@x,k,L,rng)
   vals.append(float(np.linalg.norm(A-B)**2))
   if r==0:
    mxrank=hss_rank_check(B,k,L)
    C=reconstruct(lambda x:H@x,lambda x:H.T@x,k,L,rng);exact=float(np.linalg.norm(C-H))
  d=dict(k=k,L=L,n=n,reps=reps,noise2=float(np.linalg.norm(E)**2),meanerr=float(np.mean(vals)),predicted=predicted_error(A,k,L),bound=float((2*L+2)*np.linalg.norm(E)**2),mean_ratio=float(np.mean(vals)/np.linalg.norm(E)**2),rank_tail=mxrank,exact_error=exact);out.append(d);print(d,flush=True)
 open('tree_flow_results.json','w').write(json.dumps(out,indent=2))
