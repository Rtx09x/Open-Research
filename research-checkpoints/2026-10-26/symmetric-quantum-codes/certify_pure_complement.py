"""Produce exact Farkas certificate for the pure/4-anticoherent subcase.
No numerical LP is needed; use the exact one-parameter equality elimination.
"""
import json
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
from intrinsic_lp import constraints
ROOT=Path(__file__).parent
n=18;N=19;M,H,A,b=constraints(n)
t=[sum(M[a,r] for a in range(3)) for r in range(N)]
L=s.diag(1,*[4*N*N*t[r]**2 for r in range(1,N)])
A=A.col_join(s.eye(N)[1:5,:]).col_join((M-s.eye(N))*L);b=b.col_join(s.zeros(4+N,1));G=s.Matrix.vstack(s.eye(N),H[5:,:])
red,piv=DomainMatrix.from_Matrix(A.row_join(b)).to_field().rref();red=red.to_Matrix()
assert piv==tuple(range(18))
p=s.Matrix(list(red[:18,19])+[0]);v=s.Matrix(list(-red[:18,18])+[1]);assert A*p==b and A*v==s.zeros(A.rows,1)
gp=G*p;gv=G*v
z=s.zeros(G.rows,1);z[8]=-gv[22];z[22]=gv[8]
margin=(z.T*gp)[0];assert margin<0 and (z.T*gv)[0]==0 and all(w>=0 for w in z)
z=z/(-margin)
# Select independent columns of A.T, i.e. a basis of equality rows.
_,rows=DomainMatrix.from_Matrix(A.T).to_field().rref();sub=A.T[:,list(rows)];rhs=G.T*z
rr,pp=DomainMatrix.from_Matrix(sub.row_join(rhs)).to_field().rref();rr=rr.to_Matrix();assert pp==tuple(range(len(rows)))
y=s.zeros(A.rows,1)
for i,row in enumerate(rows):y[row]=rr[i,-1]
assert A.T*y==G.T*z and (b.T*y)[0]==-1 and all(w>=0 for w in z)
out={'n':18,'condition':'a1=a2=a3=a4=0 (pure/4-anticoherent subcase ONLY)','A_rows':'e0,ones,H1..H4,e1..e4,(M-I)L rows0..18','G_rows':'I19,H5..H18','L_diagonal':[str(w)for w in L.diagonal()],'y':[str(w)for w in y],'z':[str(w)for w in z],'exact_verified':True,'proof':'A.T*y=G.T*z, z>=0, b.T*y=-1'}
(ROOT/'pure_complement_certificate.json').write_text(json.dumps(out,indent=2))
print('Pure/4-anticoherent n18 subcase excluded by exact Farkas certificate; no general exclusion.',flush=True)
