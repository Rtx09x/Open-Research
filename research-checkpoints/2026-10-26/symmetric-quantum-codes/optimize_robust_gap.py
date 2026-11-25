"""Optimize a rigorous perturbative exclusion bound; exploratory LP then exact replay."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import linprog
from sympy.polys.matrices import DomainMatrix
from intrinsic_lp import constraints
ROOT=Path(__file__).parent;N=19
M,H,A,b=constraints(18);c=[s.Rational(91,285),s.Rational(288199,1187025),s.Rational(33176,237405),s.Rational(10120,142443)];t=[sum(M[a,r]for a in range(3))for r in range(N)];L=s.diag(1,*[4*N*N*t[r]**2 for r in range(1,N)])
A=A.col_join(s.eye(N)[1:5,:]).col_join((M-s.eye(N))*L);b=b.col_join(s.zeros(23,1));G=s.Matrix.vstack(s.eye(N),H[5:,:]);ny=A.rows;nz=G.rows;nv=ny+nz+2
C=s.Matrix.hstack(A.T,-G.T,s.zeros(N,2));C=C.col_join(s.Matrix.hstack(b.T,s.zeros(1,nz+2)));target=s.zeros(N+1,1);target[-1]=-1
U=[]
for r in range(4):
 row=[s.Integer(0)]*nv;row[6+r]=N;row[-2]=-c[r];U.append(row)
for k in range(N):
 for sign in [-1,1]:
  row=[s.Integer(0)]*nv
  for r in range(N):row[10+r]=sign*(M[r,k]-(1 if r==k else 0))
  row[-1]=-1;U.append(row)
U=s.Matrix(U)
def solve(q):
 obj=np.zeros(nv);obj[-2]=float(q*q);obj[-1]=float(N*(3*N*q+2*N*N*q*q))
 return linprog(obj,A_ub=np.array(U,dtype=float),b_ub=np.zeros(U.rows),A_eq=np.array(C,dtype=float),b_eq=np.array(target,dtype=float).ravel(),bounds=[(None,None)]*ny+[(0,None)]*(nz+2),method='highs',options={'threads':1})
for den in [500,400,350,330,320,310,300,250]:
 q=s.Rational(1,den);r=solve(q);print('q',q,'nu',q*q,'bound',r.fun,flush=True)
 if r.success and r.fun<.99:last=(q,r)
q,r=last
# Exact vertex reconstruction with equality, zero nonnegative variables, active inequalities.
rows=[C];vals=[target]
for i in range(ny,nv):
 if abs(r.x[i])<1e-8:rows.append(s.eye(nv)[i:i+1,:]);vals.append(s.zeros(1,1))
res=np.array(U,dtype=float)@r.x
for i,val in enumerate(res):
 if abs(val)<1e-7:rows.append(U[i:i+1,:]);vals.append(s.zeros(1,1))
D=s.Matrix.vstack(*rows);v=s.Matrix.vstack(*vals);rr,piv=DomainMatrix.from_Matrix(D.row_join(v)).to_field().rref();rr=rr.to_Matrix()
assert nv not in piv
sol=s.zeros(nv,1)
for row,i in enumerate(piv):sol[i]=rr[row,-1]
assert C*sol==target and all(x<=0 for x in U*sol) and all(x>=0 for x in sol[ny:])
bound=sol[-2]*q*q+sol[-1]*N*(3*N*q+2*N*N*q*q);assert bound<1
out={'q':str(q),'strict_variance_lower_bound':str(q*q),'rational_bound':str(bound),'bound_float':str(bound.evalf()),'y':[str(x)for x in sol[:ny]],'z':[str(x)for x in sol[ny:ny+nz]],'A':str(sol[-2]),'w':str(sol[-1]),'exact_verified':True,'restriction':'unrestricted n18 codes; perturbative inequality, not full exclusion'}
(ROOT/'optimized_robust_gap_certificate.json').write_text(json.dumps(out,indent=2));print('EXACT',out['strict_variance_lower_bound'],out['bound_float'])
