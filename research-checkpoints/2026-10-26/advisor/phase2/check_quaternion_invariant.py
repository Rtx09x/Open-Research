"""Independent exact Gaussian-integer gauge-determinant controls; stdlib only.
Analytic proof: quaternion_invariant.md. No worker imports or floating point.
"""
from pathlib import Path
from fractions import Fraction as F
import random,json,time
start=time.time();zero=(0,0);one=(1,0);ii=(0,1)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return(a[0],-a[1])
def summ(xs):
 r=zero
 for x in xs:r=add(r,x)
 return r
def mm(A,B):return[[summ(mul(x,y)for x,y in zip(row,col))for col in zip(*B)]for row in A]
def dag(A):return[[conj(x)for x in col]for col in zip(*A)]
def tr(A):return summ(A[i][i]for i in range(len(A)))
def scale(a,n):return(a[0]*n,a[1]*n)
def real(a):assert a[1]==0;return a[0]
def det(A):
 A=[[F(x)for x in row]for row in A];result=F(1)
 for j in range(len(A)):
  k=next((k for k in range(j,len(A))if A[k][j]),None)
  if k is None:return F(0)
  if k!=j:A[k],A[j]=A[j],A[k];result=-result
  pivot=A[j][j];result*=pivot
  for k in range(j+1,len(A)):
   q=A[k][j]/pivot
   for l in range(j+1,len(A)):A[k][l]-=q*A[j][l]
 return result
sig=[[[zero,one],[one,zero]],[[zero,neg(ii)],[ii,zero]],[[one,zero],[zero,neg(one)]]]
rng=random.Random(6319);rows=[]
for d in [1,2,3,5,18]:
 for case in range(4):
  X=[[(rng.randint(-2,2),rng.randint(-2,2))for _ in range(2)]for _ in range(2*d)];S=mm(X,dag(X));t=real(tr(S))
  B=[[[p[a//d][b//d]if a%d==b%d else zero for b in range(2*d)]for a in range(2*d)]for p in sig]
  SB=[mm(S,b)for b in B];traceSB=[tr(q)for q in SB]
  H=[[real(add(scale(tr(mm(SB[i],SB[j])),2),neg(mul(traceSB[i],traceSB[j]))))for j in range(3)]for i in range(3)]
  delta=real(mul((0,2),add(tr(mm(mm(SB[0],SB[1]),SB[2])),neg(tr(mm(mm(SB[0],SB[2]),SB[1]))))))
  Z=[]
  for a in range(d):
   M=[X[a],X[d+a]];r=[tr(M)]+[mul(ii,tr(mm(M,p)))for p in sig];Z.extend([[x[0]for x in r],[x[1]for x in r]])
  gram=[[sum(row[i]*row[j]for row in Z)for j in range(4)]for i in range(4)]
  actual=det(gram);traceH=sum(H[i][i]for i in range(3));traceH2=sum(H[i][j]*H[j][i]for i in range(3)for j in range(3))
  expected=F(t**4-2*t*t*traceH-8*t*delta+2*traceH2-traceH**2,16);assert actual==expected
  rows.append({'d':d,'case':case,'determinant':str(actual),'delta':delta})
# X=I2: S=I2, t2,H=4I,delta−8 calibrates the crucial determinant sign.
delta=real(mul((0,2),add(tr(mm(mm(sig[0],sig[1]),sig[2])),neg(tr(mm(mm(sig[0],sig[2]),sig[1]))))));assert delta==-8
out={'status':'PASS','exact_integer_complex_tests':len(rows),'sign_calibration_delta':delta,'seconds':time.time()-start,'checks':rows,'scope':'exact identity controls plus separate analytic proof; no quantum-code feasibility result'}
Path(__file__).with_name('quaternion_invariant_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))
