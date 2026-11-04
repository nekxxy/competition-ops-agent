import json,unittest
from ops.core import EvidenceStore
from ops.importer import import_bundle
from test_importer import bundle
class IntegrityTests(unittest.TestCase):
 def test_same_snapshot_changed_extraction_rejected(self):
  s=EvidenceStore();b=bundle();d=import_bundle(s,json.dumps(b));b['after']['claims']=[]
  with self.assertRaises(ValueError):import_bundle(s,json.dumps(b))
  self.assertEqual(len(s.claims(d['after_id'])),6)
 def test_empty_extraction_frozen(self):
  s=EvidenceStore();b=bundle();saved=b['after']['claims'];b['after']['claims']=[];import_bundle(s,json.dumps(b));b['after']['claims']=saved
  with self.assertRaises(ValueError):import_bundle(s,json.dumps(b))
 def test_failed_reimport_leaves_no_new_before(self):
  s=EvidenceStore();b=bundle();import_bundle(s,json.dumps(b));b['before']['text']+=' new source';b['after']['claims']=[]
  with self.assertRaises(ValueError):import_bundle(s,json.dumps(b))
  self.assertEqual(s.db.execute('select count(*) from sources').fetchone()[0],2)
 def test_identical_text_different_claims_rejected(self):
  s=EvidenceStore();b=bundle();b['before']=dict(b['after']);b['before']['claims']=[]
  with self.assertRaises(ValueError):import_bundle(s,json.dumps(b))
 def test_same_content_different_url_distinct(self):
  s=EvidenceStore();a=s.snapshot('https://example.org/a','x');b=s.snapshot('https://example.org/b','x');self.assertNotEqual(a,b)
