"""Exact rational Laplacian and interval-minimax checks of the general path theorem."""
import sys,json,math,time
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from exact_search import responses

def graph(paths):
    edges=[];weights=[];verts=[];faults=[];n=2
    for p in paths:
        vs=[0]+list(range(n,n+len(p)-1))+[1];n+=len(p)-1
        verts.append(vs);fs=[]
        for a,b,r in zip(vs,vs[1:],p):fs.append(len(edges));edges.append((a,b));weights.append(F(r))
        faults.append(fs)
    return n,edges,weights,verts,faults

def check(paths,eps,minimax=True):
    start=time.time();paths=[[F(x) for x in p] for p in paths];eps=F(eps)
    n,edges,weights,verts,faults=graph(paths);qs,M=responses(n,edges,resistances=weights)
    rows={q:row for q,row in zip(qs,M)}
    def row(a,b):return rows[tuple(sorted((a,b)))]
    L=[sum(p) for p in paths];H=[1/sum(1/L[j] for j in range(len(paths)) if j!=i) for i in range(len(paths))]
    mu=min(max(min(sum(p[:k]),sum(p[k:]))**2/sum(p) for k in range(1,len(p))) for p in paths)
    assumptions=eps<min(min(weights)/2,mu/4) and all(len(p)>2 or H[i]+abs(p[0]-p[1])>2*eps for i,p in enumerate(paths))
    assert assumptions, 'Test instance is outside the theorem assumptions'
    selected={(0,1)};checks=0;badcount=0
    for i,p in enumerate(paths):
        good=[];bad=[];P=F(0)
        for k,x in enumerate(verts[i][1:-1],1):
            P+=p[k-1];Q=L[i]-P
            for j,fs in enumerate(faults):
                for f in fs:
                    pos=fs.index(f)
                    expected=(P,P+H[i]) if i==j and pos>=k else ((Q+H[i],Q) if i==j else (P*Q/L[i]+P*P/L[i]**2*H[j],P*Q/L[i]+Q*Q/L[i]**2*H[j]))
                    assert (row(0,x)[f],row(1,x)[f])==expected;checks+=1
                if i!=j and abs(H[i]-H[j])<=2*eps and min(P,Q)**2/L[i]>4*eps:
                    outside=(P*Q/L[i]+P*P/L[i]**2*H[j],P*Q/L[i]+Q*Q/L[i]**2*H[j])
                    for own in [(P,P+H[i]),(Q+H[i],Q)]:assert max(abs(a-b) for a,b in zip(own,outside))>2*eps
            gamma=H[i]+abs(L[i]-2*P)
            if gamma>2*eps:
                sep0=abs(P-(Q+H[i]));hub=0 if sep0==gamma else 1
                selected.add(tuple(sorted((hub,x))));good.append(x)
            else:bad.append((k,x))
        assert len(bad)<=1 and good
        x=max(verts[i][1:-1],key=lambda x:min(sum(p[:verts[i].index(x)]),sum(p[verts[i].index(x):])));selected.add(tuple(sorted((0,x))));selected.add(tuple(sorted((1,x))))
        for k,x in bad:
            badcount+=1;a=k-1 if p[k-1]<=p[k] else k
            q=tuple(sorted((verts[i][a],verts[i][a+1])));selected.add(q)
            assert abs(rows[q][faults[i][k-1]]-rows[q][faults[i][k]])>2*eps
    assert len(selected)<=len(edges)+len(paths)+1
    for e,f in combinations(range(len(edges)),2):assert any(abs(rows[q][e]-rows[q][f])>2*eps for q in selected)
    K=max(sum(h<=z<=h+2*eps for z in H) for h in H)
    B=max(1 if len(p)==2 else math.ceil(math.log2(len(p)-1))+1 for p in paths)
    lo=max((K+1)//2,math.ceil(math.log2(max(map(len,paths)))))
    hi=min(1+2*(K-1)+B,2*(len(paths)-1)+B)
    A=None;states=None
    if minimax:
        overlaps=[]
        for rr in M:
            ends=set(x-eps for x in rr)|set(x+eps for x in rr)
            groups={sum(1<<e for e,x in enumerate(rr) if abs(x-y)<=eps) for y in ends}
            overlaps.append(tuple(s for s in groups if s and not any(s!=t and s&t==s for t in groups)))
        @lru_cache(None)
        def dp(mask):
            if mask.bit_count()<2:return 0
            ans=1000000
            for groups in overlaps:
                subs={s&mask for s in groups}-{0}
                if mask in subs:continue
                worst=0
                for sub in sorted(subs,key=int.bit_count,reverse=True):
                    worst=max(worst,dp(sub))
                    if 1+worst>=ans:break
                ans=min(ans,1+worst)
            return ans
        A=dp((1<<len(edges))-1);states=dp.cache_info().currsize
        assert lo<=A<=hi
    return dict(theorem_assumptions=assumptions,mu=str(mu),paths=[[str(x) for x in p] for p in paths],epsilon=str(eps),K=K,lower=lo,upper=hi,adaptive_exact=A,states=states,fixed_queries=len(selected),membership_checks=checks,exceptional_vertices=badcount,seconds=time.time()-start)

if __name__=='__main__':
    cases=[([[1]*3]*3,'0'),([[1]*3]*3,'0.08'),([[1]*3,[1]*4,[1]*5],'0.08'),([[1,2,3],[2,1,1],[3,2,1]],'0.08'),([[1,2],[1,3],[2,4]],'0.04'),([[1]*3]*4,'0.08')]
    for ps,e in cases:print(json.dumps(check(ps,e)),flush=True)
    print(json.dumps(check([[1]*4]*10,'0.24',False)),flush=True)
