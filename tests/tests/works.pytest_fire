import json, unittest
from ops.fireworks import FireworksExtractor
class FireworksTests(unittest.TestCase):
 def test_locked(self):
  with self.assertRaises(RuntimeError): FireworksExtractor().extract('x')
 def test_request(self):
  r=FireworksExtractor().request('Prize $10')
  self.assertEqual(r['model'],'accounts/fireworks/models/muse-spark-open')
  self.assertEqual(r['max_tokens'],2048)
  self.assertIn('Return JSON',r['messages'][0]['content'])
  self.assertNotIn('key',r)
 def response(self,model=None,quote='Prize $10'):
  return {'model':model or FireworksExtractor.model,'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':[{'field':'prize','value':'$10','quote':quote}]})}}]}
 def test_offline_injection_validates(self):
  v=self.response();self.assertEqual(FireworksExtractor(lambda e,r:v).extract('Prize $10')[0]['value'],'$10')
  self.assertIn('model',v)
 def test_wrong_model(self):
  with self.assertRaises(ValueError):FireworksExtractor(lambda e,r:self.response('other')).extract('Prize $10')
 def test_missing_model(self):
  v=self.response();del v['model']
  with self.assertRaises(ValueError):FireworksExtractor(lambda e,r:v).extract('Prize $10')
 def test_unsupported_quote(self):
  with self.assertRaises(ValueError):FireworksExtractor(lambda e,r:self.response(quote='Prize $10 invented')).extract('Prize $10')
 def test_incomplete(self):
  v=self.response();v['choices'][0]['finish_reason']='length'
  with self.assertRaises(ValueError):FireworksExtractor(lambda e,r:v).extract('Prize $10')
