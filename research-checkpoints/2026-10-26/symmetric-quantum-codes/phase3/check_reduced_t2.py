"""Rigorous Arb verification of a rounded full-spin three-copy SDP dual.
Phase3 subset replay: all mixed P/Q cones removed; epsilon relaxed to1e-7.
No optimizer, numerical eigensolver, worker model import, or floating basis is
trusted. PSD witnesses are rational Gram factors. Algebraic coefficients are
computed by the factorial Racah formula with outward-rounded Arb balls.
"""
import json,time,math,hashlib
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from flint import arb,arb_mat,fmpq,ctx
ctx.prec=256
ROOT=Path(__file__).parent;FILE=ROOT/'reduced_t2_candidate.json';cert=json.loads(FILE.read_text());assert(cert['n'],cert['K'],cert['distance'])==(18,2,5);SCALE=cert['scale'];assert SCALE>0;n=18;N=19;j=9

def aq(x):
 x=Q(x);return arb(fmpq(x.numerator,x.denominator))
def qint(x):return aq(Q(int(x),SCALE))
def eye(d):return arb_mat([[int(a==b)for b in range(d)]for a in range(d)])
def zero(d):return arb_mat(d,d)
def tr(A):return sum((A[k,k]for k in range(A.nrows())),arb(0))
def sym(A):return (A+A.transpose())/2

def mat_int(A):return arb_mat([[qint(v)for v in row]for row in A])
def gram(item):
 B=mat_int(item['factor']);return B*B.transpose()
def trace_gram_q(item):return sum((Q(int(v)**2,SCALE*SCALE)for row in item['factor']for v in row),Q(0))

@lru_cache(None)
def six(a,b,c,d,e,f):
 triples=[(a,b,c),(a,e,f),(d,b,f),(d,e,c)];delta=Q(1)
 for x,y,z in triples:
  if min(x+y-z,x-y+z,-x+y+z)<0:return arb(0)
  delta*=Q(math.factorial(x+y-z)*math.factorial(x-y+z)*math.factorial(-x+y+z),math.factorial(x+y+z+1))
 lo=max(a+b+c,a+e+f,d+b+f,d+e+c);hi=min(a+b+d+e,a+c+d+f,b+c+e+f);summ=Q(0)
 for z in range(lo,hi+1):
  den=math.prod(math.factorial(v)for v in [z-a-b-c,z-a-e-f,z-d-b-f,z-d-e-c,a+b+d+e-z,a+c+d+f-z,b+c+e+f-z]);summ+=Q((-1)**z*math.factorial(z+1),den)
 return aq(summ)*aq(delta).sqrt()

start=time.time();M=arb_mat([[(-1)**(n+r+k)*(2*r+1)*six(j,j,r,j,j,k)for k in range(N)]for r in range(N)]);H=2*M-eye(N);shadow=arb_mat([[aq(Q(4,N))*(-1)**k*M[r,k]for k in range(N)]for r in range(N)]);W2=arb_mat([[six(j,j,k,j,j,r)for k in range(N)]for r in range(N)])
blocks={}
for J in range(28):
 Ls=[L for L in range(N)if abs(L-j)<=J<=L+j];d=len(Ls);F=arb_mat([[arb((2*L+1)*(2*K+1)).sqrt()*six(j,j,L,j,J,K)for K in Ls]for L in Ls]);D=arb_mat([[(-1)**(n-L)if a==b else 0 for b in range(d)]for a,L in enumerate(Ls)]);I=eye(d);F13=D*F*D;Psy=(I+D+F+F13+D*F+F*D)/6;Pa=(I-D-F-F13+D*F+F*D)/6
 blocks[J]={'Ls':Ls,'F':F,'D':D,'F13':F13,'Psy':Psy,'Pst':I-Psy-Pa,'support':I-Pa,'groups':[I,D,F,F13,D*F,F*D],'R':zero(d),'B':zero(d)}
 # Algebraic convention controls. Bounds are deliberately far wider than Arb radii.
 assert all(abs((F*F-I)[a,b])<arb('1e-50')for a in range(d)for b in range(d))
ra=[arb(0)for _ in range(N)];constant=Q(0)
y=[Q(int(v),SCALE)for v in cert['equality_dual']];constant+=y[0]+Q(19,2)*y[1]
for k in range(N):ra[k]-=aq(y[0])*int(k==0)+aq(y[1])+sum((aq(y[r+1])*H[r,k]for r in range(1,5)),arb(0))
pos=6
for L in range(N):
 even=(n-L)%2==0
 for kind in (['sym','std']if even else ['std']):
  yy=aq(y[pos]);pos+=1;fac=Q(4,3)if kind=='sym' else(Q(2,3)if even else Q(2))
  for k in range(N):ra[k]+=yy*aq(fac)*shadow[L,k]
  for J,b in blocks.items():
   if L not in b['Ls']:continue
   a=b['Ls'].index(L);P=b['Psy']if kind=='sym'else b['Pst'];E=zero(len(b['Ls']));E[a,a]=1;b['R']-=yy*sym(P*E)
assert pos==len(y)
# Scalar intrinsic/shadow inequalities.
z=[qint(v)for v in cert['enumerator_inequality_dual']];assert all(int(v)>=0 for v in cert['enumerator_inequality_dual']);p=0
for r in range(N):ra[r]+=z[p];p+=1
for r in range(5,N):
 for k in range(N):ra[k]+=z[p]*H[r,k]
 p+=1
for r in range(N):
 for k in range(N):ra[k]+=z[p]*shadow[r,k]
 p+=1
assert p==len(z)
# Ordinary PSD duals and the initial scalar PSD cuts were combined into these
# rational Gram factors. Any rational U gives a valid compression PSD test.
for item in cert['ordinary_PSD']:
 b=blocks[item['J2']//2];assert item['Ls']==b['Ls'];U=mat_int(item['basis_U']);B=mat_int(item['factor']);L=U*B;b['R']+=L*L.transpose()

# Helpers for pair-spectrum functionals.
def add_pair(diagcoeff,pt=False):
 coeff=diagcoeff
 if pt:
  coeff=[sum((diagcoeff[L]*W2[L,r]for L in range(N)),arb(0))for r in range(N)]
 for k in range(N):ra[k]+=sum((coeff[L]*shadow[L,k]for L in range(N)),arb(0))

def diag_pair(b,A,pt=False):
 v=[arb(0)for _ in range(N)]
 for a,L in enumerate(b['Ls']):v[L]=A[a,a] if pt else A[a,a]/(2*L+1)
 add_pair(v,pt=pt)

for item in cert['cones']:
 J=item['J2']//2;b=blocks[J];Ls=b['Ls'];d=len(Ls);Ds=gram(item);D=zero(d)
 for a,L in enumerate(item['Ls']):
  for c,Lp in enumerate(item['Ls']):D[Ls.index(L),Ls.index(Lp)]=Ds[a,c]
 F,F13=b['F'],b['F13'];D13=F*D*F;D23=F13*D*F13;kind=item['kind'];dq=trace_gram_q(item)
 if kind=='PPQ':b['R']-=D/(2*J+1);diag_pair(b,D)
 elif kind=='PQQ':b['R']+=D/(2*J+1);diag_pair(b,-D-D13);constant+=Q(2,N)*dq
 elif kind=='QQQ':b['R']-=D/(2*J+1);diag_pair(b,D+D13+D23);constant+=(Q(1)-Q(6,N))*dq
 elif kind=='PPT_Z':b['B']+=D
 elif kind=='PPT_PPQ':b['B']-=D;diag_pair(b,D)
 elif kind=='PPT_PQP':b['B']-=D;diag_pair(b,D13,pt=True)
 elif kind=='PPT_PQQ':b['B']+=D;diag_pair(b,-D);diag_pair(b,-D13,pt=True);constant+=Q(2,N)*dq
 elif kind=='PPT_QQP':b['B']+=D;diag_pair(b,-D13-D23,pt=True);constant+=Q(2,N)*dq
 elif kind=='PPT_QQQ':b['B']-=D;diag_pair(b,D);diag_pair(b,D13+D23,pt=True);constant+=(Q(1)-Q(6,N))*dq
 else:raise ValueError(kind)
# Adjoint partial-time-reversal crossing; source variables are weighted Z_J.
for J,b in blocks.items():
 Ls=b['Ls']
 for a,L in enumerate(Ls):
  for c,Lp in enumerate(Ls[:a+1]):
   value=arb(0)
   for K,bb in blocks.items():
    if L in bb['Ls']and Lp in bb['Ls']:value+=six(L,j,J,Lp,j,K)*bb['B'][bb['Ls'].index(L),bb['Ls'].index(Lp)]
   b['R'][a,c]+=value
   if a!=c:b['R'][c,a]+=value
print('cone lift done; seconds',time.time()-start,flush=True)
# Lift the KL dual into exact low-operator-rank Racah eigenspaces. The supplied
# rational h can be arbitrary: projection makes this an exact zero identity.
for item in cert['KL_projected_h']:
 L,Lp=item['L'],item['Lp'];Js=[k//2 for k in item['Js']];h=[qint(v)for v in item['h']];hp=[arb(0)for _ in Js]
 for r in range(abs(L-Lp),min(L+Lp,n,4)+1):
  u=[(-1)**(L+j+J)*arb((2*J+1)*(2*r+1)).sqrt()*six(L,j,J,j,Lp,r)for J in Js];dot=sum((a*b for a,b in zip(u,h)),arb(0))
  for a in range(len(Js)):hp[a]+=u[a]*dot
 for J,hJ in zip(Js,hp):
  b=blocks[J];a,c=b['Ls'].index(L),b['Ls'].index(Lp);A=2*b['F13']-eye(len(b['Ls']));R=zero(len(b['Ls']))
  for k in range(len(b['Ls'])):R[c,k]=A[a,k]
  b['R']-=hJ/arb(2*J+1).sqrt()*sym(R)
# Exact S3 twirl and removal of the absent antisymmetric sector. These preserve
# the residual functional on every genuine code's Z, not on an assumed real code.
maxdiag=0.0
for J,b in blocks.items():
 R=sym(b['R']);R=sum((G*R*G.transpose()for G in b['groups']),zero(len(b['Ls'])))/6;R=b['support']*R*b['support'];b['R']=R
 for a in range(R.nrows()):
  for c in range(R.ncols()):
   maxdiag=max(maxdiag,float(abs(R[a,c]).upper()))
   assert abs(R[a,c])<arb('1e-7'),('Z residual',J,a,c,str(R[a,c]))
for k,v in enumerate(ra):assert abs(v)<arb('1e-7'),('enumerator residual',k,str(v))
# Positive cone combination = constant + residual. Actual a>=0 has sum19/2;
# actual weighted Z blocks are PSD with total trace8 and block size<=19.
residual_bound=Q(19,2)*Q(1,10**7)+8*19*Q(1,10**7)
assert constant < -Q(1,10000)
assert constant+residual_bound<0
out={'rigorously_verified':True,'arithmetic':'Arb outward-rounded balls,256bits; rational Gram PSD factors','candidate_sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'constant_exact':str(constant),'constant_upper':'-1/10000','each_residual_entry_bound':'1/10000000','residual_bound_exact':str(residual_bound),'strict_negative_upper':str(-Q(1,10000)+residual_bound),'diagnostic_max_Z_residual_float':maxdiag,'diagnostic_max_a_residual_float':max(float(abs(v).upper())for v in ra),'elapsed_seconds':time.time()-start,'scope':'Necessary three-copy relaxation for unrestricted complex symmetric18-qubit rank2 distance5 codes; physical/model applicability must be independently audited.'}
(ROOT/'reduced_t2_verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
