#!/usr/bin/env python3
"""Portable independent replay of a frozen parent5 or parent11 proof bundle.

Usage: python -I -S verify.py /path/to/parent{5,11}_exclusion_frozen [--output result.json]
No precomputed PASS result is trusted: all global/required/face ancestors are
rerun in a fresh temporary directory before the recursive proof checker.
The sibling checker implementations are advisor code, not worker imports.
"""
import argparse,json,hashlib,tempfile,subprocess,sys
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')
ap=argparse.ArgumentParser();ap.add_argument('bundle',type=Path);ap.add_argument('--output',type=Path)
a=ap.parse_args();bundle=a.bundle.resolve();here=Path(__file__).resolve().parent
digest=hashlib.sha256((bundle/'MANIFEST.json').read_bytes()).hexdigest()
kind={
'1c9e09ee5eaf3a479b38de7760c53a1774e3e97779f0846c7f0e81d991a4757c':5,
'75dfbeb05aa15b14a3e6f26b33b7ef94d7ca67c5339216246cc9fddb34c162e1':11}[digest]
old='/workspace/shared/research-active/deletion-code-optimality/continuation/evidence/'
substitutions={
old+'required_receivers320':str(bundle/'evidence/required_receivers320'),
old+'dual_slack_gate519':str(bundle/'evidence/dual_slack_gate519_frozen'),
old+'dual_slack_gate263_771_frozen':str(bundle/'evidence/dual_slack_gate263_771_frozen'),
old+f'parent{kind}_exclusion_frozen':str(bundle)}
names=['check_deletion_cg_independent.py','check_deletion_forced_receivers_independent.py',
       f'check_deletion_parent{kind}_independent.py']
if kind==5:names+=['check_deletion_forced_face_independent.py','check_deletion_forced_face263_771_independent.py']
with tempfile.TemporaryDirectory(prefix='independent-deletion-proof-') as tmp:
    t=Path(tmp)
    for name in names:
        src=(here/name).read_text()
        for before,after in substitutions.items():src=src.replace(repr(before),repr(after))
        # The supplied bundle may itself live under the original evidence
        # parent; that prefix alone is therefore not an unrelocated path.
        (t/name).write_text(src)
    steps=['check_deletion_forced_receivers_independent.py']
    if kind==5:steps+=['check_deletion_forced_face_independent.py','check_deletion_forced_face263_771_independent.py']
    steps+=[f'check_deletion_parent{kind}_independent.py']
    for name in steps:
        subprocess.run([sys.executable,'-I','-S',str(t/name)],cwd=t,check=True,
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    outputs={p.name:json.loads(p.read_text()) for p in t.glob('*.json')}
    result={'status':'PASS','parent':kind,'bundle_manifest_sha256':digest,
            'ancestors_recomputed':True,'steps':steps,'results':outputs,
            'scope':f'Normalized size320 code cannot contain word{kind}; not global319.'}
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
