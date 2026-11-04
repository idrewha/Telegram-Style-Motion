#!/usr/bin/env python3
"""Render calibrated CFR footage with the V4 defaults; does not capture or sync UI."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_inputs(args):
    for executable in ("ffmpeg", "ffprobe"):
        if shutil.which(executable) is None:
            raise ValueError(f"{executable} must be available on PATH")
    if args.fps <= 0 or not finite(args.scale) or args.scale <= 0:
        raise ValueError("fps and recording pixels per point must be positive")
    try:
        size = tuple(int(v) for v in args.size.lower().split("x"))
    except ValueError as error:
        raise ValueError("size must be WIDTHxHEIGHT") from error
    if len(size) != 2 or any(v <= 0 or v % 2 for v in size):
        raise ValueError("H.264 output dimensions must be positive even integers")
    if not (finite(args.start) and finite(args.end) and 0 <= args.start < args.end):
        raise ValueError("Require finite trim bounds: 0 <= start < end")
    if any(abs(t * args.fps - round(t * args.fps)) > 0.0001 for t in (args.start, args.end)):
        raise ValueError("Trim bounds must align to the output frame grid")
    if not args.bezel.is_file():
        raise ValueError("Supply a matching bezel PNG with a transparent display")
    if args.out.exists() and not args.overwrite:
        raise ValueError("Output already exists; choose another path or pass --overwrite")
    if args.out.resolve() == (args.take / "rec.mp4").resolve():
        raise ValueError("Output must not replace the composition input")

    result = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height:frame=best_effort_timestamp_time", "-of", "json",
        str(args.take / "rec.mp4")], check=True, capture_output=True, text=True)
    metadata = json.loads(result.stdout)
    if len(metadata.get("streams", [])) != 1:
        raise ValueError("Composition input must contain one video stream")
    stream = metadata["streams"][0]
    pts = [float(f["best_effort_timestamp_time"]) for f in metadata.get("frames", [])]
    if not pts or not all(math.isfinite(t) for t in pts):
        raise ValueError("Input has no usable encoded frame timestamps")
    if any(abs(t - index / args.fps) > 0.0001 for index, t in enumerate(pts)):
        raise ValueError("Normalize input to zero-based CFR at --fps before calibrating/rendering")
    if round(args.end * args.fps) > len(pts):
        raise ValueError("Trim exceeds recorded frames; capture a real ending instead of cloning it")

    timeline = json.loads((args.take / "taps.json").read_text())
    taps = timeline.get("taps") if isinstance(timeline, dict) else timeline
    if not isinstance(taps, list):
        raise ValueError("taps.json must be a tap list or an object containing taps")
    previous = -math.inf
    for tap in taps:
        if not isinstance(tap, dict) or not all(finite(tap.get(k)) for k in ("time", "x", "y")):
            raise ValueError("Each tap requires finite time, x and y")
        if not previous < tap["time"] < len(pts) / args.fps or tap["time"] < 0:
            raise ValueError("Contacts must be ordered, distinct and inside recorded time")
        if not (0 <= tap["x"] <= stream["width"] / args.scale and
                0 <= tap["y"] <= stream["height"] / args.scale):
            raise ValueError("Tap coordinates must be in the recorded window's points")
        previous = tap["time"]
    if getattr(args, "layers", None):
        from layers import LayerPlan
        LayerPlan(args.layers, args.scale, (stream["width"], stream["height"]))
    if getattr(args, "background_video", None) and not args.background_video.is_file():
        raise ValueError("Background video must be an existing local file")
    if args.camera and not args.camera.is_file():
        raise ValueError("Camera must be an authored JSON file; auto-zoom is not the V4 default")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("take", type=Path, help="folder with normalized rec.mp4 and calibrated taps.json")
    parser.add_argument("out", type=Path)
    parser.add_argument("--bezel", required=True, type=Path)
    parser.add_argument("--scale", required=True, type=float, help="recording pixels per window point")
    parser.add_argument("--start", required=True, type=float, help="trim start in normalized video seconds")
    parser.add_argument("--end", required=True, type=float, help="captured ending in normalized video seconds")
    parser.add_argument("--camera", type=Path, help="authored moves with curve: reference; same video clock")
    parser.add_argument("--layers", type=Path, help="optional recorded-object and glint tracks on the video clock")
    parser.add_argument("--size", default="1920x1920")
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--share", type=float, default=0.94, help="full-device height / output height")
    parser.add_argument("--background", default="gradient", help="gradient, #hex, or a local image")
    parser.add_argument("--background-video", type=Path, help="optional animated backdrop on the composition clock")
    parser.add_argument("--colors", default="#c9d9ff,#e5d7ff,#bfeaff", help="gradient colors")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        if not finite(args.share) or args.share <= 0:
            raise ValueError("Phone height share must be positive and finite")
        check_inputs(args)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        sys.executable, str(Path(__file__).parent / "vendor/compose.py"),
        str(args.take), str(args.out), "--bezel", str(args.bezel),
        "--scale", str(args.scale), "--offset", "0", "--start", str(args.start),
        "--end", str(args.end), "--size", args.size, "--fps", str(args.fps),
        "--share", str(args.share), "--camera", str(args.camera) if args.camera else "none",
        "--ring", "telegram", "--tap-profile", "reference", "--static-background",
        "--no-shadow", "--background", args.background, "--colors", args.colors,
        *(["--layers", str(args.layers)] if args.layers else []),
        *(["--background-video", str(args.background_video)] if args.background_video else []),
    ], check=True)


if __name__ == "__main__":
    main()
