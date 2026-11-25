"""Positive control for the moment/Schur construction, not exact arithmetic."""
import json
from pathlib import Path
import numpy as np
from search_full_code import hermitian_errors
from spin_diagnostics import code19
ROOT=Path(__file__).parent
n=19;N=n+1;C=code19().astype(complex)
T=np.concatenate([np.eye(N,dtype=complex)[None]/np.sqrt(N),hermitian_errors(n,6)]);E=T[:16]
coef=np.einsum('kji,abij->kab',T,np.einsum('aij,bjk->abik',E,E));mom=np.einsum('ia,kij,jb->kab',C.conj(),T,C)
H=np.einsum('kab,kij->aibj',coef,mom).reshape(32,32)
V=np.einsum('aij,jb->iab',E,C).reshape(N,32);actual=V.conj().T@V
error=float(np.max(abs(H-actual)));assert error<1e-11
A=H[:18,:18];B=H[:18,18:];S=H[18:,18:]-B.conj().T@np.linalg.solve(A,B);eigs=np.linalg.eigvalsh(S)
assert np.max(abs(eigs[:-2]))<1e-10 and eigs[-2]>1e-3
record={'known19_moment_vs_direct_gram_error':error,'known19_Schur_eigenvalues':eigs.tolist(),'rank':2,'status':'numerical positive control for coefficient conventions'}
(ROOT/'moment_model_positive_control.json').write_text(json.dumps(record,indent=2));print(record)
