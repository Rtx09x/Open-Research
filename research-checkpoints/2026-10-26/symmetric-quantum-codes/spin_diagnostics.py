"""Numerical diagnostics only: irreducible tensors, known-code enumerators."""
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from intrinsic_lp import constraints
ROOT=Path(__file__).parent

def tensors(n):
 N=n+1;j=n/2
 Jp=np.diag([math.sqrt((n-w)*(w+1)) for w in range(n)],-1);Jm=Jp.T
 out=[]
 for r in range(n+1):
  top=np.linalg.matrix_power(Jp,r).copy();top/=np.linalg.norm(top);sect=[top]
  for m in range(r,-r,-1):
   top=(Jm@top-top@Jm)/math.sqrt((r+m)*(r-m+1));sect.append(top)
  out.append(sect)
 return out

def code19():
 root=json.loads((ROOT/'code19_root_certificate.json').read_text());q=np.array([1.]+[float(__import__('fractions').Fraction(x)) for x in root['center']]);v=np.zeros(20);v[::2]=q*np.sqrt([math.comb(19,w) for w in range(0,20,2)]);v/=np.linalg.norm(v);return np.array([v,v[::-1]]).T

def diagnostics():
 C=code19();P=C@C.T;T=tensors(19);A=[];B=[]
 for sect in T:
  A.append(5*sum(np.trace(P@t)**2 for t in sect))
  B.append(10*sum(np.linalg.norm(C.T@t@C)**2 for t in sect))
 errors=np.array([t for sect in T[:3] for t in sect]);vec=np.array([e@C[:,0] for e in errors]);G=vec@vec.T
 print('19 A',A);print('19 max KL lowrank',max(abs(a-b) for a,b in zip(A[:5],B[:5])));print('G eigen',np.linalg.eigvalsh(G))
 M,H,Aeq,b=constraints(18);H=np.array(H,dtype=float);Ae=np.array(Aeq,dtype=float);be=np.array(b,dtype=float).ravel()
 ranges=[]
 for k in range(1,10):
  c=np.zeros(19);c[k]=-1
  r=linprog(c,A_ub=-H,b_ub=np.zeros(19),A_eq=Ae,b_eq=be,bounds=(0,None),method='highs',options={'threads':1})
  ranges.append([k,-r.fun])
 print('n18 A_r upper',ranges)
 (ROOT/'spin_diagnostics.json').write_text(json.dumps({'code19_A':A,'code19_B':B,'code19_G_eigenvalues':np.linalg.eigvalsh(G).tolist(),'n18_Ar_upper':ranges},indent=2))
if __name__=='__main__':diagnostics()
