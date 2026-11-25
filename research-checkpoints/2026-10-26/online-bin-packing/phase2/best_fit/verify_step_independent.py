#!/usr/bin/env python3
"""Fraction-only size-ordered target proof, separate from step maximization."""
from fractions import Fraction as Q
from pathlib import Path
import sys,json,hashlib,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent))
from verify_single_thresholds import weights
D=Q(1,43);AMIN=Q(17,60)

def envelope(r,c):
    if c==D:return r
    n=max(0,-(-(r/c).numerator//(r/c).denominator)-1)
    return r+(D-c)/(AMIN-D)*min(r,n*D)

def check(items,cap,rho,c,offset,target):
    frontier=[];largest=-Q(1)
    for j,s,w in sorted(items,key=lambda t:(t[1],-t[2],t[0])):
        if w<=largest:continue
        largest=w
        if s<cap and w>rho*s:frontier.append((j,s,w))
    frontier.sort(key=lambda t:t[1],reverse=True)
    suffix=[rho*(1+(D-c)/(AMIN-D))]*(len(frontier)+1)
    for i in range(len(frontier)-1,-1,-1):suffix[i]=max(suffix[i+1],frontier[i][2]/frontier[i][1])
    nodes=0
    def visit(i,room,value):
        nonlocal nodes
        nodes+=1;assert offset+value+rho*envelope(room,c)<=target
        if i==len(frontier) or offset+value+room*suffix[i]<=target:return
        j,s,w=frontier[i];n=0
        while n*s<room:visit(i+1,room-n*s,value+n*w);n+=1
    visit(0,cap,Q(0));return nodes

start=time.time();J=json.loads((H/'best_fit_certificate.json').read_text());source=H.parent/'single_threshold_certificate.json';F=json.loads(source.read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==J['source_certificate_sha256']
assert J['parameters']==F['parameters'];R=Q(J['target']);assert R<Q(F['target'])
P={int(j):{'lo':Q(r['lower']),'hi':Q(r['upper']),'alpha':{Q(i):Q(a) for i,a in r['containers']}} for j,r in J['parameters'].items()}
reference={(s['x'],s['y']):s for s in F['scenarios']};V={Q(0),Q(1,2)}
for j,r in P.items():
    assert sum(r['alpha'].values())==1 and all(a>0 for a in r['alpha'].values())
    V.update([r['lo'],r['hi']])
    for i in r['alpha']:
        v=i if j==212 else i*r['hi'];V.update([v,1-v])
V=sorted(v for v in V if 0<=v<=Q(1,2));logs=[]
for s in J['scenarios']:
    assert all(s.get(k)==reference[s['x'],s['y']].get(k) for k in ['u','v','w'])
    N,HUGE,B,b,c,y=weights(P,s);rho=b/(B-c)
    ns=[check(N,Q(1),rho,c,0,R),check(HUGE,y,rho,c,1,R)]
    for h,items,cap in [(0,N,Q(1)),(1,HUGE,y)]:
        lookup={j:(size,w) for j,size,w in items};row=s['cases'][h]
        residual=cap-sum(lookup[j][0]*n for j,n in row['pattern']);assert residual>0
        val=h+sum(lookup[j][1]*n for j,n in row['pattern'])+rho*envelope(residual,c)
        assert val==Q(row['maximum'])<=R
    logs.append({'x':s['x'],'y':s['y'],'c':str(c),'nodes':ns})
assert sorted((Q(s['x']),Q(s['y'])) for s in J['scenarios'])==list(zip(V,V[1:])) and len(logs)==402
assert max(Q(s['maximum']) for s in J['scenarios'])==R
out={'status':'PASS','target':str(R),'target_decimal':float(R),'scenarios':402,'knapsacks':804,'nodes':sum(sum(s['nodes']) for s in logs),'seconds':time.time()-start,'checks':logs}
(H/'independent_step_verification.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='checks'})
