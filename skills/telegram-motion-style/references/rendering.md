# Portable rendering

Read this before rendering on another machine. Paths in the commands below are
user-supplied inputs, not locations assumed to exist. Run commands from the installed
skill directory, using Python 3.10+ with `requirements.txt` installed and FFmpeg/ffprobe
on PATH. Capture requires a real app project, macOS/Xcode and Simulator; rendering
existing footage does not require another application checkout.

## Prepare a calibrated composition input

Preserve raw footage and native logs. Normalize once to zero-based CFR, then detect
contacts and remove markers against those exact frames. Use
[registration](registration.md) for clock drift and coordinate conversion.

```sh
ffmpeg -i /path/to/raw-recording.mp4 -vf 'fps=60:start_time=0' -an \
  -c:v libx264 -preset fast -crf 16 /path/to/composition-input/rec.mp4
```

After a multi-input `concat` filter, explicitly set output `-r 60 -fps_mode cfr` (or the chosen composition rate). The concat output can lose its inferred rate: one checked Kino edit defaulted to 25 fps despite 60 fps filters on its branches. Rebuild from the raw sources when frames were dropped; do not upsample that rejected 25 fps export as a repair. Validate encoded frame count and PTS before contact calibration.

Do not normalize a second time after calibrating. Verify initial PTS and frame
spacing. Keep the same frame sequence for detection, cleaning, composition and audit.
Passing a metadata/CFR check alone does not establish that normalization preserved
native animation. Compare critical raw and normalized motion before calibration.
Earlier Simulator sources had duplicate PTS and decoder fallback to DTS that lost
parts of typing/holds. Input `-fflags +igndts` helped those particular sources;
use it only after demonstrating that failure, not as a universal normalization flag.

For a VFR source, apply `fps` before trimming, or normalize the entire recording
first. Seeking with `-ss` and then resetting the first decoded frame to PTS zero
can discard a static hold: the next encoded frame may be the UI reaction itself.
For selective export on the original clock, decode from the source start and use
`fps=60:start_time=0,trim=start_frame=START:end_frame=END,setpts=PTS-STARTPTS`.
Calibrate contacts on the resulting edited CFR input, not on nominal seek offsets.

For pacing revisions, re-edit the unframed screen footage and render a new continuous
camera/tap timeline. Cutting already-composited close and wide shots can reset the
camera pose or truncate a tap phase. Keep a scroll as one coherent movement; capture
the next action at its resulting position instead of inserting a return scroll solely
to match an older menu shot.

For a portable implementation of crisp or expressive glyph entry, read
[«Normal» и «Emotional» text](text-motion.md): it includes native/web adapters and the continuous
18ms promo clock. The following recording/repair constraints still apply.

For native progressive entry, capture actual per-character input in the field,
including caret and line-wrap/height changes. A bulk typing API may insert whole
chunks even when its name says “type”; inspect consecutive normalized frames before
using that take. For the references' soft glyph reveal, an explicitly planned overlay
can instead use the actual final field/text artwork: preserve typography and origin,
reveal staggered glyphs or line-wise clarity fronts with local blur/offset, and remove
the original text underneath without duplicate ink. Coordinate field accommodation
separately; do not imply physical keystrokes or a keyboard absent from the footage.
Consult [input and surfaces](corpus/input-and-surfaces.md) for checked variants.
Keep a readable completed-text hold before Send. In a chat sequence,
retain a visible pending/reveal beat and let the scroll settle before the next tap;
contact-to-contact spacing alone does not establish that the viewer can follow it.

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

An optional `--background-video /path/to/backdrop.mp4` supplies an animated local
backdrop on the same composition clock. It stays independent of camera moves;
trimming starts at that time in both videos. Supply enough frames through the
chosen ending: an exhausted backdrop fails instead of cloning its tail. A smooth
color flow can echo an actual sampled app accent when requested; this is art
direction, not a mandatory Telegram treatment.

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

An optional camera move field `"path": "projected"` interpolates the final image
translation together with scale rather than interpolating the source focus point.
Use it when both poses share a visible edge (for example, a bottom-aligned close
view returning to full device): that edge stays fixed throughout travel.
The omitted/default `"path": "focus"` preserves previous exports. This is a
composition choice, independent of the `reference` timing curve.

## Optional extracted objects and glints

Pass `--layers /path/to/layers.json` to add recorded-object focusing or small
four-point glints. Existing projects need no new argument. The schema is:

```json
{"version": 1, "layers": [
  {"type": "sprite", "asset": "button.png", "repair": "clean-plate.png",
   "screenRect": [24, 768, 44, 44], "start": 2.6,
   "enter": 0.24, "hold": 0.32, "exit": 0.28,
   "scale": 1.6, "offset": [0, 0], "dim": 0.18},
  {"type": "glint", "anchor": [55, 778], "start": 4.1,
   "duration": 0.35, "radius": 4}
]}
```

Coordinates are illustrative, in recorded window points. Asset paths resolve
relative to the JSON. Both artwork and repair must be RGBA: asset alpha isolates
the actual object; repair alpha limits replacement to its original footprint.
Capture the real backing while hiding only that object, retaining its layout.
Do not cover it with a guessed solid color on a translucent/material surface.

The repair runs before the phone is composited; the extracted object runs after
the bezel, so it can cross the physical boundary without a duplicate underneath.
Both share the camera projection. `offset` is a fraction of output width/height,
`scale` is relative to the object's original size, and `dim` shades the source
screen during emphasis. Enter uses cubic deceleration; exit uses smoothstep.
These are authoring choices, not an exact recovery of Telegram's source engine.
Glints use a sine envelope, four points and a soft glow. Time is the edited
footage clock. Check the return before the next contact and check the active
camera pose; numeric schema validation cannot establish a clean extraction.

A sprite can opt into `"exitCurve": "settle"` for one small scale undershoot
and exact restoration. Keep `offset: [0, 0]` for enlargement at its own center;
the default exit remains smoothstep. Optional `"sheen": {"start": 0.04,
"duration": 0.30, "strength": 0.24}` sweeps a soft light band through the actual
object alpha. Its start is relative to the sprite start, not a second video clock.
This does not create a second press or an unmasked rectangular light layer.

## Audio and verification

The renderer intentionally exports silent video. Do not discard supplied app sound
without explanation: align it in a separate FFmpeg mux step after measuring visible
onset on the encoded frames. Audio delay is relative to the **trimmed output clock**;
subtract `--start` from a source-video timestamp. Choose any authored delay for the
actual scenario. Preserve authored leading silence and distinguish file placement
from audible onset. Do not add unrelated music.

Check output metadata, expected frame count and full decode, for example:

```sh
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames \
  -of json /path/to/final.mp4
ffmpeg -v error -xerror -i /path/to/final.mp4 -f null -
```

Inspect extracted source/final contact frames as described in registration.md.
MP4 `nb_frames` is header metadata; the separate error-checked decode verifies
integrity. Use a counted decode only when the container lacks a reliable frame
count; avoid decoding the entire same file twice just to repeat this check.

Metadata and synthetic tests alone do not validate live-app UI alignment. Save
camera JSON, trim bounds, scale, background, frame anchors and actual checks with
each deliverable. No app UI test or live verification pass is required by this package.
