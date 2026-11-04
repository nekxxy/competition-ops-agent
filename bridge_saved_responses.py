"""Offline saved-response bridge, not an API client or live-model demonstration.

Input JSON: {title,public_data_confirmed:true,before:{url,text,response},after:...}
Output wrapper contains the importable bundle and unverified-origin disclaimer.
"""
import json,sys
from pathlib import Path
from ops.response_bundle import saved_response_bundle
if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python3 bridge_saved_responses.py PUBLIC_INPUT.json')
 p=Path(sys.argv[1])
 if p.stat().st_size>500000:raise SystemExit('Maximum500KB')
 b=json.loads(p.read_text())
 if not isinstance(b,dict) or set(b)!={'title','public_data_confirmed','before','after'} or b['public_data_confirmed'] is not True:raise SystemExit('Explicit public/synthetic input confirmation required')
 print(json.dumps(saved_response_bundle(b['title'],b['before'],b['after']),indent=2))
