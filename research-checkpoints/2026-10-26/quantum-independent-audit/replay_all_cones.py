"""Independent replay of all mixed cones on the actually constructed 19-code moments.
Uses worker coefficients, but performs no SDP solve and writes no worker files.
"""
import sys,json,time
from pathlib import Path
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j
BASE=Path(__file__).resolve().parents[1]/'symmetric-quantum-codes'/'phase2'
sys.path.insert(0,str(BASE))
from three_copy_sdp import build
from three_copy_ppt import ppt_coefficients
from intrinsic_lp import transform
start=time.time();n=19;N=n+1;j=s.Rational(n,2);m=build(n)
x=np.load(BASE/'three_copy_known19_direct.npz')['x'];coef=ppt_coefficients(m)
t=m['shadow']@x[:N];M=np.array(transform(n),float)
W2=(-1.)**(n+np.arange(N)[:,None]+np.arange(N)[None,:])*M/(2*np.arange(N)[:,None]+1);pt_pair=W2@t
rows=[]
for K2 in range(n%2,3*n+1,2):
 K=s.Rational(K2,2);Ls=[L for L in range(N)if abs(L-j)<=K<=L+j];d=len(Ls)
 F=np.array([[float((-1)**n*s.sqrt((2*L+1)*(2*Lp+1))*wigner_6j(j,j,L,j,K,Lp))for Lp in Ls]for L in Ls]);F12=np.diag([(-1)**(n-L)for L in Ls]);F13=F12@F@F12
 D=np.diag([t[L]/(2*L+1)for L in Ls]);Dpt=np.diag([pt_pair[L]for L in Ls]);Z=np.zeros((d,d))
 for b in m['blocks']:
  if b['J2']!=K2:continue
  X=np.zeros((b['m'],b['m']))
  for k,(p,q)in enumerate(b['pairs']):X[p,q]=X[q,p]=x[b['offset']+k]
  U,V=b['U'],b['V'];Z+=(U@X@U.T+(V@X@V.T if V is not None else 0))/(K2+1)
 Zp=np.zeros((d,d))
 for KK,parity,P in coef:
  if KK!=K2:continue
  keep=[a for a,L in enumerate(Ls)if L%2==parity];dd=len(keep);U=np.eye(d)[:,keep];Q=np.einsum('abv,v->ab',P,x);Zp+=U@Q@U.T
 Y13=F@D@F;Y23=F13@D@F13;P13=F@Dpt@F;P23=F13@Dpt@F13
 mats={'PPP':Z,'PT_PPP':Zp,'PPQ':D-Z,'PQQ':2/N*np.eye(d)-D-Y13+Z,'QQQ':(1-6/N)*np.eye(d)+D+Y13+Y23-Z,'PT_PPQ_1':D-Zp,'PT_PPQ_2':P13-Zp,'PT_PQQ_1':2/N*np.eye(d)-D-P13+Zp,'PT_PQQ_2':2/N*np.eye(d)-P13-P23+Zp,'PT_QQQ':(1-6/N)*np.eye(d)+D+P13+P23-Zp}
 for kind,Q in mats.items():
  rows.append(dict(J2=K2,kind=kind,min_eig=float(np.linalg.eigvalsh((Q+Q.T)/2)[0]),symmetry_error=float(np.max(abs(Q-Q.T)))))
summary={kind:min(r['min_eig']for r in rows if r['kind']==kind) for kind in mats}
out={'status':'NUMERICAL_CONTROL_PASS' if min(summary.values())>-1e-9 else 'FAIL','n':n,'actual_known19_x':True,'constraints_tested':len(rows),'min_by_kind':summary,'equality_residual':float(np.max(abs(m['E']@x-m['b']))),'seconds':time.time()-start,'rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
