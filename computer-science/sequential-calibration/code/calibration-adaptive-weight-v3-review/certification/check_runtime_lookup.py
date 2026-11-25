#!/usr/bin/env python3
"""Compare actual exact-rational policy lookup with independent boundary rules."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json

root=Path(__file__).parent
source=root.parent/'theory'/'adaptive_policy.py'
spec=importlib.util.spec_from_file_location('audited_runtime_policy',source)
runtime=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
policy_path=root.parent/'theory'/'rational_q_policy.json'
policy=json.loads(policy_path.read_text())
table={s:sorted((Q(x['lo']),Q(x['hi']),Q(x['q'])) for x in policy['rows'] if x['segment']==s) for s in (1,2)}
count=0
for segment in (1,2):
    for i,(lo,hi,q) in enumerate(table[segment]):
        lower_q=table[segment][i-1][2] if i else (table[1][-1][2] if segment==2 else q)
        for x,expected in [(lo,lower_q),((lo+hi)/2,q),(hi,q)]:
            z=x if segment==1 else Q('14.8')*x
            actual=runtime.factor(z.numerator,z.denominator)
            assert actual==expected,(segment,i,str(x),str(actual),str(expected))
            count+=1
report={'all_checks_passed':True,'exact_lookups_checked':count,
        'scope':'Actual adaptive_policy.factor compared with independent first-closed-cell endpoint rules at every endpoint and midpoint.',
        'runtime_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'policy_sha256':hashlib.sha256(policy_path.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'results'/'runtime_lookup_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
