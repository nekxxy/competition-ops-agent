import io,json,tempfile,unittest
from pathlib import Path
from ops.bounded_live import execute_one,MAX_USD,validate_request
from prepare_model_run import prepare
class BoundedLiveTests(unittest.TestCase):
 def test_max_usd(self):self.assertEqual(str(MAX_USD),'1.319424')
 def test_frozen_requests(self):
  for r in prepare()['requests']:validate_request(r['request'])
 def test_tools_rejected(self):
  r=prepare()['requests'][0]['request'];r['tools']=[]
  with self.assertRaises(ValueError):validate_request(r)
 def test_one_attempt_and_duplicate_rejection(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'key').write_text('fake-not-a-secret');calls=[]
   def op(req,timeout):
    calls.append(1);return io.BytesIO(json.dumps({'id':'test','usage':{}}).encode())
   kw=dict(approval_reference='TEST ONLY',reservation_inr=528,opener=op)
   execute_one(prepare()['requests'][0]['request'],p/'key',p/'ledger',p/'response',**kw)
   self.assertEqual(len(calls),1)
   with self.assertRaises(ValueError):execute_one(prepare()['requests'][0]['request'],p/'key',p/'ledger',p/'response',**kw)
 def test_unknown_reserves_and_never_retries(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'key').write_text('fake-not-a-secret');calls=[]
   def op(req,timeout):calls.append(1);raise TimeoutError('no')
   with self.assertRaises(RuntimeError):execute_one(prepare()['requests'][0]['request'],p/'key',p/'ledger',p/'response',approval_reference='TEST ONLY',reservation_inr=528,opener=op)
   self.assertEqual(len(calls),1);j=json.loads((p/'ledger').read_text());self.assertEqual(j['reserved_inr'],'528');self.assertEqual(j['state'],'attempted_result_unknown')
 def test_no_authority(self):
  with self.assertRaises(ValueError):execute_one(prepare()['requests'][0]['request'],'missing','missing','missing',approval_reference='',reservation_inr=528)
