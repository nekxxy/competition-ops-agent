import json,unittest,hashlib
from pathlib import Path
from ops.replay_response import validate_response

def response(claims=[]):return {'model':'muse-spark-1.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'claims':claims})}}]}
class ResponseTests(unittest.TestCase):
 def test_replay_never_live(self):self.assertFalse(validate_response('x',response())['live_meta_inference'])
 def test_label_not_authorship(self):self.assertFalse(validate_response('x',response())['remote_authorship_verified'])
 def test_contributor_rejected(self):
  r=response();r['model']='muse-spark-1.3-contributor'
  with self.assertRaises(ValueError):validate_response('x',r)
 def test_truncated_rejected(self):
  r=response();r['choices'][0]['finish_reason']='length'
  with self.assertRaises(ValueError):validate_response('x',r)
 def test_refusal_rejected(self):
  r=response();r['choices'][0]['message']['refusal']='no'
  with self.assertRaises(ValueError):validate_response('x',r)
 def test_malformed_choice(self):
  with self.assertRaises(ValueError):validate_response('x',{'choices':[None]})
 def test_invalid_json(self):
  r=response();r['choices'][0]['message']['content']='not json'
  with self.assertRaises(ValueError):validate_response('x',r)
 def test_prose_gold_spans_valid(self):
  f=json.loads(Path('fixtures/prose-evaluation-v1.json').read_text())
  for c in f['cases']:validate_response(c['text'],response(c['expected']))
