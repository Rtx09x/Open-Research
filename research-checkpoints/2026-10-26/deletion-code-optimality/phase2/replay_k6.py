#!/usr/bin/env python3
"""Hash-bound reassembly and isolated replay of the complete seven-class proof."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,zipfile,io
HERE=Path(__file__).resolve().parent
if not __debug__:raise SystemExit('Assertions must remain enabled.')
def reconstruct():
 root=HERE/'certificate_bundle_k6';m=json.loads((root/'manifest.json').read_text());parts=[]
 for row in m['parts']:
  p=root/row['file'];b=p.read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['file'];parts.append(b)
 raw=b''.join(parts);assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']=='d3fd5337d50c5ec13bfd672a0169c175aef03c2133efeabd709c19ede8aad8b4'
 return raw

def extract(raw,target):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for info in z.infolist():
   p=PurePosixPath(info.filename);assert not p.is_absolute() and '..' not in p.parts and not info.is_dir()
   assert ((info.external_attr>>16)&0o170000)!=0o120000,'symlink not allowed'
   dst=target/str(p);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(z.read(info))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--independent',action='store_true');ap.add_argument('--negative',action='store_true');a=ap.parse_args();raw=reconstruct()
 with tempfile.TemporaryDirectory(prefix='deletion-k6-proof-') as tmp:
  out=Path(tmp);extract(raw,out)
  cmd=[sys.executable,'-I','-S',str(out/'scripts/verify_syndrome_supports.py'),'--k','6']
  if a.negative:
   (out/'evidence/syndrome_k6_mixed/0000.json.gz').unlink();p=subprocess.run(cmd,cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert p.returncode!=0 and 'AssertionError' in p.stdout and 'missing_certificate' in p.stdout;print('PASS: missing canonical support rejected.');return
  subprocess.run(cmd,cwd=out,check=True)
  result=json.loads((out/'evidence/syndrome_k6_mixed_verification.json').read_text());assert result['complete'] and result['certificates_checked']==868 and result['all_supports']==1716
  if a.independent:
   src=HERE.parents[1]/'advisor/phase3/check_deletion_six_supports.py';p=out/'independent/check.py';p.parent.mkdir();shutil.copy2(src,p)
   subprocess.run([sys.executable,'-I','-S',str(p),str(out/'evidence/syndrome_k6_mixed')],cwd=out,check=True)
 print('PASS: exact original ZIP restored, complete seven-class theorem replayed; global optimum remains316–320.')
if __name__=='__main__':main()
