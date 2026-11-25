from pathlib import Path
from collections import Counter
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
ROOT=Path('/workspace/shared/research-active/deletion-code-optimality/continuation/evidence/required_receivers320')
sys.argv=['independent',str(ROOT/'global_dual.json')]
ns={'__file__':str(HERE/'check_deletion_cg_independent.py')};exec((HERE/'check_deletion_cg_independent.py').read_text(),ns)
d=ns['d'];c=json.loads((ROOT/'certificate.json').read_text());gap=d['numerator']-320*d['scale']
assert hashlib.sha256((ROOT/'global_dual.json').read_bytes()).hexdigest()==c['global_dual_sha256']
assert gap==c['gap_at_cardinality320'] and 0<gap<d['scale']
# Independently use literal one-character deletion to reconstruct each clique.
parents={}
for x in range(4096):
    word=format(x,'012b')
    for i in range(12):parents.setdefault(int(word[:i]+word[i+1:],2),set()).add(x)
def transform(word,n,g):
    s=format(word,'0%db'%n)
    if g&1:s=''.join('1' if b=='0' else '0' for b in s)
    if g&2:s=s[::-1]
    return int(s,2)
required=set();margins=[]
for rec in c['records']:
    y=rec['base_receiver'];mult=rec['multiplier']
    assert any(lam==mult and set(cl)==parents[y] for lam,cl in d['cliques'])
    assert mult>gap and rec['strict_margin']==mult-gap and rec['summed_rhs']==4
    coeff=Counter()
    assert {r['group_element'] for r in rec['transports']}==set(range(4)) and len(rec['transports'])==4
    for row in rec['transports']:
        g=row['group_element'];yy=transform(y,11,g);ps={transform(x,12,g) for x in parents[y]}
        assert yy==row['receiver'] and set(row['parents'])==parents[yy]==ps and len(ps)==13
        coeff.update(ps);required.add(yy)
    assert rec['summed_word_row']==[[w,coeff[w]] for w in sorted(coeff)]
    margins.append(mult-gap)
assert required==set(c['required_receivers']) and len(required)==16
for y in required:
    s=format(y,'011b');assert sum(a!=b for a,b in zip(s,s[1:]))==1 and 2<=s.count('1')<=9
out={'PASS':True,'independent_global_dual':True,'gap':gap,'scale':d['scale'],'required_receiver_count':16,'parents_per_receiver':13,'strict_multiplier_margins':margins,'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),'scope':'Every hypothetical320 code covers these16 outputs exactly once; not a global319 bound.'}
(HERE/'check_deletion_forced_receivers_independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
