# Portable rendering

Read this before rendering on another machine. Paths in the commands below are
user-supplied inputs, not locations assumed to exist. Run commands from the installed
skill directory, using Python 3.10+ with `requirements.txt` installed and FFmpeg/ffprobe
on PATH. Capture requires a real app project, macOS/Xcode and Simulator; rendering
existing footage does not require the original BLE or payment projects.

## Prepare a calibrated composition input

Preserve raw footage and native logs. Normalize once to zero-based CFR, then detect
contacts and remove markers against those exact frames. Use
[registration](registration.md) for clock drift and coordinate conversion.

```sh
ffmpeg -i /path/to/raw-recording.mp4 -vf 'fps=60:start_time=0' -an \
  -c:v libx264 -preset fast -crf 16 /path/to/composition-input/rec.mp4
```

Do not normalize a second time after calibrating. Verify initial PTS and frame
spacing. Keep the same frame sequence for detection, cleaning, composition and audit.

The input directory must contain:

- `rec.mp4`: normalized, marker-cleaned source at 60 fps starting at PTS zero.
- `taps.json`: ordered contacts on that video's clock, with window-point coordinates.

For example, on a **hypothetical** 1206×2622 recording of a 402×874 point window:

```json
{
  "taps": [
    {"time": 1.2, "x": 201, "y": 788},
    {"time": 3.6, "x": 123.33, "y": 420}
  ]
}
```

These values illustrate the format; measure your own targets. `time` is encoded
touch-down time in the normalized video, not touchUpInside, release, or an uncorrected
native timestamp. Preserve the original logs elsewhere. `--scale 3` in this example
means **recording pixels per window point**, not camera zoom or Retina scale guessed
from the device name. Check both axes and orientation; cropped/rotated inputs need
an adapted coordinate mapping.

## Render

```sh
python3 scripts/render.py /path/to/composition-input /path/to/final-silent.mp4 \
  --bezel /path/to/matching-portrait-bezel.png --scale 3 \
  --start 0 --end 10 --camera /path/to/camera.json
```

Choose actual trim bounds on the 60 fps grid. The example ending of 10 s is not
inferred from the contacts: measure the settled result and retain 2.5 s of recorded
hold after it. The renderer rejects unavailable tail frames and never pads a cloned
ending. It also rejects non-CFR timestamps, unordered/out-of-range contacts and an
existing output unless `--overwrite` is explicit. It does not prove that the supplied
bezel matches the device, that a target is semantically correct, or that the final
hold begins at a settled state. Check those against the real capture.

The entrypoint sets V4 tap motion, frosted material, stationary background, no added
phone shadow, 1920 square / 60 fps and a full-device height share of 0.94. Supply a
matching bezel PNG with a transparent screen and preserve its aspect ratio. Exact
width and detail-pose framing depend on that artwork. `--background` accepts a local
image, `#hex` or `gradient`; `--colors` changes gradient colors.

The underlying compositor is [vendor/compose.py](../scripts/vendor/compose.py),
with its [MIT notice](../scripts/vendor/LICENSE). Its legacy automatic timing and
defaults are retained for compatibility; use `render.py` for new calibrated V4 work.

## Camera plan

Omit `--camera` for a steady full-device shot. Add only useful transitions. A plan
is a JSON array; numeric `at` values and contacts use the same normalized video clock:

```json
[
  {"at": -0.75, "duration": 0.75, "zoom": 1.49, "focus": [201, 280], "curve": "reference"},
  {"at": 4.0, "duration": 0.75, "zoom": 1.0, "focus": [201, 437], "curve": "reference"}
]
```

This illustrates an initial upper detail already settled at time zero, followed by
a full-device view. These focus values suit only the hypothetical window above;
derive your own from the actual bezel/screen transform. `focus` is in window points;
`zoom` is relative to the full-device scale set by `--share`. The curve includes the
settling tail. Keep moves non-overlapping and use numeric times rather than legacy
`tapN` shorthand. Check the composition and complete tap-ring reach using extracted
frames from the actual output. See [camera motion](camera-motion.md).

## Audio and verification

The renderer intentionally exports silent video. Do not discard supplied app sound
without explanation: align it in a separate FFmpeg mux step after measuring visible
onset on the encoded frames. Audio delay is relative to the **trimmed output clock**;
subtract `--start` from a source-video timestamp. The historical BLE 0.14 s delay is
scenario-specific. Preserve authored leading silence and distinguish file placement
from audible onset. Do not add unrelated music.

Check output metadata, expected frame count and full decode, for example:

```sh
ffprobe -v error -count_frames -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames \
  -of json /path/to/final.mp4
ffmpeg -v error -xerror -i /path/to/final.mp4 -f null -
```

Inspect extracted source/final contact frames as described in registration.md.
Metadata and synthetic tests alone do not validate live-app UI alignment. Save
camera JSON, trim bounds, scale, background, frame anchors and actual checks with
each deliverable. No app UI test or live verification pass is required by this package.
