from fractions import Fraction as F
from itertools import combinations
import json

def profiles(m):
 g=[1/(F(3)+F(i+1,m+1)) for i in range(m)]; C=sum(g)
 pairs=[(i,i+1) for i in range(0,m-1,2)]
 if m%2: pairs.append((m-2,m-1))
 S=[]
 for i in range(m):
  for side in ['s','t']:
   v=[]
   for p,q in pairs:
    d=g[p]-g[q]
    if i==p: a=d+(1/g[p]-1)*C if side=='s' else C-d
    elif i==q: a=(1/g[q]-1)*C-d if side=='s' else C+d
    else: a=d
    v.append(a*a)
   S.append(v)
 return g,C,pairs,S
if __name__ == "__main__":
 out=[]
 for m in range(3,61):
  g,C,pairs,S=profiles(m)
  keys=[tuple(a/v[0] for a in v) for v in S]
  assert len(set(keys))==2*m,(m,'collision')
  for j,(p,q) in enumerate(pairs):
   d=g[p]-g[q]; inc=[S[2*p][j],S[2*p+1][j],S[2*q][j],S[2*q+1][j]]
   assert len(set(inc))==4 and min(inc)>d*d
  out.append({'m':m,'queries':len(pairs),'rays':len(set(keys)),'exact':True})
 print(json.dumps(out,indent=2))
