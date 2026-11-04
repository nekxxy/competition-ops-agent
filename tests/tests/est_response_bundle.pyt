import json,unittest
from ops.response_bundle import saved_response_bundle
from ops.importer import import_bundle
from ops.core import EvidenceStore
class ResponseBundleTests(unittest.TestCase):
 def version(self,value='$10',response_value=None):
  c={'field':'prize','value':response_value or value,'quote':'Prize '+(response_value or value)}
  return {'url':'https://example.org/synthetic','text':'Prize '+value,'response':{'model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':[c]})}}]}}
 def test_importable_not_live(self):
  r=saved_response_bundle('Synthetic saved envelope',self.version(),self.version('$20'));s=EvidenceStore()
  try:
   d=import_bundle(s,json.dumps(r['bundle']));self.assertEqual(d['mode'],'LOCAL PUBLIC-TEXT IMPORT');self.assertFalse(d['live_meta_inference']);self.assertEqual(d['changes'][0]['field'],'prize');self.assertFalse(r['remote_authorship_verified']);self.assertEqual(r['network_calls'],0)
  finally:s.db.close()
 def test_rejects_unsupported_quote(self):
  with self.assertRaises(ValueError):saved_response_bundle('Synthetic',self.version(),self.version('$20','$30'))
 def test_no_credential_metadata_propagates(self):
  v=self.version();v['response']['Authorization']='SYNTHETIC_NOT_REAL';r=saved_response_bundle('Synthetic',v,v);self.assertNotIn('Authorization',json.dumps(r))
 def test_rejects_extra_source_fields(self):
  v=self.version();v['action']='send'
  with self.assertRaises(ValueError):saved_response_bundle('Synthetic',v,self.version())
 def test_rejects_bad_url(self):
  v=self.version();v['url']='javascript:bad'
  with self.assertRaises(ValueError):saved_response_bundle('Synthetic',v,self.version())
