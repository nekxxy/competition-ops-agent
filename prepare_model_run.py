"""Prepare a bounded synthetic evaluation batch. Never loads keys or calls APIs."""
import hashlib,json,sys
from pathlib import Path
from ops.meta import MetaExtractor
ROOT=Path(__file__).resolve().parent
FROZEN='d4e8583addcc5616d11ea7bd3c52ff9a6743846333c3230aebe3bc5ef8e1fb64'

def prepare():
 raw=(ROOT/'fixtures/prose-evaluation-v1.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=FROZEN:raise ValueError('Frozen synthetic fixture changed')
 cases=json.loads(raw)['cases'];extractor=MetaExtractor()
 if len(cases)!=8:raise ValueError('Expected eight frozen cases')
 requests=[{'case_id':c['id'],'source_sha256':hashlib.sha256(c['text'].encode()).hexdigest(),'request':extractor.request(c['text'])} for c in cases]
 return {'mode':'PREPARATION ONLY','network_calls':0,'credentials_loaded':False,'billing_authorization':False,'fixture_sha256':FROZEN,'planned_calls':8,'maximum_completion_tokens_per_call':2048,'automatic_retries':0,'endpoint':extractor.endpoint,'model':extractor.model,'requests':requests,'warning':'This manifest neither enables a transport nor authorizes API usage. Verify applied credits and supported no-overage separately. Use synthetic input only.'}
if __name__=='__main__':print(json.dumps(prepare(),indent=2))
