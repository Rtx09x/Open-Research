"""Exact equality reduction of the pure subcase, without numerical LP trust."""
import json
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
from intrinsic_lp import constraints
ROOT=Path(__file__).parent
n=18;N=19;M,H,A,b=constraints(n)
t=[sum(M[a,r] for a in range(3)) for r in range(N)];L=s.diag(1,*[4*N*N*t[r]**2 for r in range(1,N)])
A=A.col_join(s.eye(N)[1:5,:]).col_join((M-s.eye(N))*L);b=b.col_join(s.zeros(4+N,1))
red,piv=DomainMatrix.from_Matrix(A.row_join(b)).to_field().rref();red=red.to_Matrix()
print('pivots',piv,flush=True)
assert N not in piv
free=[i for i in range(N) if i not in piv];print('free',free)
assert len(free)==1
p=s.zeros(N,1);v=s.zeros(N,1);v[free[0]]=1
for row,i in enumerate(piv):p[i]=red[row,N];v[i]=-red[row,free[0]]
G=s.Matrix.vstack(s.eye(N),H[5:,:]);gp=G*p;gv=G*v
lo=[];hi=[];contradictions=[]
for i,(a,b) in enumerate(zip(gp,gv)):
 if b>0:lo.append((-a/b,i))
 elif b<0:hi.append((-a/b,i))
 elif a<0:contradictions.append(i)
print('contradictions',contradictions)
print('lower',max(lo));print('upper',min(hi))
print('p',list(p));print('v',list(v))
(ROOT/'pure_complement_elimination.json').write_text(json.dumps({'free_coordinate':free[0],'p':[str(x)for x in p],'v':[str(x)for x in v],'lower':[str(x)for x in max(lo)],'upper':[str(x)for x in min(hi)],'contradictions':contradictions},indent=2))
