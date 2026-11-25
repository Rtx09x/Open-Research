"""Certificate-producing synthesis for fixed encodings and interaction order.

SciPy proposes solutions. Only exact Fraction checks accept feasibility or
infeasibility. Numerical uncertainty is returned as 'unresolved', never as proof.
Fixed logical states may be silent or make an up/down excursion. This is required
for a complete restricted-interaction search; silence is not imposed silently.
"""
from __future__ import annotations
from itertools import combinations,product
from fractions import Fraction as F
from math import lcm
import json,hashlib
from independent import geometry,Device,verify_device


def submasks(n,i,d):
    out=[0]
    for k in range(1,min(d,n-1)+1):
        out.extend(sum(1<<j for j in c) for c in combinations([j for j in range(n) if j!=i],k))
    return out


def add(a,b,scale=1):
    c=dict(a)
    for j,v in b.items():
        c[j]=c.get(j,0)+scale*v
        if not c[j]:del c[j]
    return c


def neg(a):return {j:-v for j,v in a.items()}


class Problem:
    def __init__(self,codes,f,n,degree=1,common=False,uniform=False,nonnegative=False,
                 fixed_additions=None,support=None):
        if not geometry(codes,f,n):raise ValueError('invalid encoding')
        if degree<0 or degree>max(0,n-1):raise ValueError('degree')
        if uniform and not common:raise ValueError('uniform implementation requires common shifts')
        fixed_additions={int(k):v for k,v in (fixed_additions or {}).items()}
        self.spec={'codes':list(codes),'f':list(f),'n':n,'degree':degree,
                   'common':common,'uniform':uniform,'nonnegative':nonnegative,
                   'fixed_additions':{} if fixed_additions is None else {str(k):v for k,v in fixed_additions.items()},
                   'support':support}
        self.variables=[];self.var_index={};self.rows=[];self.bounds=[];self.labels=[]
        def var(name):
            if name not in self.var_index:
                self.var_index[name]=len(self.variables);self.variables.append(name)
            return {self.var_index[name]:1}
        self.H=var('H');self.expr={};nonconstant=set()
        W=var('W') if uniform else None
        for i in range(n):
            for u in (True,False):
                for mask in submasks(n,i,degree):
                    if mask and support is not None and [i,mask] not in support:continue
                    if not mask:
                        if uniform:
                            v=var(f'a:{i}');v=v if u else add(v,W,-1)
                        else:v=var(f'{"a" if u else "b"}:{i}')
                    else:
                        v=var(f'{"J" if common else ("P" if u else "D")}:{i}:{mask}')
                        nonconstant.update(v)
                    self.expr[(i,u,mask)]=v
        def threshold(i,s,u):
            ans={}
            for mask in submasks(n,i,degree):
                if mask&s==mask:ans=add(ans,self.expr.get((i,u,mask),{}))
            return ans
        self.threshold=threshold
        def positive(expr,label):self.push(expr,1,label)
        def stable(s,h,label):
            for i in range(n):
                expr=add(h,threshold(i,s,False),-1) if s>>i&1 else add(threshold(i,s,True),h,-1)
                positive(expr,f'{label}:bit{i}')
        positive(self.H,'positive pulse')
        for i in range(n):
            envs=[0] if common else [s for s in range(1<<n) if not s>>i&1]
            for s in envs:positive(add(threshold(i,s,True),threshold(i,s,False),-1),f'span:{i}:{s}')
        if nonnegative:
            for v in sorted(nonconstant):self.push({v:1},0,'nonnegative:'+self.variables[v])
        fixed_additions=fixed_additions or {}
        for x,t in enumerate(f):
            A=codes[x];T=codes[t];stable(A,{},f'baseline:{x}')
            if x==t:
                p=fixed_additions.get(x)
                if p is None:
                    for i in range(n):
                        if not A>>i&1:positive(add(threshold(i,A,True),self.H,-1),f'hold:{x}:{i}')
                    continue
                if type(p)!=int or p<0 or p>=n or A>>p&1:raise ValueError('fixed excursion bit')
                P=A|1<<p;r=p
            else:
                p=((T&~A).bit_length()-1);P=A|T
                r=(A&~T).bit_length()-1 if A&~T else None
            trigger=threshold(p,A,True)
            positive(trigger,f'up above low:{x}')
            positive(add(self.H,trigger,-1),f'up below high:{x}')
            for i in range(n):
                if not A>>i&1 and i!=p:positive(add(threshold(i,A,True),trigger,-1),f'up winner:{x}:{i}')
            stable(P,trigger,f'post up:{x}')
            stable(P,self.H,f'peak:{x}')
            if r is None:
                stable(P,{},f'no deletion:{x}')
            else:
                fall=threshold(r,P,False)
                positive(fall,f'down above low:{x}')
                positive(add(self.H,fall,-1),f'down below high:{x}')
                for i in range(n):
                    if P>>i&1 and i!=r:positive(add(fall,threshold(i,P,False),-1),f'down winner:{x}:{i}')
                stable(T,fall,f'post down:{x}')
                stable(T,{},f'final:{x}')
        self.dimension=len(self.variables)
        self.fingerprint=hashlib.sha256(json.dumps({'spec':self.spec,'vars':self.variables,
            'rows':self.rows,'bounds':self.bounds},sort_keys=True).encode()).hexdigest()

    def push(self,row,b,label):
        self.rows.append(row);self.bounds.append(b);self.labels.append(label)

    def primal_ok(self,x):
        return len(x)==self.dimension and all(sum(F(v)*x[j] for j,v in row.items())>=b
                  for row,b in zip(self.rows,self.bounds))

    def dual_ok(self,y):
        if len(y)!=len(self.rows) or any(v<0 for v in y):return False
        residual=[F(0)]*self.dimension
        for weight,row in zip(y,self.rows):
            for j,c in row.items():residual[j]+=weight*c
        return not any(residual) and sum(v*b for v,b in zip(y,self.bounds))>0

    def physical(self,x):
        D=lcm(*(v.denominator for v in x));scaled=[int(v*D) for v in x]
        def evaluate(i,s,u):return sum(c*scaled[j] for j,c in self.threshold(i,s,u).items())
        H=sum(v*scaled[j] for j,v in self.H.items())
        return Device(self.spec['n'],0,[H],D,evaluate,self.spec['codes'],self.spec['f'])

    def solve(self):
        import numpy as np
        from scipy.optimize import linprog
        from scipy.sparse import csr_matrix
        rr=[];cc=[];vv=[]
        for i,row in enumerate(self.rows):
            for j,c in row.items():rr.append(i);cc.append(j);vv.append(c)
        A=csr_matrix((vv,(rr,cc)),shape=(len(self.rows),self.dimension),dtype=float)
        b=np.array(self.bounds,dtype=float)
        result=linprog(np.zeros(self.dimension),A_ub=-A,b_ub=-b,bounds=[(None,None)]*self.dimension,method='highs')
        certificate={'spec':self.spec,'fingerprint':self.fingerprint,'variables':self.variables,
                     'rows':len(self.rows),'dimension':self.dimension,'solver_status':int(result.status)}
        if result.success:
            proposals=[]
            # A common rational grid avoids enormous least-common denominators.
            # Scaling adds strict slack; exact checking remains authoritative.
            for denominator in (1,10,100,1000,1000000):
                proposals.append([2*F(round(float(v)*denominator),denominator) for v in result.x])
            for denominator in (1000,1000000,1000000000):
                proposals.append([F(float(v)).limit_denominator(denominator) for v in result.x])
            for x in proposals:
                if self.primal_ok(x):
                    d=self.physical(x);check=verify_device(d,full=d.n<=10)
                    certificate.update(status='feasible',primal=list(map(str,x)),physical_check=check)
                    return certificate
            certificate.update(status='unresolved',reason='Primal proposal failed exact arithmetic')
            return certificate
        if result.status==2:
            # Farkas: y>=0, A^T y=0, b^T y=1 disproves A x>=b.
            from scipy.sparse import vstack
            dual=linprog(np.zeros(len(self.rows)),A_eq=vstack([A.T,csr_matrix(b.reshape(1,-1))]),
                         b_eq=np.r_[np.zeros(self.dimension),1],bounds=(0,None),method='highs')
            if dual.success:
                for denominator in (1000,1000000,1000000000):
                    y=[F(float(v)).limit_denominator(denominator) for v in dual.x]
                    if self.dual_ok(y):
                        certificate.update(status='infeasible',dual={str(i):str(v) for i,v in enumerate(y) if v})
                        return certificate
            certificate.update(status='unresolved',reason='No exactly verified dual')
            return certificate
        certificate.update(status='unresolved',reason=str(result.message))
        return certificate


def verify_certificate(cert):
    p=Problem(**cert['spec'])
    if p.fingerprint!=cert['fingerprint']:raise ValueError('fingerprint mismatch')
    if cert['status']=='feasible':
        x=list(map(F,cert['primal']))
        if not p.primal_ok(x):raise ValueError('invalid primal')
        return verify_device(p.physical(x),full=p.spec['n']<=10)
    if cert['status']=='infeasible':
        y=[F(cert['dual'].get(str(i),'0')) for i in range(len(p.rows))]
        if not p.dual_ok(y):raise ValueError('invalid dual')
        return {'dual_nonzero_entries':sum(v!=0 for v in y),'contradiction':str(sum(v*b for v,b in zip(y,p.bounds)))}
    raise ValueError('Unresolved proposals are not certificates')


def phase_options(codes,f,n):
    fixed=[i for i,t in enumerate(f) if i==t]
    options=[[None]+[j for j in range(n) if not codes[i]>>j&1] for i in fixed]
    for opts in product(*options):yield {i:j for i,j in zip(fixed,opts) if j is not None}


if __name__=='__main__':
    from pathlib import Path
    R=Path(__file__).resolve().parents[1]/'results';R.mkdir(exist_ok=True)
    tasks=[([1,2,4],[1,2,0],3,0,False,False,False),
           ([1,2,4],[1,2,0],3,1,True,True,True),
           ([0,1,2,3],[0,3,3,3],2,1,False,False,False),
           ([1,3,2,0],[0,1,1,0],2,0,False,False,False)]
    report=[]
    for codes,f,n,degree,common,uniform,nonneg in tasks:
        p=Problem(codes,f,n,degree,common,uniform,nonneg);cert=p.solve();verify_certificate(cert)
        report.append(cert);print(n,degree,cert['status'],flush=True)
    (R/'synthesis_smoke.json').write_text(json.dumps(report,indent=2))
