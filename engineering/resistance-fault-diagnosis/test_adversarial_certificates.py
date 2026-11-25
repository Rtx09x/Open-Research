"""Reject forged lower certificates even when electrical values are correct."""
from fractions import Fraction as F
import copy,json,subprocess,sys
from verify import check,electrical_matrix

def triangle():
    return {'n':3,'edges':[(0,1),(1,2),(0,2)],'queries':[(0,1),(1,2),(0,1)],
      'matrix':[['2','1','1'],['1','2','1'],['2','1','1']], 'adaptive_depth':2,
      'tree':{'query':0,'children':{'2':{'edge':0},'1':{'query':1,'children':{'2':{'edge':1},'1':{'edge':2}}}}},
      'nonadaptive_queries':[0,1],'nonadaptive_depth':2,
      'nonadaptive_dual':[[0,1,'0'],[0,2,'1'],[1,2,'1']],
      'lower_certificate':{'arity':2,'root':'r','nodes':{'r':{'candidates':[0,1,2],'budget':1,'reason':'capacity'}}},
      'family':'triangle','sizes':[3]}

valid=triangle();assert check(valid,electrical=True)['static_lower']==2
attacks=[]
x=triangle();x['nonadaptive_queries']=[0,1,2];x['nonadaptive_depth']=3;x['nonadaptive_dual']=[[0,1,'-1'],[0,2,'2'],[1,2,'2']];attacks.append(('signed dual inflates optimum 2 to 3',x))
x=triangle();x['nonadaptive_queries']=[0,1,2];x['nonadaptive_depth']=3;x['nonadaptive_dual']=[[0,0,'3']];attacks.append(('self-pair dual inflates optimum',x))
x=triangle();x['nonadaptive_dual']=[[-1,1,'1'],[0,2,'1']];attacks.append(('negative fault index',x))
x=triangle();x['adaptive_depth']=3;x['theta_lower']={'paths':[[0,0,0]]};attacks.append(('duplicate lower subset inflates adaptive optimum',x))
x=triangle();x['matrix'][0].append('2');attacks.append(('irregular response matrix',x))
for name,x in attacks:
    try:check(x,electrical=True)
    except (AssertionError,IndexError):pass
    else:raise AssertionError('Forgery accepted: '+name)
assert electrical_matrix(2,[(0,1)]*3,[(0,1)],[F(1),F(2),F(3)]) == [['6/5','3/4','2/3']]
code='from verify import check\ntry:check({})\nexcept RuntimeError:pass\nelse:raise AssertionError("-O accepted")'
r=subprocess.run([sys.executable,'-O','-c',code],capture_output=True,text=True)
assert r.returncode==0,r.stderr
print(json.dumps({'valid_certificate':'passed','forged_certificates_rejected':[name for name,x in attacks],'parallel_determinant_oracle':'fixed','optimized_interpreter':'rejected'}))
