"""Optional local Chrome UI smoke test. Uses synthetic data only.
Requires websocket-client and google-chrome; not needed by the application.
"""
import base64,json,subprocess,tempfile,threading,time,urllib.request,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import websocket
import server

def run(conflict=False,hostile=False,saved=False):
 with tempfile.TemporaryDirectory() as tmp:
  server.DB=str(Path(tmp)/'state.sqlite');http=server.ThreadingHTTPServer(('127.0.0.1',8765),server.Handler);thread=threading.Thread(target=http.serve_forever);thread.start()
  proc=subprocess.Popen(['/opt/google/chrome/chrome','--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--remote-debugging-port=9229','--remote-allow-origins=http://localhost:9229','--user-data-dir='+tmp+'/chrome','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:
   for _ in range(300):
    try:
     tabs=json.load(urllib.request.urlopen('http://127.0.0.1:9229/json'));break
    except Exception:time.sleep(.1)
   else:raise RuntimeError('Chrome debugger unavailable after30seconds')
   ws=websocket.create_connection(next(t for t in tabs if t['type']=='page')['webSocketDebuggerUrl'],origin='http://localhost:9229');seq=0
   def call(method,params={}):
    nonlocal seq
    seq+=1;ws.send(json.dumps({'id':seq,'method':method,'params':params}))
    while True:
     r=json.loads(ws.recv())
     if r.get('id')==seq:
      if 'error' in r:raise RuntimeError(r['error'])
      return r.get('result',{})
   def js(expression):
    r=call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
    if 'exceptionDetails' in r:raise RuntimeError(r['exceptionDetails'])
    return r['result'].get('value')
   def until(expression):
    for _ in range(100):
     if js(expression):return
     time.sleep(.05)
    raise AssertionError((expression,js('location.href'),js('document.body ? document.body.innerText.slice(0,1000) : null')))
   call('Page.enable');call('Page.navigate',{'url':'http://127.0.0.1:8765/'})
   until('document.querySelectorAll("#claims details").length===6')
   f=json.load(urllib.request.urlopen('http://127.0.0.1:8765/api/'+('conflict-example' if conflict else 'raw-example')));f['title']='Synthetic import smoke test'
   payload='<img src=x onerror=window.injected=true><script>window.injected=true</script>'
   if hostile:
    f['title']=payload;f['after']['text']+='\nPrizes: '+payload
   if saved:
    from ops.response_bundle import saved_response_bundle
    from ops.extract import extract_explicit
    def version(v):
     return {'url':v['url'],'text':v['text'],'response':{'model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':extract_explicit(v['text'])})}}]}}
    wrapper=saved_response_bundle('Synthetic saved-response bridge, not a provider call',version(f['before']),version(f['after']))
    assert wrapper['remote_authorship_verified'] is False and wrapper['network_calls']==0
    f=wrapper['bundle']
   bundle=Path(tmp)/'bundle.json';bundle.write_text(json.dumps(f))
   dom=call('DOM.getDocument');node=call('DOM.querySelector',{'nodeId':dom['root']['nodeId'],'selector':'#bundle'})['nodeId'];call('DOM.setFileInputFiles',{'nodeId':node,'files':[str(bundle)]})
   until('document.querySelector("#title").textContent==='+json.dumps(f['title']))
   if hostile:
    assert js('window.injected===undefined && document.querySelectorAll("#sources img,#title img").length===0')
    assert payload in js('document.querySelector("#sources").textContent')
   call('Browser.setDownloadBehavior',{'behavior':'allow','downloadPath':tmp+'/downloads'})
   js('document.querySelector("#export").click()')
   downloaded=Path(tmp)/'downloads/competition-review.json'
   for _ in range(100):
    if downloaded.exists():break
    time.sleep(.05)
   report=json.loads(downloaded.read_text());assert report['external_action'] is False
   if hostile:assert report['title']==payload
   assert js('document.querySelector("#review-form").hidden') is False
   js('document.querySelector("#reviewer").value="Smoke reviewer";document.querySelector("#review-form").requestSubmit()')
   until('document.querySelector("#review-status").textContent.includes("saved locally")')
   assert 'Smoke reviewer' in js('document.querySelector("#reviews").textContent')
   assert js('reportData(active).external_action') is False
   assert len(js('reportData(active).claims'))==(4 if conflict else 7 if hostile else 6)
   if conflict:
    assert js('active.readiness.conflicts')==['registration_deadline']
    assert 'submission_deadline' in js('active.readiness.missing')
    assert js('active.plan.can_submit') is False
    assert js('document.querySelectorAll("#deadline-list .source").length')==2
    assert 'claim removed' in js('document.querySelector("#changes").textContent')
   assert 'LOCAL PUBLIC-TEXT IMPORT' in js('document.querySelector(".mode").textContent')
   js('document.querySelector("#sources details").open=true')
   for width,height,label in [(1440,1800,'desktop'),(390,3400,'mobile')]:
    call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':False})
    assert js('document.documentElement.scrollWidth <= window.innerWidth'), 'Horizontal overflow'
    shot=call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})
    Path('/downloads/competition-ops-v11-'+('saved-' if saved else 'hostile-' if hostile else 'conflict-' if conflict else 'import-')+label+'.png').write_bytes(base64.b64decode(shot['data']))
   print(json.dumps({'ui_import':True,'local_review':True,'audit_display':True,'no_horizontal_overflow':True,'screenshots':'/downloads/competition-ops-v11-'+('saved-' if saved else 'hostile-' if hostile else 'conflict-' if conflict else 'import-')+'{desktop,mobile}.png'}))
   ws.close()
  finally:
   proc.terminate();proc.wait(timeout=10);http.shutdown();thread.join();http.server_close()
if __name__=='__main__':run('--conflict' in sys.argv,'--hostile' in sys.argv,'--saved' in sys.argv)
