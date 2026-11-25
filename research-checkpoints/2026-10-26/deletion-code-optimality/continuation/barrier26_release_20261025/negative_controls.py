import json,copy,tempfile,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;c=json.loads((R/'point.json').read_text());cases=[]
b=copy.deepcopy(c);b['numerator']-=1;cases.append(('wrong_total',b))
b=copy.deepcopy(c);b['values'][0]=b['scale']+1;cases.append(('invalid_word_bound',b))
b=copy.deepcopy(c);b['values'][1625]-=1;b['numerator']-=1;cases.append(('lost_selected_integrality',b))
b=copy.deepcopy(c);b['CG_nodes'][0]['parents'][0]={'clique':[0,4095]};cases.append(('invalid_CG_parent',b))
with tempfile.TemporaryDirectory() as t:
 for name,b in cases:
  f=Path(t)/(name+'.json');f.write_text(json.dumps(b));r=subprocess.run([sys.executable,'-I','-S',str(R/'verify.py'),str(f)],capture_output=True);assert r.returncode!=0,name
print(json.dumps({'passed':True,'rejected_mutations':[n for n,_ in cases]}))
