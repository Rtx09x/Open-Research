#!/usr/bin/env python3
"""Verify frozen integration bytes; newly generated local result files are ignored."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'checkpoint_manifest.json').read_text())
for row in manifest['files']:
    raw=(root/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
print('PASS:',len(manifest['files']),'integrated files match the frozen SHA-256 manifest.')
