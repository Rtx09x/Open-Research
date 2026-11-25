"""Rebuild the 13-switch 1,000-cycle and save its exact component witnesses."""
from pathlib import Path
import json
from cycle_operations import *
from memory import check_machine,pulse
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'

def lookup(data,n,k,q):
    matches=[r for r in data.values() if (r['n'],r['k'],r['q'])==(n,k,q)]
    require(len(matches)==1,'Missing or ambiguous ingredient')
    p=matches[0]['path'];validate_cycle(n,p);return p

def main():
    original=json.loads((R/'large_cycle_witnesses.json').read_text())
    ingredients=json.loads((R/'composition_ingredients.json').read_text())
    A=lookup(original,10,4,210)
    B=lookup(ingredients,10,3,120)
    C=join(10,A,B)  # 11,4,329
    D=lookup(ingredients,11,5,462)
    E=join(11,D,C)  # 12,5,790
    F=lookup(ingredients,10,4,209)
    n,G=embed(3,one_hot_cycle(3),on=2,off=5)
    require(n==10,'Embedding dimension mismatch')
    H=join(10,F,G)  # 11,4,211
    _,I=embed(11,complement(11,H),off=1)  # 12,6,211
    J=join(12,I,E)  # 13,6,1000
    steps={'C_329':(11,C),'E_790':(12,E),'G_3':(10,G),'H_211':(11,H),
           'I_211':(12,I),'final_1000':(13,J)}
    out={}
    for name,(n,p) in steps.items():
        k,q=validate_cycle(n,p)
        out[name]={'n':n,'k':k,'q':q,'path':p}
    (R/'composed_cycles.json').write_text(json.dumps(out,indent=2)+'\n')
    for sat in (False,True):
        m=model(13,J,sat)
        report=check_machine(m)
        name='counter_1000_13_saturated' if sat else 'counter_1000_13_degree6'
        (R/(name+'.json')).write_text(json.dumps(m,indent=2)+'\n')
        print(name,report,flush=True)
    m=model(13,J,True)
    trace=[pulse(m,a) for a in m['codes']]
    (R/'counter_1000_exact_trace.json').write_text(json.dumps(trace,indent=2)+'\n')
    # Generic lifting applied to a full seven-bit middle-level cycle.
    spec=json.loads((R/'spectrum_n7.json').read_text())
    base=spec['35']['path']
    for q in range(3,72):
        p=lift(7,base,q)
        check_machine(model(9,p,True))
    print('PASS: all lifted periods 3..71 on nine bits',flush=True)
if __name__=='__main__':main()
