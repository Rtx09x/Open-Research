"""Seven-state affine/quadratic memory separation and its analytic obstruction.

The four XOR inequalities cancel for affine thresholds. Geometry forces this
encoding (up to coordinate and fixed-state relabeling), so the obstruction does
not assume a conveniently chosen encoding or silent fixed states.
"""
from pathlib import Path
import json
from itertools import permutations
from independent import geometry
from resources import explicit_device
from validate_model import validate
from synthesis import verify_certificate
from complete_bands import finish
R=Path(__file__).resolve().parents[1]/'results'
F=[0,0,0,1,4,5,6]

def quadratic_model():
    D=32;W=10
    # a = bit 0, b = bit 1, c = bit 2; integers before adding eta_i.
    polys=[{0:4,2:-2,4:-2,6:4},{0:4,1:-2,4:2},{0:4,1:7,3:-7}]
    branches={}
    for key,down in [('up',False),('down',True)]:
        rows=[]
        for i,p in enumerate(polys):
            coeff={s:v*D for s,v in p.items()};coeff[0]+=(i+1)-(W*D if down else 0)
            rows.append([{'mask':s,'coefficient':v} for s,v in sorted(coeff.items()) if v])
        branches[key]=rows
    return {'kind':'explicit_polynomial','n':3,'scale':D,'low':0,'highs':[3*D],
            'codes':[3,1,2,4,0,6,7],'f':F,**branches,
            'common_shifts':True,'uniform_span':True,'degree':2,
            'global_avalanche_free_guarantee':False,'directed_monomial_support':7}


def five_bit_two_term_model():
    # Three processing bits x,y,z plus two independent fixed-state label bits.
    n=5;D=8*(n+1);W=6
    polys=[{0:2},{0:5,1:2},{0:2,2:2},{0:4},{0:4}]
    branch={}
    for key,down in [('up',False),('down',True)]:
        rows=[]
        for i,p in enumerate(polys):
            coeff={s:v*D for s,v in p.items()}
            coeff[0]+=(i+1)-(W*D if down else 0)
            rows.append([{'mask':s,'coefficient':v} for s,v in sorted(coeff.items()) if v])
        branch[key]=rows
    return {'kind':'explicit_polynomial','n':n,'scale':D,'low':0,'highs':[3*D],
            'codes':[5,1,4,2,13,21,29],'f':F,**branch,
            'common_shifts':True,'uniform_span':True,'degree':1,
            'global_avalanche_free_guarantee':True,'directed_monomial_support':2,
            'optimality_note':'Feasible five-bit two-term upper bound; no minimum at this resource point is claimed.'}

def check_forced_geometry():
    found=0
    # No symmetry or pruning: all 8P7 = 40,320 injective encodings.
    for codes in permutations(range(8),7):
        if not geometry(list(codes),F,3):continue
        A,B,C=codes[1],codes[2],codes[3]
        assert A.bit_count()==B.bit_count()==C.bit_count()==1
        assert A|B|C==7 and codes[0]==A|B
        assert set(codes[4:])=={0,B|C,7}
        assert A|C not in codes
        found+=1
    assert found==36
    # Affine feature vectors at the four environments: 00 + 11 - 10 - 01.
    residual=[1+1-1-1,0+1-1-0,0+1-0-1]
    assert residual==[0,0,0]
    return {'injective_encodings_examined':40320,'geometrically_valid':found,
            'xor_affine_feature_residual':residual}

if __name__=='__main__':
    model=quadratic_model();check=validate(model)
    (R/'seven_state_three_switch_quadratic.json').write_text(json.dumps(model,indent=2))
    source=json.loads((R/'seven_affine_110.json').read_text())
    assert source['status']=='feasible';verify_certificate(source)
    upper=finish(source);upper_check=validate(upper)
    (R/'seven_state_four_switch_affine.json').write_text(json.dumps(upper,indent=2))
    extra=five_bit_two_term_model();extra_check=validate(extra)
    (R/'seven_state_five_switch_two_term.json').write_text(json.dumps(extra,indent=2))
    report={'f':F,'affine_minimum':4,'quadratic_minimum':3,
            'quadratic_verification':check,'affine_verification':upper_check,
            'geometry':check_forced_geometry(),
            'three_bit_exact_minimum_directed_monomials':7,
            'five_bit_two_term_upper_verification':extra_check,
            'scope':'arbitrary directed signed affine branches in the lower bound; common shifts and uniform spans attain both upper bounds'}
    (R/'seven_state_separation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
