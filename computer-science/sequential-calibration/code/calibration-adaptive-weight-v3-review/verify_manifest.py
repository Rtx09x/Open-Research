#!/usr/bin/env python3
"""Verify package and all nested hash records without writing files."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
def check(base,records):
    for r in records:
        p=(base/r['path']).resolve()
        assert p.is_relative_to(root), r['path']
        data=p.read_bytes()
        assert len(data)==r['bytes'], r['path']
        assert hashlib.sha256(data).hexdigest()==r['sha256'], r['path']
    return len(records)
m=json.loads((root/'MANIFEST.json').read_text())
count=check(root,m['files'])
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual=={r['path'] for r in m['files']}|{'MANIFEST.json'}
c=json.loads((root/'certification/MANIFEST.json').read_text())
count+=check(root/'certification',c['files']+c['audited_sibling_inputs'])
for name in ['V3_ADDENDUM_MANIFEST.json','external_erasure_audit.json']:
    count+=check(root,json.loads((root/'phase2/certification'/name).read_text())['files'])
print(f'PASS: {count} manifest/audit records; all package files accounted for.')
