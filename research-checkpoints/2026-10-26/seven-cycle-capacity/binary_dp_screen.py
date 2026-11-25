#!/usr/bin/env python3
"""Numerical screen for best ordinary binary BPZ tree; exact replay is separate.
For equal H/V and s=a at the recycled base, s_n=s^n, delta_n=delta^n,
T_n=t/(s-delta)*(1-(delta/s)^n) after normalization. Thus only A_n varies
with parenthesization. This known Gao structural identity reduces the DP to n².
"""
import json,math,argparse,time
ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=4096);args=ap.parse_args();start=time.monotonic();x=json.load(open('terminal_recycled_base.json'));a,t,s,o,h,v=x['profile'];assert a==s and h==v;u=(2*o-s)/s;tau=t/(s-(2*o-s));tn=[tau*(1-u**k) for k in range(args.max_n+1)];e=[0.0]*(args.max_n+1);split=[0]*(args.max_n+1);best=(0,0)
for n in range(2,len(e)):
 def value(i):
  j=n-i;return e[i]+e[j]+e[i]*e[j]-e[i]*tn[j]-e[j]*tn[i]+tn[i]*tn[j]
 i=max(range(1,n//2+1),key=value);e[n]=value(i);split[n]=i;gain=math.log1p(e[n])/(500*n)
 if gain>best[0]:best=(gain,n)
out={'e':e,'splits':split,'best_n':best[1],'best_log_improvement':best[0],'elapsed_seconds':time.monotonic()-start};json.dump(out,open('binary_dp_screen.json','w'));print('BEST',best,'seconds',time.monotonic()-start)
