"""Offline public-text bundle import. Never follows links or runs source code."""
import json
import hashlib
from .core import EvidenceStore
from .extract import extract_explicit
from .planning import review_plan
from .qualifiers import annotate_claims

MAX_BYTES=200_000

def validate_bundle(raw):
    if len(raw.encode())>MAX_BYTES:raise ValueError('Bundle exceeds 200 KB')
    b=json.loads(raw)
    if not isinstance(b,dict) or set(b)!={'title','public_data_confirmed','before','after'}:raise ValueError('Invalid bundle fields')
    if b['public_data_confirmed'] is not True:raise ValueError('Only public or synthetic input is permitted')
    if not isinstance(b['title'],str) or not 1<=len(b['title'])<=200:raise ValueError('Invalid title')
    sandbox=EvidenceStore()
    try:
        for k in ['before','after']:
            version=b[k]
            if not isinstance(version,dict) or set(version) not in ({'url','text','claims'},{'url','text'}):raise ValueError('Invalid source version')
            if not isinstance(version['text'],str) or not version['text'].strip():raise ValueError('Empty source')
            if 'claims' not in version:version['claims']=extract_explicit(version['text'])
            if not isinstance(version['claims'],list) or len(version['claims'])>50:raise ValueError('Maximum 50 claims per version')
            sid=sandbox.snapshot(version['url'],version['text'])
            for c in version['claims']:
                if not isinstance(c,dict) or set(c)!={'field','value','quote'}:raise ValueError('Invalid claim fields')
                sandbox.claim(sid,**c)
    finally:sandbox.db.close()
    return b

def import_bundle(store,raw):
    # Complete validation occurs before any persistent mutation.
    b=validate_bundle(raw)
    with store.atomic():
        return _import_validated(store,b)

def _import_validated(store,b):
    # An imported snapshot's extraction set cannot silently gain/lose claims.
    # A new extraction revision needs an explicit future revision mechanism.
    staged=[]
    for key in ['before','after']:
        v=b[key]
        sid=hashlib.sha256((v['url']+'\0'+v['text']).encode()).hexdigest()
        triples=sorted({(c['field'],c['value'],c['quote']) for c in v['claims']})
        digest=hashlib.sha256(json.dumps(triples).encode()).hexdigest()
        prior=store.db.execute('SELECT digest FROM extraction_sets WHERE source_id=?',(sid,)).fetchone()
        existing={(c['field'],c['value'],c['quote']) for c in store.claims(sid)}
        if (prior and prior['digest']!=digest) or (existing and existing!=set(triples)):
            raise ValueError('Existing snapshot has a different extraction set; do not silently replace evidence')
        if any(s==sid and d!=digest for s,d in staged):
            raise ValueError('Identical source text has conflicting extraction sets')
        staged.append((sid,digest))
    ids=[]
    for key in ['before','after']:
        v=b[key];sid=store.snapshot(v['url'],v['text']);ids.append(sid)
        # Re-importing a content-addressed snapshot does not duplicate claims.
        existing={(r['field'],r['value'],r['quote']) for r in store.claims(sid)}
        for c in v['claims']:
            if (c['field'],c['value'],c['quote']) not in existing:
                store.claim(sid,**c)
                existing.add((c['field'],c['value'],c['quote']))
    for sid,digest in staged:store.db.execute('INSERT OR IGNORE INTO extraction_sets VALUES(?,?)',(sid,digest))
    claims=store.claims(ids[1]);readiness=store.readiness(ids[1])
    plan=review_plan(claims,readiness)
    return {'plan':plan,'title':b['title'],'mode':'LOCAL PUBLIC-TEXT IMPORT','live_meta_inference':False,'before_id':ids[0],'after_id':ids[1],'sources':{k:store.source(sid) for k,sid in zip(['before','after'],ids)},'reviews':store.reviews(ids[1]),'changes':store.diff(*ids),'claims':annotate_claims(store.claims(ids[1])),'readiness':store.readiness(ids[1]),'note':'Claims from explicit offline parsing or user-supplied quotes. No remote verification or Meta inference.'}
