"""A generic complex n18 projector control without building a 6859² matrix.
CG coefficients obtained from J² tridiagonal diagonalization, not 6j symbols.
"""
import sys,time,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
BASE=Path(__file__).resolve().parents[1]/'symmetric-quantum-codes'/'phase2';sys.path.insert(0,str(BASE))
from three_copy_sdp import build
from three_copy_ppt import ppt_coefficients
from intrinsic_lp import transform

def cg_all(j,k):
 d,e=int(2*j+1),int(2*k+1);out={J:np.zeros((d*e,int(2*J+1)))for J in np.arange(abs(j-k),j+k+1)}
 for M in np.arange(j+k,-j-k-1,-1):
  pairs=[(a,b)for a in range(d)for b in range(e)if a+b-j-k==M];diag=[j*(j+1)+k*(k+1)+2*(a-j)*(b-k)for a,b in pairs]
  off=[np.sqrt((j-(a-j))*(j+(a-j)+1)*(k+(b-k))*(k-(b-k)+1))for a,b in pairs[:-1]]
  vals,vec=eigh_tridiagonal(diag,off)if len(pairs)>1 else(np.array(diag),np.ones((1,1)))
  inds=[a*e+b for a,b in pairs]
  for col,val in enumerate(vals):
   J=round(np.sqrt(1+4*val)-1)/2;v=vec[:,col];midx=int(J+M)
   if M==J:v*=1 if v[-1]>0 else-1
   else:
    prior=out[J][:,midx+1].reshape(d,e);lower=[]
    for a,b in pairs:
     val=0
     if a+1<d:val+=np.sqrt((j+(a+1-j))*(j-(a+1-j)+1))*prior[a+1,b]
     if b+1<e:val+=np.sqrt((k+(b+1-k))*(k-(b+1-k)+1))*prior[a,b+1]
     lower.append(val)
    v*=1 if np.dot(v,lower)>0 else-1
   out[J][inds,midx]=v
 return out
start=time.time();n=18;N=19;j=9;rng=np.random.default_rng(8675309);C,_=np.linalg.qr(rng.normal(size=(N,2))+1j*rng.normal(size=(N,2)));P=C@C.conj().T;pair=cg_all(j,j);amp={};t=np.zeros(N)
for L in range(N):
 A=pair[L].T@np.kron(C,C);t[L]=np.linalg.norm(A)**2
 for J,U in cg_all(L,j).items():amp[int(2*J),L]=U.T@np.kron(A,C)
m=build(n);x=np.zeros(m['nv']);recon=0;imag=0
for J2 in range(0,55,2):
 ls=[L for L in range(N)if(J2,L)in amp];A=np.array([amp[J2,L].ravel()for L in ls]);G=np.diag([(-1)**L for L in ls]);S=G@(A@A.conj().T)@G;imag=max(imag,float(np.max(abs(S.imag))));R=np.zeros_like(S.real)
 for b in m['blocks']:
  if b['J2']!=J2:continue
  U,V=b['U'],b['V'];X=U.T@S.real@U
  for q,(r,c)in enumerate(b['pairs']):x[b['offset']+q]=X[r,c]
  R+=U@X@U.T+(V@X@V.T if V is not None else 0)
 recon=max(recon,float(np.max(abs(R-S.real))))
# Independent normalized tensor construction by highest-weight commutators.
Jp=np.diag([np.sqrt((n-w)*(w+1))for w in range(n)],-1);Jm=Jp.T;a=[];bb=[]
for r in range(N):
 A=np.linalg.matrix_power(Jp,r);A=A/np.linalg.norm(A);sect=[A]
 for q in range(r,-r,-1):A=(Jm@A-A@Jm)/np.sqrt((r+q)*(r-q+1));sect.append(A)
 a.append(N/4*sum(abs(np.trace(P@A))**2 for A in sect));bb.append(N/2*sum(np.trace(P@A@P@A.conj().T).real for A in sect))
x[:N]=a;M=np.array(transform(n),float)
pt=ppt_coefficients(m);ptmin=min(np.linalg.eigvalsh(np.einsum('abv,v->ab',Q,x))[0]for _,_,Q in pt)
T=np.array([[(-1)**(n-i)if k==n-i else 0 for k in range(N)]for i in range(N)])
out={'n':n,'arbitrary_complex_rank2':True,'time_reversal_violation':float(np.linalg.norm(P-T@P.conj()@T.T)),'weighted_imaginary_moment_max':imag,'S3_real_reconstruction_error':recon,'pair_map_error':float(max(abs(m['shadow']@x[:N]-t))),'MacWilliams_transform_error':float(max(abs(2*M@x[:N]-bb))),'enumerator_sum_error':float(abs(sum(a)-N/2)),'all_universal_marginal_error':float(max(abs((m['E']@x-m['b'])[6:]))),'PPT_min_eigenvalue':float(ptmin),'KL_was_not_imposed':True,'seconds':time.time()-start}
assert out['time_reversal_violation']>1 and imag>1e-5
for key in ['S3_real_reconstruction_error','pair_map_error','MacWilliams_transform_error','enumerator_sum_error','all_universal_marginal_error']:assert out[key]<1e-8,(key,out[key])
assert ptmin>-1e-8
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
