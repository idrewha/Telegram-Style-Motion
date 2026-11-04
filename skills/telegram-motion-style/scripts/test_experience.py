"""Offline journal checks; never starts an app or touches the real experience store."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('experience.py')


class ExperienceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='motion-experience-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = self.root / 'experience.json'

    def run_cli(self, *args, ok=True):
        r = subprocess.run([sys.executable, str(SCRIPT), '--store', str(self.store), *args],
                           capture_output=True, text=True)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
            return json.loads(r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def start(self, use='one'):
        return self.run_cli('start', '--id', use, '--scope', 'test', '--task', 'Test recording')

    def report(self, feedback='pending'):
        p = self.root / 'report.json'
        p.write_text(json.dumps({'outcome': 'completed', 'summary': 'Test result',
                                'checks': ['fixture check'], 'observations': [],
                                'feedback': {'state': feedback, 'note': 'Fixture feedback'}}))
        return p

    def test_retry_and_feedback_do_not_inflate_usage_or_drop_history(self):
        self.start(); self.start()
        p = self.report()
        self.run_cli('finish', '--id', 'one', '--report', str(p))
        self.run_cli('finish', '--id', 'one', '--report', str(p))
        self.run_cli('finish', '--id', 'one', '--report', str(self.report('approved')))
        data = json.loads(self.store.read_text())
        self.assertEqual(len(data['uses']), 1)
        reports = data['uses']['one']['reports']
        self.assertEqual([x['report']['feedback']['state'] for x in reports], ['pending', 'approved'])

    def test_missing_evidence_does_not_overwrite_saved_report(self):
        self.start()
        p = self.report()
        self.run_cli('finish', '--id', 'one', '--report', str(p))
        before = self.store.read_bytes()
        data = json.loads(p.read_text())
        data['observations'] = [{'kind': 'verified_fact', 'text': 'Unsubstantiated', 'evidence': []}]
        p.write_text(json.dumps(data))
        self.run_cli('finish', '--id', 'one', '--report', str(p), ok=False)
        self.assertEqual(self.store.read_bytes(), before)

    def test_parallel_uses_are_not_lost(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(self.start, [f'use-{i}' for i in range(12)]))
        summary = self.run_cli('show')
        self.assertEqual(summary['trackedUses'], 12)
        self.assertEqual(summary['outcomes']['started'], 12)

    def test_unknown_use_and_id_collision_do_not_overwrite(self):
        self.start()
        before = self.store.read_bytes()
        self.run_cli('finish', '--id', 'missing', '--report', str(self.report()), ok=False)
        self.run_cli('start', '--id', 'one', '--scope', 'other', '--task', 'Different task', ok=False)
        self.assertEqual(self.store.read_bytes(), before)

    def test_corrupt_store_is_preserved(self):
        self.store.write_text('{incomplete')
        self.run_cli('show', ok=False)
        self.assertEqual(self.store.read_text(), '{incomplete')


if __name__ == '__main__':
    unittest.main()
