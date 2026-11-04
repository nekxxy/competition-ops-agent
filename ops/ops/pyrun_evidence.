"""Sanitize and bind a saved envelope to its source/request. No origin claims.

An actual authorized execution may use this to preserve evidence, but passing
validation is not proof a call happened. Never store keys or HTTP headers.
"""
import hashlib,json,datetime
from .meta import MetaExtractor
from .replay_response import validate_response

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def record_saved(source,response,captured_at):
 # Require explicit metadata unlike legacy fixture-shaped offline envelopes.
 if not isinstance(response,dict) or response.get('model')!=MetaExtractor.model:raise ValueError('Explicit Standard response model required')
 rid=response.get('id')
 if not isinstance(rid,str) or not 1<=len(rid)<=200:raise ValueError('Response ID required')
 try:ts=datetime.datetime.fromisoformat(captured_at)
 except (TypeError,ValueError):raise ValueError('Explicit UTC capture timestamp required')
 if ts.utcoffset()!=datetime.timedelta(0):raise ValueError('Explicit UTC capture timestamp required')
 usage=response.get('usage')
 fields={'prompt_tokens','completion_tokens','total_tokens'}
 if not isinstance(usage,dict) or not fields<=set(usage):raise ValueError('Token usage required')
 u={k:usage[k] for k in sorted(fields)}
 if any(type(n) is not int or n<0 for n in u.values()) or u['total_tokens']!=u['prompt_tokens']+u['completion_tokens']:raise ValueError('Invalid token usage')
 if u['completion_tokens']>2048:raise ValueError('Output exceeds bounded request')
 if not isinstance(response.get('choices'),list) or len(response['choices'])!=1 or not isinstance(response['choices'][0],dict) or response['choices'][0].get('finish_reason')!='stop':raise ValueError('Explicit complete response required')
 validated=validate_response(source,response)
 safe={'id':rid,'model':response['model'],'choices':[{'finish_reason':'stop','message':{'role':'assistant','content':response['choices'][0]['message']['content']}}],'usage':u}
 request=MetaExtractor().request(source)
 return {'format':'competition-ops-saved-evidence-v1','mode':'SAVED ENVELOPE, ORIGIN UNVERIFIED','remote_authorship_verified':False,'network_calls':0,'billing_authorization':False,'captured_at_claimed':captured_at,'timestamp_verified':False,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'request_sha256':digest(request),'response_sha256':digest(safe),'endpoint':MetaExtractor.endpoint,'request':request,'response':safe,'validated_claims':validated['claims'],'warning':'Caller-supplied timestamp, response ID and model string do not authenticate provider origin. Retain real execution proof separately. No credentials or headers retained.'}
