"""Validate an offline response envelope without asserting remote authorship."""
import hashlib,json
from .core import validate_claim
MODEL='muse-spark-1.3'

def validate_response(body,response):
    if not isinstance(body,str) or len(body.encode())>200000:raise ValueError('Invalid or oversized source')
    if not isinstance(response,dict) or not isinstance(response.get('choices'),list) or len(response['choices'])!=1:raise ValueError('Exactly one response choice required')
    if response.get('model',MODEL)!=MODEL:raise ValueError('Standard model only; unknown or Contributor model rejected')
    choice=response['choices'][0]
    if not isinstance(choice,dict) or choice.get('finish_reason','stop')!='stop':raise ValueError('Incomplete response')
    message=choice.get('message')
    if not isinstance(message,dict) or message.get('refusal'):raise ValueError('Model refusal or malformed message')
    content=message.get('content')
    if not isinstance(content,str) or len(content.encode())>200000:raise ValueError('Invalid or oversized content')
    result=json.loads(content)
    if not isinstance(result,dict) or set(result)!={'claims'} or not isinstance(result['claims'],list) or len(result['claims'])>50:raise ValueError('Invalid claims response')
    for c in result['claims']:
        if not isinstance(c,dict) or set(c)!={'field','value','quote'}:raise ValueError('Invalid claim fields')
        validate_claim(c['field'],c['value'],c['quote'],body)
    return {'mode':'SAVED RESPONSE REPLAY','live_meta_inference':False,'remote_authorship_verified':False,'response_sha256':hashlib.sha256(json.dumps(response,sort_keys=True).encode()).hexdigest(),'claims':result['claims'],'warning':'Envelope validated locally. A model label is not proof of a genuine provider call.'}
