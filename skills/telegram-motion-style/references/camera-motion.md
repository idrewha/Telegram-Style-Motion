# Reference composition and camera motion

Read when composing upper/lower phone details or deciding whether to move the camera. This is a measured example, not a requirement to use all poses in every video. Use the current approved readiness holds in SKILL.md and [tap motion](tap-motion.md).

## What the three references establish

| Reference | Composition lesson |
| --- | --- |
| Live and Motion Photos_1.mp4 | A sustained frontal close view works across a complete sequence; the phone stays centered, about 68–69% of video width, with about 4–5% top margin and the lower corpus cropped. Interface transitions happen within the stable bezel. |
| Mighty Polls_1.mp4 | The same stable large-phone composition supports a longer multi-action flow. Scrolling, keyboard/layout changes and new sheets do not require following every action with the camera. |
| Live Stories.mp4 | Three coherent poses establish context and focus on bottom controls; scale/translation change at meaningful scene boundaries, with long stationary stretches between. |

In the first two sources the full visible corpus is not vertically centered: its top is deliberately anchored near the video top, and the phone continues below the frame. Their roughly 15–16% side margins and large screen area support readability. Color fields outside the phone echo the chat environment without introducing additional objects. Some low-positioned tap rings are clipped by the video edge; for authored clips, allow extra gesture clearance when the full tap needs to be legible.

This coverage supports both a single static composition and purposeful camera changes. The Live Stories geometry below is a reproducible example, not evidence that all three videos use the same full-phone height or the same internal UI layout.

## Source and measurement limits

User-supplied `Live Stories.mp4`: 18 s, 1080×1080, 60 fps, no audio stream. Geometry was inspected in source frames and estimated from the dark bezel silhouette at settled poses and through the three camera moves. Compression, antialiasing, reflective edges and overlay occlusion create roughly 1–3 px boundary noise. Frame times have 16.7 ms sampling. Do not infer exact Apple spring API parameters or physical input timestamps from the encoded footage.

## Three reusable poses

All three remain frontal and horizontally centered. Background stays in the composition's coordinate space.

| Pose | Settled source example | Corpus width / video width | Visible edge |
| --- | --- | --- | --- |
| Upper detail | 0.00 s | About 68.5% (739 px including side details) | Phone top about y=46 px (4.3%); bottom outside the video |
| Full device | 2.50 s | About 45.5% (491 px) | Top about y=31 px; bottom about y=1048 px; centered vertically |
| Lower detail | 4.00 s | About 68.5% (739 px) | Phone bottom about y=1033 px (4.4% bottom margin); top outside the video |

The two detail views are approximately 1.5 times the full-device scale. Their difference is a vertical translation of roughly half the square video's height. A convenient reconstruction places the device center at (0.50W, 0.75H) for upper detail, (0.50W, 0.50H) for full device and (0.50W, 0.25H) for lower detail, with scales 1.5 / 1.0 / 1.5. Those center values are inferred from the measured silhouette, not supplied project coordinates. Preserve the actual bezel aspect ratio; adapt scale/translation to another device rather than stretching it to force the example bounds.

The lower pose leaves the input/reaction controls around 84–85% of video height and preserves the bottom bezel. Native keyboard and sheet changes happen inside this stable pose. A sheet moving upward is not evidence that the camera moved.

## Source timeline

| Source time | Camera and content |
| --- | --- |
| 0.00–1.50 s | Upper detail on the chats/story row; first indicator begins around 1.13 s, minimum near 1.50 s |
| About 1.50–2.25 s | Upper detail to full device; story opening overlaps the camera move; most camera displacement is complete by about 1.90 s |
| About 2.25–3.00 s | Full-device hold, about 0.75 s after the small settling tail; scene video continues moving naturally |
| About 3.00–3.75 s | Full device to lower detail; most displacement is complete by about 3.40 s; the message-control indicator starts around 3.13 s and compresses near 3.50 s |
| About 3.75–17.00 s | Lower pose remains fixed through comments, reactions, keyboard, slider sheet and confirmation |
| About 17.00–17.80 s | Lower detail directly back to upper detail at essentially unchanged scale, while the story closes |
| About 17.80–18.00 s | Brief return to the opening composition, supporting a loop |

The opening context bridge uses a full-device view; the closing return is a direct vertical reframe. Do not force every upper/lower change through the full-device pose.

## Motion shape

Main travel takes about 0.35–0.45 s, with a small spring-like residual settling through roughly 0.70–0.80 s total. Approximate progress in the first zoom-out, derived from bezel width relative to the settled endpoints: 43% by +0.10 s, 82% by +0.20 s and 98% by +0.30 s. The curve then slightly passes the target and relaxes back.

At the zoom-out's smallest point around 1.90–1.98 s, the measured width is about 487 px versus the settled 491 px. In the final upward reframe, the returning phone top passes the settled y≈46 px to y≈53 px around 17.42–17.47 s, then returns by about 17.80 s. This is a restrained overshoot, about 1% of the vertical travel in that return. Pixel estimates do not identify a unique spring implementation.

Drive scale and translation together along a coherent path. During the first move, the top remains near the upper edge as the phone shrinks into the square. During the second, the phone enlarges with the bottom remaining near the lower edge. For the final return, hold scale and move vertically. The backdrop does not need to zoom with the phone.

## Coupling with actions and slower authored pacing

The reference overlaps anticipation with camera arrival: the indicator may appear while the camera still travels, with compression near the end of its main motion. This is useful evidence, not permission to put an authored press on an unreadable moving target. In the owner-approved V4 rhythm, count the 1.2 / 1.6 s readiness hold after the target and framing settle; anticipation occupies the last 0.37 s of that hold. Preserve the compact camera transition and lengthen the quiet state after arrival instead of slowing the whole move.

Project an indicator's position and radius through the device's current per-frame transform, including during a camera move. A fixed point in the native screen is not fixed in the output video while the camera moves. Sample annular blur from that current composed frame; do not plant the indicator at the camera's final coordinates before the phone gets there. Use [registration](registration.md) for source/input timing and coordinate calibration.

Observed source action beats include opening at about 1.50 s; comments at 3.50 s; row/reaction taps near 4.50 and 5.50 s; a rapid star-reaction sequence starting around 6.50 s; input at 10.00 s; highlight control at 11.50 s; slider interaction around 12.65–13.75 s; confirmation near 15.00 s. These are visual anchors, not recovered physical touch logs. The reference often uses about one second between discrete actions and has only a short pause after camera arrival. Use the current approved holds for authored clips; 2.0 / 2.4 s is an optional gentler rhythm.

Maintain the lower camera pose throughout related bottom-control actions. Keyboard rise, sheet opening, slider feedback and particles are native/content animation; they do not each require a new zoom. After the result, use the owner's 2.5 s settled final hold unless explicitly making a differently paced loop. The source's approximately 0.2 s ending hold is not that default.


## Approved implementation

The owner approved our V4 camera dynamics and timing on 2026-10-27 and requested
future reuse. Use [approved motion](approved-motion.md) for the exact authored curve,
portable implementation and preset. Source measurements above remain historical
evidence; approval applies to our implementation rather than a claimed Apple API.


## Whole-interface/mockup zoom: choose the shot before its curve

The owner explicitly identifies awkward zooms in prior generations as a quality problem. Study and plan whole-device camera motion as its own entity, alongside local object focusing. The physical frame, recorded interface and attached overlays must share the same camera transform. An enlarged card inside a stable bezel is not evidence of this whole-device zoom.

For each intended move, state the feature/detail it explains, the source target bounds, starting and ending device poses, and where that target should land in the output. Choose a pivot/path that keeps the target legible **during** travel. Scale and translation need a coordinated path: center-only scaling can push a bottom control out of frame, and a late corrective pan makes one move feel like two unrelated motions. Preserve useful context around the target and enough room for the full indicator/focus silhouette. Do not infer the correct pivot from a generic phone center.

Use a few purposeful poses with stable intervals. A small choice may warrant a closer view; a delivered result may warrant a wider view. Keep related choices in their established view while that view serves them. Timing is separate: main arrival, overshoot extremum, residual settlement, readable hold, anticipation and native response each have their own landmark. Preserve the owner's spring-like feel where a camera move is used, with continuous position/scale and restrained overshoot; do not reset the camera on cuts or repeatedly wobble it during reading.

Inspect the rendered target path and the outer bezel together at departure, mid-travel, main arrival, overshoot and rest. Check velocity continuity at adjacent moves/cuts, coherent screen/bezel geometry, registration of overlaid rings/particles, visible control context and no corrective jump at the end. A smooth scale curve alone does not certify a well-composed zoom. For this workflow the approved V4 curve is an authoring choice; the reference's exact original engine remains unknown.

### Recently re-reviewed camera examples

[GIF captions558](https://t.me/TelegramTips/558) holds a lower-detail pose for local editing, then widens with Send to reveal delivered GIF/caption context. Native straight-rim proxy1262→841px gives~1.5006detail/wide ratio, center~960px. Camera-out starts360,10/50/90%travel at362/366/371, near-final378, width stable389. Main arrival and settlement differ. Return starts480 during editorial grain reset. The tiny width overshoot is within2–4pxmeasurement uncertainty, so it does not independently establish bounce. Whole525-frame pass and11full-context camera anchors were checked.

[Telegram login560](https://t.me/TelegramTips/560) reframes upward toward lower controls270–300 while app cards exchange horizontally inside. The540-scaled straight-rim span344→329px (~.956ratio,±1–2px) rejects an initial constant-scale interpretation. A small scale change combined with translation can do the narrative job; do not force every reframe to use1.5x. The lower pose remains stable during subsequent choices, then the initial framing returns~510–540. Whole690-frame pass and15full-device anchors were checked.

These examples refine composition decisions; the completed 50-source visual study is indexed in the corpus library. The historical Live Stories filename remains unlocated. Corpus547 now has a complete1080-frame dense visual pass and48native anchors matching its three-pose feature sequence and timing; historical-file byte identity is not established. Earlier numeric curves retain their historical measurement status rather than being presented as a new continuous fit.

###574: direct vertical reframe at unchanged width

[Communities574](https://t.me/TelegramTips/574), full1110-frame visual pass, distinguishes physical reframe from concurrent panel growth. A lowest-side-button silhouette proxy moves0px at594 to−820 at610,−946 at615,−964 at620,−966 at625,−962 at630; stable lower pose is about−960px. Main travel is roughly0.33s with a small rebound, not a new scale jump. Return840−947,845−482,850−138,8600. The consistent straight-rim width proxy is1260px in223valid native samples;643–647 are rejected for foreground contamination. See [data](corpus/data/574-camera-hardware.csv), [audited overlays](corpus/data/574-camera-hardware-proof.jpg) and [method/limits](corpus/data/574-camera-hardware-method.json). Edge uncertainty about2px;6px overshoot is a restrained visual proxy, not a recovered spring engine.

There is **no supported additional13s camera zoom**: the panel and category rows grow upward inside the held lower phone. Chevron600 triggers reframe and a separately expanding anchored panel; anticipation on the next chat overlaps camera return near850 before contact870. Use a direct translation when current scale already makes the feature readable and only its vertical position needs accommodation. Keep panel, real extracted result row and camera as separate channels on the same clock.

###540 and547: different camera solutions serve different tasks

[Gift Themes540](https://t.me/TelegramTips/540) translates entire phone UP96–120 to make lower picker/Apply legible; native90/105/120 rails remain approximately181/898px in1080source, so this is constant apparent scale, not zoom. Return511–535 restores upper frame. Exact travel/easing unmeasured. Theme choice tint changes screen, picker/CTA and exterior background together; this palette choreography is distinct from camera. Familiar access contacts30/60/90 use0.5s beats; browsing150/240/330 uses1.5s beats. Do not use a single pace for access and inspection.

[Live Stories547](https://t.me/TelegramTips/547), whole1080-frame pass, re-establishes upper→full90–135, full→lower181–225 and direct lower→upper1021–1068. Native90/96/108/120/138 and180/195/210/228 show device and content transforming together while story locally expands and comments appear. Approx settled detail/full widths739/491px agree with historical~1.5x reference; this is native-anchor comparison, not a newly fitted curve. Lower pose remains held through reactions, input, slider and paid-message confirmation. Closing story capsule collapses locally during direct constant-scale vertical return. Plan camera only at context/focus boundaries; keep local focus, emotional foreground and sheet motion independent on shared clock.

##543: perspective is a different camera operation from uniform zoom

[Group call543](https://t.me/TelegramTips/543): opening physical phone has broad lower bezel and visible bottom-port face; near-frontal240/330 has nearly parallel rails and largely hidden bottom hardware face. Root0/240 originals confirm screen and bezel change projection together. Reverse agent also checked150/450/599; input readability coincides with frontal pose, then device gradually returns. A single uniform scale/translation cannot reproduce this perspective. Plan one shared device-plane projection for captured UI and shell; source-linked targets must be projected through it too. Native modal recession and moving chat stack remain separate local transforms. No homography/focal length/pivot/engine recovered; bundled compositor currently supplies frontal scale/translation, so this source is a recipe for a separately planned perspective treatment, not a claim of implemented capability.
