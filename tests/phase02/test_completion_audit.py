"""Exercise completion-gate failure cases in isolated fixture projects."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class CompletionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ('tools', 'docs/qa', 'data/ch01'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / 'tools/phase02_completion_audit.py', self.root / 'tools')
        for name in ('dialogue.json', 'shots.json', 'missions.json'):
            shutil.copy(ROOT / 'data/ch01' / name, self.root / 'data/ch01')
        self.registry = json.loads((ROOT / 'docs/PHASE_02_REQUIREMENTS.json').read_text(encoding='utf-8'))
        # Synthetic bookkeeping fixtures, never runtime verification evidence.
        for req in self.registry['requirements']:
            req.update(status='VERIFIED', implementation_files=['implemented.gd'],
                       evidence=['fixture'], test_method='fixture', blocking_issues=[], pending_checks=[])
        (self.root / 'implemented.gd').write_text('# fixture', encoding='utf-8')

    def audit(self, registry):
        (self.root / 'docs/PHASE_02_REQUIREMENTS.json').write_text(json.dumps(registry), encoding='utf-8')
        return subprocess.run([sys.executable, '-I', str(self.root / 'tools/phase02_completion_audit.py')],
                              capture_output=True, text=True)

    def test_complete_fixture(self):
        self.assertEqual(self.audit(self.registry).returncode, 0)

    def test_missing_traceability_blocks_even_verified(self):
        for field, value in [('implementation_files', []), ('implementation_files', ['absent.gd']),
                             ('test_method', ''), ('evidence', [])]:
            with self.subTest(field=field, value=value):
                registry = copy.deepcopy(self.registry)
                registry['requirements'][0][field] = value
                self.assertEqual(self.audit(registry).returncode, 1)

    def test_missing_canonical_mappings_block(self):
        for field in ('mission_id', 'objective_id', 'dialogue_id', 'shot_id', 'scene_id'):
            with self.subTest(field=field):
                registry = copy.deepcopy(self.registry)
                for req in registry['requirements']:
                    req.pop(field, None)
                self.assertEqual(self.audit(registry).returncode, 1)

    def test_unverified_mandatory_blocks(self):
        registry = copy.deepcopy(self.registry)
        next(r for r in registry['requirements'] if r['mandatory'])['status'] = 'IMPLEMENTED_UNTESTED'
        self.assertEqual(self.audit(registry).returncode, 1)


if __name__ == '__main__':
    unittest.main()
