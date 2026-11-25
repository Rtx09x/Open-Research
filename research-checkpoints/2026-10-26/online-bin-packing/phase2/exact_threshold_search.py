#!/usr/bin/env python3
"""Float-free exact 1D convex threshold optimization with pattern generation.
Every pattern contributes two affine lower lines in z=1/(B-c); full exact
pricing supplies missing constraints. No SciPy/NumPy/SymPy dependencies.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import json,time
from exact_nonlinear_pricing import price,tiny_parameters,D
from verify_nonlinear_independent import reconstruct
H=Path(__file__).resolve().parent

def optimize(P,s):
 normal,huge,*_=reconstruct(P,s);items=[normal,huge];caps=[Q(1),Q(s['y'])];B,b=tiny_parameters(P,s)
 rows=[];lines=[];seen=set();lo=1/B;hi=1/(B-D);history=[]
 def add(huge,pattern):
  key=(huge,pattern)
  if key in seen:return False
  seen.add(key);lookup={j:(sz,w) for j,sz,w in items[huge]}
  r=caps[huge]-sum(lookup[j][0]*n for j,n in pattern);K=Q(huge)+sum(lookup[j][1]*n for j,n in pattern);q,e=divmod(r,D)
  row=len(rows);rows.append({'huge':bool(huge),'pattern':pattern,'residual':r,'constant':K})
  lines.extend([(K+b*q,b*(r+q*D-q*B),row,0),(K+b*(q+1),b*(2*r-(q+1)*B),row,1)])
  return True
 for h in [0,1]:v,p,n=price(items[h],caps[h],B,b,[(D,Q(1))],h);add(h,p)
 for it in range(30):
  choices={lo,hi}
  for (a,u,_,_),(c,v,_,_) in combinations(lines,2):
   if u!=v:
    z=(c-a)/(u-v)
    if lo<=z<=hi:choices.add(z)
  z=min(choices,key=lambda z:(max(a+u*z for a,u,_,_ in lines),z));lower=max(a+u*z for a,u,_,_ in lines);c=B-1/z
  results=[price(items[h],caps[h],B,b,[(c,Q(1))],h) for h in [0,1]];upper=max(v for v,p,n in results)
  history.append({'iteration':it,'patterns':len(rows),'c':c,'lower':lower,'upper':upper})
  print('scenario',s['x'],s['y'],'round',it,'patterns',len(rows),'gap',float(upper-lower),flush=True)
  if upper==lower:
   active=[line for line in lines if line[0]+line[1]*z==lower]
   negative=next(t for t in active if t[1]<0);positive=next(t for t in active if t[1]>0)
   lm=positive[1]/(positive[1]-negative[1]);lp=1-lm
   assert lm>0 and lp>0 and lm*negative[1]+lp*positive[1]==0 and lm*negative[0]+lp*positive[0]==lower
   return {'x':s['x'],'y':s['y'],'c':c,'target':lower,'dual_lines':[{'lambda':lm,'intercept':negative[0],'slope':negative[1],'pattern':rows[negative[2]],'piece':negative[3]},{'lambda':lp,'intercept':positive[0],'slope':positive[1],'pattern':rows[positive[2]],'piece':positive[3]}],'history':history,'oracle_nodes':[n for v,p,n in results]}
  assert upper>lower
  for h,(v,p,n) in enumerate(results):
   if v>lower:assert add(h,p)
 raise RuntimeError('finite30-round checkpoint exhausted')

if __name__=='__main__':
 start=time.time();J=json.loads((H.parent/'ah_three_parameter_full_certificate.json').read_text());P={int(j):{'lo':Q(p['lower']),'hi':Q(p['upper']),'a':{Q(i):Q(a) for i,a in p['containers']}} for j,p in J['parameters'].items()}
 selected={(Q(49,320),Q(1,6)),(Q(533,1600),Q(1,3)),(Q(3,7),Q(1,2))}
 out=[optimize(P,s) for s in J['scenarios'] if (Q(s['x']),Q(s['y'])) in selected]
 old=json.loads((H/'single_threshold_certificate.json').read_text());expected={(s['x'],s['y']):s for s in old['scenarios'] if 'target' in s}
 for s in out:assert s['c']==Q(expected[s['x'],s['y']]['c']) and s['target']==Q(expected[s['x'],s['y']]['target'])
 result={'status':'PASS; exact float-free discovery reproduces all three optimal thresholds','target':max(s['target'] for s in out),'seconds':time.time()-start,'results':out}
 (H/'exact_threshold_search.json').write_text(json.dumps(result,default=str,indent=2));print('PASS',float(result['target']),result['seconds'])
