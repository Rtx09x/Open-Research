#!/usr/bin/env python3
"""Exact row generation for continuous convex mixtures of overflow charges.
SciPy only discovers LP supports; exact rational primal/dual checks certify
finite LPs, and exact nonlinear knapsack pricing certifies all omitted patterns.
Between residual remainders, all column vectors are affine in1/(B-c), so the
listed remainder columns span every c in[0,d] for the current finite row set.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import json,math,time,warnings
import numpy as np
from scipy.optimize import linprog
from verify_nonlinear_independent import reconstruct,D
H=Path(__file__).resolve().parent

def tiny_parameters(P,s):
 x,y,w=Q(s['x']),Q(s['y']),Q(s['w']);B=b=Q(0)
 for v,a in P[212]['a'].items():
  B+=v*a
  rw=(Q(1) if v>=1-x else w) if v>Q(1,2) else (1-w if v<=x else Q(1))
  b+=a*rw
 return B,b

def extra(r,c):
 q,e=divmod(r,D);return q*(D-c)+max(Q(0),e-c)

def price(items,cap,B,b,mix,offset):
 terms=[(c,z*b/(B-c)) for c,z in mix if z and c<D]
 a=sum(z*b/(B-c) for c,z in mix)
 S=math.lcm(cap.denominator,D.denominator,*[c.denominator for c,z in terms],*[s.denominator for j,s,w in items])
 W=math.lcm(a.denominator,*[z.denominator for c,z in terms],*[w.denominator for j,s,w in items])
 C=int(cap*S);dd=int(D*S);aa=int(a*W);T=[(int(c*S),int(z*W)) for c,z in terms]
 raw=[]
 for j,s,w in items:
  size=int(s*S);g=int(w*W)*S-aa*size
  if 0<size<C and g>0:raw.append((j,size,g))
 keep=[t for t in raw if not any(u[1]<=t[1] and u[2]>=t[2] and(u[1]<t[1] or u[2]>t[2] or u[0]<t[0]) for u in raw)]
 keep.sort(key=lambda t:Q(t[2],t[1]),reverse=True)
 def hinge(space):
  q,e=divmod(space,dd);return sum(z*(q*(dd-c)+max(0,e-c)) for c,z in T)
 extra_density=sum(Q(z*(dd-c),dd) for c,z in T);best=hinge(C);bestpat=[];nodes=0;path=[]
 def visit(i,space,value):
  nonlocal best,bestpat,nodes
  nodes+=1;v=value+hinge(space)
  if v>best:best=v;bestpat=path.copy()
  if i==len(keep):return
  j,size,gain=keep[i];bound=max(Q(gain,size),extra_density)
  if value*bound.denominator+space*bound.numerator<=best*bound.denominator:return
  for n in range((space-1)//size,-1,-1):
   if n:path.append((j,n))
   visit(i+1,space-n*size,value+n*gain)
   if n:path.pop()
 visit(0,C,0)
 return Q(aa*C+best,W*S)+offset,tuple(sorted(bestpat)),nodes

def solve(A,v):
 n=len(v);M=[list(row)+[rhs] for row,rhs in zip(A,v)]
 for k in range(n):
  p=next((i for i in range(k,n) if M[i][k]),None)
  if p is None:return None
  M[k],M[p]=M[p],M[k];z=M[k][k];M[k]=[t/z for t in M[k]]
  for i in range(n):
   if i!=k and M[i][k]:
    z=M[i][k];M[i]=[a-z*b for a,b in zip(M[i],M[k])]
 return [r[-1] for r in M]

def exact_lp(rows,cols,B,b):
 A=[[b/(B-c)*(r['residual']+extra(r['residual'],c)) for c in cols] for r in rows]
 cons=[r['constant'] for r in rows];nc=len(cols)
 with warnings.catch_warnings():
  warnings.simplefilter('ignore')
  z=linprog([0.0]*nc+[1.0],A_ub=[[float(v) for v in row]+[-1.0] for row in A],b_ub=[-float(c) for c in cons],A_eq=[[1.0]*nc+[0.0]],b_eq=[1.0],bounds=[(0,None)]*nc+[(None,None)],method='highs',options={'threads':1})
 assert z.success,z.message
 support=[j for j in range(nc) if z.x[j]>1e-9];K=len(support)
 active=sorted(range(len(rows)),key=lambda i:abs(float(cons[i])+sum(float(A[i][j])*z.x[j] for j in range(nc))-z.x[-1]))
 active=[i for i in active if abs(float(cons[i])+sum(float(A[i][j])*z.x[j] for j in range(nc))-z.x[-1])<1e-7]
 answer=None
 for act in combinations(active,K):
  mat=[[Q(1)]*K+[Q(0)]]+[[A[i][j] for j in support]+[-Q(1)] for i in act]
  rhs=[Q(1)]+[-cons[i] for i in act];ans=solve(mat,rhs)
  if ans is None or min(ans[:-1])<0:continue
  if any(cons[i]+sum(A[i][j]*ans[t] for t,j in enumerate(support))>ans[-1] for i in range(len(rows))):continue
  answer=ans;break
 assert answer is not None,('exact primal reconstruction failed',support,active)
 theta=[Q(0)]*nc
 for j,v in zip(support,answer[:-1]):theta[j]=v
 R=answer[-1]
 # Independent exact dual reconstruction/check over all remainder columns.
 sr=[i for i,v in enumerate(z.ineqlin.marginals) if v< -1e-9];L=len(sr);dual=None
 for sc in combinations(support,L):
  mat=[[Q(1)]*L+[Q(0)]]+[[A[i][j] for i in sr]+[-Q(1)] for j in sc]
  ans=solve(mat,[Q(1)]+[Q(0)]*L)
  if ans is None or min(ans[:-1])<0:continue
  if any(sum(A[i][j]*ans[t] for t,i in enumerate(sr))<ans[-1] for j in range(nc)):continue
  if sum(cons[i]*ans[t] for t,i in enumerate(sr))+ans[-1]!=R:continue
  dual={'rows':sr,'lambda':ans[:-1],'v':ans[-1]};break
 assert dual is not None,('exact dual reconstruction failed',support,sr)
 return [(c,t) for c,t in zip(cols,theta) if t],R,dual

def optimize(P,s):
 normal,huge,*_=reconstruct(P,s);cases=[normal,huge];caps=[Q(1),Q(s['y'])];B,b=tiny_parameters(P,s);rows=[];seen=set();history=[]
 def add(hi,pat):
  key=(hi,pat)
  if key in seen:return False
  seen.add(key);look={j:(sz,w) for j,sz,w in cases[hi]};res=caps[hi]-sum(look[j][0]*n for j,n in pat)
  rows.append({'huge':bool(hi),'pattern':pat,'residual':res,'constant':Q(hi)+sum(look[j][1]*n for j,n in pat)});return True
 for mix in [[(D,Q(1))],[(D,Q(53,60)),(Q(1,60),Q(7,60))]]:
  for hi in [0,1]:v,p,n=price(cases[hi],caps[hi],B,b,mix,hi);add(hi,p)
 for iteration in range(30):
  cols=sorted({Q(0),D}|{r['residual']%D for r in rows});mix,R,dual=exact_lp(rows,cols,B,b)
  prices=[price(cases[hi],caps[hi],B,b,mix,hi) for hi in [0,1]];maxR=max(p[0] for p in prices)
  history.append({'iteration':iteration,'row_count':len(rows),'column_count':len(cols),'lower':str(R),'upper':str(maxR),'mix':[(str(c),str(t)) for c,t in mix]})
  print('scenario',s['x'],s['y'],'iteration',iteration,'rows',len(rows),'cols',len(cols),'bounds',float(R),float(maxR),flush=True)
  if maxR==R:
   return {'x':s['x'],'y':s['y'],'target':R,'mixture':mix,'rows':rows,'dual':dual,'columns':cols,'history':history,'oracle_cases':[{'value':v,'pattern':p,'nodes':n} for v,p,n in prices]}
  assert maxR>R
  for hi,(v,p,n) in enumerate(prices):
   if v>R:assert add(hi,p)
 raise RuntimeError('30-round checkpoint reached without exact closure')

if __name__=='__main__':
 start=time.time();f=json.loads((H.parent/'ah_three_parameter_full_certificate.json').read_text());P={int(j):{'lo':Q(p['lower']),'hi':Q(p['upper']),'a':{Q(i):Q(a) for i,a in p['containers']}} for j,p in f['parameters'].items()}
 keys={(Q(533,1600),Q(1,3)),(Q(3,7),Q(1,2)),(Q(49,320),Q(1,6))};results=[]
 for s in f['scenarios']:
  if (Q(s['x']),Q(s['y'])) in keys:results.append(optimize(P,s))
 out={'status':'three scenario continuous-mixture optima exactly certified; global repricing pending','results':results,'target':max(r['target'] for r in results),'seconds':time.time()-start}
 (H/'continuous_mixture_search.json').write_text(json.dumps(out,default=str,indent=2));print('RESULT',str(out['target']),float(out['target']),out['seconds'])
