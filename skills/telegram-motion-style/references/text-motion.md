# Эффекты текста: Normal и Emotional

Use for an intentional text reveal in an app field, heading, label, chat message or
editorial text layer. Keep copy, font, weight, color, shaping, alignment and wrapping
owned by the host. This is a portable text technique, not a Kino-specific screen.

Названия эффектов: **Normal** и **Emotional**. Программные значения
`normal` и `emotional` используются в JSON/API. В существующих планах обновите значение стиля первого эффекта на `normal`.

## Choose the style and clock

- **Normal:** crisp rising letters and opacity, no blur, rotation or
  squash. Prefer for longer copy, repeated text and restrained interfaces.
- **Emotional:** local rise, blur, vertical squash and rotation,
  followed by one damped overshoot. Prefer short accents. Use on longer input
  when explicitly chosen, as in the owner's latest promo; assess density/cost.
- Emotional text is distinct from **эмоциональный фокус** (stars/stickers/emoji).
  Selecting this text style does not itself add decorative particles or a zoom.

| Clock | Stagger | Per-unit motion | First visible unit delay | Line-break pause |
| --- | --- | --- | --- | --- |
| **promo**, both styles | 18 ms | 300 ms | 18 ms | 0 |
| source Normal | 15 ms | 500 ms | 0 | 0 |
| source Emotional | 25 ms | 680 ms | 25 ms | 0 |

`promo` is the owner's requested reusable starting pace. The Emotional variant
was used and inspected in the latest production. Normal at the same pace is a
new adaptation of its source easing, not an effect already observed in that
video. These are configurable presets; choose slower timing or a longer final
reading hold for denser copy. Do not silently slow the whole application.

One global grapheme index crosses natural wraps and explicit line breaks. Spaces
and punctuation retain their slots; a newline adds no slot. Unit `i` starts at
`firstDelay + i*stagger`. Its motion overlaps subsequent units and may overlap the
next line. **Do not wait for the previous line's last letter to settle.** The total
reveal is `firstDelay + (N-1)*stagger + duration` for N>0; an empty string takes zero.
Do not restart at each word/line or insert a full-line crossfade. Keep completed
letters sharp and still. Add reading time after the last glyph and field geometry
are both settled; a callback alone does not establish recorded readiness.

## Property equations

Normal: `e = cubicBezier(0.2,0.8,0.2,1)(local/duration)`, opacity=e,
Y=`15*(1-e)` source pixels. Correctly invert the curve's X before evaluating Y.
ScaleY=1, rotation=0, blur=0 throughout; no filter track is needed.

Emotional maps the source selector onto the requested local duration:

```text
t = local * (0.680 / duration)
local <= 0:          p = 1
local >= duration:   p = 0, properties exactly natural
0 < t < 0.180:       p = 1 - t / 0.180
otherwise:           d = t - 0.180; w = 2π
                     p = (-1/0.180) * sin(d*w) / (exp(10*d)*w)
Y = 32*p; scaleY = 1 - 0.22*p; rotation = 12*p degrees
opacity = clamp(1-p,0,1); blur = 10*max(p,0)
```

Retain negative selector values for the overshoot in Y, scaleY and rotation;
clamp only opacity and blur. With duration300ms the source's 180ms linear phase
lands at~79.41ms and its first peak at~118.7ms. Restore the exact final state at
300ms. A generic library spring is not equivalent to this formula.

Distances are source pixels, not camera/video pixels or automatically points.
Adapters divide Y and blur by explicit `pixelsPerUnit`. Use1 for CSS pixels;
use the actual recorded pixels-per-window-point ratio (for example3) when
matching a native capture. Do not divide dimensionless scale/rotation. If the
art direction needs a larger or smaller glyph lift, declare that adaptation.
Blur mappings between CSS/SwiftUI/After Effects remain visual approximations.

## Included adapters

- [motion.mjs](../assets/text-motion/motion.mjs): deterministic property sampler,
  grapheme/word plan, duration and dense WAAPI keyframes. No dependencies. Use
  the sampler directly in Canvas, a frame-driven compositor or Remotion; use
  `elapsed=frame/fps-start` so rendering/seeking never starts another wall clock.
- [web.mjs](../assets/text-motion/web.mjs): one-shot text-only DOM/WAAPI integration.
  It preserves words/trailing spaces, provides complete readable copy alongside
  the hidden visual units, cancels on teardown and restores static text at the
  end. It never loops or adds an exit. It honors the host's reduced-motion
  preference without introducing a new live-check requirement.
- [TextMotion.swift](../assets/text-motion/TextMotion.swift): the same equations,
  clock and property values, independent of app services.
- [MotionTextRenderer.swift](../assets/text-motion/MotionTextRenderer.swift): SwiftUI
  TextRenderer for iOS18/macOS15+ and corresponding platforms. Tags extended
  grapheme clusters before wrapping; all runs of a cluster share its index.
  Host owns the clock and view lifecycle. It does not replace a TextField or
  send a message. Text interpolation preserves the per-cluster custom attributes.

Use a library explicitly named by the owner when one is requested. The independent
sampler can feed that renderer; the provided WAAPI adapter is an option, not a
permission to replace the application's requested library or architecture.

### Browser

Copy both `.mjs` files together into the target project:

```js
import { revealText } from './text-motion/web.mjs';
const reveal = revealText(document.querySelector('[data-reveal]'), {
  style: 'emotional', preset: 'promo', pixelsPerUnit: 1
});
const { cancelled } = await reveal.finished;
if (!cancelled) { /* host may start the separately chosen reading hold */ }
// On unmount, replacement or navigation: reveal.cancel().
```

Use a text-only host; do not flatten rich links or interactive child nodes. Word
wrappers keep break opportunities between words and preserve trailing spaces.
For explicit newlines, tabs or repeated spaces, use the host's intentional
`white-space: pre-wrap` treatment or a host-specific layout adapter. The browser
helper rejects ambiguous collapsed-whitespace layouts rather than silently
changing them. Do not change a real product's wrapping just to satisfy the helper.
Check actual typography: inline-block character units can affect ligatures and
kerning. Complex scripts, tabs and exact rich-text shaping need the host's layout
engine with per-cluster anchors. Do not claim universal typographic parity from
an ASCII demo. Intl.Segmenter (or a grapheme polyfill) is needed for non-ASCII;
plain Array.from does not preserve ZWJ emoji/combining sequences.

### SwiftUI/native interface

Copy the two Swift files into the app's existing target; do not change signing,
bundle ID, deployment target or framework just for the reveal. Keep the normal
UI on older OS versions. Read the SwiftUI skill when implementing a native view.

```swift
// Store this tagged Text while the copy stays unchanged; preserve the app's font.
let tagged = motionTaggedText(copy)
let timing = TextMotionTiming(style: .emotional, preset: .promo, pixelsPerUnit: 3)
// Host supplies elapsed seconds from its capture/display clock.
tagged.font(.body)
    .textRenderer(MotionTextRenderer(elapsed: elapsed, style: .emotional, timing: timing))
    .transaction { $0.animation = nil }
```

For an app field, preserve the real model binding and existing Send handler.
An authorized capture-only presentation can show tagged Text over a clean native
field while the real draft holds the complete query. Keep the original editor
available outside capture mode. Do not mutate the model once per rendered frame,
auto-send, or ship capture behavior into the ordinary product flow.

Measure wrapping with the app's real font and available width, after reserving
send/mode controls. Grow the field smoothly as the next line begins (or slightly
before it to avoid clipping its rise); anchor it like the original field.
Animate surface height separately from glyph clarity. Suppress implicit fades
between placeholder and animated ink, remove duplicate placeholder backing,
and retain a caret only when the actual input treatment calls for one. A full
layout with all future lines should not expose them early through an unclipped
field. The renderer alone does not solve field geometry or text selection.

### Recorded footage and editorial text

Choose the native adapter when the actual app can be instrumented within scope.
For supplied footage, render the same motion over a prepared text-free backing,
using glyph/cluster positions from the real host/font or extracted artwork.
Preserve the recorded text's origin, line breaks and material; erase original ink
with a valid repair instead of doubling it. Place screen-bound text under the
screen mask and subject it to the same camera projection as the footage.
Intentional object lift above the bezel is a separate layer decision.

A Canvas/Remotion/custom RGBA pass can evaluate `sample` per frame and draw each
cluster around its native center, transform origin near50%55%, opacity and blur
on that cluster only. Bake it into the calibrated screen input or extend the
chosen compositor with an explicitly implemented text track. **The bundled
`--layers` currently supports sprite/glint/swipe, not an automatic `type:text` or text
layout engine.** These adapters do not by themselves connect to `render.py`.
Do not claim that a transparent text video or background-video flag repairs and
anchors footage automatically. Keep repair, glyphs, field height, camera and
contacts on one documented composition clock.

## Capture reliability and checks

Inspect the actual encoded result, not only the clock completion. Fast live
rendering can coalesce phase updates. The latest production used a deliberately
slowed native take with per-frame phase metadata, then selected recorded frames
on the desired phase clock. This is a controlled acquisition technique for an
authored reveal; ordinary app gestures/transitions stay at their natural speed.
If phases are missing, re-capture rather than silently inventing glyph frames.
See [registration](registration.md) for duplicate-PTS/best-effort timestamp issues.

Check spaces, punctuation, Cyrillic/emoji clusters and line wrapping; continuous
left-to-right onset at the wrap; exact final state; no blur in Normal; Emotional
overshoot without negative blur/opacity; geometry/clipping and clean backing;
cancellation/replacement and the reading hold before the next action. Use code
checks and recorded media. Do not launch unrelated app UI/accessibility tests.

Pure helper checks: `node --test scripts/test_text_motion.mjs`. When Swift tooling is
available, the suite also checks numerical parity with the native motion core.
Type-check the SwiftUI adapter using the target SDK; a type-check is not a visual
acceptance or a guarantee that the host field/overlay has been integrated.

## Provenance and limits

Independent adapters of the documented approaches:
[Normal](https://github.com/mishanaer/deslop),
[Normal parameters](https://api.github.com/repos/mishanaer/deslop/git/blobs/23379c9caaff183767318e550cbd47ff5121f84d),
[Emotional](https://github.com/mishanaer/deslop),
[Emotional parameters](https://api.github.com/repos/mishanaer/deslop/git/blobs/41e2da326fd759a42dbc2f102a52a491fad2bfda).
Parameter blob SHAs checked3November2026: Normal
`23379c9caaff183767318e550cbd47ff5121f84d`, Emotional
`41e2da326fd759a42dbc2f102a52a491fad2bfda`.
The imported concept is the portable recipe, not exact numeric equivalence to
the original After Effects blur/FFX or recovery of Telegram's animation engine.
The 18ms/300ms preset and continuous-wrap preference are the owner's adaptation.
This addition is self-contained and does not need the Kino worktree, research
corpus or a separately installed text-effects skill to run.
