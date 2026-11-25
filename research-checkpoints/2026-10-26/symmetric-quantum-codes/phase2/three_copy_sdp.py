"""Three-copy SU2 projector outer relaxation, numerical PSD cutting planes.
Infeasibility is exploratory until coefficients and a dual are exactly replayed.
"""
import sys,json,time,warnings
from pathlib import Path
import numpy as np
import sympy as s
from sympy.physics.wigner import wigner_6j
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from intrinsic_lp import constraints

def eigenspace(P):
 val,V=np.linalg.eigh((P+P.T)/2);return V[:,val>.5]

def build(n):
 N=n+1;j=s.Rational(n,2);blocks=[];Js=range(0,3*n+1,2) if n%2==0 else range(1,3*n+1,2)
 for J2 in Js:
  J=s.Rational(J2,2);Ls=[L for L in range(N)if abs(L-j)<=J<=L+j];d=len(Ls)
  F=np.array([[float((-1)**n*s.sqrt((2*L+1)*(2*K+1))*wigner_6j(j,j,L,j,J,K))for K in Ls]for L in Ls]);D=np.diag([(-1)**(n-L)for L in Ls]);F13=D@F@D;cyc=D@F
  assert np.linalg.norm(F@F-np.eye(d))<1e-10 and np.linalg.norm(np.linalg.matrix_power(cyc,3)-np.eye(d))<1e-10
  Ps=(np.eye(d)+D+F+F13+cyc+cyc.T)/6;Pa=(np.eye(d)-D-F-F13+cyc+cyc.T)/6
  Us=eigenspace(Ps);Up=eigenspace((np.eye(d)+D)/2-Ps);Um=2/np.sqrt(3)*(np.eye(d)-D)/2@F@Up
  assert np.linalg.norm(Um.T@Um-np.eye(Up.shape[1]))<1e-10
  for kind,U,V in [('sym',Us,None),('std',Up,Um)]:
   m=U.shape[1]
   if m:blocks.append({'J2':J2,'Ls':Ls,'kind':kind,'U':U,'V':V,'m':m})
 M,H,E,b=constraints(n);M=np.array(M,float);H=np.array(H,float);E=np.array(E,float);b=np.array(b,float).ravel();shadow=4/N*M@np.diag([(-1)**r for r in range(N)])
 nv=N
 for row in blocks:
  m=row['m'];row['pairs']=[(i,k)for i in range(m)for k in range(i,m)];row['offset']=nv;nv+=len(row['pairs'])
 # Marginal equations for separate Schur functors: sym even, std all.
 eq=[];rhs=[]
 for r,rr in zip(E,b):v=np.zeros(nv);v[:N]=r;eq.append(v);rhs.append(rr)
 for L in range(N):
  even=(n-L)%2==0
  for kind in (['sym','std']if even else ['std']):
   v=np.zeros(nv);factor=(4/3 if kind=='sym' else 2/3)if even else 2
   v[:N]=-factor*shadow[L]
   for row in blocks:
    if row['kind']!=kind or L not in row['Ls']:continue
    a=row['Ls'].index(L);u=row['U'][a];w=row['V'][a]if row['V']is not None else np.zeros_like(u)
    for k,(p,q)in enumerate(row['pairs']):v[row['offset']+k]=(u[p]*u[q]+w[p]*w[q])*(1 if p==q else 2)
   eq.append(v);rhs.append(0)
 cuts=[]
 for r in np.concatenate([np.eye(N),H[5:],shadow]):v=np.zeros(nv);v[:N]=r;cuts.append(v)
 def cut(row,v):
  c=np.zeros(nv)
  for k,(a,b)in enumerate(row['pairs']):c[row['offset']+k]=v[a]*v[b]*(1 if a==b else 2)
  return c
 for row in blocks:
  eye=np.eye(row['m'])
  for v in eye:cuts.append(cut(row,v))
  for a in range(row['m']):
   for b in range(a):
    for sign in [-1,1]:cuts.append(cut(row,eye[a]+sign*eye[b]))
 return {'n':n,'N':N,'blocks':blocks,'nv':nv,'E':np.array(eq),'b':np.array(rhs),'cuts':cuts,'cut':cut,'shadow':shadow}

def run(n=18,iterations=60,seconds=250):
 st=time.time();model=build(n);print('built',n,'vars',model['nv'],'blocks',[(r['J2'],r['kind'],r['m'])for r in model['blocks']],flush=True);history=[];cuts=model['cuts'];last=None
 for it in range(iterations):
  if time.time()-st>seconds:break
  r=linprog(np.zeros(model['nv']),A_ub=-np.array(cuts),b_ub=np.zeros(len(cuts)),A_eq=model['E'],b_eq=model['b'],bounds=[(None,None)]*model['nv'],method='highs',options={'threads':1});row={'iteration':it,'status':r.status,'message':r.message,'cuts':len(cuts),'elapsed':time.time()-st}
  if not r.success:history.append(row);print(row,flush=True);break
  low=0;added=0
  for block in model['blocks']:
   X=np.zeros((block['m'],block['m']))
   for k,(a,b)in enumerate(block['pairs']):X[a,b]=X[b,a]=r.x[block['offset']+k]
   ev,U=np.linalg.eigh(X);low=min(low,float(ev[0]))
   for k,e in enumerate(ev):
    if e< -1e-8:cuts.append(model['cut'](block,U[:,k]));added+=1
  row.update({'min_eigenvalue':low,'added':added});history.append(row);last=r.x;print(row,flush=True)
  if not added:break
 out={'n':n,'variables':model['nv'],'history':history,'elapsed_seconds':time.time()-st,'status':'numerical relaxation only; no exact infeasibility certificate'}
 path=Path(__file__).with_name(f'three_copy_n{n}.json');path.write_text(json.dumps(out,indent=2))
 if last is not None:np.savez(path.with_suffix('.npz'),x=last)
 return out
if __name__=='__main__':
 warnings.filterwarnings('ignore',category=UserWarning);run(int(sys.argv[1])if len(sys.argv)>1 else 18)
