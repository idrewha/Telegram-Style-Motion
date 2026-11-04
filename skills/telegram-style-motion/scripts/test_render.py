"""Synthetic media integration checks; never launches or inspects an app UI."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

SCRIPT = Path(__file__).with_name("render.py")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/ffprobe required")
class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="motion-render-test-")
        cls.root = Path(cls.tmp.name)
        subprocess.run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=160x320:rate=60",
            "-t", "1.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.root / "rec.mp4")
        ], check=True)
        # Original synthetic artwork, never an Apple bezel or screenshot.
        bezel = Image.new("RGBA", (180, 340), (25, 25, 30, 255))
        ImageDraw.Draw(bezel).rectangle((10, 10, 169, 329), fill=(0, 0, 0, 0))
        bezel.save(cls.root / "bezel.png")
        (cls.root / "camera.json").write_text(json.dumps([
            {"at": 0, "duration": 0.75, "zoom": 1.3, "focus": [80, 130], "curve": "reference"}
        ]))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        (self.root / "taps.json").write_text(json.dumps({"taps": [{"time": 0.5, "x": 80, "y": 160}]}))
        self.out = self.root / f"{self.id().split('.')[-1]}.mp4"

    def render(self, *extra):
        return subprocess.run([
            sys.executable, str(SCRIPT), str(self.root), str(self.out),
            "--bezel", str(self.root / "bezel.png"), "--scale", "1",
            "--start", "0", "--end", "1", "--size", "256x256",
            "--camera", str(self.root / "camera.json"), *extra
        ], capture_output=True, text=True)

    def test_synthetic_export_has_exact_frames_and_decodes(self):
        result = self.render()
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
            "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_read_frames",
            "-of", "json", str(self.out)], capture_output=True, text=True, check=True)
        stream = json.loads(result.stdout)["streams"][0]
        self.assertEqual((stream["codec_name"], stream["width"], stream["height"]), ("h264", 256, 256))
        self.assertEqual(stream["r_frame_rate"], "60/1")
        self.assertEqual(int(stream["nb_read_frames"]), 60)
        subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(self.out), "-f", "null", "-"], check=True)

    def test_animated_backdrop_preserves_composition_clock_on_trim(self):
        background = self.root / "animated-background.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i",
            "color=red:s=256x256:r=60:d=1.5,drawbox=x=0:y=0:w=iw:h=ih:color=blue:t=fill:enable='gte(t,0.5)'",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(background)
        ], check=True)
        result = self.render("--background-video", str(background), "--start", "0.5")
        self.assertEqual(result.returncode, 0, result.stderr)
        pixel = subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(self.out), "-frames:v", "1",
            "-vf", "crop=2:2:0:0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
        self.assertLess(pixel[0], 10)
        self.assertGreater(pixel[2], 230)

    def test_trim_cannot_clone_an_unrecorded_tail(self):
        result = self.render("--end", "2")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exceeds recorded frames", result.stderr)
        self.assertFalse(self.out.exists())

    def test_wrong_frame_rate_is_rejected_before_rendering(self):
        result = self.render("--fps", "30")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Normalize input", result.stderr)
        self.assertFalse(self.out.exists())

    def test_existing_output_is_preserved(self):
        self.out.write_bytes(b"existing output")
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.out.read_bytes(), b"existing output")

    def test_out_of_bounds_contact_is_rejected(self):
        (self.root / "taps.json").write_text('[{"time": 0.5, "x": 999, "y": 160}]')
        result = self.render()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("coordinates", result.stderr)
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
