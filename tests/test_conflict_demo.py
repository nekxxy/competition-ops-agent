import json,unittest
from pathlib import Path
from ops.core import EvidenceStore
from ops.importer import import_bundle
class ConflictDemoTests(unittest.TestCase):
 def test_unknowns_stay_missing(self):
  d=import_bundle(EvidenceStore(),Path('fixtures/conflict-example.json').read_text());self.assertEqual(d['readiness']['missing'],['license','prize','submission_deadline']);self.assertEqual(d['readiness']['conflicts'],['registration_deadline']);self.assertFalse(d['plan']['can_submit']);self.assertEqual(len(d['plan']['deadlines']),2)
 def test_negative_policy_not_dropped(self):
  d=import_bundle(EvidenceStore(),Path('fixtures/conflict-example.json').read_text());self.assertIn('AI assistance is prohibited',[r['value'] for r in d['claims']])
 def test_source_url_attribute_injection(self):
  with self.assertRaises(ValueError):EvidenceStore().snapshot('https://example.org/"onmouseover="alert(1)','text')
 def test_source_url_newline(self):
  with self.assertRaises(ValueError):EvidenceStore().snapshot('https://example.org/\npath','text')
