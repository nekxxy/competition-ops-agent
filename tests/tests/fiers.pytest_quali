import copy,json,unittest
from pathlib import Path
from ops.core import EvidenceStore
from ops.demo import replay
from ops.importer import import_bundle
from ops.qualifiers import detect_omitted_qualifiers,annotate_claims
from ops.report import export_report

FROZEN={'field':'prize','value':'USD 1,000','quote':'The award is USD 1,000 total, split among the winning teams.'}

def quals(claim):return [a['qualifier'] for a in detect_omitted_qualifiers(claim)]

class QualifierDetectorTests(unittest.TestCase):
 def test_frozen_example_flags_total_and_split(self):
  out=detect_omitted_qualifiers(FROZEN)
  self.assertEqual([a['qualifier'] for a in out],['total','split'])
  for a in out:
   self.assertEqual(a['type'],'omitted_qualifier');self.assertIn(a['qualifier'],FROZEN['quote']);self.assertIn(a['qualifier'],a['message'])
 def test_detector_does_not_mutate_claim(self):
  c=dict(FROZEN);before=copy.deepcopy(c);detect_omitted_qualifiers(c);annotate_claims([c]);self.assertEqual(c,before)
 def test_retained_qualifier_not_flagged(self):
  self.assertEqual(quals({**FROZEN,'value':'USD 1,000 total'}),['split'])
  self.assertEqual(quals({**FROZEN,'value':'USD 1,000 total, split'}),[])
 def test_verbatim_original_case(self):
  self.assertEqual(quals({'field':'prize','value':'$500','quote':'Prizes: $500 PER TEAM.'}),['PER TEAM'])
 def test_not_guaranteed_flagged_but_plain_guaranteed_not(self):
  self.assertEqual(quals({'field':'prize','value':'EUR 200','quote':'A prize of EUR 200 is not guaranteed.'}),['not guaranteed'])
  self.assertEqual(quals({'field':'prize','value':'EUR 200','quote':'A guaranteed prize of EUR 200.'}),[])
 def test_up_to_omitted_flagged(self):
  self.assertEqual(quals({'field':'prize','value':'$5,000','quote':'Winners receive up to $5,000.'}),['up to'])
  self.assertEqual(quals({'field':'prize','value':'up to $5,000','quote':'Winners receive up to $5,000.'}),[])
 def test_longest_phrase_wins(self):
  self.assertEqual(quals({'field':'prize','value':'Rs 1000','quote':'A prize pool of Rs 1000, approximately.'}),['prize pool','approximately'])
 def test_word_boundaries(self):
  self.assertEqual(quals({'field':'prize','value':'USD 300','quote':'Totally USD 300 for eachother.'}),[])
 def test_benign_non_monetary_claim_not_flagged(self):
  self.assertEqual(detect_omitted_qualifiers({'field':'eligibility','value':'500 teams','quote':'We welcome a total of 500 teams.'}),[])
  self.assertEqual(detect_omitted_qualifiers({'field':'license','value':'MIT','quote':'Each entry uses MIT, up to the team.'}),[])
 def test_money_value_in_other_field_is_in_scope(self):
  self.assertEqual(quals({'field':'eligibility','value':'$50 fee','quote':'Teams pay a $50 fee each.'}),['each'])
 def test_qualifier_in_other_sentence_not_flagged(self):
  self.assertEqual(quals({'field':'prize','value':'USD 1,000','quote':'The award is USD 1,000. A total of 40 teams split the venue.'}),[])
  self.assertEqual(quals({'field':'prize','value':'USD 1,000','quote':'Up to 40 teams may enter! The award is USD 1,000.'}),[])
 def test_decimal_and_abbreviation_do_not_split_sentence(self):
  self.assertEqual(quals({'field':'prize','value':'USD 1,000.50','quote':'The award is USD 1,000.50 total.'}),['total'])
  self.assertEqual(quals({'field':'prize','value':'Rs. 900','quote':'Approx. Rs. 900 in credits.'}),['Approx','in credits'])
 def test_malformed_or_unanchored_input_returns_empty(self):
  for c in [None,'x',{},{'field':'prize','value':5,'quote':'total'},{'field':'prize','value':'USD 9','quote':'USD 1 total.'}]:self.assertEqual(detect_omitted_qualifiers(c),[])

class AdvisoryIntegrationTests(unittest.TestCase):
 def test_replay_claims_carry_advisory_lists(self):
  d=replay();self.assertTrue(d['claims'])
  for c in d['claims']:self.assertIsInstance(c['advisories'],list)
 def test_import_claims_carry_advisory_lists(self):
  d=import_bundle(EvidenceStore(),Path('fixtures/conflict-example.json').read_text());self.assertTrue(d['claims'])
  for c in d['claims']:self.assertIsInstance(c['advisories'],list)
  d=import_bundle(EvidenceStore(),Path('fixtures/raw-source-example.json').read_text())
  for c in d['claims']:self.assertIsInstance(c['advisories'],list)
 def test_recorded_pilot_prize_flagged_and_others_empty(self):
  f=json.loads(Path('fixtures/meta-pilot01-recorded.json').read_text());s=EvidenceStore();r=import_bundle(s,json.dumps(f['bundle']))
  for c in r['claims']:
   if c['field']=='prize':
    self.assertEqual(c['value'],'USD 1,000');self.assertEqual([a['qualifier'] for a in c['advisories']],['total','split'])
   else:self.assertEqual(c['advisories'],[])
  self.assertFalse(r['plan']['can_submit'])
 def test_advisories_not_persisted(self):
  f=json.loads(Path('fixtures/meta-pilot01-recorded.json').read_text());s=EvidenceStore();r=import_bundle(s,json.dumps(f['bundle']))
  self.assertNotIn('advisories',s.claims(r['after_id'])[0])
  cols=[x[1] for x in s.db.execute('PRAGMA table_info(claims)')];self.assertNotIn('advisories',cols)
 def test_report_limitation_mentions_heuristic(self):
  r=json.loads(export_report(replay()));self.assertTrue(any('heuristic' in x for x in r['limitations']))
