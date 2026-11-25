"""Adversarial small-spin algebra control; numerical evidence, not proof.
Arbitrary complex projectors, integer/half-integer spin, ranks2/3.
No symmetric-code hypothesis or time-reversal invariance imposed.
"""
import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(20261025);out=[]
for N in [2,3,4,5]:
 C=np.zeros((N,N));
 for k in range(N):C[N-1-k,k]=(-1)**k
 U=np.kron(np.eye(N*N),C);dim=N**3
 S=np.zeros((dim,dim))
 for a in range(N):
  for b in range(N):
   for c in range(N):S[(c*N+b)*N+a,(a*N+b)*N+c]=1
 def tau(A):return U@A.reshape(N,N,N,N,N,N).transpose(0,1,5,3,4,2).reshape(dim,dim)@U.T
 def T(A):return tau(tau(A)@S)
 for K in range(2,min(3,N)+1):
  Q,_=np.linalg.qr(rng.normal(size=(N,K))+1j*rng.normal(size=(N,K)));P=Q@Q.conj().T
  Z=np.kron(np.kron(P,P),P);A=tau(Z);R=tau(Z@S);D=A-R/K
  Arec=K*K/(K*K-1)*(D+T(D)/K);Rrec=K*K/(K*K-1)*(T(D)+D/K)
  test=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
  row=dict(N=N,K=K,inverse_A=float(np.max(abs(A-Arec))),inverse_R=float(np.max(abs(R-Rrec))),involution=float(np.max(abs(T(T(test))-test))),D_projector=float(np.max(abs(D@D-D))),D_trace=float(np.trace(D).real),D_min=float(np.linalg.eigvalsh(D)[0]),R_trace=float(np.trace(R).real))
  assert max(row[k]for k in ['inverse_A','inverse_R','involution','D_projector'])<1e-12
  assert abs(row['D_trace']-K*(K*K-1))<1e-10 and abs(row['R_trace']-K*K)<1e-10 and row['D_min']>-1e-12
  out.append(row)
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
