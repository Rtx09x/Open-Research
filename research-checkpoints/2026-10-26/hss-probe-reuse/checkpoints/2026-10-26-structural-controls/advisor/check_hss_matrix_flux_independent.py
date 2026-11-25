"""Independent exact signed-permutation moment audit of matrix branch formulas."""
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import numpy as np,json
H=Path(__file__).resolve().parent
k,d=2,4
def eye(n): return np.array([[F(i==j) for j in range(n)] for i in range(n)],dtype=object)
def zero(n,m):return np.full((n,m),F(0),dtype=object)
def norm(M):return sum(x*x for x in M.flat)
def ortho(seq):
 O=eye(4)
 for i,j in seq:
  a,b=O[i].copy(),O[j].copy();O[i]=F(3,5)*a-F(4,5)*b;O[j]=F(4,5)*a+F(3,5)*b
 return O
OV=ortho([(0,3),(1,2),(0,1),(2,3)]);OU=ortho([(0,2),(1,3),(0,3),(1,2)])
A,B,Ap,Bp=OV[:2,:2],OV[:2,2:],OV[2:,:2],OV[2:,2:]
R,T,Rp,Tp=OU[:2,:2],OU[:2,2:],OU[2:,:2],OU[2:,2:]
X=np.array([[F(1),F(2)],[F(-3),F(4)]]);Z=np.array([[F(3),F(-1)],[F(2),F(-2)]])
Y=np.array([[F(1),F(2),F(-1),F(0)],[F(2),F(-3),F(1),F(4)]])
W=np.array([[F(2),F(-1)],[F(3),F(1)],[F(-1),F(2)],[F(1),F(4)]])
D=X-Z
F0,G,J=eye(6)[:2],eye(6)[2:4],eye(6)[4:]
def evaluate(YO,HW):
 yb,yh=YO[:,:2],YO[:,2:];wb,wh=HW[:2],HW[2:]
 # Actual physical samples, coefficient extraction, subtract and compress.
 yc=X@(A@F0+B@G)+np.concatenate((yb,yh),axis=1)@np.concatenate((Ap@F0+Bp@G,J),axis=0)
 zc=Z.T@(R@F0+T@G)+np.concatenate((wb,wh),axis=0).T@np.concatenate((Rp@F0+Tp@G,J),axis=0)
 da=T.T@yc@F0.T;dd=T.T@yc@G.T;ad=F0@zc.T@B
 yn=R.T@yc-ad@G;zn=A.T@zc-da.T@G
 xp=yn@F0.T;zp=(zn@F0.T).T
 yp=yn@np.concatenate((G,J),axis=0).T;wp=(zn@np.concatenate((G,J),axis=0).T).T
 lam=T.T@D@B+T.T@yb@Bp-Tp.T@wb@B
 loss=norm(lam)+norm(T.T@yh)+norm(wh@B)
 assert norm(D)+norm(YO)+norm(HW)-norm(xp-zp)-norm(yp)-norm(wp)==loss
 return loss,norm(da)+norm(dd)+norm(ad)
base=evaluate(zero(2,4),zero(4,2));sums=[F(0),F(0)];count=0
for p in permutations(range(4)):
 for signs in product((-1,1),repeat=4):
  O=zero(4,4)
  for i in range(4):O[i,p[i]]=F(signs[i])
  f=evaluate(Y@O,zero(4,2));g=evaluate(zero(2,4),O.T@W)
  for j in range(2):sums[j]+=f[j]+g[j]-base[j]
  count+=1
expectedloss=norm(T.T@D@B)+(1-norm(B)/d)*norm(T.T@Y)+(1-norm(T)/d)*norm(W@B)
expectedcost=norm(T.T@X)+norm(R.T@Z@B)+F(k,d)*norm(T.T@Y)+norm(T)/d*norm(W@B)
assert [v/count for v in sums]==[expectedloss,expectedcost]
# Counterexample directly average X'X'^T and Y'Y'^T, not assumed constants.
XX=np.array([[F(1),F(0)],[F(0),F(0)]]);YY=np.concatenate((XX,zero(2,2)),axis=1)
aa=np.diag([F(1),F(0)]);bb=eye(2)-aa;ex=zero(2,2);ey=zero(2,2)
for p in permutations(range(4)):
 for signs in product((-1,1),repeat=4):
  O=zero(4,4)
  for i in range(4):O[i,p[i]]=F(signs[i])
  yo=YY@O;xp=XX@aa-yo[:,:2]@bb;yp=np.concatenate((XX@bb+yo[:,:2]@aa,yo[:,2:]),axis=1)
  ex+=xp@xp.T;ey+=yp@yp.T
assert np.array_equal(ex/count,F(5,4)*XX) and np.array_equal(ey/count,F(3,4)*XX)
out={'PASS':True,'independent_orientation_assignments':count,'method':'own physical sample decoder and exact Fraction signed-permutation isotropy enumeration; no worker imports','expected_flux_loss':str(expectedloss),'expected_emission_cost':str(expectedcost),'row_covariance_counterexample':'EXX^T=5/4 diag(1,0), EYY^T=3/4 diag(1,0)','scope':'general-k algebra and second-moment identity, not general-k stability or correlated-source theorem'}
(H/'check_hss_matrix_flux_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
