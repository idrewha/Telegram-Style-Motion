"""Checks for shared-clock translation, stale-base detection inputs and source safety."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('telegram_motion', Path(__file__).with_name('motion.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'take').mkdir()
        (self.root / 'take/rec.mp4').write_bytes(b'source-placeholder')
        (self.root / 'take/taps.json').write_text('original calibrated taps')
        for name in ('bezel.png', 'sound.wav'):
            (self.root / name).write_bytes(b'asset-placeholder')
        self.plan = {'version': 1, 'fps': 60, 'trim': [1, 5],
            'base': {'take': 'take', 'bezel': 'bezel.png', 'scale': 3},
            'groups': [{'origin': 2, 'events': [
                {'id': 'tap', 'type': 'tap', 'at': .2, 'x': 20, 'y': 30},
                {'id': 'camera', 'type': 'camera', 'at': -.75, 'duration': .75, 'zoom': 1, 'focus': [20, 30]},
                {'id': 'text', 'type': 'text', 'at': 0, 'duration': 1, 'text': 'Текст', 'x': 0, 'y': 0, 'width': 200},
                {'id': 'audio', 'type': 'audio', 'at': 0, 'duration': 1, 'src': 'sound.wav'}]}]}

    def compile(self, plan=None):
        file = self.root / 'plan.json'
        file.write_text(json.dumps(plan or self.plan))
        return module.compile_plan(file)

    def test_shared_origin_and_trim(self):
        props, base = self.compile()
        self.assertEqual(props['durationInFrames'], 240)
        self.assertEqual(props['texts'][0]['from'], 60)
        self.assertEqual(props['audio'][0]['from'], 60)
        self.assertAlmostEqual(base['taps'][0]['time'], 2.2)
        self.assertEqual(base['camera'][0]['at'], 1.25)
        self.plan['groups'][0]['origin'] += .5
        newer, moved = self.compile()
        self.assertEqual(newer['texts'][0]['from'], 90)
        self.assertAlmostEqual(moved['taps'][0]['time'], 2.7)
        self.assertEqual((self.root / 'take/taps.json').read_text(), 'original calibrated taps')

    def test_cache_changes_for_recording_but_not_editorial_text(self):
        _, old = self.compile()
        self.plan['groups'][0]['events'][2]['text'] = 'Другой текст'
        _, edited = self.compile()
        self.assertEqual(old['signature'], edited['signature'])
        (self.root / 'take/rec.mp4').write_bytes(b'new-recording')
        _, changed = self.compile()
        self.assertNotEqual(old['signature'], changed['signature'])

    def test_duplicate_contacts_rejected(self):
        self.plan['groups'][0]['events'].append({'id': 'duplicate', 'type': 'tap', 'at': .2, 'x': 0, 'y': 0})
        with self.assertRaisesRegex(ValueError, 'Duplicate tap'):
            self.compile()

    def test_clipped_or_off_grid_text_rejected(self):
        for change in ({'duration': 4}, {'at': .001}):
            plan = copy.deepcopy(self.plan)
            plan['groups'][0]['events'][2].update(change)
            with self.assertRaises(ValueError):
                self.compile(plan)

    def test_unimplemented_screen_text_rejected(self):
        self.plan['groups'][0]['events'][2]['space'] = 'screen'
        with self.assertRaisesRegex(ValueError, 'composition-space'):
            self.compile()

    def test_swipe_shares_group_clock_and_invalid_duration_is_rejected(self):
        swipe = {'id': 'swipe', 'type': 'swipe', 'at': .5, 'duration': .4,
                 'from': [100, 400], 'to': [100, 150], 'radius': 100.8}
        self.plan['groups'][0]['events'].append(swipe)
        _, base = self.compile()
        self.assertEqual(base['layers'][0]['start'], 2.5)
        self.assertEqual(base['layers'][0]['from'], [100, 400])
        swipe['duration'] = -1
        with self.assertRaisesRegex(ValueError, 'Swipe travel'):
            self.compile()


if __name__ == '__main__':
    unittest.main()
