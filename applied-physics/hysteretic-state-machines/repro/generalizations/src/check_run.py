"""Reproduce exact finite checks. Standard library only; run from any directory.

These checks supplement the manuscript's general proofs. Enumeration counts
are not used as substitutes for the all-size theorems. Optional discovery
solvers are deliberately not imported.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction
import json,time,random
from memory import *
from minimize import minimize,capacity
from cycle_operations import validate_cycle,model,lift,one_hot_cycle,join,embed,complement
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'


def full_audit(m):
    n=m['n'];mn=None;mx=None;span=None
    for state in range(1<<n):
        ups=[threshold(m,i,state,True) for i in range(n)]
        dns=[threshold(m,i,state,False) for i in range(n)]
        for i in range(n):
            require(ups[i]>dns[i],'Nonpositive span')
            span=ups[i]-dns[i] if span is None else min(span,ups[i]-dns[i])
            if m['kind']!='table':
                for j in range(n):
                    if j!=i and not state>>j&1:
                        require(threshold(m,i,state|1<<j,True)>=ups[i],'Up threshold is not monotone')
                        require(threshold(m,i,state|1<<j,False)>=dns[i],'Down threshold is not monotone')
        mn=min(ups) if mn is None else min(mn,min(ups))
        mx=max(dns) if mx is None else max(mx,max(dns))
    require(mn>mx,'Global bands overlap')
    return {'n':n,'configurations':1<<n,'minimum_span_scaled':span,'band_gap_scaled':mn-mx,'scale':m['scale']}


def check_path(row):
    n,k,q=row['n'],row['k'],row['q'];p=row['path']
    require(validate_cycle(n,p)==(k,q),'Witness metadata mismatch')
    reports=[check_machine(model(n,p,sat)) for sat in (True,False)]
    codes=p[::2]+[p[-1]];f=list(range(1,q+1))+[q]
    chain=check_machine(table_compile(codes,f,n))
    return {'n':n,'k':k,'q':q,'counter':reports,'chain_states':len(codes),'chain':chain}


def main():
    start=time.monotonic();report={};unary=[]
    for m in range(1,7):
        yes=no=trials=0
        for raw in product(range(m),repeat=m):
            f=list(raw)
            if has_two_cycle(f):no+=1;continue
            trials+=check_machine(one_hot(f))['trials'];yes+=1
        row={'states':m,'all_maps':m**m,'constructed':yes,'two_cycle_rejected':no,'exact_transitions':trials}
        unary.append(row);print('UNARY',row,flush=True)
    report['unary_exhaustive']=unary
    reset=[]
    for n in range(1,17):
        for k in range(1,n+1):
            m=reset_machine(n,k);r=check_machine(m)
            require(len(m['codes'])==1+k*(n-k+1),'Reset cardinality mismatch')
            r.update(n=n,k=k,states=len(m['codes']));reset.append(r)
    report['reset_constructions']=reset
    brooms=[]
    for d in range(1,101):
        m=broom_machine(d);r=check_machine(m);r.update(leaves=d,n=m['n'])
        require((m['n']-2)**2//4<d<=(m['n']-1)**2//4,'Incorrect broom minimum')
        brooms.append(r)
    report['broom_constructions']=brooms
    minima=[];histograms=[]
    for m in range(2,5):
        hist=Counter()
        for raw in product(range(m),repeat=m):
            r=minimize(list(raw));hist[str(r['minimum'])]+=1
            if r['minimum'] is not None:
                check_machine(table_compile(r['codes'],r['f'],r['minimum']))
            minima.append(r)
        histograms.append({'states':m,'minimum_histogram':dict(hist)})
        print('MINIMA',m,dict(hist),flush=True)
    report['small_unary_minima']=histograms
    (R/'small_unary_minima.json').write_text(json.dumps(minima,indent=2)+'\n')
    amplitude=[]
    for m in (1,2,3):
        yes=no=trials=0
        for raw in product(range(m),repeat=2*m):
            table=[list(raw[2*i:2*i+2]) for i in range(m)]
            try:design=amplitude_compile(table)
            except ValueError:no+=1;continue
            trials+=check_machine(design)['trials'];yes+=1
        amplitude.append({'states':m,'tables':m**(2*m),'constructed':yes,'rejected':no,'exact_transitions':trials})
    report['amplitude_exhaustive']=amplitude
    for gates in product(range(1,5),repeat=3):check_machine(one_hot([1,2,0],list(gates),4))
    report['four_amplitude_gate_assignments']=64
    print('AMPLITUDE',amplitude,flush=True)
    gray=[]
    for q in list(range(3,129))+[255,256,257,1000,1001]:
        m=cycle_model(q);r=check_machine(m)
        require(m['n']<=2*(q-1).bit_length(),'Logarithmic construction too large')
        require(Fraction(r['minimum_slack_numerator'],r['scale'])>Fraction(7,8),'Insufficient saturation margin')
        r.update(n=m['n'],q=q);gray.append(r)
    report['gray_fallback_checks']=gray
    spectra=[]
    for file in sorted(R.glob('spectrum_n*.json')):
        data=json.loads(file.read_text());n=next(iter(data.values()))['n']
        for row in data.values():check_path(row)
        periods=sorted(map(int,data))
        require(periods==list(range(3,capacity(n)+1)),'An advertised finite spectrum has a gap')
        spectra.append({'n':n,'periods':periods,'capacity':capacity(n),'complete':True})
    report['complete_finite_spectra']=spectra
    # Independent rebuilding, not simply trusting the final composed JSON.
    initial=json.loads((R/'large_cycle_witnesses.json').read_text())
    ingredients=json.loads((R/'composition_ingredients.json').read_text())
    def get(data,n,k,q):
        rows=[v for v in data.values() if (v['n'],v['k'],v['q'])==(n,k,q)]
        require(len(rows)==1,'Missing composition ingredient');check_path(rows[0]);return rows[0]['path']
    C=join(10,get(initial,10,4,210),get(ingredients,10,3,120))
    E=join(11,get(ingredients,11,5,462),C)
    _,G=embed(3,one_hot_cycle(3),on=2,off=5)
    H=join(10,get(ingredients,10,4,209),G)
    _,I=embed(11,complement(11,H),off=1)
    final=join(12,I,E)
    saved=json.loads((R/'composed_cycles.json').read_text())
    require(final==saved['final_1000']['path'],'Final composition differs from regenerated result')
    require(capacity(12)==792<1000<=capacity(13),'Wrong minimum-size lower bound')
    report['exact_1000_minimum']=check_path(saved['final_1000'])
    for name in ('counter_1000_13_degree6','counter_1000_13_saturated'):
        m=json.loads((R/(name+'.json')).read_text())
        require(m==model(13,final,'saturated' in name),'Stored physical design does not match compiler')
        check_machine(m)
    oldtrace=json.loads((R/'counter_1000_exact_trace.json').read_text())
    trace_model=model(13,final,True)
    newtrace=[pulse(trace_model,s) for s in final[::2]]
    require(oldtrace==newtrace,'Stored event trace failed independent replay')
    for row in initial.values():check_path(row)
    lifted=[]
    bases=[(3,one_hot_cycle(3)),(4,one_hot_cycle(4))]
    for n in (5,6,7):
        data=json.loads((R/f'spectrum_n{n}.json').read_text())
        bases.append((n,data[str(capacity(n))]['path']))
    for n,p in bases:
        Q=len(p)//2
        for q in range(3,2*Q+2):
            new=lift(n,p,q);r=check_machine(model(n+2,new))
            lifted.append({'base_n':n,'base_q':Q,'q':q,'trials':r['trials']})
    p=get(initial,10,4,210)
    for q in (3,4,419,420,421):
        r=check_machine(model(12,lift(10,p,q)))
        lifted.append({'base_n':10,'base_q':210,'q':q,'trials':r['trials']})
    report['two_bit_lift_checks']=lifted
    audits=[]
    for n in range(1,8):audits.append(full_audit(reset_machine(n)))
    for d in range(1,11):audits.append(full_audit(broom_machine(d)))
    for q in (3,4,5,7,10):
        for sat in (False,True):audits.append(full_audit(cycle_model(q,sat)))
    report['full_configuration_audits']=audits
    examples={'unary_merging':one_hot([1,2,0,1,3,4,6]),
              'amplitude_gated':amplitude_compile([[1,1,1],[1,2,2],[2,2,0]]),
              'reset_35_states':reset_machine(11),'broom_35_states':broom_machine(33)}
    examples['reset_35_states']['codes']=examples['reset_35_states']['codes'][:35]
    examples['reset_35_states']['f']=[0]*35
    for name,m in examples.items():
        check_machine(m);(R/(name+'.json')).write_text(json.dumps(m,indent=2)+'\n')
    report['elapsed_seconds']=time.monotonic()-start
    (R/'verification_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: finite spectra, generic lifting, composition, 1,000-cycle, and full-state audits',flush=True)
    print('ALL EXACT CHECKS PASSED',round(report['elapsed_seconds'],2),'seconds',flush=True)
if __name__=='__main__':main()
