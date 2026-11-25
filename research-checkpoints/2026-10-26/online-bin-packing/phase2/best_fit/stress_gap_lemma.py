#!/usr/bin/env python3
"""Exact finite falsification tests supplementing, not replacing, the proof."""
from bisect import bisect_left,insort
from fractions import Fraction as Q
from pathlib import Path
import json,random,time
H=Path(__file__).resolve().parent;J=json.loads((H/'best_fit_certificate.json').read_text())
scale=25800;d=600;A=[7310,25800];alpha=[Q(v) for a,v in J['parameters']['212']['containers']]
assert [Q(a) for a,v in J['parameters']['212']['containers']]==[Q(17,60),Q(1)]
B=sum(alpha[i]*A[i] for i in range(2))/scale
cs=[0,387,430,600];rng=random.Random(428904);start=time.time();checks=0;items=0;containers=0
for mode in range(5):
    n=[0,0];records=[];gaps=[];total=0;large=[0]*len(cs)
    for t in range(5000):
        if mode==0:s=rng.randrange(1,d+1)
        elif mode==1:s=1 if t%101 else d
        elif mode==2:s=d if t%11 else 1
        elif mode==3:s=rng.choice([386,387,388,429,430,431,599,600])
        else:s=1+(t*7919+23)%d
        k=bisect_left(gaps,(s,-1))
        if k==len(gaps):
            typ=next(i for i in range(2) if n[i]<=alpha[i]*sum(n));n[typ]+=1
            idx=len(records);records.append([A[typ],0,[0]*len(cs)]);gap=A[typ]
        else:gap,idx=gaps.pop(k)
        rec=records[idx];rec[1]+=s;total+=s;items+=1
        for j,c in enumerate(cs):
            if s>c:rec[2][j]+=s;large[j]+=s
        if gap>s:insort(gaps,(gap-s,idx))
        if t%40!=39:continue
        m=len(records)
        assert all(rec[0]-rec[1]<d for rec in records[:-1])
        assert all(n[i]<alpha[i]*m+1 for i in range(2))
        for j,c in enumerate(cs):
            high=[i for i,rec in enumerate(records) if rec[0]-rec[1]>c]
            exceptions={high[0] if high else -1,m-1}
            for i in high:
                if i not in exceptions:assert records[i][2][j]>records[i][0]-d
            assert (len(high)-2)*(A[0]-d)<=large[j]
            cc=Q(c,scale);dd=Q(d,scale)
            assert (B-cc)*m<=Q(total,scale)+Q(d-c,A[0]-d)*Q(large[j],scale)+2+2*(dd-cc)
            checks+=1
    containers+=len(records)

# Exact attainability of the discontinuous continuous-size envelope.
envelopes=0
for dd in [Q(1,43),Q(1,7)]:
    for c in [dd/7,dd/2,dd*Q(9,10)]:
        for r in [Q(i,997) for i in range(1,1001)]+[n*c for n in range(1,20)]:
            z=r/c;n=-(-z.numerator//z.denominator)-1
            V=min(r,n*dd)
            if n and r<=n*dd:parts=[r/n]*n
            else:parts=[dd]*n+([r-n*dd] if r>n*dd else [])
            assert all(0<s<=dd for s in parts) and sum(parts)==r
            assert sum(s for s in parts if s>c)==V
            envelopes+=1
out={'status':'PASS','tiny_items':items,'created_containers':containers,'gap_and_charge_checks':checks,'exact_envelope_constructions':envelopes,'seconds':time.time()-start,'scope':'finite falsification tests, not a substitute for universal theorem'}
(H/'gap_lemma_stress.json').write_text(json.dumps(out,indent=2));print(out)
