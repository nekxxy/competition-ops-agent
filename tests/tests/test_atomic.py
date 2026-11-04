import json,tempfile,unittest,threading
from pathlib import Path
from ops.core import EvidenceStore
from ops.importer import import_bundle
from test_importer import bundle
class AtomicTests(unittest.TestCase):
 def test_fault_rolls_back_all_evidence(self):
  s=EvidenceStore();original=s.claim;n=0
  def failure(*a,**kw):
   nonlocal n
   n+=1
   if n==3:raise RuntimeError('injected storage failure')
   original(*a,**kw)
  s.claim=failure
  with self.assertRaises(RuntimeError):import_bundle(s,json.dumps(bundle()))
  for table in ['sources','claims','extraction_sets']:self.assertEqual(s.db.execute('select count(*) from '+table).fetchone()[0],0)
  self.assertFalse(s.db.in_transaction)
 def test_concurrent_conflicting_sets_do_not_merge(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=str(Path(tmp)/'state.sqlite');EvidenceStore(path).db.close();barrier=threading.Barrier(2);results=[]
   def worker(remove):
    s=EvidenceStore(path);b=bundle()
    if remove:b['after']['claims'].pop()
    barrier.wait()
    try:import_bundle(s,json.dumps(b));results.append('ok')
    except ValueError:results.append('rejected')
    finally:s.db.close()
   ts=[threading.Thread(target=worker,args=(x,)) for x in [False,True]]
   for t in ts:t.start()
   for t in ts:t.join()
   self.assertEqual(sorted(results),['ok','rejected'])
