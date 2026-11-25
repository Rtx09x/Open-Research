#!/usr/bin/env python3
"""Exact restricted-family shared-fork obstruction, no solver or worker imports."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
r=F(3857,2500);z=r/6;t=(2-r)/6;a=F(3,14);s=F(5,14)
oldlo=F(304,4375);oldhi=F(403,1250)
k=F(1,2)-2*(r-1)*s
inter=2*(r-1)*a-F(1,4)-k/6;slope=F(1,4)-k/6
lo=-inter/slope;hi=4*r*a-1
assert lo==F(1263,8095) and hi==oldhi and oldlo<lo<hi
assert slope>0 and k>0 and r*s>F(1,2)
f=F(1,5);beta=(1+f)/4;hard=(1-f)/4;pair=f/2;lam=(1+f)/6
assert beta==F(3,10) and hard==F(1,5) and pair==F(1,10) and lam==F(1,5)
Bmargin=r*a-beta;Cmargin=inter+slope*f
Dconst=(r-1)/18;Dmargin=(r-1)/2-hard
assert Bmargin==F(153,5000)>0 and Cmargin==F(89,8750)>0
assert Dconst>0 and Dmargin==F(357,5000)>0
assert 2*(r-1)*F(1,6)-z+t==0
assert (r-1)*F(7,18)-z+t==Dconst
assert r/2-1<0 and r*F(4,7)-1<0 and r-1>0

# Uniform perturbations, not an error that grows unchecked with b.
delta=F(1,10000)
assert Bmargin-r*delta>0
assert Cmargin-2*(r-1)*delta>0
assert Dmargin-F(7,3)*(r-1)*delta>0
assert max(2*(r-1),F(7,3)*(r-1))<r
assert r*(s-delta)>F(1,2)
assert Cmargin-2*(r-1)*(delta+lam*delta)>0
# The sign-reversed B/E perturbation does not evade this volume-only proof.
# A complementary D need only be above half and fit the preserved ready slots.
assert 2*(r-1)*(a-delta)-hard>0

# Independently reconstruct the exact inherited nine-state prefix.
rows=[((0,0,2),F(1021879,15000000)),((0,0,4),F(143,3000)),((0,0,6),F(1569121,15000000)),((0,6,1),F(121121,15000000)),((0,6,6),F(16869037,24675000000)),((0,41,1),F(93466153,4112500000)),((2,6,6),F(118071,70000000)),((6,20,4),F(1011847,9870000000)),((288,1,0),F(2438153,705000000))]
assert [sum(p[j]*m for p,m in rows) for j in range(3)]==[1,1,1]
assert sum(m for p,m in rows)==z
assert rows[0][1]+rows[3][1]==t
eps=F(1,10**12);c3=F(1,294)-294*eps;c2=(1+28*eps)/49;amax=(1+2*eps)/7
Delta=F(2053,7)*eps
assert c3+c2+(1+eps)/7==F(1,6)-Delta
for p,m in rows:assert p[0]*c3+p[1]*c2+p[2]*amax<=1

# A small genuinely causal separator trace: pick offset BEFORE each observed
# placement, then shrink the exponent interval according to the resulting mark.
T=10;left,right=1,2**(T+2);bins=[];offsets=[];marks=[]
word=[0,0,1,1,1,1,2,2,2,2]
for destination in word:
    exponent=(left+right)//2;offset=eps**2/F(8**exponent)
    while len(bins)<=destination:bins.append([])
    marked=len(bins[destination])>=2
    offsets.append(offset);marks.append(marked);bins[destination].append(a-eps+offset)
    if marked:left=exponent+1
    else:right=exponent-1
    assert left<=right
gamma=max(v for v,m in zip(offsets,marks) if not m)
assert all(v>4*gamma for v,m in zip(offsets,marks) if m)
assert sum(marks)==4 and all(sum(b)<1 for b in bins)
E=s+3*eps-3*gamma;D=F(4,7)+2*eps-2*gamma;C=F(1,2)+eps/4
bsmall=a-eps+gamma;bmax=a-eps+eps**2;bmin=a-eps
assert E>s and D>F(4,7) and C>F(1,2)
assert 2*E<1 and 4*bmax<1
assert E+3*bsmall<=1 and D+2*bsmall<=1
for v,m in zip(offsets,marks):
    if m:
        assert E+(a-eps+v)+2*bmin>1
        assert D+(a-eps+v)+bmin>1
for ready in [2*amax,6*c2+amax,2*bsmall]:
    assert ready+C<1 and ready+D<=1
Eabove=s-3*eps-3*gamma;Babove=a+eps+gamma
Dabove=F(4,7)-2*eps-2*gamma
assert 2*Eabove<1 and Eabove+C+amax<1
assert Dabove>F(1,2) and Dabove+2*Babove<=1
assert 2*Babove+C<1

# Exact natural-count offline constructions and defender costs; these upper
# constructions are NOT used in the universal survival proof.
b=F(13643,15000);h=(1-f)*b/2;e=(b-h)/3;dc=(b+h)/2
cc=e+b/2+F(1,4);y=(b-F(1,2))/2
assert e==b/5 and 6*e+3*y>=1 and h<=1
assert C+bmax+2*amax<1
assert C+E+6*(c3+c2)<1
assert C+2*bmax+3*(c3+c2)<1
assert E+3*bsmall<=1 and 4*bmax+amax<1
assert 6*(amax+c3+c2)<1 and 42*(c3+c2)<1
AB=z+beta*b;AE=AB+e/2;AC=max(AE,AE+cc-t-pair*b)
AD=max(AB,AB+dc-t-pair*b)
assert r*cc-AC>0
assert r*(F(1,6)+a*b+F(4,7)*dc)-AD>0

# Finite-prefix counts of the causal 10-B/2-E schedules have uniformly bounded
# discrepancy, independently of the eventual batch lengths.
maxerr=F(0)
for n in range(501):
    block,tail=divmod(n,10)
    opened=3*block+len(set(word[:tail]))
    pairs=block+int(tail>=2)
    marked=4*block+max(0,min(tail-4,2))+max(0,tail-8)
    maxerr=max(maxerr,abs(opened-beta*n),abs(pairs-pair*n),abs(marked-F(2,5)*n))
    assert abs(opened-beta*n)<=3 and abs(pairs-pair*n)<=1 and abs(marked-F(2,5)*n)<=4
assert maxerr<=4
out={'status':'PASS restricted causal obstruction, not a global online algorithm',
 'ratio':str(r),'surviving_f_interval':[str(lo),str(hi)],'selected_f':str(f),
 'B_margin':str(Bmargin),'C_uniform_cone_margin':str(Cmargin),'D_constant_margin':str(Dconst),'D_slope_margin':str(Dmargin),
 'uniform_B_deficit_bound':str(delta),'causal_separator_items':T,'causal_separator_marked':sum(marks),
 'natural_counts':{k:str(v) for k,v in [('b',b),('h',h),('e',e),('D',dc),('C',cc),('ALG_B',AB),('ALG_E',AE),('ALG_C',AC),('ALG_D',AD),('C_actual_OPT_slack',r*cc-AC)]},
 'scope':'fixed nine-state prefix; common B history branches to arbitrary D, or E prefixes up to(b-h)/3 followed by arbitrary near-half C; actual OPT lower bounds used'}
(H/'shared_fork_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
