from fractions import Fraction as F
import json

def query_cover(m):
 sizes=[3]*(m//3)
 if m%3:sizes[-1]+=m%3
 qs=[];off=0
 for sz in sizes:
  qs += [(off+i,off+i+1) for i in range(sz-1)]
  off+=sz
 return qs
out=[]
for m in [4,5,6,7,8,9,10,100,500,501,502]:
 qs=query_cover(m)
 supports=[tuple(j for j,(p,q) in enumerate(qs) if i in [p,q]) for i in range(m)]
 assert all(supports) and len(set(supports))==m and len(qs)==(2*m+2)//3
 out.append({'m':m,'queries':len(qs),'distinct_nonempty_supports':m})
m=500;eps=F(1,200);Hbound=F(4,m-1)
assert eps>=F(2,m-1) and eps+Hbound<F(1,72)
b=[F(2)+F(i+1,m+1) for i in range(m)]
w=[x/(1+x) for x in b];beta=[1/(1+x) for x in b];C=sum(beta);H=1/C
qs=query_cover(m);checks=0
for i in [0,1,2,100,249,498,499]:
 for side in ['s','t']:
  for t in [F(1,2),F(3,4),F(1)]:
   a1=1+t if side=='s' else F(1);b1=b[i]+t if side=='t' else b[i]
   wi=a1*b1/(a1+b1);betai=a1/(a1+b1);H1=1/(C-beta[i]+1/(a1+b1));dw=wi-w[i]
   for p,q in qs:
    wp=wi if p==i else w[p];wq=wi if q==i else w[q]
    bp=betai if p==i else beta[p];bq=betai if q==i else beta[q]
    delta=wp+wq+(bp-bq)**2*H1-(w[p]+w[q]+(beta[p]-beta[q])**2*H)
    local=dw if i in [p,q] else 0
    assert abs(delta-local)<=Hbound
    # threshold midway between class intervals, valid at either noise endpoint
    for ans in [delta-eps,delta+eps]:
     predicted='none' if ans<F(1,72) else ('t' if ans<F(23,168) else 's')
     expected=side if i in [p,q] else 'none'
     assert predicted==expected,(i,side,t,p,q,ans)
    checks+=1
out.append({'m':m,'epsilon':str(eps),'exact_fault_query_checks':checks,'both_adversarial_endpoints':True,'A':m//2+1,'N':len(qs)})
print(json.dumps(out,indent=2))
