"""Small authored-fixture parser regression check, not a model benchmark."""
import json
from pathlib import Path
from ops.extract import extract_explicit

def evaluate():
    cases=json.loads((Path(__file__).parent/'fixtures/evaluation.json').read_text())
    passed=0;tp=fp=fn=0;rows=[]
    for c in cases:
        actual={(r['field'],r['value']) for r in extract_explicit(c['text'])};expected={tuple(r) for r in c['expected']}
        exact=actual==expected;passed+=exact;tp+=len(actual&expected);fp+=len(actual-expected);fn+=len(expected-actual)
        rows.append({'name':c['name'],'exact_match':exact,'expected':sorted(expected),'actual':sorted(actual)})
    return {'scope':'Deterministic parser, 14 authored synthetic regression cases. Not a generalization or LLM accuracy benchmark.','live_meta_calls':0,'case_exact_match':f'{passed}/{len(cases)}','claim_true_positive':tp,'claim_false_positive':fp,'claim_false_negative':fn,'limitations':['Labeled hostile text is retained as quoted data, never followed','No semantic entailment or URL-authenticity evaluation','Natural-language dates intentionally omitted'],'cases':rows}
if __name__=='__main__':print(json.dumps(evaluate(),indent=2))
