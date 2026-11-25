#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,tarfile,tempfile,subprocess,sys
if not __debug__:raise SystemExit('Assertions required')
H=Path(__file__).resolve().parent;inv=json.loads((H/'archive_inventory.json').read_text());arc=H/inv['archive'];raw=arc.read_bytes();assert len(raw)==inv['bytes']and hashlib.sha256(raw).hexdigest()==inv['sha256'];expected={r['path']:r for r in inv['members']}
with tempfile.TemporaryDirectory(prefix='root-exclusion-proof-')as td:
 root=Path(td)
 with tarfile.open(arc,'r:xz')as t:
  members=t.getmembers();assert len(members)==len(expected)and len({m.name for m in members})==len(members)
  for m in members:
   p=(root/m.name).resolve();assert m.isfile()and p.is_relative_to(root)and m.name in expected;r=expected[m.name];b=t.extractfile(m).read();assert len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for kind in [5,11]:
  p=root/f'parent{kind}_exclusion_frozen';assert hashlib.sha256((p/'MANIFEST.json').read_bytes()).hexdigest()==inv['bundle_manifests'][p.name]
  subprocess.run([sys.executable,'-I','-S','verify.py','--negative-controls'],cwd=p,check=True)
  subprocess.run([sys.executable,'-I','-S',str(H/'independent/verify.py'),str(p)],check=True)
print('PASS: both frozen primary and independently reconstructed root-case proofs, including corruption controls.')
