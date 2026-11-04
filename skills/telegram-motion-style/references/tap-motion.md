# Reference tap motion and approved pacing

Use this when implementing or tuning the indicator and action pauses. The owner asked to adopt the observed tap behavior from `Live and Motion Photos_1.mp4` and `Mighty Polls_1.mp4`, while giving viewers more time between actions than those Telegram references do. The later owner-approved V4 uses 1.2 / 1.6 s readiness holds, while 2.0 / 2.4 s remains a gentler option. See [approved motion](approved-motion.md); explicit current requests take precedence.

## Evidence and limits

Both supplied references are 1080×1080, 60 fps; durations are 10 s and 20 s respectively. Frame-by-frame comparison shows the same growth/compression/recovery profile in both. Timing is approximate to encoded-frame resolution (16.7 ms); the minimum-size frame is a visual press anchor, not a measurement of physical touch-down. Absolute material opacity and the original animation engine cannot be recovered uniquely from the rendered files. Do not label the result as confirmed Apple Spring or claim exact damping/stiffness values.

Representative source times:

| Visual phase | Mighty Polls: question field | Live and Motion Photos: Live menu |
| --- | --- | --- |
| First visible appearance | 2.133 s | 3.633 s |
| Maximum diameter | 2.333 s | 3.833 s |
| Minimum diameter | 2.500 s | 4.000 s |
| Fading recovery, clearly visible | 2.633–2.700 s | 4.133–4.200 s |
| Essentially gone | 2.783 s | 4.283 s |

Measured outer radius in the 1080 px question-field example is approximately 167 px at maximum and 84 px at minimum; the Live example is approximately 165 px and 82 px. These are source-video pixels, not screen points or universal fixed output sizes. The fading recovery reaches roughly 70–75% of maximum radius. Around the peak and press, inner radius is approximately 55–60% of outer radius. The hole grows proportionally larger during disappearance, leaving a thinner ring.

## Reusable motion contract

Normalize maximum outer radius to 1.0. In authored clips align maximum compression with the measured contact time; preserve the separate release/action time from the native capture.

| Time relative to contact | Outer radius / maximum | Opacity envelope | Annulus behavior |
| --- | --- | --- | --- |
| About -0.37 s | About 0.45 | Starts at 0 and rises quickly | Appears softly |
| About -0.17 s | 1.00 | At authored peak | Inner/outer ratio about 0.55–0.60 |
| 0 s | 0.50 | Still at authored peak | Clearly legible compression |
| 0 to about +0.28 s | Recovers toward 0.70–0.75 | Falls smoothly to 0 | Inner/outer ratio approaches 0.75–0.80 |

The opacity envelope is a relative multiplier on the translucent material, not a command to make it opaque white. Blur only the annulus using the current composed frame after the camera transform; preserve its clear center and a restrained tint. A peak diameter around 48% of screen width reproduces the reference scale. Derive this in window points and project through the phone/camera transform, rather than using source pixels as points.

Shape the first growth as fast arrival with a soft slowdown near maximum, followed by a smooth reversal into a decisive compression and one smaller outward recovery. A spring or authored curves can implement this profile; matching the observed phases matters more than naming the animation API. Animate thickness and opacity separately from outer radius. The static indicator does not travel between controls. For an intentionally moving target, follow the trajectory guidance in [registration](registration.md).

Let native UI react at its real trigger while the indicator's tail fades. A touchUpInside control may react after release; do not shift the compression to that later callback or wait for the indicator to disappear before running the action. Do not invent a press duration from these MP4s; retain the native contact/release logs and frame calibration.

## Current approved rhythm defaults

- Ordinary state: wait 1.2 s from continuous actual readiness to the next contact.
- Information-rich sheet, menu or result requiring reading: start with 1.6 s, extending for content when useful.
- A sequence of simple actions without a transition: aim for 1.2 s between contacts. If content moves or readiness is lost, start a new readiness hold after settlement.
- Final result: capture a 2.5 s hold after it settles, extending when the result needs more reading time.

The 0.37 s anticipation is inside each readiness hold. For a 1.2 s hold, leave about 0.83 s of clean reading time, then show the indicator for the last 0.37 s before contact. For 1.6 s, the clean portion is about 1.23 s. Do not add another full hold after anticipation, or require the previous tail to disappear before starting the readiness clock; these intervals may overlap naturally. At 60 fps, -22/-10/0/+17 frames are useful approximate appearance/peak/contact/end anchors, with continuous interpolation between frames.

The reference's roughly one-second contact cadence is evidence of its original edit, not the default for this skill. Preserve the tap's compact dynamic while lengthening the quiet portions. Preserve native spring, light, scrolling and transition speed; create the extra time in recorded settled states. Explicit user timing overrides these defaults.

Historical project integration notes describe their own takes. When reusing their compositors, reconcile legacy constants with this profile and the current timing request; do not change app projects merely while maintaining this skill's documentation.
