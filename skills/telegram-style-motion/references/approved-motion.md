# Owner-approved V4 motion preset

The owner explicitly approved the Bluetooth V4 result on 2026-10-27, including its
timing and spring-like dynamics, and asked to reuse that feel in future clips.
Use this authored preset as the starting point unless a current request or content
requires another rhythm. Earlier 2.0 / 2.4 s holds remain a gentler option; they are
not the current approved starting point. This preference comes from approval of our
V4 implementation, not a new claim about the Telegram reference animation engine.

## Reproduce the motion

Machine-readable constants: [approved-v4.json](../assets/motion-presets/approved-v4.json).
Portable executable curves: [motion_profile.py](../scripts/motion_profile.py).
Keep `owner-approved-v4` as a stable baseline: use per-take overrides or a newly named
preset for experiments rather than silently changing its coefficients. A later approved
revision can replace the default while retaining this baseline.
The helper contains only progress/material-envelope math. Use the bundled
compositor through [render.py](../scripts/render.py) for frames, bezel, blur,
projection and encoding; see [rendering](rendering.md).

- Reading: 1.2 s from continuous target/framing readiness to contact; 1.6 s for a
  sheet, 2.5 s settled ending. Extend for genuinely denser content. Tap anticipation
  is already inside those holds, leaving about 0.83 / 1.23 s of clean reading.
- Camera: main arrival around 0.4 s, one approximately 1.33% overshoot of travel,
  complete settlement at 0.75 s. Scale and position share one progress curve.
  Preserve the useful edge and horizontal center, and keep the backdrop stationary.
- Tap: keep the existing 0.65 s cycle and the separately animated thinning annulus.
  It is an authored cubic growth/compression/recovery profile, not a physical spring.
  See [tap motion](tap-motion.md) for the full material and contact contract.

For the camera, normalize elapsed time to u=elapsed/duration and set t=0.75u:

```
p = 1 - exp(-11*t) * (cos(8*t) + (11/8)*sin(8*t))
q = cubicEaseInOut(clamp((t - 0.60) / 0.15, 0, 1))
progress = p*(1-q) + q
```

Clamp completed motion to exactly 1. Do not clamp intermediate progress to 1: that
would remove the approved overshoot. The final blend stops residual drift and the
single small recovery avoids visible repeated bouncing. These are our authored
coefficients; do not advertise them as recovered Apple damping/stiffness settings
or map them blindly to a platform spring API.

Use `camera_progress(elapsed, duration=.75)` and `tap_state(relativeToContact)` from
the helper, or port the same curves and compare sampled outputs. A different
implementation is acceptable if it preserves the observed shape and timing.
The maintained BLE compositor's `curve: "reference"` and `--tap-profile reference`
matched this portable preset in sampled parity checks when it was recorded.

## Keep the scope clear

V4's cold contrasting palette is a useful example, not a requirement for every app.
The Bluetooth retry's 1.45 s narrowing belongs to its native payment state machine;
it must remain before ascent, but it is not a generic camera/tap spring parameter.
Preserve native app transitions and create pacing changes in reading holds.

Historical owner-local evidence (not distributed with this skill):
`bluetooth-payment-v4.mp4`, and `take-09/camera.json`, `render-settings.json`,
`camera-poses.png`, `final-tap-phases.png`, `compression-before-launch.png`,
`validation.json`. The compositor can evolve; compare against the saved
preset before claiming its current `reference` mode still reproduces the approved
version. Do not depend only on an external checkout path for the curve definition.
