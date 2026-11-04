"""Prepare, never publish, a source-only candidate from an explicit allowlist.

Operational plans/logs, local databases, credentials and evaluation outputs are
excluded. Inspect the generated manifest before any repository publication.
"""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES=['LICENSE','README.md','EVALUATION.md','server.py','evaluate.py','replay_response.py','score_prose.py','prepare_model_run.py','record_response_evidence.py','bridge_saved_responses.py','.gitignore']
DIRS=['ops','static','fixtures','tests','scripts']
EXTENSIONS={'.py','.json','.html'}

def candidates():
    files=[ROOT/n for n in NAMES]
    files += [p for d in DIRS for p in (ROOT/d).rglob('*') if p.is_file() and p.suffix in EXTENSIONS and '__pycache__' not in p.parts]
    return sorted(set(files))

def package(destination):
    manifest=[]
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for p in candidates():
            relative=p.relative_to(ROOT).as_posix();data=p.read_bytes()
            z.writestr(relative,data);manifest.append({'path':relative,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        z.writestr('SOURCE_MANIFEST.json',json.dumps(manifest,indent=2))
    return manifest
if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:raise SystemExit('Usage: python3 scripts/package_public.py OUTPUT.zip')
    print(json.dumps(package(sys.argv[1]),indent=2))
