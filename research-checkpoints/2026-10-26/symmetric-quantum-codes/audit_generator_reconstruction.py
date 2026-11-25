"""Known19 positive control for the degree-ordered reconstruction identities."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from search_full_code import hermitian_errors
from spin_diagnostics import code19
from generator_defect_diagnostics import spin
ROOT=Path(__file__).parent
n=19;N=20;C=code19().astype(complex);E=np.concatenate([np.eye(N,dtype=complex)[None]/np.sqrt(N),hermitian_errors(n,2)]);W=np.einsum('aij,jb->iab',E,C).reshape(N,18);joint=W.conj().T@W;G=(joint[::2,::2]+joint[1::2,1::2])/2;L=np.linalg.cholesky(G);U=W@np.kron(np.linalg.inv(L).conj().T,np.eye(2));V=null_space(U.conj().T);Q=np.column_stack([U,V]);assert np.max(abs(Q.conj().T@Q-np.eye(N)))<1e-12
F=np.vstack([np.kron(L.conj().T,np.eye(2)),np.zeros((2,18))]);errors=[];boundary=[]
for J in spin(n):
 Jhat=Q.conj().T@J@Q;boundary.append(float(np.max(abs(Jhat[:8,18:]))))
 for a in range(4):
  coeff=np.einsum('bij,ji->b',E,J@E[a]);rhs=F@np.kron(coeff[:,None],np.eye(2));lhs=Jhat@F[:,2*a:2*a+2];errors.append(float(np.max(abs(lhs-rhs))))
record={'code_first_two_coordinate_error':float(np.max(abs(Q.conj().T@C-np.eye(N)[:,:2]))),'max_degree_one_closure_error':max(errors),'max_low_shell_boundary_error':max(boundary),'unitarity_error':float(np.max(abs(Q.conj().T@Q-np.eye(N))))};assert max(record.values())<1e-11
(ROOT/'generator_reconstruction_positive_control.json').write_text(json.dumps(record,indent=2));print(record)
