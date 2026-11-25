"""Restricted no-go: n18 code cannot have time-reversal-invariant projector."""
from pathlib import Path
import json
import numpy as np
import sympy as s
from sympy.polys.matrices import DomainMatrix
from scipy.optimize import linprog
from intrinsic_lp import constraints
ROOT=Path(__file__).parent
n=18;M,H,A,b=constraints(n);A=A.col_join(s.eye(n+1)[1::2,:]);b=b.col_join(s.zeros(9,1));G=s.Matrix.vstack(s.eye(n+1),H[5:,:]);C=s.Matrix.hstack(A.T,-G.T).col_join(s.Matrix.hstack(b.T,s.zeros(1,G.rows)));rhs=s.zeros(C.rows,1);rhs[-1]=-1
r=linprog(np.zeros(C.cols),A_eq=np.array(C,dtype=float),b_eq=np.array(rhs,dtype=float).ravel(),bounds=[(None,None)]*A.rows+[(0,None)]*G.rows,method='highs',options={'threads':1});assert r.success
inds=[i for i,x in enumerate(r.x)if abs(x)>1e-9];red,piv=DomainMatrix.from_Matrix(C[:,inds].row_join(rhs)).to_field().rref();red=red.to_Matrix();assert piv==tuple(range(len(inds)))
f=s.zeros(C.cols,1)
for i,j in enumerate(inds):f[j]=red[i,-1]
y=f[:A.rows,0];z=f[A.rows:,0];assert A.T*y==G.T*z and (b.T*y)[0]==-1 and all(x>=0 for x in z)
(ROOT/'time_reversal_certificate.json').write_text(json.dumps({'n':18,'restriction':'odd intrinsic a_r=0 (time-reversal-invariant projector ONLY)','y':[str(x)for x in y],'z':[str(x)for x in z],'exact_verified':True},indent=2));print('Restricted time-reversal-invariant code excluded. This is a direct established LP corollary, novelty unconfirmed.')
