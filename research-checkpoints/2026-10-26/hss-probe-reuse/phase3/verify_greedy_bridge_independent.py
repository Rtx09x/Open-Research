"""Independent exact check of the external all-depth greedy HSS family.
Full sparse row/column covariance decisions, not hard-coded basis choices.
Uses Fraction only. This is a verifier plus an algebraic proof audit, not novelty.
"""
from fractions import Fraction as F
import json


def sq(a):return sum(v*v for v in a.values())
def dot(a,b):return sum(v*b.get(j,0) for j,v in a.items())
def select(a,n,transpose=False):
 groups={}
 for (r,c),v in a.items():
  if transpose:r,c=c,r
  groups.setdefault(r,{})[c]=v
 chosen=[];competitions=[]
 for p in range(n//2):
  x,y=groups.get(2*p,{}),groups.get(2*p+1,{})
  g0,g1,cross=dot(x,x),dot(y,y),dot(x,y)
  assert cross==0
  keep=0 if g0>=g1 else 1
  chosen.append(2*p+keep)
  if g0 and g1:
   assert {g0,g1}=={F(1),F(9,4)}
   competitions.append((p,str(g0),str(g1),keep))
 return chosen,competitions


def case(L):
 n=2**(L+1);w=2**L;z=3*2**(L-1)
 a={(2**j,w):F(1) for j in range(L)};a[0,z]=F(3,2)
 original=a.copy();rmap=list(range(n));cmap=list(range(n));loss=[];decisions=[]
 for level in range(1,L+1):
  assert all(r//2!=c//2 for r,c in a)
  u,ud=select(a,n);v,vd=select(a,n,True)
  ur={r:i for i,r in enumerate(u)};vr={c:i for i,c in enumerate(v)}
  nxt={(ur[r],vr[c]):val for (r,c),val in a.items() if r in ur and c in vr}
  residual={key:val for key,val in a.items() if key[0] not in ur or key[1] not in vr}
  assert sq(a)==sq(nxt)+sq(residual)
  assert sq(residual)==1
  loss.append(sq(residual));decisions.append(dict(level=level,row_competitions=ud,column_competitions=vd))
  rmap=[rmap[r] for r in u];cmap=[cmap[c] for c in v];a=nxt;n//=2
 output={(rmap[r],cmap[c]):val for (r,c),val in a.items()}
 assert output=={(0,z):F(3,2)}
 error={key:val-output.get(key,0) for key,val in original.items()}
 assert sq(error)==L
 # Root-cut singular values squared are L and9/4; global rank-one signal attains9/4.
 optimum=min(F(L),F(9,4));assert optimum==F(9,4)
 weighted=sum(F(3+20*(L-ell+1))*e for ell,e in enumerate(loss,1))
 assert weighted==10*L*L+13*L
 return dict(L=L,N=2**(L+1),optimum_squared=str(optimum),level_losses=[str(x) for x in loss],
             greedy_error_squared=str(sq(error)),weighted_ledger=str(weighted),
             ratio_weighted_over_L_optimum=str(weighted/(L*optimum)),decisions=decisions)


def main():
 report=dict(status='PASS',arithmetic='Fraction sparse exact covariance selection',
             external_claim_independently_implemented=True,results=[case(L) for L in range(3,13)])
 with open('greedy_bridge_independent_results.json','w') as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2))


if __name__=='__main__':main()
