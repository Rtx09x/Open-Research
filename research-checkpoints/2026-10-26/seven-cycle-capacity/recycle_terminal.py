#!/usr/bin/env python3
"""Apply already-admissible BPZ S2a to the new finite seven-family representation.
No assumption of physical point-private pairs is used anywhere.
"""
import sys,json,decimal,time,argparse,hashlib
sys.set_int_max_str_digits(0);sys.path.insert(0,'published')
from shannon import bpz
ap=argparse.ArgumentParser();ap.add_argument('--levels',type=int,default=8);ap.add_argument('--digits',type=int,default=30);args=ap.parse_args();start=time.monotonic();x=json.load(open('terminal_recycled_base.json'));v=tuple(x['vector']);dimension=x['base_dimension'];baseM=v[0]+v[4];decimal.getcontext().prec=args.digits+30;rows=[]
assert not bpz.rule_problems(bpz.S2a)
for k in range(args.levels+1):
 M=v[0]+v[4];approx=(decimal.Decimal(M).ln()/dimension).exp();rows.append({'level':k,'dimension':dimension,'approximate_root':str(approx),'M_digits':len(str(M))});print(k,dimension,approx,flush=True)
 if k<args.levels:v=bpz.apply_rule(bpz.S2a,[v,v]);dimension*=2
scale=10**args.digits;r=int(approx*scale);target=M*scale**dimension
while r**dimension>target:r-=1
while (r+1)**dimension<=target:r+=1
assert r**dimension<=target<(r+1)**dimension
bound=f'{r//scale}.{r%scale:0{args.digits}d}'
assert M>baseM**(2**args.levels)
out={'source_base':'terminal_recycled_base.json','source_base_sha256':hashlib.sha256(open('terminal_recycled_base.json','rb').read()).hexdigest(),'operation':'S2a(previous, previous)','levels':args.levels,'terminal_labels':['B','O'],'dimension':dimension,'final_vector':v,'M':M,'certified_lower_bound':bound,'root_numerator':r,'root_denominator':scale,'improves_published_bound_exact':True,'comparison_published_power':2**args.levels,'rows':rows,'elapsed_seconds':time.monotonic()-start}
open('recycled_terminal_certificate.json','w').write(json.dumps(out,indent=2)+'\n');print('CERTIFIED',bound,'dimension',dimension,'seconds',time.monotonic()-start,flush=True)
