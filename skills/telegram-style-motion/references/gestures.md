# Swipe indicators

Use the same frosted annulus as taps, above the bezel, projected through the
phone/camera transform. Do not add trails, arrows or particles without a request.

## Approved compact swipe preset

Preset `compact-swipe-v1` was explicitly approved by the owner on3November2026
for reuse in similar dynamic app demos: horizontal hero swipes and vertical
feed/catalog scrolling. Use it as the starting choice for those cases without
asking the owner to select the same rhythm again. Adapt travel to the actual
screen and source movement; it is not a universal setting for every video.

| Phase / property | Approved starting value |
| --- | --- |
| Output and review | 60fps; inspect every gesture frame,16.7ms per frame |
| Anticipation | 0.12s; fade into a fixed-size ring at the starting point |
| Horizontal visible contact/travel | 14frames =0.2333s |
| Vertical visible contact/travel | 16frames =0.2667s |
| Lift fade, both directions | 5frames =0.0833s, still following the content |
| Held ring | `steady:true`, `heldRadius:0.64`, hole ratio0.60; no size pulse |
| Base radius | screenWidth×0.24 in window points, shared tap material |
| Motion after lift | Short decelerating tail; about0.3s for the hero and0.6–0.65s for the measured lists, including lift fade |
| Residual list distance after the ring disappears | Modest: approximately20–33% of total travel in the approved example |
| Camera | Fixed scale throughout approach/contact/lift; reframe between gestures |

Pattern: brief approach → decisive short movement → early lift → small native
settling tail → clean reading. The finger does not accompany the entire scroll.
While visible, its per-frame displacement follows content one-to-one; for hero
crossfade/parallax it follows the measured transition phase. Preserve stationary
frames and use the same source-frame map for the footage and path. Reduce native
fling distance by capture when needed rather than hiding excess travel with cuts.

Choose source timing to achieve this perceived rhythm. The approved edit used
uniform2× hero,3× home-scroll and2.5× catalog-scroll retiming of complete motions.
Those multipliers describe that capture, not settings to apply blindly to new
footage. Do not stack independent easing or speed ramps onto the ring. Keep the
short contact and modest tail when adapting to a different screen or frame rate.
Do not transfer film names, tap coordinates, list distance or the16.35s total
clip duration to unrelated scenarios. Keep existing V4 camera/tap material,
legible settled pauses and a real2.5s final success hold. Verify the native
checkmark or other success state before ending an add/save demonstration.

Provenance: approved by the owner on 3 November 2026 after reviewing a real
Kino carousel/feed demo. The local source video, plan, frame map and review boards
are intentionally not distributed. These values preserve that authoring preference;
they do not claim independently reproduced evidence or Telegram engine parameters.

## Path authoring

Prefer a measured frame path, in window points, on the normalized footage clock:

```json
{"id":"scroll","type":"swipe","at":1.2,"duration":0.5,
 "from":[210,720],"to":[210,360],"radius":100.8,
 "path":[[0,210,720],[0.0166666667,210,712],[0.5,210,360],
         [0.6,210,330]],
 "steady":true,"heldRadius":0.64,"anticipation":0.2,"release":0.1}
```

Example only: production paths need a sample at every output frame. Each triple
is [seconds relative to at, x, y]. Times increase strictly from zero and cover
at least duration. Samples may extend through the release fade: do not freeze the
indicator while content is still moving under a fading contact. Before the first
sample and after the last, position is held. `to` is the position at duration.
`radius` is the tap-equivalent maximum, usually screenWidth×0.24. In steady mode
its multiplier stays constant (default0.64), as does the hole ratio; only opacity
fades on approach/release. This avoids a breathing or shrinking drag indicator.

For a list during visible contact, derive position from the same feature's
measured frame displacement: fingerY = initialY + contentY(frame) − contentY(start).
Track another feature with an overlapping frame when the first leaves the screen.
Check correlation/confidence and exclude obstructed or offscreen patches. This
is a visual alignment proxy, not recovered hardware touch telemetry. After lift,
let the content continue its native inertia without a pointer. End the lift fade
before the projected finger leaves the screen.

Finger contact duration is separate from the full content animation. For a short
flick, fade the indicator soon after the compact travel; do not leave it attached
until the list settles. Keep a modest residual distance and a short deceleration
after lift. For similar dynamic demos use the approved compact preset above. When retiming
source motion, retime the complete gesture uniformly and sample both footage and
indicator from the same frame map; record the chosen rate for that capture. Re-record when
the original inertia travels too far. Confirm an actual native success state in
the recorded ending before declaring an add/save action complete.

A hero crossfade/parallax does not translate like a list. Fit its actual transition
phase from the recorded artwork or reliable app telemetry, and drive the authored
finger path from that phase. Do not equate a small parallax offset to full finger
travel. State this distinction when reporting accuracy.

Legacy from/to-only events still use linear travel. Do not use an independent
linear interpolation when repairing a reported velocity mismatch. Preserve
stationary frames and the source motion curve. Keep camera scale fixed while a
swipe is visible. Do not cut or independently speed-ramp the middle of a coupled
scroll; trim idle waits outside the complete gesture and its settling tail.

Capture: warm the whole route, including paginated list data and images. Check
that the native scrollbar length stays stable before recording. Dense drag input
is preferable to coarse default steps: in the Kino capture,50pt input jumps
produced visible chunks. Increasing output fps alone cannot repair those jumps;
re-record if needed. Never repaint native UI to hide a loading artefact without
an explicit reason and disclosure.

Review every gesture frame at output60fps, including approach, contact, lift and
inertia. Use per-frame displacement comparisons plus consecutive exported-frame
boards or a slowed diagnostic; a few distant stills do not establish velocity
alignment. Remap all events after cuts and verify the final MP4, not only the plan.

Reference: [Telegram Tips538](https://t.me/TelegramTips/538), reviewed in
[input and surfaces](corpus/input-and-surfaces.md). Native
frames600/620/640 show a moving round cue following a reorder handle across the
bezel;660 shows the separate Save contact. This supports the moving-ring grammar,
not universal scroll timing or exact engine coefficients. Measured paths and a
constant drag radius are authoring choices for synchronization, not claims about
Telegram's implementation.

Checks: `python3 -m unittest discover -s scripts -p 'test_*.py'`.
