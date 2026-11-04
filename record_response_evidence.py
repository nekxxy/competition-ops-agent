"""Offline saved-evidence recorder. No keys, HTTP or provider-origin guarantee."""
import json,sys
from pathlib import Path
from ops.run_evidence import record_saved
if __name__=='__main__':
 if len(sys.argv)!=4:raise SystemExit('Usage: python3 record_response_evidence.py SOURCE.txt RESPONSE.json UTC_TIMESTAMP')
 source,response=map(Path,sys.argv[1:3])
 if source.stat().st_size>200000 or response.stat().st_size>200000:raise SystemExit('Maximum 200KB per input')
 print(json.dumps(record_saved(source.read_text(),json.loads(response.read_text()),sys.argv[3]),indent=2))
