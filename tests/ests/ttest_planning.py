import unittest
from ops.core import EvidenceStore
from ops.planning import review_plan
class PlanningTests(unittest.TestCase):
 def test_offset_conversion(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','2026-11-22T23:59:00+01:00');s.claim(sid,'submission_deadline','2026-11-22T23:59:00+01:00','2026-11-22T23:59:00+01:00');p=review_plan(s.claims(sid),s.readiness(sid));self.assertEqual(p['deadlines'][0]['local_value'],'2026-11-23T04:29:00+05:30')
 def test_conflict_not_resolved(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','2026-11-01T10:00+01:00 and 2026-11-02T10:00+01:00')
  for v in ['2026-11-01T10:00+01:00','2026-11-02T10:00+01:00']:s.claim(sid,'registration_deadline',v,v)
  p=review_plan(s.claims(sid),s.readiness(sid));self.assertEqual(len(p['deadlines']),2);self.assertTrue(all(x['conflicting'] for x in p['deadlines']));self.assertFalse(p['can_submit'])
 def test_missing_fields_blocked(self):self.assertEqual(len(review_plan([],{'missing':['prize'],'conflicts':[]})['tasks']),1)
 def test_no_prize_value_guessed(self):self.assertEqual(review_plan([],{'missing':['prize'],'conflicts':[]})['deadlines'],[])
