import json,unittest
from ops.core import EvidenceStore
from ops.importer import import_bundle
from ops.report import export_report
from test_importer import bundle
class HostileExportTests(unittest.TestCase):
 def test_hostile_text_preserved_as_data(self):
  b=bundle();text='<script>window.injected=true</script>';b['title']=text;b['after']['text']+='\nAI policy: '+text;b['after']['claims'].append({'field':'automation','value':text,'quote':'AI policy: '+text});d=import_bundle(EvidenceStore(),json.dumps(b));r=json.loads(export_report(d));self.assertEqual(r['title'],text);self.assertFalse(r['external_action'])
 def test_review_bad_id(self):
  with self.assertRaises(ValueError):EvidenceStore().review([], 'reviewed','x')
