"""Deliberately corrupt independent certificates; every mutation must fail."""
import json,copy,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];good=json.loads((ROOT/'evidence/best_dual.json').read_text());checker=ROOT/'scripts/verify_cg_hierarchy.py';cases=[]
bad=copy.deepcopy(good);bad['numerator']-=1;cases.append(('wrong_numerator',bad))
bad=copy.deepcopy(good);bad['cliques']=[];bad['node_multipliers']=[];bad['orbit_upper']=[];bad['numerator']=0;cases.append(('uncovered_objective',bad))
bad=copy.deepcopy(good);bad['cliques'][0][0]=-1;cases.append(('negative_dual_weight',bad))
bad=copy.deepcopy(good);bad['nodes'][0]['divisor']=0;cases.append(('invalid_CG_divisor',bad))
bad=copy.deepcopy(good);bad['cliques'][0][1]=[0,4095];cases.append(('nonclique_geometry',bad))
with tempfile.TemporaryDirectory() as t:
 for name,data in cases:
  f=Path(t)/(name+'.json');f.write_text(json.dumps(data));r=subprocess.run([sys.executable,'-I','-S',str(checker),str(f)],capture_output=True,text=True);assert r.returncode!=0,name
print(json.dumps({'passed':True,'rejected_mutations':[n for n,_ in cases]}))
