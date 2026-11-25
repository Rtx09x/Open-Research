"""Exact nontrivial rational control for the nilpotent regression identity.
N8,k1,L2,width3; unrelated dense left/right transfers and signed frames.
"""
from fractions import Fraction as F
import json


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[dot(row,col) for col in zip(*b)] for row in a]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def zero(n,m):return [[F(0) for _ in range(m)] for _ in range(n)]
def outer(a,b):return [[x*y for y in b] for x in a]
def add(a,b,scale=1):return [[x+scale*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def lin(c,s,a,b):return [c*x+s*y for x,y in zip(a,b)]
def bd(blocks):
 out=zero(sum(len(b) for b in blocks),sum(len(b[0]) for b in blocks));i=j=0
 for b in blocks:
  for r in range(len(b)):
   for c in range(len(b[0])):out[i+r][j+c]=b[r][c]
  i+=len(b);j+=len(b[0])
 return out


def main():
 fixed=[([(F(3,5),F(4,5))]*4,[(F(5,13),F(12,13))]*4),
        ([(F(8,17),F(15,17))]*2,[(F(7,25),F(24,25))]*2)]
 left=[];right=[];types=[];levels=[];eu=ev=eye(8)
 for ell,(us,vs) in enumerate(fixed):
  nu=[];nv=[]
  for i,((c,s),(a,b)) in enumerate(zip(us,vs)):
   au,du=lin(c,s,eu[2*i],eu[2*i+1]),lin(-s,c,eu[2*i],eu[2*i+1])
   av,dv=lin(a,b,ev[2*i],ev[2*i+1]),lin(-b,a,ev[2*i],ev[2*i+1])
   left += [du,du,au];right += [av,dv,dv];types += ['F','F','T'];levels += [ell]*3
   nu.append(au);nv.append(av)
  eu,ev=nu,nv
 for u in eu:
  for v in ev:left.append(u);right.append(v);types.append('F');levels.append(2)
 def probe(side):
  e=eye(3);inc=[(e[0],e[1],e[2]),(e[1],e[2],e[0])];counter=0
  for pair in reversed(fixed):
   rows=[];nxt=[]
   for i,(c,s) in enumerate(pair[side]):
    f,g,h=inc[i];g=[((-1)**(counter+side))*x for x in g];counter+=1
    f0,f1=lin(c,-s,f,g),lin(s,c,f,g)
    rows += [f0,f1];nxt += [(f0,f1,h),(f1,h,f0)]
   inc=nxt
  return rows
 om,ps=probe(1),probe(0);d=len(left)
 ro,lp=mul(right,om),mul(left,ps)
 T=[[dot(left[i],left[j])*dot(ro[i],ro[j]) if types[i]=='F' else dot(right[i],right[j])*dot(lp[i],lp[j]) for j in range(d)] for i in range(d)]
 K=add(T,eye(d),-1);K2=mul(K,K);K3=mul(K2,K)
 assert K3==zero(d,d)
 assert all(K[i][j]==0 for i in range(d) for j in range(d) if levels[i]<=levels[j])
 A=[[F((i*7+j*3)%11-5) for j in range(8)] for i in range(8)]
 Y,Z=mul(A,om),mul(tr(A),ps)
 rhs=[]
 for i in range(d):
  if types[i]=='F':rhs.append(dot(mul([left[i]],Y)[0],ro[i]))
  else:rhs.append(dot(mul([right[i]],Z)[0],lp[i]))
 x=mul(add(add(eye(d),K,-1),K2),[[v] for v in rhs]);x=[v[0] for v in x]
 coeff=[]
 for us,vs in fixed:
  U=bd([[[c],[s]] for c,s in us]);V=bd([[[a],[b]] for a,b in vs]);Dblocks=[]
  for i,((c,s),(a,b)) in enumerate(zip(us,vs)):
   ui,wi,vi,zi=[c,s],[-s,c],[a,b],[-b,a]
   oo,pp=om[2*i:2*i+2],ps[2*i:2*i+2];yy,zz=Y[2*i:2*i+2],Z[2*i:2*i+2]
   f,g=mul([vi],oo)[0],mul([zi],oo)[0];p,q=mul([ui],pp)[0],mul([wi],pp)[0]
   yd,zd=mul([wi],yy)[0],mul([zi],zz)[0]
   aa,bb,cc=dot(yd,f),dot(yd,g),dot(p,zd);coeff += [aa,bb,cc]
   db=add(add([[aa*z for z in row] for row in outer(wi,vi)],[[bb*z for z in row] for row in outer(wi,zi)]),[[cc*z for z in row] for row in outer(ui,zi)])
   Dblocks.append(db)
  D=bd(Dblocks);Y,Z=mul(tr(U),add(Y,mul(D,om),-1)),mul(tr(V),add(Z,mul(tr(D),ps),-1));om,ps=mul(tr(V),om),mul(tr(U),ps)
 coeff += [v for row in mul(Y,tr(om)) for v in row]
 assert coeff==x
 report=dict(status='PASS',arithmetic='Fraction only',N=8,k=1,L=2,width=3,
             coefficient_dimension=d,strict_ancestor=True,K_cubed_zero=True,
             original_sample_solve_equals_LM=True)
 with open('triangular_regression_exact_results.json','w') as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2))


if __name__=='__main__':main()
