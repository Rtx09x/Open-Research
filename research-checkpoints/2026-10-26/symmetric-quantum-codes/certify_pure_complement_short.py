"""Restricted no-go needs only rank1 and3 complement equalities."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from sympy.polys.matrices import DomainMatrix
from scipy.optimize import linprog
from intrinsic_lp import constraints
ROOT=Path(__file__).parent;N=19;M,H,A,b=constraints(18);t=[sum(M[a,r]for a in range(3))for r in range(N)];L=s.diag(1,*[4*N*N*t[r]**2 for r in range(1,N)])
A=A.col_join(s.eye(N)[1:5,:]).col_join(((M-s.eye(N))*L)[[1,3],:]);b=b.col_join(s.zeros(6,1));G=s.Matrix.vstack(s.eye(N),H[5:,:]);C=s.Matrix.hstack(A.T,-G.T).col_join(s.Matrix.hstack(b.T,s.zeros(1,G.rows)));rhs=s.zeros(C.rows,1);rhs[-1]=-1
r=linprog(np.zeros(C.cols),A_eq=np.array(C,dtype=float),b_eq=np.array(rhs,dtype=float).ravel(),bounds=[(None,None)]*A.rows+[(0,None)]*G.rows,method='highs',options={'threads':1});assert r.success
inds=[i for i,x in enumerate(r.x)if abs(x)>1e-9];rr,piv=DomainMatrix.from_Matrix(C[:,inds].row_join(rhs)).to_field().rref();rr=rr.to_Matrix();assert piv==tuple(range(len(inds)))
v=s.zeros(C.cols,1)
for i,j in enumerate(inds):v[j]=rr[i,-1]
y=v[:A.rows,0];z=v[A.rows:,0];assert A.T*y==G.T*z and (b.T*y)[0]==-1 and all(a>=0 for a in z)
out={'n':18,'restriction':'a1=a2=a3=a4=0 ONLY','A_rows':'e0,ones,H1..H4,e1..e4,((M-I)L)1,3','G_rows':'I19,H5..H18','y':[str(a)for a in y],'z':[str(a)for a in z],'exact_verified':True};(ROOT/'pure_complement_short_certificate.json').write_text(json.dumps(out,indent=2));print('Exact certificate passed with complement rows1 and3 only.');print(out)
