# Payment account/error/retry integration

This is a historical owner-local integration, not a bundled runnable app.
Its app sources, captures, account data and diagnostic artifacts are not distributed.
Paths below are relative to that private example project and explain the mechanism;
do not try to open them on another user's machine. Use the bundled
[rendering workflow](rendering.md) for new projects and keep their capture adapter
in that project's own workspace. The payment renderer was an adapter to the
[BLE compositor](ble.md).

## Native capture and adapter

- Debug driver: `BluetoothPayment/Sources/Animations/Stable/Viper/View/BluetoothPromoCapture.swift`, enabled by `-bluetoothPromo`; `StableViewController` starts it after launch settles. Capture reuses shipped control handlers, not injected physical touches.
- Recorder: `scripts/Promo/record.py`; it starts recording after app launch, restores appearance/status overrides and returns to ordinary launch without autoplay.
- Renderer: `scripts/Promo/render.py`; it normalizes footage once, detects startup/contact pulses, creates a clean composition input and mapped timeline, renders with the maintained compositor (legacy and measured-reference profiles), and muxes the app's provided success sound.
- Source-frame diagnostic: `scripts/Promo/audit_taps.py`; it marks centers/bounds on the clean source used for composition. Final-video contact frames still require inspection; this script alone does not validate the composed indicator or UIKit hit testing.

These are scenario-specific scripts: account IDs, capture ROIs, thresholds, paths and initial state need adaptation. Do not assume the checkout, volume mount or uncommitted Debug helper exists in another environment.

This revision keeps balances visible and has no eye tap. Native holds: 2.0 s before the first payment, 2.4 s to read the account sheet, 2.0 s before retry. Contact and touchUpInside release are separated by 120 ms. A 1.7 s wide-camera reading beat follows the 0.95 s ease-out before descent. Preserve native light phase durations.

## Observed failure and verified correction

The account row's former full-width center was x=201 pt, while its amount/name stack is centered at approximately x=123.33 pt on this 402×874 pt simulator. The two pay-button centers are (201, 788) pt. These are measurements of this take, never reusable coordinates for another layout.

In `Artifacts/BluetoothPaymentPromo/take-05/sync.json`, startup origin is 5.283333 s in the normalized source. Contact measurements:

| Target | Native contact (s) | Encoded source (s) | Source relative to sync (s) | Residual vs native (approx.) |
| --- | ---: | ---: | ---: | ---: |
| payInsufficient | 9.335302 | 14.616667 | 9.333333 | −2 ms |
| selectAccount | 13.144431 | 18.433333 | 13.150000 | +6 ms |
| paySuccess | 15.484565 | 20.566667 | 15.283333 | −201 ms |

This demonstrates why an otherwise plausible single startup offset missed the last press. It does not establish a general cause in Simulator/FFmpeg. Per-contact encoded pulses anchor the actual frames; normalization alone does not remove native/video clock disagreement.

Startup pulse: [60,160,24,24] pt; contact ROI: [40,300,8,8] pt, magenta for 100 ms. The adapter removes only the contact pulse frame ranges over a black patch. Verify that assumption for any changed app scene. The raw recording/log stay untouched.

## Artifacts and limits

Previous revised output: `Artifacts/BluetoothPaymentPromo/bluetooth-payment-v2.mp4`, 19.2 s, 1920×1920, H.264/AAC, 60 fps.

Under `Artifacts/BluetoothPaymentPromo/take-05/`:

- `rec.mp4`, `taps.json`: original source and native log.
- `rec-cfr.mp4`, `sync.json`: normalized frames and detected contacts.
- `composition-input/rec.mp4`, `composition-input/taps.json`: cleaned source and mapped timing.
- `camera.json`, `render-settings.json`, `amber-background.png`: composition inputs.
- `tap-centers.png`, `tap-registration.json`: source-frame alignment evidence.
- `composed-contacts.png`: contact frames extracted from the final MP4.

The amber plate has a dim diagonal shaft and diffuse spill, following the existing camera parallax; the app beam is brighter. This is an art direction example, not a global orange background requirement.

The 19.2 s export retains actual recorded ending frames. During this revision a short real-footage tail was rendered separately and concatenated (`extend-tail.py` and `composed-tail.mp4` in the take); the maintained adapter now selects the captured ending directly. It is not a freeze-frame extension.

Verified in this work: app build, script syntax, source/final contact-frame inspection, media metadata and full decode. Contact anchors are measured, but the adapter still estimates other native events by interpolation/extrapolation; visible success/audio onset was not independently frame- or sample-verified. Apply the stronger reveal/hold guidance in [registration](registration.md) for subsequent exact audio/timing work. No live UI-test pass is implied.


## Updated skill rebuild (take-06)

`Artifacts/BluetoothPaymentPromo/bluetooth-payment-v3.mp4` is the measured-reference
profile rebuild: 19.333 s, 1920 square, 60 fps, H.264/AAC. The maintained compositor now
accepts `--tap-profile reference` while preserving legacy motion as its default.
Peak outer radius is 0.24 × window width (96.48 pt in this take); the independently
animated hole ratio runs from 0.58 to 0.78. Contact stays registered to encoded frames.

Yellow pulses mark readiness, magenta marks contacts and cyan marks completion.
Seven encoded anchors measured reading holds of 2.0167 / 2.4000 / 2.0167 s.
The driver records 2.8 s after completion; trimming retains 2.5 s after the recorded
success region matches its settled appearance, without a cloned tail.

A crop of final UIKit icon bounds was insufficient to detect visible onset: the
Metal handover moves the glyph. The revised detector covers its travel and uses
white-face/black-check contrast along vertical offsets, sustained for three frames.
`success-timing-audit.png` documents the operational 5% contrast onset and final state;
this is an explicit visual criterion with frame resolution, not exact physical latency.

The complete sound file is placed 0.14 s after that onset. At a -50 dB threshold the
provided asset contains about 107 ms of leading silence, retained as authored; file
placement and first audible signal are distinct measurements.
`visual-timing.json`, `sync.json`, `final-tap-phases.png` and render settings preserve
these decisions. See the actual run report for which checks have completed.


## Faster, contrasting rebuild with app-side retry fix (take-09)

Latest clip: `Artifacts/BluetoothPaymentPromo/bluetooth-payment-v4.mp4`, 15.3667 s,
922 frames at 60 fps, 1920 square H.264/AAC. The owner's current request explicitly
overrides slower defaults for this clip: holds 1.2 / 1.6 / 1.2 s (encoded 1.2167 /
1.6000 / 1.2167). Keep the 2.5 s recorded final hold. A stationary ice-blue/lavender
backdrop contrasts the black phone and warm beam. Upper detail is 68.5% video width;
the undistorted full device is 45.98% width and 94% height. The maintained camera
supports a reference curve: fast main displacement in ~0.4 s, one ~1.33% travel
overshoot and settlement by 0.75 s. Phone, targets and radii use the same transform.

The user explicitly requested a production-code correction as well: a successful
retry in the insufficientFunds demo was resolving immediately because the controller
used the original scenario's flag after the account had changed. StableViewController
now derives anticipation from actual funds: an insufficient attempt still rejects
immediately; a funded retry waits for the configured 1.45 s confirmation narrowing
before launch. A regression checks pending confirmation on the funded retry, and
all 55 PayTests passed. Recorded source frames in
`take-09/compression-before-launch.png` independently show narrowing then ascent.

Readiness pulses changed from yellow to green, with markerColors logged explicitly:
the longer confirmation sequence yielded four yellow detector runs for three real
readiness events in a rejected take. The new take passed strict counts/order with
seven stage markers. Preserve those rejected sources; do not relax count checks to
force a calibration through. This faster cadence and palette remain clip-specific.

`take-09/camera-poses.png`, `final-tap-phases.png`, `projection-audit.json` and
`validation.json` hold the media checks. The complete peak tap rings fit the frame.
No separate live UI automation/screenshot verification pass was performed.
