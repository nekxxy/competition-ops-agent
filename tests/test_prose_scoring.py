import json,unittest
from pathlib import Path
from score_prose import score
class ProseScoreTests(unittest.TestCase):
 def responses(self):
  return {c['id']:{'model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':c['expected']})}}]} for c in json.loads(Path('fixtures/prose-evaluation-v1.json').read_text())['cases']}
 def test_gold_replay_not_provider_accuracy(self):
  r=score(self.responses());self.assertEqual(r['exact_cases'],8);self.assertFalse(r['remote_authorship_verified']);self.assertEqual(r['live_meta_calls'],0)
 def test_invalid_abstention_not_correct(self):
  rs=self.responses();rs['p03']={};r=score(rs);self.assertEqual(r['exact_cases'],7);self.assertEqual(r['valid_cases'],7)
 def test_missing_case_rejected(self):
  rs=self.responses();rs.pop('p08')
  with self.assertRaises(ValueError):score(rs)

 def test_gold_abstention_and_conflict_metrics(self):
  r=score(self.responses());self.assertEqual(r['required_abstention_cases'],3);self.assertEqual(r['correct_abstentions'],3);self.assertEqual(r['multi_value_cases'],3);self.assertEqual(r['preserved_multi_value_cases'],3);self.assertEqual(r['field_value_precision'],1);self.assertEqual(r['field_value_recall'],1)
 def test_invalid_abstention_not_counted(self):
  rs=self.responses();rs['p03']={};self.assertEqual(score(rs)['correct_abstentions'],2)
 def test_losing_conflict_branch_detected(self):
  rs=self.responses();c=json.loads(rs['p04']['choices'][0]['message']['content']);c['claims']=c['claims'][:1];rs['p04']['choices'][0]['message']['content']=json.dumps(c);self.assertEqual(score(rs)['preserved_multi_value_cases'],2)
 def test_empty_prediction_precision_undefined(self):
  rs={k:{'model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':'{"claims":[]}'}}]} for k in self.responses()};r=score(rs);self.assertIsNone(r['field_value_precision']);self.assertEqual(r['field_value_recall'],0);self.assertEqual(r['correct_abstentions'],3)
