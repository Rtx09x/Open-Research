#!/usr/bin/env python3
"""Extract exact numerical AH facts from the primary HTML; no worker/advisor input."""
from pathlib import Path
from fractions import Fraction as F
from html.parser import HTMLParser
import re,json,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('source_html',type=Path);ap.add_argument('output_json',type=Path);args=ap.parse_args();source_path=args.source_html
class Tables(HTMLParser):
 def __init__(self):super().__init__();self.rows={};self.row=None;self.cell=None;self.math=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='tr':self.row=[a.get('id',''),[]]
  if tag=='td' and self.row:self.cell=[]
  if tag=='math':
   self.math+=1
   if self.cell is not None:self.cell.append(a.get('alttext',''))
 def handle_endtag(self,t):
  if t=='math':self.math-=1
  if t=='td' and self.row:self.row[1].append(''.join(self.cell).strip());self.cell=None
  if t=='tr' and self.row:self.rows[self.row[0]]=self.row[1];self.row=None
 def handle_data(self,x):
  if self.cell is not None and not self.math:self.cell.append(x)
source=source_path.read_text(); parser=Tables();parser.feed(source)
def number(s):
 a=re.findall(r'\\frac\{(-?\d+)\}\{(\d+)\}',s)
 if a:return F(*map(int,a[0]))
 if s.startswith('A_'):s=s.rsplit('=',1)[-1]
 return F(s.split('=')[0].strip())
def endpoints(s):return tuple(F(int(a),int(b)) for a,b in re.findall(r'\\frac\{(-?\d+)\}\{(\d+)\}',s))
C={}
for rid,row in parser.rows.items():
 if not rid.startswith('A1.T1.1.') or not row[0].isdigit() or int(row[0])==1:continue
 j=int(row[0])
 if j not in C:C[j]=[number(row[1]),number(row[2]),{}]
 C[j][2][number(row[3])]=number(row[4])
# Appendix A's exact parametric large-class row, checked present literally.
assert r'\frac{22145926}{78181827}' in source and r'\frac{56035901}{78181827}' in source
assert r'0.35-\frac{j-5}{9600}' in source
for j in range(6,166):C[j]=[F(7,20)-F(j-5,9600),F(7,20)-F(j-6,9600),{F(1):F(22145926,78181827),F(2):F(56035901,78181827)}]
assert set(C)==set(range(2,213))
S={}
for rid,row in parser.rows.items():
 if rid.startswith('A2.T2.1.') and len(row)==4:
  ep=endpoints(row[1])
  if len(ep)==2:S[ep]=(None,None,number(row[2]))
 if rid.startswith('A2.T3.1.') and len(row)==5:
  ep=endpoints(row[0])
  if len(ep)==2:S[ep]=tuple(map(number,row[1:4]))
assert r'w=\frac{413913}{524288}' in source and 'w=0' in source

assert r'\frac{10060574276093395247}{6374352691333693440}' in source
facts={'schema':'AH-independent-primary-numerical-facts-v1',
 'source':{'url':'https://arxiv.org/html/1707.01728v1','sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'audit_date':'2026-10-25','sections':'Appendix A class parameters including parametric classes 6..165; Appendix B u,v,w tables and special ranges','extraction':'standalone HTMLParser; only mathematical numerical facts retained'},
 'original_exact_bound':'10060574276093395247/6374352691333693440',
 'classes':{str(j):{'lower':str(lo),'upper':str(hi),'containers':[[str(i),str(alpha)]for i,alpha in A.items()]} for j,(lo,hi,A) in sorted(C.items())},
 'weight_intervals':[{'lower':str(lo),'upper':str(hi),'u':str(u)if u is not None else None,'v':str(v)if v is not None else None,'w':str(w)} for (lo,hi),(u,v,w) in sorted(S.items())],
 'special_weight_intervals':[{'lower':'0','upper':'1/6','w':'0'},{'lower':'3/10','upper':'1/3','w':'413913/524288'}]}
for lo,hi,A in C.values():assert sum(A.values())==1 and all(a>0 for a in A.values())
args.output_json.write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps({'status':'EXTRACTED','classes':len(C),'explicit_weight_intervals':len(S),'source_sha256':facts['source']['sha256'],'output':str(args.output_json)},indent=2))
