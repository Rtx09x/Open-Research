#!/usr/bin/env python3
"""Separate size-ordered Fraction checker; no imports from discovery/pricing."""
from fractions import Fraction as F
from pathlib import Path
import sys,json,hashlib,time
sys.dont_write_bytecode=True
HOME=Path(__file__).resolve().parent;ROOT=HOME.parent.parent;sys.path.insert(0,str(ROOT/'phase2'))
from verify_single_thresholds import weights
d=F(1,43)

def charge(P,B,b,mix):
    answer=[];assert sum(F(row[3]) for row in mix)==1
    for row in mix:
        c,g,q,t=map(F,row);assert 0<=c<=g<=d and q>=0 and t>0
        k=sum(alpha*max(F(0),1-q*(A-g)) for A,alpha in P[212]['alpha'].items())
        den=B-c-(g-c)*k;assert den>=B-g>0
        base=t*b/den;answer.append((c,g,base,base*(g-c)*q,base*(1+(g-c)*q)))
    return answer

def fill(room,terms):
    answer=F(0)
    for c,g,base,step,excess in terms:
        if c==0:large=room
        elif c==d:large=F(0)
        else:
            z=room/c;count=(z.numerator-1)//z.denominator
            large=min(room,count*d)
        full=room//d;left=room-full*d
        spill=full*(d-g)+max(F(0),left-g)
        answer+=base*room+step*large+excess*spill
    return answer

def verify(items,capacity,terms,offset,R):
    base=sum(z[2] for z in terms)
    density=sum(z[2]+z[3]+z[4]*(d-z[1])/d for z in terms)
    frontier=[];weightmax=-F(1)
    for j,s,w in sorted(items,key=lambda z:(z[1],-z[2],z[0])):
        if w<=weightmax:continue
        weightmax=w
        if s<capacity and w>base*s:frontier.append((j,s,w))
    frontier.sort(key=lambda z:z[1],reverse=True)
    suffix=[density]*(len(frontier)+1)
    for i in range(len(frontier)-1,-1,-1):suffix[i]=max(suffix[i+1],frontier[i][2]/frontier[i][1])
    nodes=0
    def dfs(i,room,value):
        nonlocal nodes
        nodes+=1;assert offset+value+fill(room,terms)<=R
        if i==len(frontier) or offset+value+room*suffix[i]<=R:return
        j,s,w=frontier[i];count=0
        while count*s<room:
            dfs(i+1,room-count*s,value+count*w);count+=1
    dfs(0,capacity,F(0));return nodes

start=time.time();path=HOME/'successor_mixture_certificate.json';J=json.loads(path.read_text())
source=ROOT/'phase3/bf_type/type_mixture_certificate.json';S=json.loads(source.read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==J['source_certificate_sha256'] and S['parameters']==J['parameters']
R=F(J['target']);assert R<F(S['target'])
P={int(j):{'lo':F(row['lower']),'hi':F(row['upper']),'alpha':{F(i):F(a) for i,a in row['containers']}} for j,row in J['parameters'].items()}
V={F(0),F(1,2)}
for j,p in P.items():
    assert sum(p['alpha'].values())==1 and all(a>0 for a in p['alpha'].values())
    V.update([p['lo'],p['hi']])
    for i in p['alpha']:
        volume=i if j==212 else i*p['hi'];V.update([volume,1-volume])
V=sorted(v for v in V if 0<=v<=F(1,2));old={(s['x'],s['y']):s for s in S['scenarios']};logs=[]
for s in J['scenarios']:
    previous=old[s['x'],s['y']]
    assert all(s.get(k)==previous.get(k) for k in ['u','v','w','c'])
    if(s['x'],s['y'])!=('3/7','1/2'):
        assert s['analysis_mixture']==[[c,str(d),q,t] for c,q,t in previous['analysis_mixture']]
    normal,huge,B,b,c,y=weights(P,s);terms=charge(P,B,b,s['analysis_mixture'])
    ns=[verify(normal,F(1),terms,0,R),verify(huge,y,terms,1,R)]
    for h,items,cap in [(0,normal,F(1)),(1,huge,y)]:
        lookup={j:(size,w) for j,size,w in items};row=s['cases'][h]
        r=cap-sum(lookup[j][0]*n for j,n in row['pattern']);assert r>0
        value=h+sum(lookup[j][1]*n for j,n in row['pattern'])+fill(r,terms)
        assert value==F(row['maximum'])<=R
    logs.append({'x':s['x'],'y':s['y'],'nodes':ns})
assert sorted((F(s['x']),F(s['y'])) for s in J['scenarios'])==list(zip(V,V[1:])) and len(logs)==402
# Endpoint controls: g=d removes every excess term; c=g removes the step.
for r in [F(1,10000),F(1,60),d,2*d,F(1)]:
    c=F(1,60);q=1/(1-d);T=charge(P,B,b,[[c,d,q,F(1)]])[0]
    assert T[4]*( (r//d)*(d-d)+max(F(0),r-(r//d)*d-d))==0
    T=charge(P,B,b,[[c,c,q,F(1)]])[0];assert T[3]==0 and T[2]==b/(B-c) and T[4]==T[2]
out={'status':'PASS','target':str(R),'target_decimal':float(R),'scenarios':402,'knapsacks':804,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nodes':sum(sum(z['nodes']) for z in logs),'seconds':time.time()-start,'checks':logs}
(HOME/'independent_verification.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='checks'})
