"""Seeded independent sanity checks of necessity on arbitrary threshold tables.

Only closed sets on which all test pulses obey the budget are classified.
This finite randomized check is supplementary evidence, not a general proof.
"""
from pathlib import Path
import json,random
from memory import threshold,pulse,amplitude_certificate,code_certificate,require
ROOT=Path(__file__).resolve().parents[1]

def main():
    rng=random.Random(8102026);rows=[]
    for n in (3,4):
        D=8*(n+1);survivors=states_total=nonself=0
        for trial in range(1000):
            plus=[[0]*(1<<n) for _ in range(n)];minus=[[0]*(1<<n) for _ in range(n)]
            for i in range(n):
                for env in range(1<<n):
                    if env>>i&1:continue
                    p=rng.randint(2,12);d=rng.randint(-6,p-1)
                    plus[i][env]=D*p+i+1;minus[i][env]=D*d+i+1
            m={'kind':'raw','n':n,'scale':D,'low':0,'highs':[3*D,6*D,9*D],
               'plus':plus,'minus':minus}
            transitions={}
            for s in range(1<<n):
                try:outputs=[pulse(m,s,a)['final'] for a in range(3)]
                except ValueError:continue
                transitions[s]=outputs
            active=set(transitions)
            while True:
                nxt={s for s in active if all(t in active for t in transitions[s])}
                if nxt==active:break
                active=nxt
            if not active:continue
            codes=sorted(active);index={s:i for i,s in enumerate(codes)}
            table=[[index[t] for t in transitions[s]] for s in codes]
            cert=amplitude_certificate(table)
            code_certificate(codes,cert['f'],n)
            indegrees=[cert['f'].count(i) for i in range(len(codes))]
            for i,d in enumerate(indegrees):
                bound=1+(n+1)**2//4 if cert['f'][i]==i else (n-1)**2//4
                require(d<=bound,'Fan-in bound violated')
            survivors+=1;states_total+=len(codes)
            nonself+=sum(v!=i for i,row in enumerate(table) for v in row)
        rows.append({'n':n,'random_models':1000,'nonempty_closed_budgeted_sets':survivors,
                     'code_states_checked':states_total,'nonself_symbol_transitions':nonself})
    (ROOT/'results'/'adversarial_raw_report.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
