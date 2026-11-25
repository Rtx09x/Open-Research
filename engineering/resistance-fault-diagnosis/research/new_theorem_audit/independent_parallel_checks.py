"""Independent Fraction nodal elimination; no imports from research verifier.
Run from any directory: python independent_parallel_checks.py
"""
from fractions import Fraction as F
from itertools import combinations
import random, json
from pathlib import Path

def network(ps):
    edges=[]; vs=[]; fs=[]; n=2
    for pp in ps:
        vv=[0]+list(range(n,n+len(pp)-1))+[1]; n+=len(pp)-1
        ff=[]
        for a,b,r in zip(vv,vv[1:],pp):
            ff.append(len(edges));edges.append((a,b,F(r)))
        vs.append(vv);fs.append(ff)
    return n,edges,vs,fs

def lap_inverse(n,edges,fault):
    # Ground t=1; invert by solving all unit RHS via forward/back elimination.
    nodes=[v for v in range(n) if v!=1]; idx={v:i for i,v in enumerate(nodes)}; d=n-1
    a=[[F(0) for j in range(2*d)] for i in range(d)]
    for e,(u,v,r) in enumerate(edges):
        if e==fault:continue
        c=1/r
        for x,y in [(u,v),(v,u)]:
            if x==1:continue
            a[idx[x]][idx[x]]+=c
            if y!=1:a[idx[x]][idx[y]]-=c
    for i in range(d):a[i][d+i]=1
    for k in range(d):
        for i in range(k+1,d):
            if not a[i][k]:continue
            f=a[i][k]/a[k][k]
            for j in range(k,2*d):a[i][j]-=f*a[k][j]
    out=[[F(0)]*d for _ in range(d)]
    for k in range(d-1,-1,-1):
        for j in range(d):out[k][j]=(a[k][d+j]-sum(a[k][i]*out[i][j] for i in range(k+1,d)))/a[k][k]
    def res(u,v):
        def z(x,y):return F(0) if 1 in (x,y) else out[idx[x]][idx[y]]
        return z(u,u)+z(v,v)-z(u,v)-z(v,u)
    return res

def run(ps,eps,full=True):
    ps=[[F(x) for x in pp] for pp in ps]; eps=F(eps)
    n,edges,vs,fs=network(ps); L=list(map(sum,ps)); p=len(ps)
    H=[1/sum(1/L[j] for j in range(p) if j!=i) for i in range(p)]
    pref=[[sum(pp[:k]) for k in range(1,len(pp))] for pp in ps]
    mu=[max(min(x,L[i]-x)**2/L[i] for x in xx) for i,xx in enumerate(pref)]
    assert eps<min(min(r for _,_,r in edges)/2,min(mu)/4)
    assert all(len(pp)>2 or H[i]+abs(pp[0]-pp[1])>2*eps for i,pp in enumerate(ps))
    qs=list(combinations(range(n),2)); selected={(0,1)}; badcuts=[]
    for i,pp in enumerate(ps):
        bad=[]
        for k,P in enumerate(pref[i],1):
            Q=L[i]-P; x=vs[i][k]
            if H[i]+abs(P-Q)<=2*eps:bad.append(k)
            else:selected.add(tuple(sorted((0 if abs(P-Q-H[i])==H[i]+abs(P-Q) else 1,x))))
        assert len(bad)<=1
        k=max(range(1,len(pp)),key=lambda k:min(pref[i][k-1],L[i]-pref[i][k-1]))
        selected.update([tuple(sorted((0,vs[i][k]))),tuple(sorted((1,vs[i][k])))])
        for k in bad:
            e=k-1 if pp[k-1]<=pp[k] else k
            selected.add(tuple(sorted(vs[i][e:e+2])));badcuts.append((i,k))
    assert len(selected)<=len(edges)+p+1
    # All faults for small cases, representative faults in symmetric large case.
    faults=range(len(edges)) if full else [fs[0][0],fs[0][1],fs[0][2],fs[0][3],fs[1][0]]
    rows={q:{} for q in qs}
    for f in faults:
        R=lap_inverse(n,edges,f)
        for q in qs: rows[q][f]=R(*q)
        j=next(i for i,ff in enumerate(fs) if f in ff); pos=fs[j].index(f)
        assert rows[0,1][f]==H[j]
        for i,pp in enumerate(ps):
            for k,P in enumerate(pref[i],1):
                Q=L[i]-P;x=vs[i][k]
                expected=(P,P+H[i]) if i==j and pos>=k else ((Q+H[i],Q) if i==j else (P*Q/L[i]+(P/L[i])**2*H[j],P*Q/L[i]+(Q/L[i])**2*H[j]))
                actual=(rows[tuple(sorted((0,x)))][f],rows[tuple(sorted((1,x)))][f])
                assert actual==expected
    for e,f in combinations(faults,2):assert any(abs(rows[q][e]-rows[q][f])>2*eps for q in selected)
    if full:
        # Independently verify the binary-response fact for every path/query.
        for ff in fs:
            for q in qs:assert len({rows[q][f] for f in ff})<=2
        # Terminal coverage: the two edges incident to every untouched internal
        # vertex have identical response at every query avoiding that vertex.
        for vv,ff in zip(vs,fs):
            for k,x in enumerate(vv[1:-1],1):
                for q in qs:
                    if x not in q:assert rows[q][ff[k-1]]==rows[q][ff[k]]
    return {'paths':[[str(x) for x in pp] for pp in ps],'epsilon':str(eps),'mu_min':str(min(mu)),'bad_cuts':len(badcuts),'faults_checked':len(faults),'fixed_queries':len(selected),'all_pairs_separated':True,'full_matrix':full}

def main():
    rng=random.Random(47139); result=[]
    for _ in range(16):
        ps=[[F(rng.randint(1,9),rng.randint(1,4)) for _ in range(rng.randint(2,5))] for __ in range(3)]
        L=list(map(sum,ps)); mu=min(max(min(sum(pp[:k]),sum(pp[k:]))**2/sum(pp) for k in range(1,len(pp))) for pp in ps)
        eps=min(min(map(min,ps))/2,mu/4)*F(999,1000)
        result.append(run(ps,eps))
    result.append(run([[1]*4]*10,F(6,25),True))
    # Exact two-parameter spacing and finite cluster envelope checks.
    count=0
    for p in range(3,21):
        for L in [p,p+1,2*p,100*p]:
            hs=sorted(1/sum(F(1,L+j) for j in range(p) if j!=i) for i in range(p))
            delta=F(1,4*(p-1)**2); U=F(4,(p-1)**2)
            assert all(delta<b-a<U for a,b in zip(hs,hs[1:]))
            for eps in [F(0),F(1,10000),F(1,100),F(1,13)]:
                K=max(sum(a<=b<=a+2*eps for b in hs) for a in hs)
                assert min(p,1+(2*eps)//U)<=K<=min(p,1+(2*eps)//delta)
                count+=1
    out={'seed':47139,'cases':result,'phase_checks':count,'status':'all passed'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({'status':'all passed','network_cases':len(result),'phase_checks':count}))
if __name__=='__main__': main()
