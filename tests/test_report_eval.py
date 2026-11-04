import json,unittest
from ops.demo import replay
from ops.report import export_report
from evaluate import evaluate
class ReportTests(unittest.TestCase):
 def test_report_effect_boundary(self):
  r=json.loads(export_report(replay()));self.assertFalse(r['external_action']);self.assertFalse(r['live_meta_inference']);self.assertIn('limitations',r)
 def test_report_whitelist(self):
  r=replay();r['api_key']='TEST_SENTINEL';self.assertNotIn('TEST_SENTINEL',export_report(r))
 def test_review_report_preserves_evidence(self):self.assertEqual(len(json.loads(export_report(replay()))['claims']),6)
 def test_eval_authored_cases(self):self.assertEqual(evaluate()['case_exact_match'],'14/14')

 def test_report_retains_recorded_provenance(self):
  r=replay();r['recorded_meta']={'model':'muse-spark-1.3','response_id':'test','usage':{'total_tokens':2037}};j=json.loads(export_report(r));self.assertEqual(j['recorded_meta'],r['recorded_meta'])
