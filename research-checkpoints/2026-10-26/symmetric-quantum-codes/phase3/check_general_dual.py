"""Standalone rigorous general-t Z/PPT/lifted-KL finite witness verifier.
Only stdlib and python-flint. Exact rational Gram PSD factors; factorial Racah
6j coefficients enclosed by outward-rounded Arb balls. No solver/model import.
"""
import json,sys,math,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from flint import arb,arb_mat,fmpq,ctx
ctx.prec=256
ROOT=Path(__file__).parent;n=int(sys.argv[1]);t=int(sys.argv[2]);N=n+1;FILE=ROOT/f'general_dual_n{n}_t{t}.json';raw=FILE.read_bytes();c=json.loads(raw);assert(c['n'],c['t'],c['K'],c['distance'])==(n,t,2,2*t+1);scale=c['scale'];assert scale>0

def aq(x):
 x=Q(x);return arb(fmpq(x.numerator,x.denominator))
def rq(v):return Q(int(v),scale)
def mat(x):return arb_mat([[aq(rq(v))for v in row]for row in x])
def zero(d):return arb_mat(d,d)
def eye(d):return arb_mat([[int(a==b)for b in range(d)]for a in range(d)])
def sym(A):return(A+A.transpose())/2
def gram(x):
 A=mat(x['factor']);return A*A.transpose()
@lru_cache(None)
def f(k):return math.factorial(k)
@lru_cache(None)
def six2(a,b,c,d,e,f0):
 delta=Q(1)
 for x,y,z in[(a,b,c),(a,e,f0),(d,b,f0),(d,e,c)]:
  if(x+y+z)%2 or min(x+y-z,x-y+z,-x+y+z)<0:return arb(0)
  delta*=Q(f((x+y-z)//2)*f((x-y+z)//2)*f((-x+y+z)//2),f((x+y+z)//2+1))
 lo=[(a+b+c)//2,(a+e+f0)//2,(d+b+f0)//2,(d+e+c)//2];hi=[(a+b+d+e)//2,(a+c+d+f0)//2,(b+c+e+f0)//2]
 val=sum((Q((-1)**z*f(z+1),math.prod(f(z-u)for u in lo)*math.prod(f(u-z)for u in hi))for z in range(max(lo),min(hi)+1)),Q(0))
 return aq(val)*aq(delta).sqrt()
start=time.time();M=arb_mat([[(-1)**(n+r+k)*(2*r+1)*six2(n,n,2*r,n,n,2*k)for k in range(N)]for r in range(N)]);H=2*M-eye(N);shadow=arb_mat([[(-1)**k*M[r,k]for k in range(N)]for r in range(N)]);pair=aq(Q(4,N))*shadow;blocks={}
for J2 in range(n%2,3*n+1,2):
 ls=[L for L in range(N)if abs(2*L-n)<=J2<=2*L+n];d=len(ls);I=eye(d);F=arb_mat([[(-1)**n*arb((2*L+1)*(2*K+1)).sqrt()*six2(n,n,2*L,n,J2,2*K)for K in ls]for L in ls]);D=arb_mat([[(-1)**(n-L)if a==b else 0 for b in range(d)]for a,L in enumerate(ls)]);F13=D*F*D;group=[I,D,F,F13,D*F,F*D];Psy=sum(group,zero(d))/6;Pa=(I-D-F-F13+D*F+F*D)/6;blocks[J2]=dict(ls=ls,I=I,F=F,F13=F13,group=group,Psy=Psy,Pstd=I-Psy-Pa,support=I-Pa,R=zero(d),B=zero(d))
 assert all(abs((F*F-I)[a,b])<arb('1e-40')for a in range(d)for b in range(d))
ra=[arb(0)for _ in range(N)];y=list(map(rq,c['equality_dual']));constant=y[0]+Q(N,2)*y[1]
for k in range(N):ra[k]-=aq(y[0])*int(k==0)+aq(y[1])+sum((aq(y[r+1])*H[r,k]for r in range(1,2*t+1)),arb(0))
at=2+2*t
for L in range(N):
 even=(n-L)%2==0
 for kind in(['Psy','Pstd']if even else['Pstd']):
  yy=aq(y[at]);at+=1;fac=Q(4,3)if kind=='Psy'else(Q(2,3)if even else Q(2))
  for k in range(N):ra[k]+=yy*aq(fac)*pair[L,k]
  for b in blocks.values():
   if L not in b['ls']:continue
   a=b['ls'].index(L);E=zero(len(b['ls']));E[a,a]=1;b['R']-=yy*sym(b[kind]*E)
assert at==len(y)
z=[aq(rq(v))for v in c['enumerator_inequality_dual']];assert all(int(v)>=0 for v in c['enumerator_inequality_dual']);at=0
for r in range(N):ra[r]+=z[at];at+=1
for r in range(2*t+1,N):
 for k in range(N):ra[k]+=z[at]*H[r,k]
 at+=1
for r in range(N):
 for k in range(N):ra[k]+=z[at]*shadow[r,k]
 at+=1
assert at==len(z)
for item in c['ordinary_PSD']:
 b=blocks[item['J2']];assert item['Ls']==b['ls'];U=mat(item['basis_U']);V=U*mat(item['factor']);b['R']+=V*V.transpose()
for item in c['PPT']:
 b=blocks[item['J2']];A=gram(item)
 for a,L in enumerate(item['Ls']):
  for d,Lp in enumerate(item['Ls']):b['B'][b['ls'].index(L),b['ls'].index(Lp)]+=A[a,d]
for J2,b in blocks.items():
 for a,L in enumerate(b['ls']):
  for d,Lp in enumerate(b['ls'][:a+1]):
   v=arb(0)
   for K2,bb in blocks.items():
    if L in bb['ls']and Lp in bb['ls']:v+=(-1)**n*six2(2*L,n,J2,2*Lp,n,K2)*bb['B'][bb['ls'].index(L),bb['ls'].index(Lp)]
   b['R'][a,d]+=v
   if a!=d:b['R'][d,a]+=v
print('PPT lift seconds',time.time()-start,flush=True)
for item in c['KL']:
 L,Lp,r=item['L'],item['Lp'],item['r'];assert abs(L-Lp)<=r<=min(L+Lp,n,2*t);yy=aq(rq(item['multiplier']))
 for J2,b in blocks.items():
  if L not in b['ls']or Lp not in b['ls']:continue
  coeff=(-1)**((2*L+n+J2)//2)*arb(2*r+1).sqrt()*six2(2*L,n,J2,n,2*Lp,2*r);a,d=b['ls'].index(L),b['ls'].index(Lp);A=2*b['F13']-b['I'];R=zero(len(b['ls']))
  for k in range(len(b['ls'])):R[d,k]=A[a,k]
  b['R']-=yy*coeff*sym(R)
eps=Q(1,10**8);maxZ=0.
for J2,b in blocks.items():
 R=sym(b['R']);R=sum((G*R*G.transpose()for G in b['group']),zero(len(b['ls'])))/6;R=b['support']*R*b['support']
 for a in range(R.nrows()):
  for d in range(R.ncols()):
   assert abs(R[a,d])<aq(eps),('Z',J2,a,d,str(R[a,d]));maxZ=max(maxZ,float(abs(R[a,d]).upper()))
for k,v in enumerate(ra):assert abs(v)<aq(eps),('a',k,str(v))
budget=(Q(N,2)+8*N)*eps;assert constant+budget<0
out=dict(n=n,t=t,rigorously_verified=True,witness_sha256=hashlib.sha256(raw).hexdigest(),constant_exact=str(constant),each_residual_entry_bound=str(eps),residual_budget_exact=str(budget),strict_negative_upper_exact=str(constant+budget),diagnostic_max_Z_residual=maxZ,diagnostic_max_a_residual=max(float(abs(v).upper())for v in ra),seconds=time.time()-start,scope='Unrestricted complex symmetric rank2 code, distance2t+1; independent arithmetic and model audits remain separate.')
(ROOT/f'general_dual_n{n}_t{t}_verified.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)
