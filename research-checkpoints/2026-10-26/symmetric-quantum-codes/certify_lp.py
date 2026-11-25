"""Produce exact Farkas proofs, then check with rational SymPy arithmetic."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import linprog
from intrinsic_lp import constraints
ROOT=Path(__file__).parent

def certificate(n,d=5):
 M,H,A,b=constraints(n,d)
 G=s.Matrix.vstack(s.eye(n+1),H[d:,:])
 # Find y free and z>=0: A.T y = G.T z, b.T y = -1.
 C=s.Matrix.hstack(A.T,-G.T)
 C=C.col_join(s.Matrix.hstack(b.T,s.zeros(1,G.rows)))
 target=s.zeros(C.rows,1);target[-1]=-1
 cf=np.array(C,dtype=float);tf=np.array(target,dtype=float).ravel()
 r=linprog(np.zeros(C.cols),A_eq=cf,b_eq=tf,bounds=[(None,None)]*A.rows+[(0,None)]*G.rows,method='highs',options={'threads':1})
 if not r.success: return {'n':n,'success':False,'status':r.message}
 inds=[i for i,v in enumerate(r.x) if abs(v)>1e-8]
 # Exact sparse solve on nonzero support returned by LP.
 sub=C[:,inds]
 sol,params=sub.gauss_jordan_solve(target)
 if params.rows: sol=sol.subs({p:0 for p in params})
 full=s.zeros(C.cols,1)
 for i,v in zip(inds,sol):full[i]=v
 y=full[:A.rows,0];z=full[A.rows:,0]
 assert A.T*y==G.T*z and (b.T*y)[0]==-1
 assert all(v>=0 for v in z)
 return {'n':n,'d':d,'success':True,'y':[str(v) for v in y],'z':[str(v) for v in z], 'margin': '-1','proof':'A.T*y=G.T*z, z>=0, b.T*y=-1 contradict G*x>=0 and A*x=b.'}

if __name__=='__main__':
 out=[]
 for n in range(9,18):
  c=certificate(n);out.append(c);print(n,c['success'],c.get('y'),flush=True)
 (ROOT/'lp_exact_certificates.json').write_text(json.dumps(out,indent=2))
