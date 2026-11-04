import json,unittest
from pathlib import Path
from ops.core import EvidenceStore
from ops.importer import import_bundle
class RecordedPilotTests(unittest.TestCase):
 def test_actual_saved_response_and_qualifier_remain_visible(self):
  f=json.loads(Path('fixtures/meta-pilot01-recorded.json').read_text());s=EvidenceStore();r=import_bundle(s,json.dumps(f['bundle']))
  prize=next(c for c in r['claims'] if c['field']=='prize')
  self.assertEqual(prize['value'],'USD 1,000');self.assertIn('USD 1,000 total',prize['quote']);self.assertIn('lost the word total',f['note']);self.assertFalse(r['live_meta_inference']);self.assertFalse(r['plan']['can_submit'])
 def test_ledger_has_no_private_authority_or_key(self):
  raw=Path('fixtures/meta-pilot01-recorded.json').read_text()
  for x in ['approval_reference','Authorization','password','reserved_inr','key_path']:self.assertNotIn(x,raw)
 def test_usage(self):
  f=json.loads(Path('fixtures/meta-pilot01-recorded.json').read_text());self.assertEqual(f['response']['usage']['total_tokens'],2037)
