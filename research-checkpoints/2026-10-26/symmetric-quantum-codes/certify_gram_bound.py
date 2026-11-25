"""Exact intrinsic LP bound forcing all nine degree-two syndromes independent."""
from pathlib import Path
import json
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j
from scipy.optimize import linprog
from intrinsic_lp import constraints
ROOT=Path(__file__).parent
n=18;N=n+1;j=s.Rational(n,2)
c=[]
for r in range(5):
 value=0
 for a in range(3):
  for b in range(3):
   if abs(a-b)<=r<=a+b:
    value+=(2*a+1)*(2*b+1)*wigner_6j(a,b,r,j,j,j)**2
 c.append(s.simplify(value))
print('exact c',c,flush=True)
M,H,A,b=constraints(n);G=s.Matrix.vstack(s.eye(N),H[5:,:]);obj=s.Matrix([0]+[v/N for v in c[1:]]+[0]*(n-4))
# Produce dual upper bound 1/(2N^2), slightly larger than optimum.
upper=s.Rational(1,2*N*N)
C=s.Matrix.hstack(A.T,-G.T);C=C.col_join(s.Matrix.hstack(b.T,s.zeros(1,G.rows)));target=obj.col_join(s.Matrix([upper]))
r=linprog(np.zeros(C.cols),A_eq=np.array(C,dtype=float),b_eq=np.array(target,dtype=float).ravel(),bounds=[(None,None)]*A.rows+[(0,None)]*G.rows,method='highs',options={'threads':1})
assert r.success,r.message
inds=[i for i,v in enumerate(r.x) if abs(v)>1e-9];sol,params=C[:,inds].gauss_jordan_solve(target)
if params.rows:sol=sol.subs({p:0 for p in params})
full=s.zeros(C.cols,1)
for i,v in zip(inds,sol):full[i]=v
y=full[:A.rows,0];z=full[A.rows:,0]
assert A.T*y-G.T*z==obj and (b.T*y)[0]==upper and all(v>=0 for v in z)
out={'n':18,'N':19,'d':5,'K':2,'c':[str(v) for v in c],'variance_objective':[str(v) for v in obj], 'upper_bound':str(upper),'y':[str(v) for v in y],'z':[str(v) for v in z],'exact_verified':True,'conclusion':'||G-I_9/19||_F^2 <= 1/(2*19^2); hence lambda_min(G)>=(1-1/sqrt(2))/19>0.'}
(ROOT/'gram_bound_exact_certificate.json').write_text(json.dumps(out,indent=2))
print('Certified variance upper',upper,'<',s.Rational(1,N*N),flush=True)
