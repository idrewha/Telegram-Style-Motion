# BLE integration and compositor provenance

The original integration used a private BLE application with a compositor derived
from [finkoegor/telegram-style-motion](https://github.com/finkoegor/telegram-style-motion)
at `85aea23028517b3597bd2a37ad3679a055c3373f` (MIT).
A portable snapshot is now bundled in [scripts/vendor/compose.py](../scripts/vendor/compose.py),
with its [license](../scripts/vendor/LICENSE). Use [render.py](../scripts/render.py)
and the [rendering guide](rendering.md); an external BLE checkout is not required.

The historical app's Debug flags were `-openStable -stablePromo`, single pass.
`StablePromoCapture.swift` wrote `tmp/demo-taps.json` with `started`, `taps`,
`events` and optional error. Those files/handlers belong to that application and
are not included. Adapt capture to the user's actual app and existing handlers.
Do not alter native phase durations just to pace a promo.

A historical camera started at 2.1x on the upper search light, held one sweep,
and eased to the full device over 0.95 s before descent. These are scenario
parameters, superseded as shared defaults by the V4 preset. A historical first
reaction at 7.6167 s calibrated one take only. Never reuse it in another recording;
use [per-contact registration](registration.md) when clocks disagree.

Supply a matching device-bezel PNG and any application-owned sound locally.
The original bezel was an iPhone 17 Pro portrait asset with a transparent display
and its own Dynamic Island detail; Apple artwork and the application's audio are
not distributed. Preserve original take/logs and per-take settings with the result.
