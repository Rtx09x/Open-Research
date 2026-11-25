#!/usr/bin/env python3
import sys,json,decimal,time,hashlib,argparse
sys.set_int_max_str_digits(0);sys.path.insert(0,'published')
from shannon import bpz
ap=argparse.ArgumentParser();ap.add_argument('--digits',type=int,default=18);args=ap.parse_args();start=time.monotonic();basepath='terminal_recycled_base.json';x=json.load(open(basepath));screen=json.load(open('binary_dp_screen.json'));splits=screen['splits'];target=screen['best_n'];nodes=[];values=[];memo={}
def build(n):
 if n in memo:return memo[n]
 if n==1:node={'operation':'base','leaves':1};v=tuple(x['vector'])
 else:
  l=splits[n];r=n-l;li,ri=build(l),build(r);node={'operation':'S2a','children':[li,ri],'leaves':n};v=bpz.apply_rule(bpz.S2a,[values[li],values[ri]])
 i=len(nodes);nodes.append(node);values.append(v);memo[n]=i;return i
root=build(target);v=values[root];M=v[0]+v[4];d=500*target;decimal.getcontext().prec=args.digits+30;approx=(decimal.Decimal(M).ln()/d).exp();scale=10**args.digits;r=int(approx*scale);power=M*scale**d
print('root_check_start',d,'M_digits',len(str(M)),'approx',approx,flush=True)
while r**d>power:r-=1
while (r+1)**d<=power:r+=1
assert r**d<=power<(r+1)**d
old=json.load(open('recycled_terminal_certificate.json'));assert d%old['dimension']==0 and M>old['M']**(d//old['dimension']);bound=f'{r//scale}.{r%scale:0{args.digits}d}'
out={'source_base':basepath,'source_base_sha256':hashlib.sha256(open(basepath,'rb').read()).hexdigest(),'nodes':nodes,'root':root,'leaf_count':target,'dimension':d,'terminal_labels':['B','O'],'final_vector':v,'M':M,'certified_lower_bound':bound,'root_numerator':r,'root_denominator':scale,'strictly_improves_128000_certificate':True,'elapsed_seconds':time.monotonic()-start}
open('optimized_recycle_certificate.json','w').write(json.dumps(out,indent=2)+'\n');print('CERTIFIED',bound,'dimension',d,'seconds',time.monotonic()-start,flush=True)
