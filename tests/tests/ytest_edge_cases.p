import json,unittest
from ops.core import EvidenceStore
from ops.importer import import_bundle
from test_importer import bundle
from ops.meta import MetaExtractor
class EdgeTests(unittest.TestCase):
 def test_removed_claim_retains_prior_evidence(self):
  s=EvidenceStore();a=s.snapshot('https://example.org','Prize $10');b=s.snapshot('https://example.org','No prize info');s.claim(a,'prize','$10','Prize $10');d=s.diff(a,b)[0];self.assertEqual(d['after'],[]);self.assertEqual(d['previous_evidence'][0]['quote'],'Prize $10')
 def test_duplicate_claim_inside_import(self):
  b=bundle();b['after']['claims']*=2;s=EvidenceStore();d=import_bundle(s,json.dumps(b));self.assertEqual(len(d['claims']),6)
 def test_review_survives_reimport(self):
  s=EvidenceStore();raw=json.dumps(bundle());d=import_bundle(s,raw);s.review(d['after_id'],'reviewed','Example');self.assertEqual(len(import_bundle(s,raw)['reviews']),1)
 def test_review_does_not_mutate_source(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','x');s.review(sid,'needs_changes','Example');self.assertEqual(s.source(sid)['body'],'x')
 def test_invalid_claim_type(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','x')
  with self.assertRaises(ValueError):s.claim(sid,[],'x','x')
 def test_invalid_review_type(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','x')
  with self.assertRaises(ValueError):s.review(sid,'reviewed',None)
 def test_invalid_url_type(self):
  with self.assertRaises(ValueError):EvidenceStore().snapshot(None,'x')
 def test_model_naive_deadline_rejected(self):
  c={'field':'submission_deadline','value':'2026-11-01T10:00','quote':'2026-11-01T10:00'}
  def transport(e,r):return {'choices':[{'message':{'content':json.dumps({'claims':[c]})}}]}
  with self.assertRaises(ValueError):MetaExtractor(transport).extract(c['quote'])
