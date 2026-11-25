"""Hardened public validator: global model validity AND designated operation.

An orbit-only pass is not a physical-model certificate. Unknown large global
span problems are rejected as unverified, never silently accepted. Common
polynomial shifts admit an algebraic all-environment span certificate.
"""
from __future__ import annotations
from fractions import Fraction as F
import argparse,json
from independent import from_legacy,verify_device,geometry,InvalidDynamics
from resources import explicit_device

class UnverifiedModel(ValueError):pass

def integer(v,label):
    if type(v)!=int:raise ValueError(f'{label} must be an exact integer')
    return v

def shape(m):
    n=integer(m.get('n'),'n')
    if not 0<=n<=10000:raise ValueError('n outside validator resource limit')
    if 'terms' in m:
        # The original archive stores rational coefficients and an alternating path.
        if len(m['a'])!=n or len(m['b'])!=n or len(m['terms'])!=n:raise ValueError('original row shape')
        for i,row in enumerate(m['terms']):
            for t in row:
                s=integer(t['mask'],'mask')
                if not 0<=s<1<<n or s>>i&1:raise ValueError('self-dependence or invalid mask')
                F(t['coefficient'])
        if not m['path'] or len(m['path'])%2:raise ValueError('alternating path')
        codes=m['path'][::2];f=list(range(1,len(codes)))+[0]
        for x,A in enumerate(codes):
            P=m['path'][2*x+1];T=codes[f[x]]
            if type(P)!=int or P!=(A|T) or (P^A).bit_count()!=1 or (P^T).bit_count()!=1:
                raise ValueError('stored alternating path is inconsistent')
    else:
        D=integer(m.get('scale'),'scale')
        if D<=0:raise ValueError('scale must be positive')
        integer(m.get('low'),'low')
        highs=m.get('highs')
        if not isinstance(highs,list) or not highs:raise ValueError('pulse list')
        if any(integer(h,'high')<=m['low'] for h in highs) or highs!=sorted(set(highs)):
            raise ValueError('highs must be distinct increasing values above low')
        codes=m.get('codes');f=m.get('f')
        if not isinstance(codes,list) or not isinstance(f,list) or not codes:raise ValueError('code map')
        if 'gates' in m and m['gates'] is not None:
            if len(m['gates'])!=len(codes) or any(type(g)!=int or not 1<=g<=len(highs)+1 for g in m['gates']):
                raise ValueError('gate domain')
        kind=m.get('kind')
        if kind=='affine':
            if len(m['a'])!=n or len(m['b'])!=n or len(m['J'])!=n:raise ValueError('affine shape')
            for v in m['a']+m['b']:integer(v,'bare threshold')
            for i,row in enumerate(m['J']):
                if len(row)!=n or row[i]!=0:raise ValueError('affine shape or self-coupling')
                for c in row:integer(c,'coupling')
        elif kind=='explicit_polynomial':
            for key in ('up','down'):
                if len(m[key])!=n:raise ValueError('polynomial row count')
                for i,row in enumerate(m[key]):
                    used=set()
                    for t in row:
                        s=integer(t['mask'],'mask');integer(t['coefficient'],'coefficient')
                        if not 0<=s<1<<n or s>>i&1 or s in used:raise ValueError('invalid or duplicate term')
                        used.add(s)
        elif kind=='raw':
            if n>16:raise UnverifiedModel('Raw tables exceed the exhaustive validation limit')
            for key in ('plus','minus'):
                if len(m[key])!=n or any(len(row)!=1<<n for row in m[key]):raise ValueError('raw shape')
                for row in m[key]:
                    for v in row:integer(v,'raw threshold')
        elif kind in ('polynomial','saturating'):
            k=integer(m['k'],'layer rank')
            if not 0<=k<n or any(len(m[key])!=n for key in ('a','b','zeros','fours')):raise ValueError('layer shape')
            for v in m['a']+m['b']:integer(v,'bare threshold')
            for i in range(n):
                for key in ('zeros','fours'):
                    vals=m[key][i]
                    if len(set(vals))!=len(vals):raise ValueError('duplicate incidence')
                    for s in vals:
                        integer(s,'incidence')
                        if not 0<=s<1<<n or s>>i&1 or s.bit_count()!=k:raise ValueError('invalid incidence')
                if set(m['zeros'][i])&set(m['fours'][i]):raise ValueError('conflicting labels')
            if n>16:raise UnverifiedModel('This adapter requires a table expansion above the configured limit')
        elif kind=='table':
            if n>16:raise UnverifiedModel('Table expansion exceeds the configured limit')
            for key in ('up','down'):
                for s,i in m[key].items():
                    if not 0<=int(s)<1<<n or type(i)!=int or not 0<=i<n:raise ValueError('labeled edge domain')
        else:raise ValueError('unknown model kind')
    if not geometry(codes,f,n):raise ValueError('invalid code geometry, map, or encoding')
    if 'terms' in m and n>16:raise UnverifiedModel('Original polynomial adapter expansion exceeds limit')
    return n


def validate(m,exhaustive_limit=13):
    n=shape(m)
    d=explicit_device(m) if m.get('kind')=='explicit_polynomial' else from_legacy(m)
    global_method='all-environment enumeration'
    if n<=exhaustive_limit:
        checked=verify_device(d,full=True)
    else:
        kind=m.get('kind')
        if kind in ('affine','polynomial','saturating') or 'terms' in m:
            widths=[F(a)-F(b) for a,b in zip(m['a'],m['b'])]
        elif kind=='explicit_polynomial':
            widths=[]
            for plus,minus in zip(m['up'],m['down']):
                a={t['mask']:t['coefficient'] for t in plus};b={t['mask']:t['coefficient'] for t in minus}
                if any(a.get(s,0)!=b.get(s,0) for s in (set(a)|set(b))-{0}):
                    raise UnverifiedModel('Large branch-dependent polynomial needs an explicit global-span certificate')
                widths.append(F(a.get(0,0)-b.get(0,0),m['scale']))
        else:raise UnverifiedModel('Global span not certified for this large model')
        if any(w<=0 for w in widths):raise InvalidDynamics('nonpositive span')
        global_method='symbolic cancellation of identical branch shifts'
        checked=verify_device(d)
        checked['min_span']=None if not widths else str(min(widths))
        checked['min_span_units']='unscaled field units'
    return {'global_model_valid':True,'global_validation_method':global_method,
            'designated_operation_valid':True,**checked}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('model');ap.add_argument('--exhaustive-limit',type=int,default=13)
    args=ap.parse_args()
    try:
        with open(args.model) as stream:m=json.load(stream)
        print(json.dumps(validate(m,args.exhaustive_limit),indent=2))
    except (ValueError,KeyError,IndexError,TypeError) as exc:
        print(json.dumps({'accepted':False,'reason':str(exc)}));raise SystemExit(1)

if __name__=='__main__':main()
