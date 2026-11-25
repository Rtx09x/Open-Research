"""Independent exact hysteron audit. Does not import either earlier simulator.

The internal model uses integer threshold tables, or sparse polynomial rows.
All transitions are chosen from thresholds, never from requested successors.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb,lcm
from typing import Callable

class InvalidDynamics(ValueError):
    pass

@dataclass
class Device:
    n: int
    low: int
    highs: list[int]
    scale: int
    evaluate: Callable[[int,int,bool],int]
    codes: list[int]
    successors: list[int]
    gates: list[int] | None = None


def from_legacy(data:dict) -> Device:
    """Read the two supplied archive formats into separately generated tables."""
    n=data['n']; size=1<<n
    if 'terms' in data:  # Original rational polynomial format.
        den=lcm(*(Fraction(v).denominator for key in ('a','b') for v in data[key]),
                *(Fraction(t['coefficient']).denominator for row in data['terms'] for t in row),
                Fraction(data['low']).denominator,Fraction(data['high']).denominator)
        rows=[]
        for up in (True,False):
            branch=[]
            for i in range(n):
                values=[0]*size
                values[0]=int(Fraction(data['a' if up else 'b'][i])*den)
                for term in data['terms'][i]:
                    mask=term['mask']
                    assert not mask>>i&1
                    values[mask]+=int(Fraction(term['coefficient'])*den)
                for bit in range(n):
                    for s in range(size):
                        if s>>bit&1: values[s]+=values[s^(1<<bit)]
                branch.append(values)
            rows.append(branch)
        codes=data['path'][::2]
        return Device(n,int(Fraction(data['low'])*den),[int(Fraction(data['high'])*den)],den,
                      lambda i,s,u:rows[0 if u else 1][i][s],codes,
                      list(range(1,len(codes)))+[0])
    D=data['scale']; kind=data['kind']
    if kind=='affine':
        a=[v*D+i+1 for i,v in enumerate(data['a'])]
        b=[v*D+i+1 for i,v in enumerate(data['b'])]
        coeff=[[(1<<j,c*D) for j,c in enumerate(row) if c] for row in data['J']]
        def evaluate(i,s,u):
            return (a if u else b)[i]+sum(c for mask,c in coeff[i] if s&mask)
    elif kind=='raw':
        plus=data['plus'];minus=data['minus']
        def evaluate(i,s,u):return (plus if u else minus)[i][s&~(1<<i)]
    else:
        all_rows=[]
        for i in range(n):
            if kind in ('polynomial','saturating'):
                k=data['k']; zero=set(data['zeros'][i]);four=set(data['fours'][i])
                values=[0]*size
                for env in range(size):
                    if not env>>i&1 and env.bit_count()==k:
                        values[env]=0 if env in zero else 4 if env in four else 2
                if kind=='polynomial':
                    for j in range(n):
                        for s in range(size):
                            if s>>j&1:values[s]+=values[s^(1<<j)]
                else:
                    for j in range(n):
                        for s in range(size):
                            if s>>j&1:values[s]=max(values[s],values[s^(1<<j)])
                plus=[D*(data['a'][i]+v)+i+1 for v in values]
                minus=[D*(data['b'][i]+v)+i+1 for v in values]
            elif kind=='table':
                plus=[];minus=[]
                for s in range(size):
                    env=s&~(1<<i)
                    plus.append(D*(2 if data['up'].get(str(env))==i else 4)+i+1)
                    minus.append(D*(1 if data['down'].get(str(env|1<<i))==i else -2)+i+1)
            else:raise ValueError(kind)
            all_rows.append((plus,minus))
        def evaluate(i,s,u):return all_rows[i][0 if u else 1][s]
    return Device(n,data['low'],data['highs'],D,evaluate,data.get('codes',[]),data.get('f',[]),data.get('gates'))


def sweep(d:Device,initial:int,symbol:int=0) -> dict:
    """Follow both ramps, rejecting ties, avalanches, endpoint events and >1 flips.

    Tracking the current field explicitly catches backwards-time events. Every
    bit, including the just-flipped bit, is checked after an event.
    """
    n=d.n; T=d.evaluate; state=initial; events=[]; gaps=[]
    if not (0<=initial<1<<n and d.low<d.highs[symbol]):raise InvalidDynamics('domain')
    def stable(h):
        for i in range(n):
            gap=h-T(i,state,False) if state>>i&1 else T(i,state,True)-h
            if gap<=0:raise InvalidDynamics('unstable or avalanche')
            gaps.append(gap)
    stable(d.low)
    for direction,start,end in ((1,d.low,d.highs[symbol]),(-1,d.highs[symbol],d.low)):
        field=start; count=0
        while True:
            choices=[(T(i,state,direction==1),i) for i in range(n) if (state>>i&1)==(0 if direction==1 else 1)]
            if not choices:stable(end);break
            val,bit=(min(choices) if direction==1 else max(choices))
            if direction*(val-end)>0:stable(end);break
            if val==end:raise InvalidDynamics('endpoint tie')
            if direction*(val-field)<=0:raise InvalidDynamics('backwards event or avalanche')
            if count:raise InvalidDynamics('budget')
            for other,j in choices:
                if j!=bit:
                    gap=direction*(other-val)
                    if gap<=0:raise InvalidDynamics('winner tie')
                    gaps.append(gap)
            old=state;state^=1<<bit;count+=1
            stable(val);events.append([direction,bit,val,old,state]);field=val
            gaps.extend((abs(end-val),abs(val-start)))
    return {'final':state,'events':events,'margin':min(gaps,default=d.highs[symbol]-d.low)}


def verify_device(d:Device,full=False) -> dict:
    trials=0; margin=None
    for a in range(len(d.highs)):
        for x,s in enumerate(d.codes):
            result=sweep(d,s,a)
            target=x if d.gates is not None and a+1<d.gates[x] else d.successors[x]
            if result['final']!=d.codes[target]:raise InvalidDynamics('wrong successor')
            margin=result['margin'] if margin is None else min(margin,result['margin'])
            trials+=1
    out={'trials':trials,'scale':d.scale,'margin':margin}
    if full:
        width=None;minup=None;maxdown=None
        for i in range(d.n):
            for s in range(1<<d.n):
                p=d.evaluate(i,s,True);b=d.evaluate(i,s,False)
                if p<=b:raise InvalidDynamics('nonpositive span')
                if p!=d.evaluate(i,s^(1<<i),True) or b!=d.evaluate(i,s^(1<<i),False):
                    raise InvalidDynamics('self-dependence')
                width=p-b if width is None else min(width,p-b)
                minup=p if minup is None else min(minup,p)
                maxdown=b if maxdown is None else max(maxdown,b)
        out.update(min_span=width,band_gap=None if width is None else minup-maxdown)
    return out


def geometry(codes:list[int],f:list[int],n:int)->bool:
    """Direct geometric criterion; separate implementation using sets."""
    if len(set(codes))!=len(codes) or len(f)!=len(codes):return False
    if any(type(x)!=int or not 0<=x<1<<n for x in codes):return False
    if any(type(t)!=int or not 0<=t<len(f) for t in f):return False
    sets=[frozenset(i for i in range(n) if c>>i&1) for c in codes]
    peak_targets={}
    for x,t in enumerate(f):
        if x==t:continue
        A,B=sets[x],sets[t]
        if len(B-A)!=1 or len(A-B)>1:return False
        P=A|B
        if A<B:
            if f[t]!=t:return False
        elif P in sets:return False
        if P in peak_targets and peak_targets[P]!=B:return False
        peak_targets[P]=B
    return True
