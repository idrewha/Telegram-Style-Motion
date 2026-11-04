"""Check portable presets against the bundled compositor; no app or UI required."""
import math
import sys
from pathlib import Path
import unittest

from motion_profile import camera_progress, tap_state

sys.path.insert(0, str(Path(__file__).parent / "vendor"))
from compose import Camera, reference_camera_progress, reference_ring_shape


class MotionProfileTests(unittest.TestCase):
    def test_camera_parity_and_single_restrained_overshoot(self):
        values = []
        for index in range(901):
            elapsed = index / 1000
            value = camera_progress(elapsed)
            self.assertAlmostEqual(value, reference_camera_progress(elapsed / 0.75), places=12)
            values.append(value)
        self.assertEqual(values[0], 0)
        self.assertEqual(values[-1], 1)
        self.assertGreater(max(values), 1.01)
        self.assertLess(max(values), 1.02)

    def test_projected_path_preserves_a_common_visible_edge(self):
        bottom = 930
        center = (210,456)
        target = (210,bottom-(bottom-center[1])/1.5)
        camera = Camera([(0,.75,1.5,target,'reference','projected')],center)
        for i in range(91):
            z,(_,fy)=camera.at(i/120)
            self.assertAlmostEqual(z*(bottom-fy),bottom-center[1],places=9)
        self.assertEqual(camera.at(1),(1.5,target))

    def test_tap_parity_and_contact_compression(self):
        for index in range(-500, 501):
            t = index / 1000
            for portable, compositor in zip(tap_state(t), reference_ring_shape(t)):
                self.assertAlmostEqual(portable, compositor, places=12)
        self.assertEqual(tap_state(-0.17), (1.0, 1.0, 0.58))
        self.assertEqual(tap_state(0), (0.5, 1.0, 0.58))
        self.assertEqual(tap_state(0.28)[1], 0)
        self.assertAlmostEqual(tap_state(0.28)[2], 0.78)

    def test_invalid_timings_are_rejected(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                camera_progress(value)
            with self.assertRaises(ValueError):
                tap_state(value)
        for duration in (0, -1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                camera_progress(0.1, duration)


if __name__ == "__main__":
    unittest.main()
