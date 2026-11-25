"""Exact actual-frame branch vs normalized recurrence; finite orientation group.
Also checks independent full N8 coefficient regression inverse on20 assignments.
"""
from fractions import Fraction as F
from itertools import permutations,product
import json,random
from verify_triangular_regression_exact import dot,tr,mul,eye,lin
from verify_wide_reachable_cone import step,cost


def group():
 return [[[F(signs[i]) if j==p[i] else F(0) for j in range(2)] for i in range(2)] for p in permutations(range(2)) for signs in product([-1,1],repeat=2)]
def bank_path(c,s,top,source):
 e=eye(3);comp=mul(top,[e[1],e[2]]);g=comp[0]
 fchild=lin(c,-s,e[0],g);base=[lin(s,c,e[0],g),comp[1]]
 return e[0],g,mul(source,base)[0]
def branch(left,right,kind):
 P,Q,Qchild=left;F0,G,Gchild=right
 y=[F(0)]*3 if kind=='da' else [-v for v in Gchild]
 z=[-v for v in Qchild] if kind=='da' else [F(0)]*3
 r,t,a,b=F(8,17),F(-15,17),F(7,25),F(-24,25)
 da,dd,ad=t*dot(y,F0),t*dot(y,G),b*dot(z,P)
 yn=[r*v-ad*w for v,w in zip(y,G)]
 coeff=[da,dd,ad,yn[0],yn[1]]
 return coeff


def atoms(fixed):
 le=[];ri=[];typ=[];eu=ev=eye(8)
 for us,vs in fixed:
  nu=[];nv=[]
  for i,((c,s),(a,b)) in enumerate(zip(us,vs)):
   u,w=lin(c,s,eu[2*i],eu[2*i+1]),lin(-s,c,eu[2*i],eu[2*i+1]);v,z=lin(a,b,ev[2*i],ev[2*i+1]),lin(-b,a,ev[2*i],ev[2*i+1])
   le +=[w,w,u];ri +=[v,z,z];typ +=['F','F','T'];nu.append(u);nv.append(v)
  eu,ev=nu,nv
 for u in eu:
  for v in ev:le.append(u);ri.append(v);typ.append('F')
 return le,ri,typ

def physical_probe(fixed,side,ht,hs):
 e=eye(3);inc=[(e[0],[e[1],e[2]]),(e[1],[e[0],e[2]])]
 for ell in reversed(range(2)):
  nxt=[];rows=[]
  for node,(c,s) in enumerate(fixed[ell][side]):
   f,base=inc[node];h=ht if ell==1 and node==0 else hs if ell==0 and node==0 else eye(2)
   comp=mul(h,base);g=comp[0];f0,f1=lin(c,-s,f,g),lin(s,c,f,g)
   rows +=[f0,f1];nxt +=[(f0,[lin(s,c,f,g),comp[1]]),(f1,[lin(-c,s,f,g),comp[1]])]
  inc=nxt
 return rows


def main():
 gg=group();lp=[bank_path(F(8,17),F(15,17),a,b) for a in gg for b in gg];rp=[bank_path(F(7,25),F(24,25),a,b) for a in gg for b in gg]
 sums=[F(0),F(0)];cross=F(0)
 for left in lp:
  for right in rp:
   x,y=branch(left,right,'da'),branch(left,right,'ad');sums[0]+=1+dot(x,x);sums[1]+=1+dot(y,y);cross+=dot(x,y)
 p,q=F(15,17)**2,F(24,25)**2;expected=[]
 for kind in ['da','ad']:
  v=(F(0),F(0),F(kind=='ad'),F(kind=='da'));e=1+cost(*v,p,q,2);X,Z,U,W=step(*v,p,q,2);expected.append(e+X+U/2)
 means=[v/4096 for v in sums];assert means==expected and cross==0
 fixed=[([(F(3,5),F(4,5))]*4,[(F(5,13),F(12,13))]*4), ([(F(8,17),F(15,17))]*2,[(F(7,25),F(24,25))]*2)]
 le,ri,typ=atoms(fixed);rng=random.Random(9731)
 for trial in range(20):
  ids=[rng.randrange(8) for _ in range(4)];hu,gu,hv,gv=[gg[i] for i in ids]
  om=physical_probe(fixed,1,hv,gv);ps=physical_probe(fixed,0,hu,gu);ro,pl=mul(ri,om),mul(le,ps)
  T=[[dot(le[i],le[j])*dot(ro[i],ro[j]) if typ[i]=='F' else dot(ri[i],ri[j])*dot(pl[i],pl[j]) for j in range(22)] for i in range(22)]
  for source,kind in [(0,'da'),(2,'ad')]:
   x=[]
   for i in range(22):x.append((F(i==source)-sum(T[i][j]*x[j] for j in range(i)))/T[i][i])
   bc=branch(bank_path(F(8,17),F(15,17),hu,gu),bank_path(F(7,25),F(24,25),hv,gv),kind)
   assert dot(x,x)==1+dot(bc,bc)
 report=dict(status='EXACT_FRACTION_PASS',orientation_assignments=4096,inverse_da_mean=str(means[0]),inverse_ad_mean=str(means[1]),same_birth_cross_mean='0',full_N8_inverse_controls=40,scope='Finite two-level actual-frame bridge; all-depth proof is separate')
 print(json.dumps(report,indent=2));open('wide_inverse_branch_exact_results.json','w').write(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
