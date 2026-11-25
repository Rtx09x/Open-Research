"""Exact integer arithmetic check for finite sign spaces and sharp path example.
Matrix values, probes, and reconstructed entries remain exactly represented integers.
Equality checks are integer equalities, not floating tolerances.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import numpy as np,itertools,json
from tree_flow import reconstruct,predicted_error,dyadic_tree
rng=np.random.default_rng(91);out=[]
for L in [1,2]:
 n=2**(L+1);A=rng.integers(-3,4,size=(n,n));total=0;count=0
 for ss in itertools.product([-1,1],repeat=2*n):
  sig=np.array(ss[:n]);tau=np.array(ss[n:]);B=reconstruct(lambda x:A@x,lambda x:A.T@x,1,L,rng,signs=(sig,tau));assert np.array_equal(B,np.round(B));D=(A-B).astype(np.int64);total+=sum(int(v)**2 for v in D.ravel());count+=1
 edges,adj,pa,color,order=dyadic_tree(L)
 support={(i,i) for i in range(n)}|set(edges)|{(b,a) for a,b in edges}
 predicted=0
 for i in range(n):
  dist={i:0};q=[i]
  for a in q:
   for b in adj[a]:
    if b not in dist:dist[b]=dist[a]+1;q.append(b)
  for j in range(n):
   if (i,j) not in support:predicted+=(2 if color[i]==color[j] else 1+dist[j])*int(A[i,j])**2
 assert total==predicted*count,(L,total,predicted,count)
 d=dict(L=L,n=n,sign_assignments=count,total_integer_squared_error=total,exact_expected_error=predicted,identity_pass=True);out.append(d);print(d,flush=True)
for L in [1,2,4,7]:
 n=2**(L+1);A=np.zeros((n,n));i=n//2-1;j=n-1;A[i,j]=1
 for rep in range(20):
  B=reconstruct(lambda x:A@x,lambda x:A.T@x,1,L,rng);D=(A-B).astype(np.int64);err=sum(int(v)**2 for v in D.ravel());assert err==2*L+2,(L,err)
 d=dict(L=L,n=n,sharp_error=err,tree_optimal_error=1,full_HSS_optimal_error=0,twenty_sign_trials_pass=True);out.append(d);print(d,flush=True)
open('exact_tree_results.json','w').write(json.dumps(out,indent=2))
