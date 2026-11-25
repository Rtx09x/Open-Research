"""Numerical implementation of the audited128-real-variable exact reformulation.
An optimizer result is NOT an exact certificate. Exact algebra is described in
generator_reformulation.md; this module supplies coefficient-consistent search
and independent KL verification interfaces.
"""
import numpy as np
from search_full_code import hermitian_errors,pack,residual_jac
from generator_defect_diagnostics import spin

class GeneratorModel:
 def __init__(self,n=18):
  if n!=18:raise ValueError('This codimension-one implementation is for n=18 only')
  self.n=n;self.N=n+1;self.j=n/2
  self.T=np.concatenate([np.eye(self.N,dtype=complex)[None]/np.sqrt(self.N),hermitian_errors(n,5)]);self.E=self.T[:9];self.J=spin(n)
  self.sigma=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
  self.gramcoef=np.einsum('kji,abij->kab',self.T,np.einsum('aij,bjk->abik',self.E,self.E))
  self.kcoef=np.array([np.einsum('kji,abij->kab',self.T,np.einsum('aij,jk,bkl->abil',self.E,J,self.E))for J in self.J])
  self.upper=np.triu_indices(self.N,1)
 def moments(self,x):
  if len(x)!=68:raise ValueError('68 real moment parameters required')
  out=np.zeros((36,2,2),complex);out[0]=np.eye(2)/np.sqrt(self.N);idx=0
  for k in range(1,36):
   for p in ([0]if k<25 else range(4)):out[k]+=x[idx]*self.sigma[p];idx+=1
  return out
 def compress(self,x):
  moments=self.moments(x);h=np.einsum('kab,kij->aibj',self.gramcoef,moments).reshape(18,18);G=(h[::2,::2]+h[1::2,1::2])/2
  L=np.linalg.cholesky(G);F=np.kron(np.linalg.inv(L).conj().T,np.eye(2));K=np.einsum('qkab,kij->qaibj',self.kcoef,moments).reshape(3,18,18)
  A=np.array([F.conj().T@K_i@F for K_i in K]);return A,G
 def generators(self,y):
  if len(y)!=128:raise ValueError('128 real parameters required')
  A,G=self.compress(y[:68]);v=(y[68:98]+1j*y[98:128]).reshape(3,10)
  out=np.zeros((3,19,19),complex);out[:,:18,:18]=A;out[:,8:18,18]=v;out[:,18,8:18]=v.conj();out[:,18,18]=-np.trace(A,axis1=1,axis2=2)
  return out,G
 def hvec(self,H):
  return np.r_[H.diagonal().real,np.sqrt(2)*H[self.upper].real,np.sqrt(2)*H[self.upper].imag]
 def residual(self,y):
  J,G=self.generators(y);out=[]
  for i,j,k in [(0,1,2),(1,2,0),(2,0,1)]:out.append(self.hvec((-1j*(J[i]@J[j]-J[j]@J[i])-J[k])/90))
  out.append(self.hvec(sum(a@a for a in J)/90-np.eye(19)))
  return np.concatenate(out)
 def decode_numerically(self,y):
  """Only meaningful at an accurately solved point; returns separate KL residual."""
  J,G=self.generators(y);eigenvalues,V=np.linalg.eigh(J[2]);raising=V.conj().T@(J[0]+1j*J[1])@V;phases=np.ones(19,complex)
  for m in range(18):
   value=raising[m+1,m]
   if abs(value)<1e-14:raise ValueError('Raising operator does not connect the spin ladder')
   phases[m+1]=phases[m]*value/abs(value)
  V=V*phases[None,:];C=V.conj().T[:,:2]
  kl=residual_jac(pack(C),18,hermitian_errors(18,4))
  return {'C':C,'generator_residual':float(np.linalg.norm(self.residual(y))),'KL_residual':float(np.linalg.norm(kl)),'Jz_ladder_error':float(np.max(abs(eigenvalues-np.arange(-9,10))))}

if __name__=='__main__':
 m=GeneratorModel();y=np.zeros(128);A,G=m.compress(y[:68]);assert np.max(abs(G-np.eye(9)/19))<1e-12;J,G=m.generators(y);assert np.max(abs(J-J.conj().transpose(0,2,1)))<1e-12
 print('Model initialized:128 real variables;1444 real residual coordinates; zero-moment test Gram I9/19 verified. No feasibility claim.')
