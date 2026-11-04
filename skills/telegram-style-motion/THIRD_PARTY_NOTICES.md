# Third-party notices

`scripts/vendor/compose.py` derives from
[finkoegor/telegram-style-motion](https://github.com/finkoegor/telegram-style-motion),
base commit `85aea23028517b3597bd2a37ad3679a055c3373f`.
Copyright (c) 2026 Egor Finko. MIT; full notice: [vendor/LICENSE](scripts/vendor/LICENSE).

The bundled version includes local changes for explicit trim bounds, frosted
annular blur, the reference tap/camera profiles and stationary backgrounds.
This distribution additionally rejects truncated output, removes automatic cloned
ending frames and provides a calibrated-input entrypoint in `scripts/render.py`.
It is a snapshot; no external project checkout is required at runtime.

Pillow and NumPy are runtime dependencies installed separately with their own
licenses. FFmpeg/ffprobe are external executables, not distributed here.

Apple device artwork, Telegram reference videos, application footage, audio and
private project sources are not included. Supply assets you have permission to use.
Telegram is a style reference; this project is not affiliated with Telegram or Apple.
