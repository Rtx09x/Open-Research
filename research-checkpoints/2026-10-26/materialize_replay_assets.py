#!/usr/bin/env python3
"""Reassemble hash-bound mathematical data only inside an explicit disposable copy."""
from pathlib import Path
import hashlib,json,argparse

def materialize(root):
 root=Path(root).resolve()
 p=root/'replay-assets/manifest.json'
 if not p.exists():return
 for item in json.loads(p.read_text())['assets']:
  out=(root/item['target']).resolve();assert out.is_relative_to(root),item['target'];chunks=[]
  for part in item['parts']:
   src=(root/part['path']).resolve();assert src.is_relative_to(root);b=src.read_bytes();assert len(b)==part['bytes'] and hashlib.sha256(b).hexdigest()==part['sha256'],part['path'];chunks.append(b)
  b=b''.join(chunks);assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['target'];out.parent.mkdir(parents=True,exist_ok=True)
  if out.exists():assert out.read_bytes()==b,'Refusing to overwrite a different existing file'
  else:out.write_bytes(b)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();materialize(a.root);print('PASS: every asset reassembled with exact SHA-256.')
