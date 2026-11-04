import json,unittest
from prepare_model_run import prepare
from ops.meta import MetaExtractor
class PreparationTests(unittest.TestCase):
 def test_never_live(self):
  p=prepare();self.assertEqual(p['network_calls'],0);self.assertFalse(p['credentials_loaded']);self.assertFalse(p['billing_authorization']);self.assertEqual(p['automatic_retries'],0)
 def test_exact_frozen_batch(self):
  p=prepare();self.assertEqual(len(p['requests']),8);self.assertEqual(len({r['case_id'] for r in p['requests']}),8)
 def test_bounded_standard_only(self):
  for row in prepare()['requests']:
   r=row['request'];self.assertEqual(r['model'],'muse-spark-1.3');self.assertEqual(r['max_completion_tokens'],2048);self.assertNotIn('temperature',r);self.assertEqual(set(json.loads(r['messages'][1]['content'])),{'untrusted_source_text'})
 def test_adapter_still_locked(self):
  with self.assertRaises(RuntimeError):MetaExtractor().extract('Prize $10')

 def test_rejects_bad_input_before_transport(self):
  for x in [None,[],5,'','   ','a'*200001,'é'*100001]:
   with self.assertRaises(ValueError):MetaExtractor().request(x)
 def test_accepts_byte_boundary(self):
  self.assertIn('untrusted_source_text',MetaExtractor().request('a'*200000)['messages'][1]['content'])
