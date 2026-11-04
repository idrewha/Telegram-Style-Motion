# Plan recorded footage and composited layers together

The deliverable starts from an actual application recording and a scenario. Some visible elements already live in that footage; others are added over it in the final composition. The owner explicitly asks for this distinction to remain part of research and authoring decisions across different applications.

## Separate observation from production choice

A flattened reference proves appearance and timing, not whether its author implemented an effect in the application or compositing software. Record `observedInReference` separately from `plannedLayer`; use `originConfidence: unknown` where provenance cannot be established. A visible particle, blur or floating card alone does not identify its original implementation.

For a new production, make a small layer plan for the meaningful objects/effects:

| Layer role | Source and responsibility |
| --- | --- |
| Recorded application | Actual interface, navigation, content, native gestures, loading and playback. Preserve this as the causal base. Identify effects already present so they are not duplicated by overlays. |
| Extracted real object | A mask/crop or supplied real asset from the recorded UI when selective focusing requires it. Preserve its changing content and original attachment; supply a clean plate or other valid occlusion repair where it leaves the footage. |
| Decorative overlay | Added tap indicator, stars, emoji, particles, glints or captions when requested. Own its entrance, hold and exit separately from the app's reaction. |
| Device and composition | Matching bezel, screen mask, background, shared phone/camera transforms, and explicit foreground/background stacking. These do not imply a change to app code. |

Do not invent an extraction just because decoration is needed. A star around a control can sit over intact footage. An extracted UI card requires a different plan: avoid leaving two copies visible, preserve text/material and provide a coherent return. When clean separation is unavailable, choose an achievable focus treatment or capture supporting material rather than hiding a broken removal with arbitrary blur.

For each added/extracted layer note only what the shot needs: source asset/frame range, anchor in source-screen coordinates, transform parent, draw order/mask, trigger on the calibrated edited clock, entrance/settling/reading/exit landmarks, and whether its content must keep animating. This can be a short table or structured record; it is not a requirement to fill a large form for every static pixel.

## Bind space and time to the recording

Use one calibrated edited-footage clock. Trim/retime mappings must move contacts, overlays and any audio consistently; a decorative timeline is not an independent reason to shift the native result. An overlay contact must lead the recorded reaction at the actual trigger, not follow a film that has already opened. Preserve native main-motion speed where practical and adjust settled holds to improve reading.

Track a moving target in the footage before applying the shared screen-to-device-to-camera transform. A zoom moves footage, extracted objects and source-linked indicators coherently. Composition-space elements such as the background stay independent unless explicitly animated. An effect may need an explicit handoff: follow a moving control on entry, then leave a decaying particle tail near the former position after the control navigates away. Do not silently attach that tail to unrelated incoming content.

Screen masking and foreground draw order are separate. Ordinary recorded content is clipped by the display; an intentional lifted object, ring or particle may draw above the bezel. A foreground object can still require occlusion by another foreground surface. Audit its full visible bounds, not just the control center.

## Check the assembled result

Inspect the same encoded moments in source and final composition: before contact, contact, first app response, overlap, settled result and effect exit. Check double images, mask seams, stale text, drifting anchors, wrong layer order, abrupt tail clipping and readability after all layers are combined. A correct isolated overlay does not prove the final montage works.

A captured rectangle carries its original backing. In the Kino revision, freezing a
status clock with a rectangular patch left old digits at its edge and a gray block
over the player; that optional patch was removed. Check extracted artwork against
every background it traverses, use a valid alpha/repair when separation is needed,
and avoid adding a cosmetic replacement that the shot does not require.

The bundled renderer handles calibrated footage, bezel/background, camera and tap rings. Its optional `--layers` plan additionally supports a real extracted RGBA object, its clean repair patch, shared camera projection and small four-point glints; see [rendering](rendering.md). Arbitrary animated stickers, complex inter-object occlusion and general mask tracking still require additional support. Capture-only app instrumentation may obtain a real clean plate; keep the editorial lift in the compositor.
