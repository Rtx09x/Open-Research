#!/usr/bin/env python3
"""Exact rational realization of the certified adaptive SPR labeler.
Not a forecaster and not a finite-test replacement for the uniform proof.
"""
from bisect import bisect_left
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import json,random,time

RHO=Q('.0097');KAPPA=Q('.6');DELTA=Q('14.8')
POLICY=json.loads(Path(__file__).with_name('rational_q_policy.json').read_text())
TABLE={seg:sorted([(Q(r['lo']),Q(r['hi']),Q(r['q'])) for r in POLICY['rows'] if r['segment']==seg]) for seg in (1,2)}
ENDS={s:[x[1] for x in TABLE[s]] for s in TABLE}


def factor(tau,h):
    z=Q(tau,h)
    if z<=DELTA*RHO:seg,x=1,z
    else:seg,x=2,z/DELTA
    i=bisect_left(ENDS[seg],x);lo,hi,q=TABLE[seg][i]
    assert lo<=x<=hi and Q(1,2)<=q<=Q('.76')
    return q


class A:
    def __init__(self,l,r,w=Q(1)):
        self.l=l;self.r=r;self.w=w;self.count=0
        self.epoch=B(l,r,w,0) if l<r else None
    def label(self,j):
        assert self.l<=j<=self.r
        if self.l==self.r:
            result=1 if self.w>=1 else -1
        else:
            if self.epoch.exhausted():self.epoch=B(self.l,self.r,self.w,self.count)
            result,child,shifted=self.epoch.label(j)
        self.count+=1
        if self.l<self.r:
            assert self.count==self.epoch.tau+sum(self.epoch.counts)+self.epoch.c
            if shifted:
                assert child.l==self.l and child.r==self.r
                assert self.count>=2*child.count
                assert Q(1,2)<=child.w/self.w<=2
            else:
                assert child.r-child.l < self.r-self.l and child.w==self.w
        assert result in (-1,1)
        return result


class B:
    def __init__(self,l,r,w,tau):
        self.l=l;self.r=r;self.m=(l+r)//2;self.w=w;self.tau=tau
        self.children=[A(l,self.m,w),A(self.m+1,r,w)]
        self.counts=[0,0];self.phase=1;self.L=0;self.c=0;self.shift=None
    def exhausted(self):return self.phase==2 and self.c==self.L
    def label(self,j):
        if self.phase==2:
            assert self.c<self.L and self.shift is not None
            ans=self.shift.label(j);self.c+=1
            return ans,self.shift,True
        side=int(j>self.m);self.counts[side]+=1
        child=self.children[side];ans=child.label(j)
        h=max(self.counts);ell=min(self.counts)
        if DELTA*ell>=self.tau and ell>=RHO*h:
            assert self.counts[side]==ell
            ell0=max(Q(self.tau)/DELTA,RHO*h)
            assert ell0<=ell<ell0+1
            self.L=(KAPPA*h).__floor__();self.phase=2
            q=factor(self.tau,h)
            if self.L:
                self.shift=A(self.l,self.r,self.w*q if side else self.w/q)
        return ans,child,False


def step(board,instance,j):
    assert board[j]==0
    b=board.copy()
    for i,s in enumerate(b):
        if (i<j and s==-1) or (i>j and s==1):b[i]=0
    b[j]=instance.label(j)
    signs=[s for s in b if s]
    assert not any(signs[i]==-1 and signs[i+1]==1 for i in range(len(signs)-1))
    return b


def run_tests():
    start=time.monotonic();counts={'exhaustive_edges':0,'random_edges':0};maxsign=0
    def dfs(board,a,h):
        nonlocal maxsign
        maxsign=max(maxsign,sum(bool(s) for s in board))
        if h==0:return
        for j,s in enumerate(board):
            if not s:
                ac=deepcopy(a);bc=step(board,ac,j);counts['exhaustive_edges']+=1
                dfs(bc,ac,h-1)
    for n,h in [(1,8),(2,10),(4,9)]:dfs([0]*n,A(0,n-1),h)
    rng=random.Random(261007623)
    for n in [8,16,32]:
        for trial in range(150):
            board=[0]*n;instance=A(0,n-1)
            for t in range(120):
                empty=[j for j,s in enumerate(board) if not s]
                if not empty:break
                if trial%4==0:j=empty[0]
                elif trial%4==1:j=empty[-1]
                elif trial%4==2:j=empty[t%len(empty)]
                else:j=rng.choice(empty)
                board=step(board,instance,j);counts['random_edges']+=1
    result={'scope':'Exact rational policy operational invariants and legal normal-form transcripts only; does not prove asymptotic bound.','all_checks_passed':True,**counts,'max_exhaustive_signs':maxsign,'seconds':time.monotonic()-start}
    Path(__file__).with_name('adaptive_policy_tests.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run_tests()
