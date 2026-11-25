"""Independent direct-CG check of the third-factor rank-one channel.

No worker imports. SymPy supplies only exact CG/6j arithmetic; the channel is
built directly from raising/lowering matrices on the last physical spin.
"""
from pathlib import Path
from functools import lru_cache
import json, time
import sympy as s
from sympy.physics.wigner import clebsch_gordan, wigner_6j

start=time.time()
def weights(j): return [s.Rational(-j)+i for i in range(int(2*j+1))]
@lru_cache(None)
def intertwiner(j,L,Lp,J):
    left=[(m,n) for m in weights(L) for n in weights(j)]
    right=[(m,n) for m in weights(Lp) for n in weights(j)]
    U=s.Matrix([[clebsch_gordan(L,j,J,m,n,M) for M in weights(J)] for m,n in left])
    V=s.Matrix([[clebsch_gordan(Lp,j,J,m,n,M) for M in weights(J)] for m,n in right])
    return U*V.T
def spin(j):
    ms=weights(j); d=len(ms); plus=s.zeros(d)
    for a,m in enumerate(ms[:-1]): plus[a+1,a]=s.sqrt((j-m)*(j+m+1))
    return s.diag(*ms),plus,plus.T

rows=[]
for j,L,Lp in [(s.Rational(1,2),0,1),(s.Integer(1),0,1),(s.Integer(1),1,1),(s.Integer(1),1,2),(s.Rational(3,2),1,2)]:
    js=[abs(L-j)+i for i in range(int(2*min(L,j)+1))]
    js=[J for J in js if abs(Lp-j)<=J<=Lp+j]
    z,p,m=spin(j)
    zl,pl,ml=[s.kronecker_product(s.eye(2*L+1),a) for a in (z,p,m)]
    zr,pr,mr=[s.kronecker_product(s.eye(2*Lp+1),a) for a in (z,p,m)]
    norm=s.Rational(3)/((2*j+1)*j*(j+1))
    channel=s.zeros(len(js))
    for a,J in enumerate(js):
        E=intertwiner(j,L,Lp,J)
        direct=norm*(zl*E*zr+(pl*E*mr+ml*E*pr)/2)
        reconstructed=s.zeros(E.rows,E.cols)
        for b,K in enumerate(js):
            EK=intertwiner(j,L,Lp,K)
            coefficient=s.simplify(s.trace(EK.T*direct)/(2*K+1))
            prediction=s.simplify(3*(2*J+1)*(-1)**(L+Lp)*wigner_6j(j,K,L,J,j,1)*wigner_6j(j,K,Lp,J,j,1))
            assert s.simplify(coefficient-prediction)==0
            reconstructed+=coefficient*EK; channel[b,a]=coefficient
            rows.append(dict(j=str(j),L=L,Lp=Lp,J=str(J),K=str(K),coefficient=str(coefficient)))
        assert all(s.simplify(v)==0 for v in direct-reconstructed)
    casimir=2*j*(j+1)*s.eye(len(js))-2/norm*channel
    expected={s.Integer(r*(r+1)):1 for r in range(abs(L-Lp),int(min(L+Lp,2*j))+1)}
    assert casimir.eigenvals()==expected
    ranks=list(range(abs(L-Lp),int(min(L+Lp,2*j))+1))
    U=s.Matrix([[(-1)**int(L+j+J)*s.sqrt((2*J+1)*(2*r+1))*wigner_6j(L,j,J,j,Lp,r) for r in ranks] for J in js])
    D=s.diag(*[s.sqrt(2*J+1)for J in js])
    assert all(s.simplify(v)==0 for v in U.T*U-s.eye(len(js)))
    assert all(s.simplify(v)==0 for v in D*casimir*D.inv()*U-U*s.diag(*[r*(r+1)for r in ranks]))

out=dict(status='PASS',exact_channel_coefficients=len(rows),all_channel_reconstructions=True,
         all_local_casimir_spectra=True,exact_racah_eigenvector_formula=True,seconds=time.time()-start,checks=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
