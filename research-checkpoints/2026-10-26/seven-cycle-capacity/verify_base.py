#!/usr/bin/env python3
"""Independent exact checks: ordinary coordinate pairs and disjoint binary cubes."""
import json,itertools,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
D=json.load(open(ROOT/'published/data/base_c7.json'))
def word(w):
 if isinstance(w,int):return tuple((w//7**j)%7 for j in range(5))
 if isinstance(w,str):return tuple(map(int,w))
 return tuple(w)
def verify(C):
 C=list(map(word,C));d=len(C[0]);assert len(set(C))==len(C)
 for u,v in itertools.combinations(C,2):
  assert any((a-b)%7 not in (0,1,6) for a,b in zip(u,v)),(u,v)
 # Independently: closed {x,x+1} cubes intersect exactly for confusable words.
 occupied={}
 for w in C:
  for offset in itertools.product((0,1),repeat=d):
   point=tuple((a+b)%7 for a,b in zip(w,offset))
   assert point not in occupied,(w,occupied.get(point))
   occupied[point]=w
 return {'words':len(C),'dimension':d,'pair_comparisons':len(C)*(len(C)-1)//2,'disjoint_cube_points':len(occupied),'sha256':hashlib.sha256(json.dumps(sorted(C)).encode()).hexdigest()}
if __name__=='__main__':
 result={k:verify(D[k]) for k in ('I0','X')}
 (ROOT/'base_verification.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
