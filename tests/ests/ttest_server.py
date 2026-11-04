import unittest,threading,tempfile,json,urllib.request,urllib.error
from pathlib import Path
import server
from test_importer import bundle
class ServerTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();server.DB=str(Path(cls.tmp.name)/'state.sqlite');cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.thread=threading.Thread(target=cls.http.serve_forever);cls.thread.start();cls.base='http://127.0.0.1:'+str(cls.http.server_port)
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.thread.join();cls.http.server_close();cls.tmp.cleanup()
 def request(self,path,data=None,headers=None):
  h={'Host':'127.0.0.1:8765','Content-Type':'application/json','X-Ops-Local':'1',**(headers or {})};req=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers=h)
  try:
   with urllib.request.urlopen(req) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def test_demo(self):self.assertEqual(self.request('/api/demo')[1]['mode'],'OFFLINE REPLAY')
 def test_import_review(self):
  code,d=self.request('/api/import',bundle());self.assertEqual(code,200);code,r=self.request('/api/review',{'source_id':d['after_id'],'reviewer':'Test reviewer','decision':'reviewed'});self.assertFalse(r['external_action'])
 def test_unknown_review(self):self.assertEqual(self.request('/api/review',{'source_id':'no','decision':'reviewed','reviewer':'x'})[0],400)
 def test_cross_origin(self):self.assertEqual(self.request('/api/import',bundle(),{'Origin':'https://evil.invalid'})[0],403)
 def test_missing_custom_header(self):self.assertEqual(self.request('/api/import',bundle(),{'X-Ops-Local':''})[0],403)
 def test_host_header_attack(self):self.assertEqual(self.request('/api/import',bundle(),{'Host':'evil.invalid'})[0],403)
 def test_no_external_action_endpoint(self):self.assertEqual(self.request('/api/submit',{})[0],404)
 def test_no_filesystem_read(self):self.assertEqual(self.request('/PLAN.md')[0],404)

 def test_recorded_pilot(self):
  code,d=self.request('/api/recorded-pilot');self.assertEqual(code,200);self.assertFalse(d['live_meta_inference']);self.assertEqual(d['recorded_meta']['usage']['total_tokens'],2037)
 def test_missing_recorded_pilot_is_safe_503(self):
  from unittest.mock import patch
  with patch.object(server,'ROOT',Path(self.tmp.name)):
   code,d=self.request('/api/recorded-pilot');self.assertEqual(code,503);self.assertIn('no API call',d['error']);self.assertNotIn(self.tmp.name,str(d))
