"""Intrinsic SU(2) LP for general complex PI quantum codes; no PR ansatz."""
import json, time
from pathlib import Path
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j
from scipy.optimize import linprog
ROOT=Path(__file__).parent

def transform(n):
 j=s.Rational(n,2)
 return s.Matrix(n+1,n+1,lambda r,k:(-1)**(n+r+k)*(2*r+1)*wigner_6j(j,j,r,j,j,k))

def constraints(n,d=5,K=2):
 M=transform(n); H=K*M-s.eye(n+1)
 # normalized A0=1 and sum A=N/K; constraints H A >= 0, H[1:d] A=0
 Aeq=s.Matrix.vstack(s.eye(n+1)[:1,:],s.ones(1,n+1),H[1:d,:]); beq=s.Matrix([1,s.Rational(n+1,K)]+[0]*(d-1))
 return M,H,Aeq,beq

def solve(n,d=5,K=2):
 M,H,A,b=constraints(n,d,K)
 r=linprog(np.zeros(n+1),A_ub=-np.array(H,dtype=float),b_ub=np.zeros(n+1),A_eq=np.array(A,dtype=float),b_eq=np.array(b,dtype=float).ravel(),bounds=(0,None),method='highs',options={'threads':1})
 out={'n':n,'d':d,'K':K,'success':r.success,'status':r.message}
 if r.success:out['A']=r.x.tolist()
 return out
if __name__=='__main__':
 out=[]
 for n in range(4,20):
  row=solve(n,3 if n<9 else 5);out.append(row);print(row,flush=True)
 (ROOT/'intrinsic_lp_scan.json').write_text(json.dumps(out,indent=2))
