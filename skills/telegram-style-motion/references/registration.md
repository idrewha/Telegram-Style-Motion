# Spatial and temporal registration

Use this when implementing tap capture, diagnosing missed targets, or changing clip timing. Geometry, native callbacks and encoded video frames are separate measurements.

## 1. Choose and measure the visible target

A full-width row's geometric center can be empty space. Anchor an account-selection tap to its amount/name stack or another meaningful visible subview, while retaining the containing button's hit bounds. Prefer stable accessibility IDs or an explicit capture anchor over fragile subview indexes.

Wait for native readiness: enabled, interactive, visible, attached to a window, completed presentation, and settled geometry/opacity including animated ancestors. For a static contact, compare window-space geometry across consecutive display frames. Merely comparing a child's local frame to its model can miss an animated parent. Reset the reading timer when readiness is lost; time out with a recorded error instead of pressing blindly.

For an animating UIKit hierarchy, convert between presentation layers all the way to the visible window:

```swift
if let source = anchor.layer.presentation(),
   let destination = window.layer.presentation() {
    let center = source.convert(
        CGPoint(x: source.bounds.midX, y: source.bounds.midY),
        to: destination
    )
    let targetBounds = source.convert(source.bounds, to: destination)
    // Convert the button's hit bounds through the same presentation tree.
    // Log center, targetBounds, hitBounds and coordinateSource at contact.
}
```

If presentation layers are unavailable, wait for commitment or use model-to-model conversion only after confirming a settled hierarchy; record the fallback. Do not combine a presentation `position` with a model UIView conversion. Presentation geometry approximates the displayed state; it is not a measurement of the future encoded frame. [Apple presentation API](https://developer.apple.com/documentation/quartzcore/calayer/presentation()), [point conversion](https://developer.apple.com/documentation/quartzcore/calayer/convert(_:to:)-7dcke).

Log stable target identity, window dimensions/orientation, center in points, semantic target bounds, actual hit bounds, contact time, release time, and the source of geometry. Validate finite coordinates and center containment in the hit region. A bounding rectangle is only a coarse check for irregular/occluded controls; handler dispatch does not prove hit testing.

## 2. Preserve the coordinate chain

Keep named spaces: window points → recorded screen pixels → bezel display origin → output camera transform. Derive pixel scale from actual video size and logged window size; check both axes and orientation. Do not assume 3x for another simulator.

For the maintained compositor's uniform scale:

```
layerPoint = bezelDisplayOrigin + screenPoint * recordingPixelsPerPoint
outputPoint = cameraTranslation + layerPoint * currentLayerScale
outputRadius = radiusInPoints * recordingPixelsPerPoint * currentLayerScale
```

Use the exact same transform and camera time as the phone image. Account for cropping/rotation if present. A diagnostic crosshair belongs at that projected point. If a target intentionally moves during anticipation, record/sample its trajectory or wait for settlement rather than assuming a contact-time point describes the whole approach.

## 3. Separate contact from release

In a native Debug driver, log/show contact and highlight the control at touch-down; dispatch the existing action at its normal trigger. For a touchUpInside action, a short press such as the payment example's 120 ms leaves contact on the original UI before the reaction replaces or moves it. Log release separately. Do not delay controls whose actual behavior fires on touch-down or substitute this for gesture-driven interactions.

`sendActions` is native handler reuse, not a UITouch injection or a UI test. Keep the driver gated by a Debug launch flag, with one pass, timeout and cleanup. Restore capture-only appearance/status-bar overrides, terminate capture mode and relaunch without autoplay.

## 4. Calibrate on the frames that will be composed

Preserve the raw VFR recording and native log. Create one normalized copy, for example:

```sh
ffmpeg -i rec.mp4 -vf 'fps=60:start_time=0' -an \
  -c:v libx264 -preset fast -crf 16 rec-cfr.mp4
```

This duplicates/drops frames to obtain CFR; it does not fix disagreement with the app clock. Verify the normalized stream's initial PTS and frame spacing before treating `frameIndex / fps` as time. Use this same frame sequence for detection, cleaning, composition and audits. Do not correlate raw-VFR frame indexes with a differently decoded/fps-filtered sequence. [FFmpeg fps documentation](https://ffmpeg.org/ffmpeg-filters.html#fps).

A startup sync pulse before the trim anchors the beginning. For multi-action drift, put a brief unique-color patch into the same native transaction as each contact. The payment example uses 100 ms magenta pulses in a dedicated ROI; its coordinates/color threshold are examples, not defaults for other screens. Choose a region that cannot be mistaken for app content; use distinct IDs/colors when ordering is ambiguous. Log ROI, expected pulse sequence and times.

Detect pulse first/last frame indexes, not file birth time. Require the expected count/order and strictly increasing native/encoded times. If a pulse is absent, merged or ambiguous, stop that calibration and correct/re-record it; do not silently substitute old offsets. First-visible-frame timing has frame quantization and capture latency; at 60 fps the sampling interval is 16.7 ms, not proof of sub-frame input accuracy.

Remove patches only from their measured frame ranges. Prefer a removable margin/crop or a known-empty region. Black fill is valid only when that patch is genuinely black throughout the affected frames; it must not erase text, an animated glow or a gradient. Preserve raw evidence and inspect the cleaned composition frames for remnants or seams.

## 5. Keep clock mapping explicit

For native monotonic time `n`, encoded source time `v`, encoded sync origin `v0`, and composition trim `s`:

```
compositionContact = v - v0
outputContact = compositionContact - s
nativeClockResidual = (v - v0) - (n - nativeSync)
```

Measure residuals at multiple contacts. If they exceed the allowed output-frame tolerance or vary, one offset is insufficient. Anchor each contact to its measured encoded frame. Piecewise linear mapping between ordered native/encoded anchors can place intervening logged events, but those values remain estimates. It maps metadata, not playback speed; do not stretch native motion to fit the log.

Do not claim an unmarked reveal, camera boundary or sound is frame-calibrated merely because contact anchors fit exactly. For a critical reveal, add its own frame anchor or locate its visible onset in the recording; schedule sound from that onset plus the authored delay. For a moving/warped reveal, inspect its rendered travel rather than only final UIKit bounds; a final-position crop can miss the true appearance. State the visual onset criterion. Distinguish sound-file placement from its first audible signal: measure leading silence before deciding whether to retain or trim it; do not silently remove authored timing. Avoid blind extrapolation beyond the first/last anchor. In particular, select the final trim from actual completion and captured hold frames, excluding recorder padding; do not compute it from a drifting native end time. Keep all mapped events, camera starts, sound placement and trim bounds in documented time spaces.

## 6. Validate the complete composition

For each contact, inspect the same normalized/clean source frame used by the compositor and frames from the final MP4 immediately before contact, at maximum compression, and after release. Use the final output frame grid rather than claiming sub-frame precision.

A useful contact sheet overlays semantic bounds, hit bounds and a crosshair; annotate target ID, native center, source frame/PTS and output time. Also inspect the actual indicator on the final phone: a source crosshair does not test the bezel/camera transform, and a pre-contact screenshot can hide an indicator that arrives after the UI changes. Review marker removal in the composition input. Keep these diagnostic overlays separate from the delivered video.

Check reading holds against visible settlement in the recorded footage, plus camera/descent order, success/audio placement and actual final hold. Then check output size/fps/codecs/duration and full-file decode. Save an audit report that separates numerical consistency, visual media inspection and any checks not performed. Recorded-frame media QA does not authorize a separate live simulator UI-test/screenshot pass.
