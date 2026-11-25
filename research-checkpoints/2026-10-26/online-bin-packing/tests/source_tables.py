"""Portable replay of independently parsed numerical source-table facts."""
"""Independent AH weight/pricing audit from primary HTML; stdlib only."""
from fractions import Fraction as F
from pathlib import Path
import re,json,math,time,html,hashlib
start=time.time();ROOT=Path(__file__).resolve().parents[1];facts=json.loads((ROOT/'tests/source_table_facts.json').read_text())
def table_rows(prefix):
 return facts["tables"][prefix]
def number(s):
 m=re.search(r'\\frac\{(-?\d+)\}\{(\d+)\}',s)
 if m:return F(int(m[1]),int(m[2]))
 return F(s.split('=')[-1] if s.startswith('A_') else s.split('=')[0])
classes={}
for row in table_rows('A1.T1.1')[2:]:
 j=int(row[0])
 if j==1:continue
 if j not in classes:classes[j]={'min':number(row[1]),'max':number(row[2]),'types':[]}
 classes[j]['types'].append((number(row[3]),number(row[4])))
for j in range(6,166):classes[j]={'min':F(7,20)-F(j-5,9600),'max':F(7,20)-F(j-6,9600),'types':[(F(1),F(22145926,78181827)),(F(2),F(56035901,78181827))]}
assert set(classes)==set(range(2,213))
for j,p in classes.items():assert sum(z for i,z in p['types'])==1
