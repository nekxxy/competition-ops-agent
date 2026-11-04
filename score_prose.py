"""Score saved envelopes on the frozen authored prose set. Never calls a model.

Input: JSON object mapping case IDs to saved provider-shaped response objects.
A model string does not authenticate origin. Output is always offline/unverified.
"""
import hashlib,json,sys
from pathlib import Path
from ops.replay_response import validate_response
ROOT=Path(__file__).parent
FROZEN='d4e8583addcc5616d11ea7bd3c52ff9a6743846333c3230aebe3bc5ef8e1fb64'

def score(responses):
    raw=(ROOT/'fixtures/prose-evaluation-v1.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=FROZEN:raise ValueError('Frozen evaluation set changed')
    cases=json.loads(raw)['cases']
    if not isinstance(responses,dict) or set(responses)!={c['id'] for c in cases}:raise ValueError('Exactly the eight frozen case IDs required')
    rows=[];tp=fp=fn=exact=valid=0;abstention_total=correct_abstentions=conflict_cases=preserved_conflicts=0
    for c in cases:
        expected={(r['field'],r['value']) for r in c['expected']}
        abstention_total+=not expected
        expected_conflicts={f for f,v in expected if len({x for k,x in expected if k==f})>1}
        conflict_cases+=bool(expected_conflicts)
        try:
            validated=validate_response(c['text'],responses[c['id']]);actual={(r['field'],r['value']) for r in validated['claims']};valid+=1
            ok=actual==expected;correct_abstentions+=not expected and not actual;preserved_conflicts+=bool(expected_conflicts) and all({x for k,x in expected if k==f}<={x for k,x in actual if k==f} for f in expected_conflicts);exact+=ok;tp+=len(actual&expected);fp+=len(actual-expected);fn+=len(expected-actual)
            rows.append({'case_id':c['id'],'valid_envelope':True,'exact_field_value_match':ok,'missing':sorted(expected-actual),'extra':sorted(actual-expected)})
        except (ValueError,TypeError,RecursionError) as e:
            fn+=len(expected);rows.append({'case_id':c['id'],'valid_envelope':False,'exact_field_value_match':False,'error':str(e)})
    return {'mode':'OFFLINE SAVED-ENVELOPE SCORING','remote_authorship_verified':False,'live_meta_calls':0,'dataset_sha256':FROZEN,'valid_cases':valid,'exact_cases':exact,'total_cases':len(cases),'field_value_precision':tp/(tp+fp) if tp+fp else None,'field_value_recall':tp/(tp+fn) if tp+fn else None,'required_abstention_cases':abstention_total,'correct_abstentions':correct_abstentions,'multi_value_cases':conflict_cases,'preserved_multi_value_cases':preserved_conflicts,'field_value_tp':tp,'field_value_fp':fp,'field_value_fn':fn,'cases':rows,'limitations':['Developer-authored synthetic cases, not independent or representative','Exact gold wording is strict and can reject semantically equivalent wording','Envelope labels do not establish provider origin','Invalid response cases never count as correct abstentions','Multiple values can be complementary; preservation is measured, not semantic contradiction']}
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python3 score_prose.py RESPONSES.json')
    p=Path(sys.argv[1])
    if p.stat().st_size>1600000:raise SystemExit('Maximum 1.6 MB')
    print(json.dumps(score(json.loads(p.read_text())),indent=2))
