import copy,json,unittest
from ops.run_evidence import record_saved
class RunEvidenceTests(unittest.TestCase):
 def response(self):
  return {'id':'example-unverified','model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':[{'field':'prize','value':'$10','quote':'Prize $10'}]})}}],'usage':{'prompt_tokens':100,'completion_tokens':20,'total_tokens':120},'headers':{'Authorization':'SYNTHETIC_SECRET_NOT_REAL'},'email':'private@example.org'}
 def record(self,r=None,t='2026-11-03T14:20:00+00:00'):
  return record_saved('Prize $10',self.response() if r is None else r,t)
 def test_never_proves_live(self):
  p=self.record();self.assertFalse(p['remote_authorship_verified']);self.assertFalse(p['timestamp_verified']);self.assertEqual(p['network_calls'],0);self.assertFalse(p['billing_authorization'])
 def test_removes_unapproved_metadata(self):
  p=json.dumps(self.record());self.assertNotIn('SYNTHETIC_SECRET_NOT_REAL',p);self.assertNotIn('private@example.org',p);self.assertNotIn('headers',self.record()['response'])
 def test_rejects_implicit_model(self):
  r=self.response();del r['model']
  with self.assertRaises(ValueError):self.record(r)
 def test_rejects_contributor(self):
  r=self.response();r['model']='muse-spark-1.3-contributor'
  with self.assertRaises(ValueError):self.record(r)
 def test_rejects_non_utc_and_naive(self):
  for t in ['2026-11-03T19:30:00+05:30','2026-11-03T14:00:00','bad']:
   with self.assertRaises(ValueError):self.record(t=t)
 def test_rejects_bad_usage(self):
  for v in [True,-1,1.5,'1']:
   r=self.response();r['usage']['prompt_tokens']=v
   with self.assertRaises(ValueError):self.record(r)
 def test_rejects_inconsistent_usage(self):
  r=self.response();r['usage']['total_tokens']=999
  with self.assertRaises(ValueError):self.record(r)
 def test_rejects_output_over_bound(self):
  r=self.response();r['usage'].update(completion_tokens=2049,total_tokens=2149)
  with self.assertRaises(ValueError):self.record(r)
 def test_rejects_incomplete(self):
  r=self.response();r['choices'][0]['finish_reason']='length'
  with self.assertRaises(ValueError):self.record(r)
 def test_rejects_unsupported_claim(self):
  r=self.response();r['choices'][0]['message']['content']=json.dumps({'claims':[{'field':'prize','value':'$50','quote':'Prize $50'}]})
  with self.assertRaises(ValueError):self.record(r)
 def test_hash_binding_and_determinism(self):
  p=self.record();self.assertEqual(p,self.record());r=self.response();r['id']='other';q=self.record(r);self.assertNotEqual(p['response_sha256'],q['response_sha256']);self.assertEqual(p['request_sha256'],q['request_sha256'])

 def test_rejects_malformed_choice(self):
  for choice in [None,[],5,'bad']:
   r=self.response();r['choices']=[choice]
   with self.assertRaises(ValueError):self.record(r)
 def test_requires_explicit_finish_reason(self):
  r=self.response();del r['choices'][0]['finish_reason']
  with self.assertRaises(ValueError):self.record(r)
