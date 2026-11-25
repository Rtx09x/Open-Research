"""Convert certified polynomial witnesses to explicit band-separated devices.

Adding the same positive constant to every up threshold and pulse maximum
preserves each designated transition and improves the hysteresis spans. For
nonnegative polynomial shifts, separated bands certify global avalanche freedom.
Small per-element offsets remove ties without consuming the certified margins.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import json
from synthesis import Problem,verify_certificate
from resources import explicit_device
from independent import verify_device

def finish(cert):
    verify_certificate(cert)
    p=Problem(**cert['spec']);x=list(map(F,cert['primal']));D=lcm(*(z.denominator for z in x))
    n=p.spec['n'];den=16*(n+1);scale=D*den
    branch={}
    for u,key in ((True,'up'),(False,'down')):
        rows=[]
        for i in range(n):
            values={}
            for (j,flag,mask),expr in p.expr.items():
                if j!=i or flag!=u:continue
                z=sum(c*x[v] for v,c in expr.items())
                if z:values[mask]=int(z*scale)
            values[0]=values.get(0,0)+i+1
            rows.append([{'mask':mask,'coefficient':c} for mask,c in sorted(values.items()) if c])
        branch[key]=rows
    def ext(row,maximum):
        return sum(t['coefficient'] for t in row if not t['mask'] or
                   (t['coefficient']>0 if maximum else t['coefficient']<0))
    smallest=min(ext(row,False) for row in branch['up'])
    biggest=max(ext(row,True) for row in branch['down'])
    lift=max(0,biggest-smallest+2*scale)
    for row in branch['up']:
        constant=next((t for t in row if t['mask']==0),None)
        if constant is None:row.insert(0,{'mask':0,'coefficient':lift})
        else:constant['coefficient']+=lift
    H=sum(c*x[v] for v,c in p.H.items())
    model={'kind':'explicit_polynomial','n':n,'scale':scale,'low':0,
           'highs':[int(H*scale)+lift],'codes':p.spec['codes'],'f':p.spec['f'],**branch,
           'band_lift_scaled':lift,'source_fingerprint':cert['fingerprint'],
           'common_shifts':p.spec['common'],'uniform_span':p.spec['uniform'],
           'nonnegative_shifts':p.spec['nonnegative']}
    verify_device(explicit_device(model),full=True)
    support={(i,t['mask']) for branch in (model['up'],model['down']) for i,row in enumerate(branch)
             for t in row if t['mask'] and t['coefficient']}
    model['directed_monomial_support']=len(support)
    return model

if __name__=='__main__':
    R=Path(__file__).resolve().parents[1]/'results';out=[]
    for name in ('cycle_n6_q15_d1_c0_u0_p1','cycle_n7_q35_d2_c1_u1_p1'):
        cert=json.loads((R/(name+'.json')).read_text());model=finish(cert)
        result=verify_device(explicit_device(model),full=True)
        # Check candidate ties at every environment on both branches.
        dev=explicit_device(model)
        for s in range(1<<dev.n):
            for up in (True,False):
                vals=[dev.evaluate(i,s,up) for i in range(dev.n) if bool(s>>i&1)!=up]
                assert len(vals)==len(set(vals))
        out.append({'file':name+'_completed.json','n':model['n'],'q':len(model['codes']),
                    'degree':cert['spec']['degree'],'common':cert['spec']['common'],
                    'uniform':cert['spec']['uniform'],'support':model['directed_monomial_support'],
                    **result})
        (R/(name+'_completed.json')).write_text(json.dumps(model,indent=2))
    (R/'improved_cycle_constructions.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
