import unittest
import json
import tempfile
from pathlib import Path
from gestures import swipe_state


class GestureTests(unittest.TestCase):
    def setUp(self):
        self.track = {'start': 1, 'duration': .4, 'from': [350, 300], 'to': [70, 300], 'radius': 100.8}

    def test_travel_and_restoration(self):
        a = swipe_state(self.track, 1)
        b = swipe_state(self.track, 1.2)
        c = swipe_state(self.track, 1.4)
        self.assertEqual(a[:2], (350, 300))
        self.assertAlmostEqual(b[0], 210)
        self.assertAlmostEqual(c[0], 70)
        self.assertIsNone(swipe_state(self.track, .7))
        self.assertIsNone(swipe_state(self.track, 1.7))

    def test_no_trail_after_release_and_bounded_material(self):
        for i in range(100):
            t = .79+i*.01
            v = swipe_state(self.track, t)
            if v is not None:
                self.assertTrue(0 <= v[3] <= 1)
                self.assertTrue(0 < v[4] < 1)
                if t > 1.4:
                    self.assertEqual(v[:2], (70, 300))

    def test_seek_does_not_accumulate_motion(self):
        before = swipe_state(self.track, 1.15)
        swipe_state(self.track, 9)
        self.assertEqual(before, swipe_state(self.track, 1.15))

    def test_measured_path_preserves_holds_and_moves_during_lift(self):
        track = dict(self.track, duration=.2, release=.1, steady=True,
                     path=[[0,350,300],[.05,350,300],[.1,320,300],
                           [.15,280,300],[.2,280,300],[.3,240,300]])
        self.assertEqual(swipe_state(track, 1.05)[:2], (350,300))
        self.assertAlmostEqual(swipe_state(track, 1.15)[0], 280)
        self.assertAlmostEqual(swipe_state(track, 1.15)[1], 300)
        self.assertAlmostEqual(swipe_state(track, 1.25)[0], 260)
        radii = [swipe_state(track, t)[2] for t in (.9,1,1.1,1.2,1.25)]
        self.assertTrue(all(r == .64 for r in radii))

    def test_nonuniform_source_velocity_is_not_replaced_by_linear_motion(self):
        track = dict(self.track, duration=.3, path=[[0,350,300],[.1,340,300],
                      [.2,250,300],[.3,70,300]])
        self.assertAlmostEqual(swipe_state(track, 1.1)[0],340)
        self.assertAlmostEqual(swipe_state(track, 1.2)[0],250)

    def test_frosted_material_preserves_center_and_uses_current_projection(self):
        from PIL import Image
        from layers import LayerPlan
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / 'layers.json'
            track = dict(self.track, type='swipe', radius=20,
                         **{'from': [40, 80], 'to': [140, 80]})
            file.write_text(json.dumps({'version': 1, 'layers': [track]}))
            plan = LayerPlan(file, 1, (220, 180))
            frame = Image.new('RGBA', (220, 180), (20, 60, 100, 255))
            plan.draw(frame, 1.2, lambda x, y: (x+20, y+10), 1)
            self.assertEqual(frame.getpixel((110, 90)), (20, 60, 100, 255))
            self.assertEqual(frame.getpixel((60, 90)), (20, 60, 100, 255))
            self.assertNotEqual(frame.getpixel((100, 90)), (20, 60, 100, 255))


if __name__ == '__main__':
    unittest.main()
