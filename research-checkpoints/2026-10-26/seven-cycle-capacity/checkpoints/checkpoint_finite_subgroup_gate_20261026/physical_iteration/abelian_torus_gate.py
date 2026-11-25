"""Exact finite abelian torus gates, order368..401, rank<=5.
Homomorphisms into five circles are specified by five characters. Domain
invariant factors divide each other. A surjective coordinate splits off the
largest cyclic factor and normalizes to the final projection by a DOMAIN
isomorphism. If none is surjective, all five characters are enumerated as one
single plus two pairs. No codomain row operations are used.
"""
import itertools,math,json,time,resource,os,argparse
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
START=0

def invtypes(N,prefix=()):
 lo=prefix[-1] if prefix else 2
 if N>=lo and (not prefix or N%lo==0):yield prefix+(N,)
 for d in range(lo,math.isqrt(N)+1):
  if N%d==0 and (not prefix or d%lo==0):yield from invtypes(N//d,prefix+(d,))

def run_case(factors,mode):
 N=math.prod(factors);e=factors[-1];k=(2*e+6)//7;allg=list(itertools.product(*(range(d) for d in factors)))
 gs=[g for g in allg if any(g) and g<=tuple((-x)%d for x,d in zip(g,factors)) and (mode!='surjective' or min(g[-1],e-g[-1])<k)]
 full=(1<<len(gs))-1;masks={};excluded_bad=0;excluded_full=0
 for a in allg:
  coeff=tuple(x*(e//d) for x,d in zip(a,factors));order=e//math.gcd(e,*coeff)
  if mode=='no_surjective' and order==e:excluded_full+=1;continue
  # One image with fractional clique bound<=3 yields at most
  # 3*theta(C7)^4 < 3*(1659/500)^4 <368 words in any5-coordinate code.
  if N>=368 and order*1<=3*((2*order+6)//7):excluded_bad+=1;continue
  m=0
  for j,g in enumerate(gs):
   v=sum(c*x for c,x in zip(coeff,g))%e
   if min(v,e-v)>=k:m|=1<<j
  masks.setdefault(m,a)
 mm=list(masks);total=0
 for m in mm:total|=m
 out={'factors':factors,'order':N,'exponent':e,'distance':k,'mode':mode,'difference_classes':len(gs),'candidate_masks':len(mm),'excluded_bad_image_characters':excluded_bad,'excluded_surjective_characters':excluded_full,'characters':None}
 if total!=full:out['obstruction']='all_candidate_characters_miss_difference';out['missed_difference']=gs[((full^total)&-(full^total)).bit_length()-1];return out
 pairs={}
 for i,a in enumerate(mm):
  for b in mm[i:]:pairs.setdefault(a|b,(masks[a],masks[b]))
 values=list(pairs);n=len(values);columns=[0]*len(gs)
 for j,m in enumerate(values):
  bit=1<<j
  while m:
   b=m&-m;m-=b;columns[b.bit_length()-1]|=bit
 allpartners=(1<<n)-1;tests=0;outer=0;found=None
 firsts=[0] if mode=='surjective' else sorted(mm,key=int.bit_count,reverse=True)
 for s in firsts:
  for m in values:
   need=full^(s|m);possible=allpartners;outer+=1
   while need and possible:
    b=need&-need;need-=b;possible&=columns[b.bit_length()-1];tests+=1
   if possible:
    j=(possible&-possible).bit_length()-1;first=(0,)*(len(factors)-1)+(1,) if mode=='surjective' else masks[s];found=[first,*pairs[m],*pairs[values[j]]];break
   if outer%1000==0 and time.monotonic()-START>245:return {**out,'complete':False,'reason':'checkpoint time budget','pair_masks':n,'outer_tests':outer,'bitset_intersections':tests}
  if found:break
 out.update({'pair_masks':n,'outer_tests':outer,'bitset_intersections':tests,'characters':found,'complete':True})
 if found:
  coeffs=[tuple(a*(e//d) for a,d in zip(char,factors)) for char in found]
  mind=min(max(min(sum(c*x for c,x in zip(co,g))%e,(-sum(c*x for c,x in zip(co,g)))%e) for co in coeffs) for g in allg if any(g));assert mind>=k
  words={tuple(sum(c*x for c,x in zip(co,g))%e for co in coeffs) for g in allg};assert len(words)==N
  physical={tuple(7*x//e for x in w) for w in words};assert len(physical)==N and all(any((x-y)%7 not in(0,1,6) for x,y in zip(a,b)) for a,b in itertools.combinations(physical,2));out['physical_code']=sorted(physical);out['actual_distance']=mind
 return out

def main():
 global START
 ap=argparse.ArgumentParser();ap.add_argument('--resume',action='store_true');args=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(270,270));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});START=time.monotonic()
 # Elementary rational upper theta(C7)<3.318 from pi>3.14 and cos Taylor.
 x=F(157,350);c=1-x*x/2+x**4/24;assert 7*c/(1+c)<F(1659,500);assert 3*F(1659,500)**4<368
 path=P/'abelian_torus_gate.json';old=json.loads(path.read_text()) if args.resume else {};records=[r for r in old.get('records',[]) if r.get('complete',True)];done={(tuple(r['factors']),r['mode']) for r in records};types=[f for N in range(368,402) for f in invtypes(N) if 2<=len(f)<=5];skipped_high_rank=[f for N in range(368,402) for f in invtypes(N) if len(f)>5]
 types.sort(key=lambda f:(f!=(2,196),len(f),math.prod(f),f));jobs=[(f,mode) for f in types for mode in ['surjective','no_surjective']]
 for f,mode in jobs:
  if (f,mode) in done:continue
  e=f[-1];k=(2*e+6)//7
  if 3*e<=10*k:
   # E_(e/k) cohomomorphically maps to E10/3, whose exact theta<16/5.
   assert all(min((10*a//e-10*b//e)%10,(10*b//e-10*a//e)%10)>=3 for a in range(e) for b in range(e) if min((a-b)%e,(b-a)%e)>=k)
   r={'factors':f,'order':math.prod(f),'exponent':e,'mode':mode,'characters':None,'complete':True,'obstruction':'exact_theta_E10_over3_cohomomorphism'}
  else:r=run_case(f,mode)
  records.append(r);print(json.dumps({k:v for k,v in r.items() if k!='physical_code'}),flush=True)
  out={'records':records,'noncyclic_group_types':len(types),'jobs':len(jobs),'skipped_rank_gt5':skipped_high_rank,'complete':len(records)==len(jobs) and all(r.get('complete',True) for r in records),'seconds_this_checkpoint':time.monotonic()-START,'maxRSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Finite abelian subgroup codes of order368..401 in five circles at distance2/7, with rational image-order theta pruning. Cyclic groups are covered separately by prior exact gate. Nonlinear near-packing/rounding-completion remains outside.'};path.write_text(json.dumps(out,indent=2)+'\n')
  if r.get('characters') or not r.get('complete',True) or time.monotonic()-START>240:break
 print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':main()
