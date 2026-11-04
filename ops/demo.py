import json
from pathlib import Path
from .core import EvidenceStore,normalize_time
from .planning import review_plan
from .qualifiers import annotate_claims

def replay():
    f=json.loads((Path(__file__).parent.parent/'fixtures/replay.json').read_text())
    store=EvidenceStore()
    ids=[]
    for version in ['before','after']:
        sid=store.snapshot(f['url'],f[version])
        for field,value,quote in f['claims_'+version]: store.claim(sid,field,value,quote)
        ids.append(sid)
    return {'plan':review_plan(store.claims(ids[1]),store.readiness(ids[1])),'mode':'OFFLINE REPLAY','live_meta_inference':False,'fixture':f['label'],'source_url':f['url'],'before_id':ids[0],'after_id':ids[1],'sources':{k:store.source(sid) for k,sid in zip(['before','after'],ids)},'reviews':[],'changes':store.diff(*ids),'claims':annotate_claims(store.claims(ids[1])),'readiness':store.readiness(ids[1]),'local_deadline':normalize_time('2026-11-22T23:59:00+01:00','Asia/Kolkata'),'authority':'Review only. No terms acceptance, spending, messages or entries.'}
