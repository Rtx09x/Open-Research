"""New sparse common-shift unary realization. No earlier constructors imported."""
from __future__ import annotations
from independent import from_legacy,verify_device

def sparse_unary(f:list[int])->dict:
    n=len(f)
    if not n or any(type(t)!=int or not 0<=t<n for t in f):raise ValueError('invalid map')
    if any(t!=s and f[t]==s for s,t in enumerate(f)):raise ValueError('two-cycle')
    J=[[0]*n for _ in range(n)]
    # A source makes its successor easier to activate; the successor releases it.
    for s,t in enumerate(f):
        if s!=t:
            J[t][s]=-2
            J[s][t]=4
    # Suppress premature activation of the successor's own successor at the peak.
    for s,t in enumerate(f):
        r=f[t]
        if len({s,t,r})==3:
            assert J[r][s]>=0
            J[r][s]=max(2,J[r][s])
    maxpos=max(sum(max(c,0) for c in row) for row in J)
    minneg=min(sum(min(c,0) for c in row) for row in J)
    B=max(4,1+maxpos-minneg)
    D=8*(n+1)
    return {'kind':'affine','n':n,'scale':D,'low':0,'highs':[(B-1)*D],
            'a':[B]*n,'b':[-3]*n,'J':J,'codes':[1<<i for i in range(n)],'f':list(f),
            'nonzero_directed_influences':sum(c!=0 for row in J for c in row),
            'nonfixed_edges':sum(i!=t for i,t in enumerate(f)),
            'global_band_guarantee':True,'global_avalanche_free_guarantee':False}

if __name__=='__main__':
    from itertools import product
    import json,time
    from pathlib import Path
    out=[];start=time.monotonic()
    for n in range(1,7):
        passed=trials=0;worst=0
        for f in product(range(n),repeat=n):
            if any(t!=s and f[t]==s for s,t in enumerate(f)):continue
            m=sparse_unary(list(f));r=verify_device(from_legacy(m))
            assert m['nonzero_directed_influences']<=3*m['nonfixed_edges']
            assert r['margin']*8>7*m['scale']
            passed+=1;trials+=r['trials'];worst=max(worst,m['nonzero_directed_influences'])
        out.append({'n':n,'maps':passed,'transitions':trials,'max_support':worst})
        print(out[-1],flush=True)
    cycles=[]
    for n in (3,4,5,10,35,100):
        m=sparse_unary(list(range(1,n))+[0]);r=verify_device(from_legacy(m),full=n<=10)
        cycles.append({'n':n,'support':m['nonzero_directed_influences'],**r})
    report={'exhaustive':out,'cycles':cycles,'seconds':time.monotonic()-start}
    R=Path(__file__).resolve().parents[1]/'results'
    (R/'sparse_universal_verification.json').write_text(json.dumps(report,indent=2))
    (R/'sparse_100_counter.json').write_text(json.dumps(sparse_unary(list(range(1,100))+[0]),indent=2))
    print(json.dumps(report,indent=2))
