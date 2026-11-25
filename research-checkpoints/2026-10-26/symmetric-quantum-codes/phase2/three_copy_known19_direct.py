"""Construct the actual known19 P^tensor3 twirl, not an SDP feasibility proxy."""
import sys,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from three_copy_sdp import build
from three_copy_kl_lift import kl_lift
from three_copy_ppt import ppt_coefficients
from spin_diagnostics import code19,tensors
from intrinsic_lp import transform

def coupling(j1,j2):
 n1,n2=int(2*j1+1),int(2*j2+1);lower1=np.diag(np.sqrt([(j1+m)*(j1-m+1)for m in np.arange(-j1+1,j1+1)]),1);lower2=np.diag(np.sqrt([(j2+m)*(j2-m+1)for m in np.arange(-j2+1,j2+1)]),1)
 out={J2:np.zeros((n1*n2,J2+1))for J2 in range(int(2*abs(j1-j2)),int(2*(j1+j2))+1,2)}
 for M2 in range(int(2*(j1+j2)),-int(2*(j1+j2))-1,-2):
  M=M2/2;inds=[(a,b)for a in range(n1)for b in range(n2)if abs(a-j1+b-j2-M)<1e-10];diag=np.array([j1*(j1+1)+j2*(j2+1)+2*(a-j1)*(b-j2)for a,b in inds]);off=[]
  for(a,b),(aa,bb)in zip(inds,inds[1:]):
   m1,m2=a-j1,b-j2;off.append(np.sqrt((j1-m1)*(j1+m1+1)*(j2+m2)*(j2-m2+1)))
  e,V=eigh_tridiagonal(diag,np.array(off))if len(diag)>1 else (diag,np.ones((1,1)))
  for k,ev in enumerate(e):
   J2=int(round(np.sqrt(1+4*ev)-1));J=J2/2;v=V[:,k];col=int(round(J+M));flat=[a*n2+b for a,b in inds]
   if M2==J2:v=v*(1 if v[-1]>=0 else -1)
   else:
    prev=out[J2][:,col+1].reshape(n1,n2);lower=(lower1@prev+prev@lower2.T).ravel()[flat];v=v*(1 if v@lower>=0 else -1)
   out[J2][flat,col]=v
 allU=np.column_stack(list(out.values()));assert np.max(abs(allU.T@allU-np.eye(n1*n2)))<2e-11
 return out

start=time.time();n=19;N=20;j=n/2;m=build(n);C=code19();P=C@C.T;a=np.array([N/4*sum(abs(np.trace(P@T))**2 for T in sect)for sect in tensors(n)]);pair=coupling(j,j);amps={}
for L in range(N):
 B=pair[2*L].T@np.kron(C,C);triple=np.kron(B,C)
 for J2,U in coupling(L,j).items():amps[J2,L]=U.T@triple
x=np.zeros(m['nv']);x[:N]=a;Zdata={};control=[]
for J2 in range(1,3*n+1,2):
 J=J2/2;Ls=[L for L in range(N)if abs(L-j)<=J<=L+j];A=np.array([amps[J2,L].ravel()for L in Ls]);D=np.diag([(-1)**L for L in Ls]);Z=D@(A@A.T)@D;Zdata[J2]=(Ls,Z)
 for b in m['blocks']:
  if b['J2']!=J2:continue
  U,V=b['U'],b['V'];X=U.T@Z@U
  if V is not None:control.append(np.max(abs(X-V.T@Z@V)))
  for k,(r,s)in enumerate(b['pairs']):x[b['offset']+k]=X[r,s]
Ekl,meta=kl_lift(m);ppt=ppt_coefficients(m);out={'n':19,'actual_P_tensor3_twirl_constructed':True,'equality_error':float(max(abs(m['E']@x-m['b']))),'lifted_KL_error':float(max(abs(Ekl@x))),'standard_copy_error':float(max(control)),'PPT_min':float(min(np.linalg.eigvalsh(np.einsum('abv,v->ab',P,x))[0]for _,_,P in ppt)),'elapsed_seconds':time.time()-start};assert out['equality_error']<1e-8 and out['lifted_KL_error']<1e-8 and out['PPT_min']>-1e-8
np.savez(Path(__file__).with_suffix('.npz'),x=x);Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(out)
