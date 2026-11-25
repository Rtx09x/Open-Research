"""Build a rational, unnormalized 68-variable moment model (no Cholesky radicals).
All computations use exact Q(i) matrices and the physical weighted adjoint.
"""
import json,time
from pathlib import Path
import sympy as s
N=19;n=18;I=s.I

def build():
 Jp=s.MutableSparseMatrix(N,N,{(w+1,w):n-w for w in range(n)});Jm=s.MutableSparseMatrix(N,N,{(w,w+1):w+1 for w in range(n)})
 Jz=s.diag(*[w-9 for w in range(N)]);J=[(Jp+Jm)/2,(Jp-Jm)/(2*I),Jz]
 weights=[s.Rational(1,s.binomial(n,w))for w in range(N)]
 def adj(A):return s.MutableSparseMatrix(N,N,{(j,i):s.conjugate(v)*weights[i]/weights[j]for(i,j),v in A.todok().items()})
 B=[s.eye(N)];meta=[{'rank':0,'q':0,'part':'scalar'}]
 for r in range(1,6):
  T=Jp**r;rankbasis=[]
  for q in range(r,-1,-1):
   if q:
    U=adj(T);rankbasis.extend([(q,'real',(T+U)/2),(q,'imag',(T-U)/(2*I))])
   else:rankbasis.append((0,'real',T))
   T=Jm*T-T*Jm
  for q,part,A in sorted(rankbasis,key=lambda row:(row[0],row[1])):
   A=s.MutableSparseMatrix(A);assert A==adj(A);B.append(A);meta.append({'rank':r,'q':q,'part':part})
 norms=[s.trace(A*A)for A in B];assert all(x>0 for x in norms)
 entries=[A.todok()for A in B]
 for k in range(36):
  for l in range(k):assert sum(v*B[l][j,i]for(i,j),v in entries[k].items())==0
 def encode(z):
  z=s.expand(z);return [str(s.re(z)),str(s.im(z))]
 def coeff(P):
  vals=[s.expand(sum(v*P[j,i]for(i,j),v in en.items())/norm)for en,norm in zip(entries,norms)]
  rebuilt=s.zeros(N)
  for a,v in zip(B,vals):
   if v:rebuilt+=v*a
  assert rebuilt==P
  return [[k,*encode(v)]for k,v in enumerate(vals)if v]
 gram=[];K=[[],[],[]]
 for a in range(9):
  for b in range(9):
   gram.append({'a':a,'b':b,'coefficients':coeff(B[a]*B[b])})
   for i in range(3):K[i].append({'a':a,'b':b,'coefficients':coeff(B[a]*J[i]*B[b])})
  print('verified row',a,flush=True)
 return {'n':n,'dimension':N,'basis_description':'B0=I; ranks1..5 from unnormalized lowering commutators of Jplus^r; q0 then imag/real q>0; weighted adjoint weights 1/binomial(18,w)','basis':[{**m,'HS_norm_squared':str(norm),'entries':[[i,j,*encode(v)]for(i,j),v in en.items()]}for m,norm,en in zip(meta,norms,entries)],'gram':gram,'K_xyz':K,'all_324_product_expansions_verified_exactly':True}

if __name__=='__main__':
 start=time.time();data=build();data['elapsed_seconds']=time.time()-start;path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(data,separators=(',',':')));print('Wrote',path,'bytes',path.stat().st_size,'seconds',data['elapsed_seconds'])
