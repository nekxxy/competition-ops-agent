"""Offline CLI: python3 replay_response.py SOURCE.txt RESPONSE.json"""
import json,sys
from pathlib import Path
from ops.replay_response import validate_response
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python3 replay_response.py SOURCE.txt RESPONSE.json')
    source,response=map(Path,sys.argv[1:])
    if source.stat().st_size>200000 or response.stat().st_size>200000:raise SystemExit('Maximum 200 KB per input')
    print(json.dumps(validate_response(source.read_text(),json.loads(response.read_text())),indent=2))
