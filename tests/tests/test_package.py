import tempfile,unittest,zipfile,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('package_public',Path('scripts/package_public.py'));pkg=importlib.util.module_from_spec(spec);spec.loader.exec_module(pkg)
class PackageTests(unittest.TestCase):
 def test_private_operational_files_excluded(self):
  names=[p.relative_to(pkg.ROOT).as_posix() for p in pkg.candidates()]
  for n in ['PLAN.md','BUILDLOG.md','MILESTONES.md','DEMO_STORY.md','local-state.sqlite','META_24H.md','PRE_CLOSE_20261103.md','SUBMISSION_WORKING_DRAFT.md','PUBLICATION_AUDIT.md']:self.assertNotIn(n,names)
  self.assertFalse(any('__pycache__' in n or '.env' in n for n in names))
 def test_manifest_matches_archive(self):
  with tempfile.TemporaryDirectory() as tmp:
   dest=Path(tmp)/'source.zip';m=pkg.package(dest)
   with zipfile.ZipFile(dest) as z:self.assertEqual(set(z.namelist())-{'SOURCE_MANIFEST.json'},{r['path'] for r in m})
