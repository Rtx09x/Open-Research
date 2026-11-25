"""Replay all stored exact LP certificates and certify the small-map classification.

No numerical solver is imported. Fresh geometry enumeration checks the coverage
of every smaller dimension; all fixed-state excursion options are included.
"""
from pathlib import Path
from collections import Counter
import json,time
from fractions import Fraction
from synthesis import Problem,phase_options,verify_certificate
from encoding_search import encodings,unrestricted_minimum,isotype
from independent import geometry
from validate_model import validate
R=Path(__file__).resolve().parents[1]/'results'

def walk(value):
    if isinstance(value,dict):
        if 'spec' in value and 'fingerprint' in value and 'status' in value:
            yield value
        else:
            for v in value.values():yield from walk(v)
    elif isinstance(value,list):
        for v in value:yield from walk(v)

def main():
    start=time.monotonic();certificates={};unresolved=[];occurrences=0
    for path in sorted(R.glob('*.json')):
        for c in walk(json.loads(path.read_text())):
            if c['status']=='unresolved':unresolved.append({'file':path.name,'fingerprint':c['fingerprint']});continue
            # Verify every copy. Deduplication is only for reporting.
            verify_certificate(c);occurrences+=1
            certificates[(c['fingerprint'],c['status'])]=c
    small=json.loads((R/'affine_minima_through6.json').read_text())['records']
    seven=json.loads((R/'unary_seven_extension.json').read_text())['records']
    all_minima=[{'f':x['f'],'geometry_minimum':x['unrestricted_minimum'],'affine':x} for x in small]
    all_minima += [{'f':x['f'],'geometry_minimum':x['geometry']['minimum'],'affine':x['affine']}
                   for x in seven if x['affine'] is not None]
    covered_systems=covered_codes=0;differences=[];returning_fixed_witnesses=0
    for rec in all_minima:
        f=rec['f'];a=rec['affine'];assert a['status']=='exact' and not a['unresolved']
        fresh=unrestricted_minimum(f);assert fresh['minimum']==rec['geometry_minimum']
        w=a['witness'];verify_certificate(w)
        assert w['spec']['n']==a['minimum'] and w['spec']['f']==f
        if w['spec']['fixed_additions']:returning_fixed_witnesses+=1
        lower={c['fingerprint']:c for c in a['rejected']}
        for n in range((len(f)-1).bit_length(),a['minimum']):
            for codes in encodings(f,n):
                covered_codes+=1
                for phase in phase_options(codes,f,n):
                    p=Problem(codes,f,n,min(1,max(0,n-1)),fixed_additions=phase)
                    assert p.fingerprint in lower
                    assert lower[p.fingerprint]['status']=='infeasible'
                    covered_systems+=1
        if a['minimum']!=rec['geometry_minimum']:
            differences.append({'f':f,'unrestricted':rec['geometry_minimum'],'affine':a['minimum']})
    assert len(all_minima)==326 and len(differences)==1
    assert differences[0]['f']==[0,0,0,1,4,5,6]
    # Explicit final models, including the uniform-sign constructions.
    names=['seven_state_three_switch_quadratic.json','seven_state_four_switch_affine.json',
           'seven_state_five_switch_two_term.json','sparse_100_counter.json']
    names += [f'reset37_11bits_degree{d}.json' for d in (1,2,3,6)]
    names += [v['file'] for v in json.loads((R/'improved_cycle_constructions.json').read_text())]
    models=[{'file':name,**validate(json.loads((R/name).read_text()))} for name in names]
    result={'certificate_copies_verified':occurrences,'distinct_certified_systems':len(certificates),
            'distinct_statuses':dict(Counter(k[1] for k in certificates)),
            'unresolved_discovery_proposals':unresolved,'feasible_small_types_classified':len(all_minima),
            'fixed_returning_excursion_witnesses':returning_fixed_witnesses,
            'lower_dimension_codes_covered':covered_codes,'lower_dimension_phase_systems_covered':covered_systems,
            'interaction_order_separations_through_seven':differences,
            'explicit_final_models':models,'seconds':time.monotonic()-start}
    (R/'stored_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
