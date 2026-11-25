"""Independent exact verifier: Python standard library only, no NumPy/SciPy.
Checks the rational nonmonotone-energy witness, NOT any failure of RE-02.
"""
from fractions import Fraction as Q
import json,itertools,pathlib,time
p=pathlib.Path(__file__).resolve().parent
c=json.loads((p/'rational_potential_certificate.json').read_text())
params=c['coarse_rotation_halfangle_parameters']
bases=[]
for level in params:
 sides=[]
 for side in level:
  us=[]
  for text in side:
   t=Q(text);us.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
  sides.append(us)
 bases.append(sides)
a=list(map(Q,c['input_active_coefficients']))

def dot(x,y):return sum((u*v for u,v in zip(x,y)),Q(0))
def scale(s,x):return [s*t for t in x]
def add(x,y):return [u+v for u,v in zip(x,y)]
def sub(x,y):return [u-v for u,v in zip(x,y)]
def normsq(rows):return sum((dot(row,row) for row in rows),Q(0))
def frame(side,signs):
 rows=[[Q(1),Q(0)],[Q(0),Q(1)]];cursor=0
 for level in reversed(bases):
  new=[]
  for i,(u,v) in enumerate(level[side]):
   f=rows[i];g=[-signs[cursor]*f[1],signs[cursor]*f[0]];cursor+=1
   new.append(sub(scale(u,f),scale(v,g)));new.append(add(scale(v,f),scale(u,g)))
  rows=new
 return rows

def shrink(y,z,om,ps,level):
 yy=[];zz=[];oo=[];pp=[]
 for i,((u0,u1),(v0,v1)) in enumerate(zip(level[0],level[1])):
  y0,y1=y[2*i:2*i+2];z0,z1=z[2*i:2*i+2];o0,o1=om[2*i:2*i+2];p0,p1=ps[2*i:2*i+2]
  ya=add(scale(u0,y0),scale(u1,y1));yd=add(scale(-u1,y0),scale(u0,y1))
  za=add(scale(v0,z0),scale(v1,z1));zd=add(scale(-v1,z0),scale(v0,z1))
  f=add(scale(v0,o0),scale(v1,o1));g=add(scale(-v1,o0),scale(v0,o1))
  ph=add(scale(u0,p0),scale(u1,p1));qh=add(scale(-u1,p0),scale(u0,p1))
  dad=dot(ph,zd);dda=dot(yd,f)
  yy.append(sub(ya,scale(dad,g)));zz.append(sub(za,scale(dda,qh)));oo.append(f);pp.append(ph)
 return yy,zz,oo,pp

def value(signs):
 om=frame(1,signs[:6]);ps=frame(0,signs[6:]);g0=[-om[0][1],om[0][0]]
 weighted=[sum((a[j]*ps[j][col] for j in range(8)),Q(0)) for col in range(2)]
 b=dot(ps[0],weighted);aa=a.copy();aa[0]-=b;y=[scale(v,g0) for v in aa];z=[[Q(0),Q(0)] for _ in range(8)]
 y,z,om,ps=shrink(y,z,om,ps,bases[0]);before=normsq(y)+normsq(z)
 y,z,om,ps=shrink(y,z,om,ps,bases[1]);after=normsq(y)+normsq(z)
 return after-before

if __name__=='__main__':
 t=time.time();total=Q(0);count=0
 for signs in itertools.product([-1,1],repeat=12):total+=value(signs);count+=1
 mean=total/count;expected=Q(c['expected_energy_increase_exact']);assert mean==expected
 assert mean>0 and count==4096
 print('PASS: independent exact rational verification over4096 sign choices.')
 print('Expected final-level energy increase =',mean)
 print('Decimal (display only) =',float(mean),'elapsed seconds =',round(time.time()-t,3))
 print('Scope: disproves the monotone-energy shortcut only; no counterexample to RE-02 or to the uniform-energy bound.')
