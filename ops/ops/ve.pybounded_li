"""Fail-closed one-shot Standard transport. No implicit authorization or retries.

The caller supplies an approved INR reservation, not an invented FX guarantee.
Source-priced worst case uses full model context plus bounded completion.
Private ledgers, key paths and raw responses are never source deliverables.
"""
import datetime,hashlib,json,os,urllib.request,urllib.error
from decimal import Decimal
from pathlib import Path
from .meta import MetaExtractor
from .run_evidence import digest
MAX_CONTEXT=1048576
MAX_OUTPUT=2048
MAX_USD=Decimal(MAX_CONTEXT)*Decimal('1.25')/1000000+Decimal(MAX_OUTPUT)*Decimal('4.25')/1000000

def validate_request(request):
    if request.get('model')!='muse-spark-1.3' or request.get('max_completion_tokens')!=2048:raise ValueError('Standard bounded model only')
    if set(request)!={'model','max_completion_tokens','messages','response_format'}:raise ValueError('Unapproved request fields')
    messages=request['messages']
    if len(messages)!=2 or messages[0]['role']!='system' or messages[1]['role']!='user':raise ValueError('Single source request only')
    source=json.loads(messages[1]['content'])
    if set(source)!={'untrusted_source_text'}:raise ValueError('Invalid source boundary')
    if request!=MetaExtractor().request(source['untrusted_source_text']):raise ValueError('Request changed from frozen adapter')
    return source['untrusted_source_text']

def execute_one(request,key_path,ledger_path,response_path,*,approval_reference,reservation_inr,total_budget_inr=1000,opener=None):
    validate_request(request)
    reservation=Decimal(str(reservation_inr));budget=Decimal(str(total_budget_inr))
    if not approval_reference or not 0<reservation<=budget or budget>1000:raise ValueError('Explicit bounded authority required')
    ledger_path,response_path=Path(ledger_path),Path(response_path)
    if ledger_path.exists() or response_path.exists():raise ValueError('Existing attempt: inspect before any new request')
    ledger_path.parent.mkdir(parents=True,exist_ok=True);response_path.parent.mkdir(parents=True,exist_ok=True)
    record={'state':'reserved_before_network','attempts':0,'automatic_retries':0,'approval_reference':approval_reference,'reserved_inr':str(reservation),'total_budget_inr':str(budget),'source_priced_maximum_usd':str(MAX_USD),'inr_settlement_verified':False,'request_sha256':digest(request),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    fd=os.open(ledger_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:json.dump(record,f,indent=2)
    # One read at execution time; never log the secret or outgoing headers.
    key=Path(key_path).read_text().strip()
    if not key:raise ValueError('Empty credential')
    req=urllib.request.Request(MetaExtractor.endpoint,data=json.dumps(request).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    record.update(state='attempted_result_unknown',attempts=1)
    ledger_path.write_text(json.dumps(record,indent=2))
    try:
        with (opener or urllib.request.urlopen)(req,timeout=180) as response:
            body=response.read(200001)
            if len(body)>200000:raise ValueError('Oversized response, reservation retained')
            data=json.loads(body)
        # Retain response on any complete HTTP success, even validation failure.
        fd=os.open(response_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:json.dump(data,f,indent=2)
        usage=data.get('usage',{})
        record.update(state='http_success_pending_validation',response_sha256=digest(data),usage=usage,completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    except Exception as e:
        # No exception body, request object, headers or credential in output.
        record.update(state='attempted_result_unknown',error_type=type(e).__name__)
        ledger_path.write_text(json.dumps(record,indent=2));raise RuntimeError('One attempt failed or unknown; reservation retained, no retry') from None
    ledger_path.write_text(json.dumps(record,indent=2))
    return record
