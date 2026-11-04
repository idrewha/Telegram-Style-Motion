# Compositor provenance

The bundled compositor derives from
[finkoegor/telegram-style-motion](https://github.com/finkoegor/telegram-style-motion)
at `85aea23028517b3597bd2a37ad3679a055c3373f` (MIT).
A portable snapshot is bundled in [scripts/vendor/compose.py](../scripts/vendor/compose.py),
with its [license](../scripts/vendor/LICENSE).
Use [render.py](../scripts/render.py) and the [rendering guide](rendering.md);
an external application checkout is not required.

Supply the actual app recording, calibrated timeline, matching device bezel and
optional application-owned sound. Preserve native animation durations and keep
capture adapters and per-take diagnostics in the application's own workspace.
