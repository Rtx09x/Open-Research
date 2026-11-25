#!/usr/bin/env python3
"""Separate Fraction target recursion and exact fixed-mixture dual verifier."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,hashlib,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_single_thresholds import weights
D=Q(1,43)

def build(P,B,b,mix):
    out=[]
    assert sum(Q(z[2]) for z in mix)==1
    for cc,qq,tt in mix:
        c,q,t=map(Q,[cc,qq,tt]);assert 0<c<=D and q>=0 and t>0
        penalty=sum(alpha*max(Q(0),1-q*(A-D)) for A,alpha in P[212]['alpha'].items())
        denom=B-c-(D-c)*penalty;assert denom>=B-D>0
        out.append((c,t*b/denom,t*b*(D-c)*q/denom))
    return out

def tiny(r,terms):
    value=Q(0)
    for c,rho,extra in terms:
        value+=rho*r
        if c<D:
            z=r/c;n=-(-z.numerator//z.denominator)-1
            value+=extra*min(r,n*D)
    return value

def check(items,cap,terms,offset,target):
    rho=sum(z[1] for z in terms);density=sum(z[1]+z[2] for z in terms)
    front=[];largest=-Q(1)
    for j,s,w in sorted(items,key=lambda t:(t[1],-t[2],t[0])):
        if w<=largest:continue
        largest=w
        if s<cap and w>rho*s:front.append((j,s,w))
    front.sort(key=lambda t:t[1],reverse=True);suffix=[density]*(len(front)+1)
    for i in range(len(front)-1,-1,-1):suffix[i]=max(suffix[i+1],front[i][2]/front[i][1])
    nodes=0
    def visit(i,room,value):
        nonlocal nodes
        nodes+=1;assert offset+value+tiny(room,terms)<=target
        if i==len(front) or offset+value+room*suffix[i]<=target:return
        j,s,w=front[i];n=0
        while n*s<room:visit(i+1,room-n*s,value+n*w);n+=1
    visit(0,cap,Q(0));return nodes

start=time.time();J=json.loads((H/'type_mixture_certificate.json').read_text());source=ROOT/'phase2/best_fit/best_fit_certificate.json';S=json.loads(source.read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==J['source_certificate_sha256'];assert J['parameters']==S['parameters']
R=Q(J['target']);assert R<Q(S['target'])
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'alpha':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
ref={(s['x'],s['y']):s for s in S['scenarios']};V={Q(0),Q(1,2)}
for j,p in P.items():
    assert sum(p['alpha'].values())==1 and all(a>0 for a in p['alpha'].values())
    V.update([p['lo'],p['hi']])
    for i in p['alpha']:
        v=i if j==212 else i*p['hi'];V.update([v,1-v])
V=sorted(v for v in V if 0<=v<=Q(1,2));logs=[]
for s in J['scenarios']:
    assert all(s.get(k)==ref[s['x'],s['y']].get(k) for k in ['u','v','w','c'])
    N,HUGE,B,b,c,y=weights(P,s);terms=build(P,B,b,s['analysis_mixture'])
    ns=[check(N,Q(1),terms,0,R),check(HUGE,y,terms,1,R)]
    for h,items,cap in [(0,N,Q(1)),(1,HUGE,y)]:
        look={j:(size,w) for j,size,w in items};row=s['cases'][h]
        residual=cap-sum(look[j][0]*n for j,n in row['pattern']);assert residual>0
        val=h+sum(look[j][1]*n for j,n in row['pattern'])+tiny(residual,terms)
        assert val==Q(row['maximum'])<=R
    if(s['x'],s['y'])==('3/7','1/2'):
        rows=J['critical_fixed_mixture_dual'];theta=Q(J['critical_theta']);assert 0<theta<1
        assert sum(Q(row['lambda_weight']) for row in rows)==1
        for row in rows:
            assert Q(row['lambda_weight'])>0;h=int(row['huge']);look={j:(sz,w) for j,sz,w in (HUGE if h else N)}
            r=(y if h else Q(1))-sum(look[j][0]*n for j,n in row['pattern'])
            K=h+sum(look[j][1]*n for j,n in row['pattern']);assert r==Q(row['residual'])>0 and K==Q(row['constant'])
            vals=[]
            for index in [1,0]:
                component=s['analysis_mixture'][index];terms1=build(P,B,b,[[component[0],component[1],'1']])
                vals.append(K+tiny(r,terms1))
            assert vals[0]==Q(row['intercept']) and vals[1]-vals[0]==Q(row['slope'])
            assert vals[0]+theta*(vals[1]-vals[0])==R
            # Both active residuals are one-item limits attaining every
            # component simultaneously; no relaxation-only dual claim.
            for cc,qq,tt in s['analysis_mixture']:
                c=Q(cc);assert r<=D and (r<=c or r>c)
                z=r/c;n=-(-z.numerator//z.denominator)-1
                assert min(r,n*D)==(r if r>c else 0)
        assert sum(Q(row['lambda_weight'])*Q(row['slope']) for row in rows)==0
        assert sum(Q(row['lambda_weight'])*Q(row['intercept']) for row in rows)==R
    logs.append({'x':s['x'],'y':s['y'],'nodes':ns})
assert sorted((Q(s['x']),Q(s['y'])) for s in J['scenarios'])==list(zip(V,V[1:])) and len(logs)==402
out={'status':'PASS','target':str(R),'target_decimal':float(R),'scenarios':402,'knapsacks':804,'fixed_two_charge_dual':'PASS, physically attained active infimum patterns','nodes':sum(sum(s['nodes']) for s in logs),'seconds':time.time()-start,'checks':logs}
(H/'independent_mixture_verification.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='checks'})
