"""Diagnose the codimension-r generator completion, not a proof of infeasibility."""
import json
from pathlib import Path
import numpy as np
from search_full_code import hermitian_errors
from spin_diagnostics import code19
ROOT=Path(__file__).parent

def spin(n):
 jp=np.diag(np.sqrt([(n-w)*(w+1)for w in range(n)]),-1).astype(complex);jm=jp.T
 return np.array([(jp+jm)/2,(jp-jm)/(2j),np.diag(np.arange(n+1)-n/2)])

def compress_from_moments(n,mom):
 N=n+1;T=np.concatenate([np.eye(N,dtype=complex)[None]/np.sqrt(N),hermitian_errors(n,5)]);E=T[:9];J=spin(n)
 gramcoef=np.einsum('kji,abij->kab',T,np.einsum('aij,bjk->abik',E,E));h=np.einsum('kab,kij->aibj',gramcoef,mom).reshape(18,18)
 G=(h[0::2,0::2]+h[1::2,1::2])/2;L=np.linalg.cholesky(G);F=np.kron(np.linalg.inv(L).conj().T,np.eye(2));A=[]
 for jj in J:
  coeff=np.einsum('kji,abij->kab',T,np.einsum('aij,jk,bkl->abil',E,jj,E));K=np.einsum('kab,kij->aibj',coeff,mom).reshape(18,18);A.append(F.conj().T@K@F)
 return np.array(A),G

def summarize(A,n):
 R=n/2*(n/2+1)*np.eye(18)-sum(a@a for a in A);D=[]
 for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:D.append(1j*A[k]-(A[i]@A[j]-A[j]@A[i]))
 return {'casimir_defect_eigenvalues':np.linalg.eigvalsh(R).tolist(),'commutator_defect_singular_values':[np.linalg.svd(d,compute_uv=False).tolist()for d in D],'common_defect_span_singular_values':np.linalg.svd(np.column_stack(D),compute_uv=False).tolist(),'combined_defect_eigenvalues':[np.linalg.eigvalsh(R+sign*1j*d).tolist()for d in D for sign in [-1,1]]}

if __name__=='__main__':
 print('Helper module for generator_model.py and audit_generator_reconstruction.py.')
 print('Standalone exploratory NPZ diagnostics are not part of this curated checkpoint.')
