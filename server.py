"""Local-only evidence desk. No remote fetches or external actions."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import json,os
from pathlib import Path
from ops.demo import replay
from ops.core import EvidenceStore
from ops.importer import import_bundle,MAX_BYTES
ROOT=Path(__file__).parent
DB=os.environ.get('OPS_DB',str(ROOT/'local-state.sqlite'))
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,data,ctype='application/json'):
        b=data if isinstance(data,bytes) else json.dumps(data).encode()
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(b)));self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if self.path=='/api/recorded-pilot':
            try:
                fixture=json.loads((ROOT/'fixtures/meta-pilot01-recorded.json').read_text());store=EvidenceStore()
                try:result=import_bundle(store,json.dumps(fixture['bundle']))
                finally:store.db.close()
                result.update(mode='RECORDED META PILOT REPLAY',note=fixture['note'],recorded_meta={'response_id':fixture['response']['id'],'model':fixture['response']['model'],'captured_at':fixture['captured_at'],'usage':fixture['response']['usage']},reviews=[])
            except (OSError,ValueError,TypeError,KeyError,AttributeError):
                return self.reply(503,{'error':'Recorded pilot unavailable; no API call was made'})
            self.reply(200,result)
        elif self.path=='/api/demo':self.reply(200,replay())
        elif self.path=='/api/conflict-example':self.reply(200,json.loads((ROOT/'fixtures/conflict-example.json').read_text()))
        elif self.path=='/api/raw-example':self.reply(200,json.loads((ROOT/'fixtures/raw-source-example.json').read_text()))
        elif self.path=='/api/example':
            f=json.loads((ROOT/'fixtures/replay.json').read_text());self.reply(200,{'title':'Synthetic example','public_data_confirmed':True,**{k:{'url':f['url'],'text':f[k],'claims':[dict(zip(['field','value','quote'],c)) for c in f['claims_'+k]]} for k in ['before','after']}})
        elif self.path in ['/','/index.html']:self.reply(200,(ROOT/'static/index.html').read_bytes(),'text/html; charset=utf-8')
        else:self.reply(404,{'error':'Not found'})
    def do_POST(self):
        # Same-origin JSON plus a custom header blocks cross-site form attacks.
        host=self.headers.get('Host','')
        if host not in {'127.0.0.1:8765','localhost:8765'} or self.headers.get('Origin') not in {None,'http://'+host} or self.headers.get('X-Ops-Local')!='1' or self.headers.get('Content-Type')!='application/json':
            return self.reply(403,{'error':'Local same-origin JSON requests only'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=MAX_BYTES:raise ValueError('Request must be 1-200000 bytes')
            raw=self.rfile.read(length).decode();s=EvidenceStore(DB)
            try:
                if self.path=='/api/import':result=import_bundle(s,raw)
                elif self.path=='/api/review':
                    b=json.loads(raw)
                    if not isinstance(b,dict) or set(b)!={'source_id','decision','reviewer'}:raise ValueError('Invalid review fields')
                    result=s.review(**b)
                    result['reviews']=s.reviews(b['source_id'])
                else:return self.reply(404,{'error':'Not found'})
            finally:s.db.close()
            self.reply(200,result)
        except (ValueError,TypeError,KeyError,AttributeError,RecursionError) as e:self.reply(400,{'error':str(e)})
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
