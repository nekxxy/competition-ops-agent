import json,unittest
from pathlib import Path
from ops.core import EvidenceStore
from ops.importer import import_bundle,validate_bundle

def bundle():
 f=json.loads(Path('fixtures/replay.json').read_text())
 return {'title':'Synthetic example','public_data_confirmed':True,**{k:{'url':f['url'],'text':f[k],'claims':[dict(zip(['field','value','quote'],c)) for c in f['claims_'+k]]} for k in ['before','after']}}
class ImportTests(unittest.TestCase):
 def test_import(self):self.assertEqual(len(import_bundle(EvidenceStore(),json.dumps(bundle()))['changes']),2)
 def test_duplicate(self):
  s=EvidenceStore();raw=json.dumps(bundle());a=import_bundle(s,raw);import_bundle(s,raw);self.assertEqual(len(s.claims(a['after_id'])),6)
 def test_private_rejected(self):
  b=bundle();b['public_data_confirmed']=False
  with self.assertRaises(ValueError):validate_bundle(json.dumps(b))
 def test_no_partial_write(self):
  s=EvidenceStore();b=bundle();b['after']['claims'][0]['quote']='invented'
  with self.assertRaises(ValueError):import_bundle(s,json.dumps(b))
  self.assertEqual(s.db.execute('select count(*) from sources').fetchone()[0],0)
 def test_value_not_entailed(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','Prize $10')
  with self.assertRaises(ValueError):s.claim(sid,'prize','$100','Prize $10')
 def test_naive_deadline(self):
  s=EvidenceStore();sid=s.snapshot('https://example.org','2026-11-01T10:00')
  with self.assertRaises(ValueError):s.claim(sid,'submission_deadline','2026-11-01T10:00','2026-11-01T10:00')
 def test_extra_effect_fields(self):
  b=bundle();b['send_email']='yes'
  with self.assertRaises(ValueError):validate_bundle(json.dumps(b))
 def test_oversize(self):
  with self.assertRaises(ValueError):validate_bundle('x'*200001)
 def test_bad_url(self):
  with self.assertRaises(ValueError):EvidenceStore().snapshot('https://user:secret@example.org','x')
