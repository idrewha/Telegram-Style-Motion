"""Compare the fast screen mask to the original four-connected Pillow fill."""
import unittest

import numpy as np
from PIL import Image, ImageDraw
from vendor.compose import screen_hole


class BezelTests(unittest.TestCase):
    def test_matches_original_for_irregular_and_disconnected_transparency(self):
        rng = np.random.default_rng(7)
        samples = [rng.choice([0, 127, 249, 250, 255], size=(39, 33)) for _ in range(30)]
        # A narrow channel and a disconnected exterior, as on device artwork.
        enclosed = np.zeros((71, 45), dtype=np.uint8)
        enclosed[4:-4, 4:-4] = 255
        enclosed[8:-8, 8:-8] = 0
        enclosed[20:50, 15:30] = 255
        enclosed[34:37, 20:24] = 0
        samples.extend([enclosed, np.zeros((7, 9), dtype=np.uint8)])
        for index, alpha in enumerate(samples):
            with self.subTest(index=index):
                cy, cx = np.array(alpha.shape) // 2
                alpha[cy, cx] = 0
                old = Image.fromarray(np.where(alpha < 250, 255, 0).astype(np.uint8)).copy()
                ImageDraw.floodfill(old, (int(cx), int(cy)), 128)
                np.testing.assert_array_equal(screen_hole(alpha), np.asarray(old) == 128)


if __name__ == '__main__':
    unittest.main()
