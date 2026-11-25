"""Independent physical signed-orientation covariance plus rational phase-return audit."""
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import numpy as np,json,time
H=Path(__file__).resolve().parent;start=time.monotonic()
def zero(n,m):return np.full((n,m),F(0),dtype=object)
def eye(n):return np.array([[F(i==j) for j in range(n)] for i in range(n)],dtype=object)
def angles(m):
 v=[(F((m-j)**2-j*j,(m-j)**2+j*j),F(2*j*(m-j),(m-j)**2+j*j)) for j in range(m+1)]
 return [(c*C+s*S,c*S-s*C) for (c,s),(C,S) in zip(v,v[1:])]
Os=[]
for p in permutations(range(2)):
 for signs in product((-1,1),repeat=2):
  O=zero(2,2)
  for i in range(2):O[i,p[i]]=F(signs[i])
  Os.append(O)
f,g,j=eye(3)
def physical_map(r,t,a,b,O):
 L=zero(6,6);Q=zero(3,6)
 fc=a*f+b*g;pc=r*f+t*g;vc=np.array([-b*f+a*g,j]);uc=np.array([-t*f+r*g,j])
 for i,v in enumerate(eye(6)):
  x,z=v[:2];u=v[2:4];w=v[4:]
  Y=x*fc+u@O@vc;Z=z*pc+w@uc
  da=t*(Y@f);dd=t*(Y@g);ad=b*(Z@f)
  Yn=r*Y-ad*g;Zn=a*Z-da*g
  L[:,i]=[Yn@f,Zn@f,Yn@g,Yn@j,Zn@g,Zn@j];Q[:,i]=[da,dd,ad]
 return L,Q
def advance(C,r,t,a,b):
 out=zero(6,6);cost=F(0)
 for O in Os:
  L,Q=physical_map(r,t,a,b,O);out+=L@C@L.T;cost+=sum(np.diag(Q@C@Q.T))
 return out/len(Os),cost/len(Os)
checks=[]
for m in(4,8,16):
 seq=angles(m);rho=F(1)
 for r,t in seq:rho*=r
 U,A=F(3,5),F(2,7);xi=np.array([-rho,-rho-1,F(0),F(0),F(0),F(0)]);u=eye(6)[2]
 C=A*np.outer(xi,xi)+U*np.outer(u,u)+F(1,10)*(np.outer(xi,u)+np.outer(u,xi))
 total=F(0)
 for r,t,a,b in[(F(1),F(0),F(0),F(1))]+[(r,t,F(1),F(0)) for r,t in seq]:C,cost=advance(C,r,t,a,b);total+=cost
 q=rho*rho;Up=U/2+A;An=U/2
 assert C[0,0]==rho*rho*An and C[1,1]==(rho+1)**2*An and C[0,1]==rho*(rho+1)*An
 assert C[4,4]+C[5,5]==0 and C[2,2]+C[3,3]==q*Up
 assert total==(1+rho)**2*A+(1-q)*An+(1-q)*Up/2
 checks.append({'m':m,'physical_covariance_cycle':True,'nonzero_initial_xi_u_correlation':True})
finite=[]
for m in(16,32,64,128):
 rho=F(1);c,s=F(1),F(0)
 for r,t in angles(m):
  assert r*r+t*t==1 and r>0 and 1-r<=F(8,m*m)
  rho*=r;c,s=c*r-s*t,s*r+c*t
 assert (c,s)==(-1,0) and rho>=1-F(8,m)
 q=rho*rho;U,A=F(1),F(0);cost=F(1)
 for i in range(m):
  Un=q*(U/2+A);An=U/2
  cost+=(1+rho)**2*A+(1-q)*U/2+(1-q)*(U/2+A)/2
  U,A=Un,An
 finite.append({'m':m,'ancestor_depth':m*(m+1),'integer_lower':cost.numerator//cost.denominator})
assert [r['integer_lower'] for r in finite]==[5,8,14,26]
out={'PASS':True,'method':'own actual sample coefficient/subtraction decoder, full six-dimensional exact covariance, eight forward orientations per step; no worker imports','physical_checks':checks,'finite_pure_source_lower_bounds':finite,'scope':'Refutes uniform one-bank conditional source bound at fixed finitewidth; not unconditional scalar theorem or full HSS','seconds':time.monotonic()-start}
(H/'check_hss_one_bank_obstruction_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
