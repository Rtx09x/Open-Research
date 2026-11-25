#!/usr/bin/env python3
"""Independent all-character covering test; no proposer imports."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
from math import prod,gcd,isqrt
import json,time,hashlib,resource,os
P=Path('/workspace/shared/research-active/seven-cycle-capacity/physical_iteration')
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(270,270))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
start=time.monotonic()
def types(n,last=2):
    # Independent recursive divisor construction, including final factor.
    for d in range(last,n+1):
        if n%d or d%last and last!=2: continue
        # At root last=2 is a lower bound only, not a divisibility constraint.
        if n==d: yield (d,)
        elif n//d>=d:
            for tail in types_tail(n//d,d): yield (d,)+tail
def types_tail(n,last):
    for d in range(last,n+1,last):
        if n%d: continue
        if n==d:yield(d,)
        elif n//d>=d:
            for tail in types_tail(n//d,d):yield(d,)+tail

# Derive the circulant theta dual rather than trust numerical theta values.
def plus(a,b):return(a[0]+b[0],a[1]+b[1])
def times(a,b):return(a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
y=[(F(60),F(-20)),(F(140),F(-60)),(F(90),F(-40))]
fourier=[[(F(1,2),F(-1,2)),(F(-1,2),F(-1,2)),(-1,0)],
         [(F(-1,2),F(-1,2)),(F(-1,2),F(1,2)),(1,0)],
         [(-2,0),(2,0),(-1,0)]]
for j,target in enumerate((20,20,10)):
    z=(F(target),F(0))
    for a,row in zip(y,fourier):z=plus(z,times(a,row[j]))
    assert z==(0,0)
assert all(a+b*F(9,4)>=0 for a,b in y)
assert F(67,30)**2<5<F(9,4)**2
assert F(16,5)**5<336
pi_lo=16*sum((-1)**i*F(1,5)**(2*i+1)/(2*i+1) for i in range(8))-4*F(1,239)
assert pi_lo>F(314159,100000)
x=F(314159,700000)
cu=1-x*x/2+x**4/24-x**6/720+x**8/40320
theta=7*cu/(1+cu)
assert theta**5<402 and 3*theta**4<368

def gate(ds,surj):
    e=ds[-1]; threshold=(2*e+6)//7
    if 3*e<=10*threshold:
        for a in range(e):
            for b in range(e):
                if min((a-b)%e,(b-a)%e)>=threshold:
                    u=(10*a//e-10*b//e)%10
                    assert min(u,10-u)>=3
        return 'theta',0
    group=list(product(*(range(d) for d in ds)))
    # Use a different representative ordering than the proposer: retain >=-g.
    differences=[g for g in group if any(g) and g>=tuple((-v)%d for v,d in zip(g,ds))
                 and (not surj or min(g[-1],e-g[-1])<threshold)]
    allbits=(1<<len(differences))-1
    masks=set()
    for a in group:
        coeff=[v*(e//d) for v,d in zip(a,ds)]
        order=e//gcd(e,*coeff)
        if not surj and order==e:continue
        if order<=3*((2*order+6)//7):continue
        bits=0
        for i,g in enumerate(differences):
            v=sum(x*z for x,z in zip(coeff,g))%e
            if threshold<=v<=e-threshold:bits|=1<<i
        masks.add(bits)
    union=0
    for m in masks:union|=m
    if union!=allbits:return 'uncovered',len(masks)
    pairs=sorted({a|b for a,b in combinations_with_replacement(masks,2)})
    # Column bitsets index pairs that cover a specified difference.
    columns=[0]*len(differences)
    for i,m in enumerate(pairs):
        while m:
            b=m&-m;m^=b;columns[b.bit_length()-1]|=1<<i
    base=[0] if surj else list(masks)
    for s in base:
        for p in pairs:
            need=allbits&~(p|s)
            candidates=(1<<len(pairs))-1
            while need and candidates:
                b=need&-need;need^=b;candidates&=columns[b.bit_length()-1]
            assert candidates==0,('feasible character cover',ds,surj)
    return 'exhaustive',len(pairs)

alltypes=[d for n in range(368,402) for d in types(n) if len(d)>1]
assert len(alltypes)==len(set(alltypes))
kept=[d for d in alltypes if len(d)<=5]
assert len(kept)==44
records=[]
for ds in sorted(kept,key=lambda d:(len(d),prod(d),d)):
    for surj in (True,False):
        reason,count=gate(ds,surj)
        records.append({'factors':ds,'surjective_coordinate':surj,'reason':reason,'count':count})
        print(ds,surj,reason,flush=True)
out={'status':'PASS','noncyclic_types':44,'jobs':len(records),'rank_gt5_types':[d for d in alltypes if len(d)>5],
     'records':records,'seconds':time.monotonic()-start,
     'scope':'Noncyclic finite subgroup orders368..401 at toroidal distance2/7; cyclic gate is separate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',out['seconds'])
