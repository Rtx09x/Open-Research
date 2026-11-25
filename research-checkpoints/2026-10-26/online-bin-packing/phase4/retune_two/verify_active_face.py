#!/usr/bin/env python3
"""Exact P/Z/G fixed-charge two-coordinate floor, no discovery imports."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_single_thresholds import weights
J=json.loads((HERE/'retuned_certificate.json').read_text());S=json.loads((ROOT/'phase4/ordered_suffix/ordered_suffix_certificate.json').read_text())
def parse(J):return {int(j):{'lo':F(r['lower']),'hi':F(r['upper']),'alpha':{F(i):F(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
P=parse(J);OLD=parse(S);s=next(z for z in J['scenarios'] if(z['x'],z['y'])==('3/7','1/2'));N,_,B,b,_,_=weights(P,s);ON,*_=weights(OLD,s)
look={j:(sz,w) for j,sz,w in N};oldlook={j:(sz,w) for j,sz,w in ON}
def coord(P,j):return 1/sum(i*a for i,a in P[j]['alpha'].items())
x,y=coord(P,179),coord(P,167);ox,oy=coord(OLD,179),coord(OLD,167)
assert F(1,10)<x<F(1,2) and F(1,3)<y<1
assert P[179]['alpha'][F(2)]==(10-1/x)/8 and P[167]['alpha'][F(1)]==(3-1/y)/2
c=F(997,2100120);g=F(11,500);R=F(J['target'])
def row(pattern,L):
 r=1-sum(L[j][0] for j in pattern);K=sum(L[j][1] for j in pattern);assert 0<r<F(1,43)
 tiny=b*r/(B-c) if r<=c else b*(r+max(F(0),r-g))/(B-g)
 return r,K+tiny
p,PV=row([1,165,179,205,208,211],look);z,ZV=row([1,167,168,189],look);rr,GV=row([1,165,172],look)
_,OP=row([1,165,179,205,208,211],oldlook);_,OZ=row([1,167,168,189],oldlook);_,OG=row([1,165,172],oldlook)
assert p==c and z==F(1,3360) and rr==F(1,60) and PV==ZV==GV==OG==R
assert (PV-OP)/(x-ox)==-F(1,4) and (ZV-OZ)/(y-oy)==-F(1,2)
CP=PV+x/4;CZ=ZV+y/2;assert x==4*(CP-R) and y==2*(CZ-R)
out={'status':'PASS exact fixed-charge two-coordinate optimum','target':str(R),'target_decimal':float(R),'x':str(x),'y':str(y),'P_intercept':str(CP),'P_slope_x':'-1/4','Z_intercept':str(CZ),'Z_slope_y':'-1/2','constant_G_pattern':[1,165,172],'constant_G_residual':str(rr),'scope':'classes167/179 proportions only, fixed other parameters and fixed charges; not joint analysis/algorithm optimum or true ratio','certificate_sha256':hashlib.sha256((HERE/'retuned_certificate.json').read_bytes()).hexdigest()}
(HERE/'active_face_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
