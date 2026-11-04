"""Build importable quoted evidence from saved envelopes, never calls a model."""
import json
from .replay_response import validate_response
from .importer import validate_bundle

def saved_response_bundle(title,before,after):
    versions={}
    for label,v in [('before',before),('after',after)]:
        if not isinstance(v,dict) or set(v)!={'url','text','response'}:raise ValueError('Expected URL, source text and saved response')
        result=validate_response(v['text'],v['response'])
        versions[label]={'url':v['url'],'text':v['text'],'claims':result['claims']}
    b={'title':title,'public_data_confirmed':True,**versions}
    validate_bundle(json.dumps(b))
    return {'bundle':b,'mode':'OFFLINE SAVED RESPONSE BRIDGE','network_calls':0,'remote_authorship_verified':False,'warning':'Quote validation and an importable bundle do not authenticate a provider call. UI remains LOCAL PUBLIC-TEXT IMPORT, not live inference. Supply public or synthetic text only.'}
