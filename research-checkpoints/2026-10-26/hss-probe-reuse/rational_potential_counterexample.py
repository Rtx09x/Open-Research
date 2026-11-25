"""Exact rational certification of a failed monotone-energy proof shortcut.
This is NOT a counterexample to HSS approximation or to a uniform-energy bound.
Checkpointed runs stop before4 minutes; rerun to resume.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from fractions import Fraction as F
import numpy as np,json,time,pathlib
from scipy.linalg import block_diag
from baseline import make_hss
from frozen_operator import sign_frame
from conditional_ledger import batchledger
rng=np.random.default_rng(156);make_hss(1,2,rng);_,fixed=make_hss(1,3,rng)
params=[];rfixed=[]
for us,vs in fixed[1:]:
 sides=[];tsides=[]
 for bs in [us,vs]:
  out=[];tt=[]
  for u in bs:
   t=F(float(u[1,0]/(1+u[0,0]))).limit_denominator(20);u1=(1-t*t)/(1+t*t);u2=2*t/(1+t*t);out.append(np.array([[u1],[u2]],dtype=object));tt.append(str(t))
  sides.append(out);tsides.append(tt)
 rfixed.append(tuple(sides));params.append(tsides)
a=np.array([F(0),F(-917,1000),F(393,1000),F(65,1000),F(0),F(0),F(0),F(0)],dtype=object)
zeros=lambda shape:np.full(shape,F(0),dtype=object)
def eye(n):
 x=zeros((n,n))
 for i in range(n):x[i,i]=F(1)
 return x

def rframe(side,ss):
 x=eye(2);p=0
 for us,vs in reversed(rfixed):
  bs=us if side=='u' else vs;out=[]
  for i,u in enumerate(bs):
   f=x[i:i+1];w=np.array([[-u[1,0]],[u[0,0]]],dtype=object);g=ss[p]*np.array([[-f[0,1],f[0,0]]],dtype=object);p+=1;out.append(u@f+w@g)
  x=np.vstack(out)
 return x

def norm2(x):return sum(v*v for v in x.flat)
def calc(ss):
 om=rframe('v',ss[:6]);ps=rframe('u',ss[6:]);g=np.array([-om[0,1],om[0,0]],dtype=object);b=ps[0]@(ps.T@a);aa=a.copy();aa[0]-=b;y=np.outer(aa,g);z=zeros(y.shape);values=[]
 for us,vs in rfixed:
  n=len(om);U=block_diag(*us);V=block_diag(*vs);D=zeros((n,n));before=norm2(y)+norm2(z)
  for i,(u,v) in enumerate(zip(us,vs)):
   sl=slice(2*i,2*i+2);pu=u@u.T;pv=v@v.T;D[sl,sl]=(eye(2)-pu)@y[sl]@om[sl].T+pu@((eye(2)-pv)@z[sl]@ps[sl].T).T
  y=U.T@(y-D@om);z=V.T@(z-D.T@ps);om=V.T@om;ps=U.T@ps;after=norm2(y)+norm2(z);values.append(after-before)
 return values[-1]

if __name__=='__main__':
 import sys
 path=pathlib.Path('rational_potential_checkpoint.json');start=0;acc=F(0)
 if path.exists():d=json.load(open(path));start=d['count'];acc=F(d['sum'])
 t0=time.time()
 for count in range(start,4096):
  ss=[1 if count&(1<<b) else -1 for b in range(12)];acc+=calc(ss)
  if (count+1)%32==0:
   json.dump({'count':count+1,'sum':str(acc)},open(path,'w'));print('checkpoint',count+1,'elapsed',time.time()-t0,'mean',float(acc/(count+1)),flush=True)
   if time.time()-t0>220:break
 if count+1==4096:
  mean=acc/4096;assert mean>0
  d={'claim':'Expected carried sketch energy can increase; only disproves a monotone-potential shortcut.','k':1,'L':3,'coarse_rotation_halfangle_parameters':params,'input_active_detail_column':0,'input_active_coefficients':[str(v) for v in a],'input_frobenius_norm_squared':str(sum(v*v for v in a)),'expected_energy_increase_exact':str(mean),'expected_energy_increase_decimal':float(mean),'positive_exact_integer_numerator':mean.numerator>0,'coarse_sign_assignments':4096,'finest_signs':'integrated analytically; single degree-one Walsh channel'}
  json.dump(d,open('rational_potential_certificate.json','w'),indent=2);print('EXACT POSITIVE:',float(mean),'numerator digits',len(str(mean.numerator)),'denominator digits',len(str(mean.denominator)),flush=True)
