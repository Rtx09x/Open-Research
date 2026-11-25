"""Exact spinor invariant controls over Q(i), including all boundary strata."""
import json,time
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
N=19;j=9;p=19;I=s.I
Jp=s.MutableSparseMatrix(N,N,{(w+1,w):18-w for w in range(18)})
Jm=s.MutableSparseMatrix(N,N,{(w,w+1):w+1 for w in range(18)})
J=[(Jp+Jm)/2,(Jp-Jm)/(2*I),s.diag(*range(-9,10))]
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]

def invariant(A):
 d=A[0].rows;T=s.MutableSparseMatrix.vstack(s.MutableSparseMatrix.hstack(j*s.eye(d)-A[2],A[0]-I*A[1]),s.MutableSparseMatrix.hstack(A[0]+I*A[1],j*s.eye(d)+A[2]));S=p*T-T*T
 t=s.trace(S);S2=S*S;S3=S2*S;B=[s.kronecker_product(sig,s.eye(d))for sig in pauli]
 SB=[S*b for b in B];H=s.Matrix(3,3,lambda a,b:2*s.trace(SB[a]*SB[b])-s.trace(SB[a])*s.trace(SB[b]));delta=2*I*s.trace(SB[0]*SB[1]*SB[2]-SB[0]*SB[2]*SB[1])
 F=s.simplify((t**4-2*t*t*s.trace(H)-8*t*delta+2*s.trace(H*H)-s.trace(H)**2)/16)
 return {'rankT':DomainMatrix.from_Matrix(T).rank(),'rankS':DomainMatrix.from_Matrix(S).rank(),'e3':str(s.simplify((t**3-3*t*s.trace(S2)+2*s.trace(S3))/6)),'cubic_branch':str(s.simplify(s.trace(T*T*T)-30*s.trace(T*T)+67536)),'orientation_F':str(F),'traceS':str(t)}

start=time.time();out={}
for name,omit in [('coherent',18),('m_zero',9)]:
 inds=[a for a in range(N)if a!=omit];A=[M.extract(inds,inds)for M in J];out[name]=invariant(A)
# Rational orthogonal (not normalized) basis for q=e0+e1 in metric diag(1/C18w).
U=s.zeros(N);U[0,0]=1;U[1,0]=-18
for k in range(1,18):U[k+1,k]=1
U[0,18]=1;U[1,18]=1
A=[(U.inv()*M*U)[:18,:18]for M in J];out['rank3_generic_rational_q']=invariant(A)
for row in out.values():assert row['rankT']==18 and row['rankS']in[1,2]and row['e3']==row['cubic_branch']==row['orientation_F']=='0'
out['elapsed_seconds']=time.time()-start
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
