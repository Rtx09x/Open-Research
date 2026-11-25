"""Independent exact three-pattern lower envelope within the two-proportion AH family.
This is optimality of the fixed-weight analysis family, NOT an online lower bound.
"""
from pathlib import Path
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parents[1]
exec(Path(__file__).with_name('source_tables.py').read_text())
d=json.loads((ROOT/'ah_three_parameter_result.json').read_text())

def weights(x,y,w):
 result={1:F(w)}
 for j,p in classes.items():
  if j==2 and y>F(1,3):continue # threshold weight unused by the three patterns
  num=den=F(0)
  for i,a in p['types']:
   vol=i if j==212 else i*p['max']
   if vol>F(1,2):rw=w if vol<=1-y else F(1);assert vol<=1-y or vol>=1-x
   else:rw=1-w if vol<=x else F(1);assert vol<=x or vol>=y
   num+=a*rw;den+=a*(i-F(1,43)if j==212 else i)
  result[j]=num/den
 return result
crit=weights(F(3,10)+F(159,4800),F(1,3),F(413913,524288));high=weights(F(3,7),F(1,2),F(1))
alpha=dict(classes[172]['types']);w0=F(413913,524288)
pattern=[(1,1),(165,1),(172,1)]
size=lambda j:F(1,2)if j==1 else classes[j]['min']
used=sum(size(j)*m for j,m in pattern);assert used<1
c=(2-alpha[F(1)])/4;b=1-alpha[F(1)]*w0
C1=high[212]*(1-used)+high[1]+high[165]+F(1,4)
C2=crit[212]*(1-used)+crit[1]+crit[165]
lines=[(C1,-c),(C2,b)];assert lines==[tuple(map(F,r))for r in d['two_lines']]
x=1/(sum(i*a for i,a in alpha.items())+4*F(d['delta']));R=F(d['target'])
assert all(a+bb*x==R for a,bb in lines)
lam=[b/(b+c),c/(b+c)];assert lam==list(map(F,d['dual']))
assert sum(lam)==1 and min(lam)>0 and sum(t*line[1]for t,line in zip(lam,lines))==0 and sum(t*line[0]for t,line in zip(lam,lines))==R
out={'status':'PASS','exact':True,'same_physical_pattern':[1,165,172],'strict_infimum_feasibility':True,'two_affine_lines_independently_derived':True,'positive_dual':list(map(str,lam)),'intersection':str(R),'scope':'floor for fixed published weight-function analysis with classes167,172,179 transfers only; not an algorithm lower bound or global AH optimum'}
Path(__file__).with_name('ah_two_scenario_floor_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
