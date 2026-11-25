#!/usr/bin/env python3
"""Independent exact SPR finite-horizon solver. No deletion dominance assumed.
Code: ternary digits 0=empty,1=plus,2=minus, least significant digit=leftmost.
V[h,s] includes pointer's immediate stopping option. Full board terminates.
"""
import argparse, hashlib, json, time
from pathlib import Path


def decode(s,n):
    a=[]
    for _ in range(n): a.append(s%3);s//=3
    return a

def fmt(s,n): return ''.join('.+-'[a] for a in decode(s,n))

def build(n):
    pw=[3**j for j in range(n)]
    moves=[];counts=[]; refl=[]; expanded=0
    for s in range(3**n):
        a=decode(s,n);counts.append(sum(v!=0 for v in a))
        refl.append(sum((3-v if v else 0)*pw[n-1-j] for j,v in enumerate(a)))
        sm=[]
        for j in range(n):
            if a[j]:continue
            eligible=[k for k,v in enumerate(a) if (k<j and v==2) or (k>j and v==1)]
            removals=[0]
            for k in eligible:removals += [r+a[k]*pw[k] for r in removals]
            targets=[s-r+v*pw[j] for r in removals for v in (1,2)]
            all_del=removals[-1]
            sm.append((j,targets,(s-all_del+pw[j],s-all_del+2*pw[j])))
            expanded+=len(targets)
        moves.append(sm)
    return moves,counts,refl,expanded

def solve(n,h,out):
    begin=time.monotonic(); moves,cnt,refl,expanded=build(n)
    layers=[bytes(cnt)];greedy=[bytes(cnt)];witnesses=[]
    for t in range(1,h+1):
        prev=layers[-1];gprev=greedy[-1];cur=bytearray(cnt);gc=bytearray(cnt)
        for s,sm in enumerate(moves):
            for j,targets,all_del in sm:
                v=min(prev[x] for x in targets)
                cur[s]=max(cur[s],v)
                gv=min(gprev[x] for x in all_del)
                gc[s]=max(gc[s],gv)
                if not witnesses and min(prev[x] for x in all_del)>v:
                    winners=[x for x in targets if prev[x]==v]
                    witnesses.append({'n':n,'h':t,'state':s,'board':fmt(s,n),'request_0based':j,'best':v,'delete_all':min(prev[x] for x in all_del),'successors':[fmt(x,n) for x in winners],'all_delete_successors':[fmt(x,n) for x in all_del]})
        for s in range(3**n):
            assert cur[s]==cur[refl[s]],('reflection',n,t,s)
            assert prev[s]<=cur[s]<=n
            if cnt[s]==n: assert cur[s]==n
        layers.append(bytes(cur));greedy.append(bytes(gc))
    payload=b''.join(layers);target=out/f'values_n{n}.bin';target.write_bytes(payload)
    data={'n':n,'max_horizon':h,'state_count':3**n,'transitions_per_layer':expanded,'initial_values':[a[0] for a in layers],'delete_all_initial_values':[a[0] for a in greedy],'delete_all_witness':witnesses,'sha256':hashlib.sha256(payload).hexdigest(),'file':target.name,'seconds':time.monotonic()-begin}
    (out/f'metadata_n{n}.json').write_text(json.dumps(data,indent=2)+'\n');return data

def main():
    p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=8);p.add_argument('--horizon',type=int,default=16);p.add_argument('--out',default='exact');a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    results=[]
    for n in range(1,a.max_n+1):
        r=solve(n,a.horizon,out);results.append(r);print(json.dumps(r),flush=True)
    (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
