"""Finite independent replay of every n368..401 circular-template exclusion."""
from pathlib import Path
from math import gcd
import json,time,resource,os
p=Path(__file__).with_name('check_c7_circular382_independent.py');ns={}
exec(p.read_text().split('units=[u')[0],ns)
resource.setrlimit(resource.RLIMIT_AS,(400*1024**2,400*1024**2));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
# Replace the deliberately fixed382 residue range in the independently authored
# routine, keeping the same exact exhaustive pair-mask algorithm.
source=p.read_text();f=source[source.index('def enumerate_case'):source.index('units=[u')].replace('range(1,192)','range(1,n//2+1)')
exec(f,ns);start=time.monotonic();records=[]
for n in range(368,402):
 k=(2*n+6)//7;ns.update(n=n,k=k)
 units=[a for a in range(1,n)if gcd(a,n)==1]
 nonunits=[a for a in range(1,n//2+1)if gcd(a,n)>1]
 divisors=sorted({gcd(a,n)for a in nonunits})
 assert all(any(a*u%n==gcd(a,n)for u in units)for a in range(1,n))
 assert not ns['enumerate_case'](1,list(range(1,n//2+1)))
 for g in divisors:assert not ns['enumerate_case'](g,nonunits)
 records.append({'n':n,'threshold':k,'no_unit_gcd_cases':divisors,'infeasible':True})
 print(n,'PASS',flush=True)
out={'PASS':True,'cases':sum(1+len(r['no_unit_gcd_cases'])for r in records),'records':records,'seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Rank-one circular templates only; all n368..401 direct ceil(2n/7) thresholds. Zero coordinates reduce to repeated nonzero coordinates. Not nonlinear codes.'}
Path(__file__).with_name('c7_circular_range_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='records'},indent=2))
