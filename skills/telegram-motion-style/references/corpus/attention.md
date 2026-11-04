# Фокусирование (focusing): object extraction and emphasis

Read when the task needs the viewer to notice a small control, changed property or result. Preserve object identity and its relation to the surrounding UI. Choose the emphasis track that explains the task; these examples are not permission to add every effect to a clip.

## Reusable treatment for different interfaces

The owner calls this technique **фокусирование**. It means selectively directing attention to an actual interface object: isolate a row, card, label, property, text fragment or control; temporarily emphasize it; preserve its origin and meaning; return it to context when the story needs another action. An extracted object may cross the device mockup boundary. This is a compositing treatment usable with different mobile, desktop and web interfaces; Telegram supplies examples, not required components or colors. Camera reframing and tap indication are separate techniques.

Choose its communication job before choosing the effect. A small overlooked affordance may need whole-object extraction (551/560); a content property may need an explanatory glass label (563); author/owner/source relationships can use a capsule or traveling character emphasis (552/564/565); an already active management strip may need emphasis without any tap (567). A quoted source may remain emphasized while attached to its moving message (566). Plain readable framing is sufficient when no special detail needs attention. Do not repeat focusing at every step.

For implementation, retain the following layer and timing relationships:

- Extract the real object's pixels or its actual rendering layer at sufficient resolution. Include its relevant icon, label, state and padding. A whole-row treatment is different from a word treatment; do not accidentally include neighboring rows. If the source media keeps moving, preserve that motion rather than freezing the lifted copy.
- Keep a stable origin in source coordinates. Mask or replace the original occurrence coherently so lifting does not leave a second active copy. Preserve the real underlying context; a guessed clean plate can expose fabricated pixels when the object moves away.
- Composite the ordinary interface within the display mask. Composite the extracted foreground in a layer that can extend over the bezel and beyond the mockup, using the same camera transform and perspective. Cropping it by the display mask defeats boundary crossing. Keep rim, blur/refraction, shadow, content and background attenuation as independent tracks when the checked reference calls for them.
- Track bounds, content scale, position and material separately. A glass capsule's width does not directly measure text scale; a subcontrol may translate outward as the containing strip grows. Anchor an extracted object to its moving source when the surrounding feed continues to scroll (566).
- Separate departure, growth/main arrival, clarity, explanatory hold, return and restored readiness. Coordinate the material and typography through those phases. Use measured samples only for the feature they actually track; no universal spring, blur radius or bounce is established by these sources.
- Restore the original object and remove temporary layers seamlessly. For a subsequent tap, preserve the actual target and encoded contact time; do not let a decorative extracted copy imply an action that the app has not performed. Untapped explanatory focusing remains untapped.

For each new use, record the target, origin/mask, reason for emphasis, boundary overlap, entrance/hold/exit, surrounding motion and relation to the next action. Reuse the appropriate source recipe below; adapt to that interface's density and the requested reading time. A successful extraction is useful because it explains a detail, not because it adds movement.

## Traveling type emphasis — discover an overlooked link

Source: [Log In With Passkeys, Telegram Tips 552](https://t.me/TelegramTips/552), 3 s, 1920 square at 60 fps. All 180 target-region frames were inspected, plus eight native-resolution anchors. Data: [native trajectory](data/552-link-wave.csv), [measurement and uncertainty](data/552-measurement.json).

The device, form and line position stay fixed. The effect moves through individual glyphs from left to right: leading glyphs enlarge, gain weight and a blue depth/shadow treatment, then restore while later glyphs remain emphasized. The neighboring instruction and connective text fade down and recover. This requires staggered glyph tracks; the line's aggregate bounding width cannot be used as one global scale curve.

Measured blue-ink bounds expand from 492 to 884 native px (about 1.797×); the recorded maximum is frame 77, 1.2833 s. At that point the bounds span about 68.5% of the estimated display width versus 38.1% initially. These include ink/shadow/spacing, not authored font metrics. The neighboring instruction's luminance-derived opacity proxy falls to about .059; it is not recovered authored alpha. The final roughly .5 s restores the ordinary readable link.

Reconstruction: keep a stable line anchor; stagger per-glyph scale/weight/depth envelopes; coordinate surrounding-copy attenuation with the local growth. Restore the leading glyphs before the last glyph settles. Obtain a readable final baseline. Do not introduce a tap if the source's purpose is discovery rather than action. For longer copy, assess whether the whole phrase can still be read during the wave instead of simply extending the same timings.

## Extracted settings row — make a small target legible

Source: [Passkeys, Telegram Tips 551](https://t.me/TelegramTips/551), core event 3.3–4.6 s, 78 consecutive source frames reviewed. Data: [separate geometry tracks](data/551-row.csv), [phase landmarks and candidate fits](data/551-row-phases.json).

The row leaves its ordinary visual bounds, expands across the bezel, then contracts into place. The local key icon grows/shifts horizontally while its vertical center remains near y=1218–1221 in the 1920px source. The surrounding page does not scale. Content, white surface, glass rim and shadow are separate visible tracks: measuring the white capsule width does not measure the content scale.

| Landmark | Source frame | Source time |
| --- | ---: | ---: |
| 10% of segmented icon-height growth | 213 | 3.5500 s |
| 50% growth | 219 | 3.6500 s |
| 90% growth | 227 | 3.7833 s |
| 10% recovery from peak | 242 | 4.0333 s |
| 50% recovery | 248 | 4.1333 s |
| 90% recovery | 254 | 4.2333 s |

The icon's segmented height changes 90→129 px (about 1.433×). White-surface span peaks at 1547 px, with threshold-dependent bounds. For this one growth envelope, sine-in-out and smoothstep over approximately .35 s fit to about .91 native px RMS; the errors are effectively indistinguishable. Neither fit establishes the source engine or unique easing coefficients. Preserve the empirical samples when a close match matters. First/last ordinary row states differ slightly, so do not infer an exact symmetric scale from the peak alone.

Reconstruction: extract the real row content with its visible padding, anchor it to the source row, then coordinate content growth, local translation, glass boundary and shadow. Keep nearby controls as context. Restore the row before pressing it. Decide the quiet hold from actual readiness and readability rather than adding the highlight duration to every click interval. Microanalysis of this event does not by itself validate blur radius, shadow opacity or the entire source clip.

## Capsule-to-lens metadata emphasis — observed, not yet calibrated for replay

Source: [Repeated Messages, Telegram Tips 549](https://t.me/TelegramTips/549), 6.0–7.2 s. Seventy-two consecutive target frames were inspected, with native crops and a .25× preview in the local research archive.

The time/frequency metadata first enlarges inside a rounded capsule tied to the real message. The capsule approaches a circular shape, then returns through a capsule stage. A green perimeter stroke draws and retracts on an independent schedule; the content magnifies while surrounding context stays recognizable.

A fit to only the visible green arc can pass a numerical residual check yet describe a smaller circle inside the actual capsule. That fit was rejected by visual overlay inspection. Do not use the partial stroke's bbox/radius as the full lens geometry, or claim a fixed circular scale/opacity curve. Recover the silhouette and content magnification separately before implementing an exact replay. This is currently a qualitative, source-linked option, not a calibrated preset.

## Relating emphasis to the next press

In source 551, the reviewed row returns near ordinary geometry around frame 254 (4.2333 s). The next ring becomes visible around frame 278 (4.6333 s), reaches its large phase around frames 289–290, and compresses around frames 299–300 (4.9833–5.0000 s). The row is visibly pressed near this minimum; horizontal native navigation starts around frame 302 (5.0333 s) while the ring tail continues fading. Thus emphasis recovery, quiet reading, ring anticipation, contact and UI reaction are distinct phases. The approximately .4 s clean gap and .77 s recovery-to-contact interval describe this source, not a default reading duration for all apps.

## Enlarge a whole tile around its own center

Source: [Gift Auctions, Telegram Tips550](https://t.me/TelegramTips/550),1080 square60fps. All900 frames were inspected in relevant crops. The extracted tile's60native frames were measured; [width trajectory](data/550-tile.csv), [phase landmarks](data/550-tile-phases.json). This is a different geometry from Passkeys' laterally shifted row.

Long gold vertical border strokes give baseline width188px and peak287px at F100(1.667s), approximately1.53×. Left edge moves238→189px while horizontal center stays≈332→332.5px. At peak the tile overlaps the display/bezel boundary. Ribbon, illustration and Join button grow together; illustration rotation is secondary and its silhouette should not be used to infer tile scale. Gold-height measurement includes the ribbon and is less stable than width. Threshold/reflection uncertainty is about2–4nativepx.

The width reaches10/50/90%of expansion at F82/88/96(1.367/1.467/1.6s). Recovery reaches10/50/90%at F112/117/125(1.867/1.95/2.083s). Growth and restoration form a soft pulse; this measurement does not establish repeated bounce or a unique easing engine. Use the empirical trajectory when a close replay is needed rather than forcing a spring onto every emphasis.

The tile is restored by about F131(2.183s), next tap anticipation begins near F158(2.633s), and compression is near F180(3.0s). Thus the emphasis returns to real context before action: about.45s of quiet restored context before anticipation, and.82s to contact. These are source timings, not defaults overriding the requested reading pace.

Suitable when a tile has an overlooked badge, illustration and action that should be read as one object. Preserve the full object and original center, allow deliberate boundary overlap, keep neighboring grid context, and restore before navigation. Do not infer that editorial enlargement is itself a user selection.

## Explanatory control medallion and extruded headline — 554

Source: [AI Summaries](https://t.me/TelegramTips/554), 1920-square60fps,6.5s. All390frames reviewed; native title and material/transition anchors checked.

Use when a small unfamiliar control needs explanation before activation, or the identity of a changed document needs emphasis. The phone remains fixed. Around0.52s the summary control grows into a dark translucent gold/brown medallion with curved explanatory lettering, inward-arrow icon and glints. It changes orientation, overlaps the bezel, and reveals/distorts the current underlying scene. Large by~0.92s, it remains large through~2s and contracts toward the control before2.5s contact. The subsequent frosted tap annulus is a separate effect. Full rim, rotation angle and material coefficients are uncalibrated: do not equate a color-mask outline with the physical coin boundary.

After the summary settles, only its blue headline enlarges; normal-size subtitle and body provide a stationary context. Blue offset facets add depth, with pale glints. [Native ink envelope](data/554-title-ink.csv) and [measurement limits](data/554-title-measurement.json): resting width~241px, peak540px atF240/4s, approximately2.24times. Rise10/50/90% atF219/226/233; return10/50/90% atF249/255/262; near restF269/4.48s. The ink includes the depth effect and is not the original text transform. Position shifts too; do not implement it as a centered page zoom. No undershoot is established. F219 was already growing and was rejected as a rest baseline.

For reconstruction, separate title position/scale, facet visibility and glints. Keep supporting text readable, then leave a quiet result interval after restoration. This example supports local emphasis without a camera move; it does not override the approved camera bounce preset.

## Sequential metadata emphasis while context scrolls — 556

[Member Tags](https://t.me/TelegramTips/556): five labels change sequentially nearF155–179,185–209,215–239,245–269,275–299 (roughly.5s start stagger,~.4s each). Old short metadata grows into an elongated local capsule; individual letters distort/change, then restore to small right-aligned text. Examples change role labels into phone-model tags. Chat continues slowly upward beneath fixed header/composer; each local cue follows its own message. Whole-phone framing stays fixed, so the viewer can compare several cases without repeated zooms.

Use this when teaching a repeated small property across a list. Preserve each label's anchor to its moving item; stagger attention so one cue leads at a time, then restore normal context. Shape, text transition and local emphasis are separate tracks. Full capsule geometry and exact glyph easing remain uncalibrated; do not derive a lens boundary from a partial stroke or call editorial choreography a live data update.

## Two-ended contour, pulsing fill, then targeted removal — 557

[Disable Sharing](https://t.me/TelegramTips/557),13s/780frames fully inspected. A comparison menu establishes aroundF445/7.42s. FromF446 a short red stroke at the top center extends both ways, rounds the upper corners, descends both sides, then approaches the lower center. A small bottom gap remains through its fade. The pink-red rounded fill appears much faster and pulses independently: stronger nearF455, lighter nearF475, stronger again nearF490. Only Copy/Forward/Share/Save Image are enclosed; Reply/Pin/Delete remain outside.

[Strict-red ink data](data/557-outline-ink.csv) and [audited limits](data/557-outline-measurement.json) record visible stroke, not original path trim. AtF450 the top stroke spans~408nativepx; byF460 it reaches down both sides; byF470 it rounds the lower corners; strong stroke fades from~F488 and is absent byF499. A permissive color mask was rejected because it included the pulsing fill and letter edges. Ink area combines path length, thickness, opacity and compression; do not fit unique easing or full-rectangle size from a partial stroke bbox. Interior median RGB records the fill pulse but cannot recover authored alpha through glass/background.

Grain starts~F501/8.35s after the highlight recedes. Four row icons/labels disperse; surviving actions and the photo/menu layout reflow from~F505 while particles persist. Explanation appears~F509, reduced menu reads aroundF525/8.75s, most grain is gone nearF570/9.5s. Maintain object identities: the affected subset disappears, survivors remain legible and move. Do not dissolve the entire menu or wait for the last particle before layout changes.

Use for an exact before/after change in available actions. Separate subset fill, two-ended contour, fill pulse, contour exit, glyph/particle removal and survivor layout. The source comparison is editorial; it does not establish that restricted controls were still actually usable. Outer phone stays fixed; selected photo/menu enlargement is local.

## Functional selection before isolated token emphasis — 559

[Date Formatting](https://t.me/TelegramTips/559), all630frames inspected. Blue selection handles appearF121–122/2.02s around only `tomorrow at 10.`. The rest of the sentence stays legible. A small toolbar capsule begins~126, grows with strongly bent outer labels, approaches final size~160 and settles~180. Selection is already present before2.5s; earlier inventory merged these phases. Use the app's functional selection itself as precise emphasis when the story transforms part of a larger object. Keep selection bounds anchored while the action surface changes above them.

The later date action is different: compression480/8s, background blur/lift481, old relative phrase exits upward while explicit date/time enters below around486, explicit label readable~489. Menu underneath grows with bent copy, mostly readable503 and settled516/8.6s. Native anchors confirm the relative/absolute overlap. Isolate only the semantic token, keep its origin understandable, then reveal applicable actions; a whole-device zoom would not provide the same precision. Separate token movement, label substitution, blur and menu geometry. Exact warp and easing remain unknown; the late moving token leaves the native crop, so whole normalized frames supply its later context.

The physical phone stays approximately constant: [15bezel anchors](data/559-bezel-measurement.json) span343–346px in540scaled source, within1–2px endpoint uncertainty. Local menu/calendar enlargement and chat insertion are not whole-phone camera moves or manual scrolling.

## Extract a small action before using it — 560

[Log In With Telegram](https://t.me/TelegramTips/560), all690frames inspected, starts by enlarging only Connect Telegram. [Native fill-envelope measurement](data/560-connect-measurement.json): span534px atF0,629atF10,701atF20,731peakF29–30,654atF40,597atF50,533atF60. Peak~1.369times baseline; center stays~480px in the native crop. The enlarged pill extends beyond physical bezel, with changing cyan sheen/bright edge. It restores by contact60/1s; page expansion begins63. Eight mask-proof anchors and raw0/30/60 inspected. Fill mask excludes white rim/glow, with~2–4px uncertainty; no unique spring or light shader recovered.

Adapt when a small but important affordance needs introduction: preserve its original location, enlarge the complete recognizable control, let lighting signal extraction, restore it before the consequential action. Scale, lighting, indicator and native response need separate tracks. Keep compositor stacking coherent if the object crosses the bezel. Do not infer that the production app itself enlarges its control outside the display, or substitute this relatively long1s emphasis for every click.

## Carry a recognizable target across applications — 560

The browser's robot emoji is readable by~F175/2.92s and held until the4.5s app exchange. The same robot is the center choice on the next sheet, between devil and pumpkin. Sheet copy arrives before options; approximate first/center/last emoji onsets307/313/318, all established~330/5.5s; center compression360/6s. Local emoji rotation/growth makes the choices lively while preserving identity. Stable target identity, a clear memory hold and recognizable options convey the cross-app relationship; avoid simultaneous unrelated changes that make the viewer search again. This is a motion/narrative observation, not an independent security evaluation.

## Creative-tool spectacle introduces an affordance — 561

[AI Text Editor](https://t.me/TelegramTips/561) decorates the small composer AI control before its first use. AroundF81/1.35s, while text is still entering, colorful crayon/pencil-like tools, paint traces, loops and letters emerge. A large circular Ai medallion is prominent~90–100; it contracts back toward the small control by~120/2s while decorative objects continue across the text edge and outside the bezel. Tail mostly clears~158/2.63s as tap anticipation begins; compression180/3s opens editor. Native81/95/120anchors checked. This is a feature introduction, not success confetti; exact paths/material/scale curves remain uncalibrated.

Use a short semantic spectacle when its objects explain the capability: drawing tools point to creative editing. Preserve the functional control as the ending anchor, separate its restoration from decoration exit, and clear competing motion before selection. The second editing pass reuses the small AI affordance without repeating the giant tool spectacle. A demo can teach an operation once, then use the established visual vocabulary more economically. See [AI response rhythm](ai-response.md) for later generation/correction phases.


## Explain a media property with an extracted glass label — 563

[Live and Motion Photos](https://t.me/TelegramTips/563), all600frames inspected, starts with a received moving dog photo. Its tiny Live icon expands into a wide `LIVE PHOTO` glass pill, extending left across the physical bezel. This is explanatory emphasis without a tap, not a menu or success message. The dog keeps moving underneath; the pill shows blurred/distorted scene and bezel through its tinted material. Text becomes uncovered as its bounds develop: nativeF10stillclips the right-side label, F25shows the full capsule. Native0/10/25/80/90anchors checked.

Near-final size is reached aroundF25/.417s, then held through~F80/1.333s. Return starts aroundF83/1.383s; nativeF90has a small fading portion of the label, and the original compact mark is restored by~F95/1.583s. The next real action is attachment compressionF120/2s. Position, pill bounds, text reveal, scene distortion and restoration are separate tracks; this is not merely a larger opaque text label. Exact glass shader and motion envelope remain unmeasured.

Use when a tiny content property explains what the viewer is seeing. Preserve the mark's relationship to its media, let the explanation cross the bezel only with coherent compositing, then restore it before the next action. Compare with560's extracted actionable Connect button: both teach a small affordance/property, but563does not show a click on the extracted label. The approximately fixed phone lets this local movement carry the focus.


## Explain an ownership relationship before following its link — 564

[Managed Bots](https://t.me/TelegramTips/564), all720frames inspected, separates creator lobster identity from created#007identity. After the new bot's profile arrives~F570/9.5s, its small gray `Created and managed by` attribution becomes a glass capsule. It grows from~F571, crosses both physical bezels, keeps its code symbol and cyan manager handle, and changes regular gray copy into brighter, heavier lettering. Bezel distortion remains visible through the glass. The rest of the profile stays readable in the same phone pose.

Large copy reads by~F590/9.833s and is near its large plateauF610–630/10.167–10.5s. Return starts~631, with a small tail still at661/11.017s. It restores before manager-handle compression690/11.5s; the ring is centered on the attribution link **below** Open App. The creator mini-app then rises. An initial inventory called this an Open App tap; native690and the full-width cue corrected that attribution. Preserve which exact object is highlighted and subsequently activated.

[White-prefix ink measurement](data/564-attribution-white-prefix-measurement.json) supports only audited state comparison: code symbol plus white prefix522×38nativepx atF570,949–955×66atF610/630, about1.83times the baseline width. This is an ink envelope with weight/material changes, not a uniform font transform or full capsule bounds. The attempted continuous bbox curve was rejected: broad bezel exclusions cut moving leading glyphs, and transient highlights contaminate an apparent1176px maximum atF600. Eight proof anchors and full native570/610/690were inspected. Do not publish that maximum as a bounce or fit original easing to this track.

Use this treatment when a small relationship—author, owner, source or manager—is the point of the demonstration. Carry the exact label/link into a temporary explanation, preserve surrounding identity, restore normal layout, then let the real action follow. Compare563's untapped media-property explanation and560's extracted Connect action; their similar local extraction language serves different communication jobs. Full-width evidence matters when the emphasis extends outside an ordinary phone crop.


## A character wave emphasizes an existing attribution — 565

[Guest Bots](https://t.me/TelegramTips/565), all420frames inspected, already displays `Mira for Monica` in the incoming reply. Native275/300confirm this before emphasis. AroundF305/5.083s, leading Mira grows and becomes brighter/heavier blue; by315Mira/forare large while trailing Monica letters remain compressed/overlapped. Native325shows later letters expanding,330the complete large phrase. During return~F340–369, leading characters shrink earlier while trailing characters spread apart and fade toward their original lighter treatment; native345/360show this spacing tail. Quote and answer body remain at normal geometry.

This is neither a semantic rename nor one uniformly scaled screenshot. Local character size/weight, spacing, clarity and timing differ across the same string. Build~305→330is about.42s, full large state is brief~330–339/.15s, return~340–369about.48s. These are visual phase landmarks, not recovered per-glyph easing coefficients. The enlarged name explains who answered whom while leaving the answer readable. An early inventory misread the effect as changing Mira to a personalized name; dense/native evidence rejected that interpretation.

Use when an existing author/source relationship deserves a precise reading cue. Preserve the exact label, emphasize across its characters, then restore typography before the next task. Compare554's isolated headline growth and564's whole glass attribution extraction:565lets different parts of a single label move at different times, without enlarging the entire reply or moving the camera.


## A quoted relationship stays enlarged while its context moves — 566

[Bot-to-Bot Communication](https://t.me/TelegramTips/566), all360frames inspected, begins with an already established human→DevBot→GitBot exchange. AroundF30/.5s, the DevBot source quote **inside** GitBot's reply expands into a translucent rounded plate. Its colored left bar, source name and quoted command enlarge together, extending beyond the bubble sides; the enclosing author and answer body retain ordinary size. NearF60/1s the glass plate is established; it stays large through~130/2.17s, then narrows back to its original inset by~149/2.48s. Native27/60/120/139/149checked. Exact shader and scale envelope are unmeasured.

The extracted quote remains attached to its moving message. The conversation travels upward underneath fixed header/composer while the local plate stays emphasized; it is neither a full-camera zoom nor a screen-pinned callout. Audited [purple author-ink translation](data/566-header-y.csv), [limits](data/566-header-y-measurement.json) and [overlay proof](data/566-header-y-proof.jpg) separate this context motion from the enlarged quote: native author-center y1421.5 atF30,1343 at60,1149.5 at90,957 at120,880.5 at149. The largest measured10-frame average is−480px/s over83–93; ink-threshold uncertainty is roughly1–3px. This interval does not establish physical swipe/release or a native inertia engine.

Use when provenance or handoff matters while a feed advances: preserve the source relationship, attach the emphasis to the actual item, keep its body readable and restore ordinary geometry before the next task. Compared with551's row restored before pressing and565's character-wave attribution,566emphasizes a quoted relationship during continuing context motion. Avoid an unrelated camera move that competes with this already active focus.


## Extract an active management strip without pressing it — 567

[Chat Automation in Profiles](https://t.me/TelegramTips/567), all540frames reviewed, first establishes a populated example chat and its persistent bot-management strip. From~F361/6.017s, avatar, name, status, Stop and settings icon enlarge together on a glass capsule crossing both bezels. The large state is established near375/6.25s and remains through~420/7s; it returns~421–451/7.517s. The conversation and header keep ordinary geometry. No Stop tap occurs: this explains active status and available control, not a demonstrated stop action.

[Blue Stop-fill samples](data/567-stop-fill.csv), [measurement limits](data/567-stop-fill-measurement.json) and [checked overlay](data/567-stop-fill-proof.jpg) separate local control geometry from whole-panel bounds. Native F360fill190×80px,centerX1280.5; F390248×104,centerX1376.5; F449186×79,centerX1272.5. The large fill width is about1.305times the initial sample, while its center moves~96px outward. These are threshold fill bounds with~2–4px uncertainty, not recovered capsule scale or authored font metrics. Slight baseline differences do not establish a bounce. Five raw anchors and five overlays checked.

Adapt when a persistent status strip deserves explanation after setup: keep the whole functional object together, let its subcontrols move coherently within the extraction, preserve readable evidence behind it and restore ordinary layout before leaving. Glass carries the scene/bezel colors, with changing sheen during the hold; exact shader is unknown. Unlike551's actionable settings row restored before pressing,567's bar is never activated. About1s of ordinary-size result remains after restoration before the loop.


##527: two ringless extractions with different silhouettes

[Topics navigation](https://t.me/TelegramTips/527) was reviewed by the authorized reverse-study agent:780consecutive frames/26dense sheets plus25native/overlay anchors. A comparison card containing both alternatives and labels lifts across **both** phone edges, then a later narrow sidebar lifts over the **left** rim. Both are untapped explanation beats. The card's miniature illustration keeps changing during its return; freezing it would break this internal demonstration. Physical phone stays frontal even during a separate inner-screen-plane flip346–380.

Card departure~184, largest width~200, return~211, restored~230. A corrected white-row silhouette proxy gives nativewidth609at180→802at200→788at210→609at230, ratio~1.317, center~540px, uncertainty±4px. Initial threshold included bezel glints and initial crop clipped labels; both limits are retained in [measurement](data/527-focus-card-measurement.json) and [samples](data/527-focus-card-width.csv). This is not recovery of spring coefficients. Sidebar departs~399, is large410–420 and restored~440; its full height/scale is not measured. Restore each emphasis before the ensuing actual selection.


##570: local media enlargement inside an unchanged watch

[Watch Apps](https://t.me/TelegramTips/570) demonstrates focusing through local enlargement and context defocus, with no spill of the media outside the watch. Contact300 enlarges the same circular portrait down/right while chat details blur away, retaining time/back. Face playback and white progress arc continue during the held result. Manual native envelopes at300/305/315/330 have widths~421/505/586/586px, ratio~1.392; center shifts~95.5px right and102.5px down, uncertainty±5px. See [anchor overlays](data/570-manual-circle-anchors.jpg) and [method/limits](data/570-manual-circle-measurement.json). Four anchors do not recover exact easing or establish bounce. The media remains circular; physical bezel/crown/strap do not zoom.

Main growth is already near final size315, near-rest330; Back390 follows1s after that ready pose, including anticipation368. Return393–420 reintroduces blurred chat and restores the media's small original location and play triangle. Choose this variant when consumption of an existing media item is the next semantic task. Changing portrait pixels prove playback, not a camera movement or a stable tracking landmark.


##530: opaque circular emphasis follows a moving tab

[Collaborative checklists](https://t.me/TelegramTips/530), reverse-agent review of600frames/20dense sheets,macro and23original-resolution anchors, enlarges Checklist icon **and label** on an opaque white circular backing48–80. Gallery exits left and Contact enters right as strip travels; emphasis follows the Checklist target's changing position. Large poses60/70 contract~74–80, selected purple/page transition appears81–85. No separate hollow tap annulus establishes a second Checklist press. Distinguish this white local bulge from the click material.

The physical phone appears fixed; base chat recession when a sheet opens is an internal modal-stack change, not whole-device zoom. For a reproduction, keep actual footage as base and plan source-linked local extraction/enlargement only if needed, with clean backing, shared target transform and coherent restoration. Flattened source leaves exact lens/extraction mechanism unknown; no scale/easing curve or numerical whole-phone track recovered.


##531: explain an unfamiliar affordance before contact

[Suggested posts](https://t.me/TelegramTips/531), reverse-agent720-frame pass/24dense sheets and14original-resolution anchors, uses a black expanding tooltip with a short pointer tied to the bottom-left DM icon. First31, readable43, settled48, contact90: explanation precedes the action; ring begins~68 and spills across left bezel. After sheet arrival, empty-state badge grows to an oversized pose~105 and settles~120; the next composer tooltip begins121, readable130. This is staged discovery of an unfamiliar affordance, not click feedback or a whole-device zoom. Keep pointer/tooltip on the actual moving target and allow explanation before advancing. Native modal-stack recession stays inside apparently fixed physical bezel; no numerical camera/pivot curve recovered.


##533: the focus outline is a traveling segment

[Posts tab533](https://t.me/TelegramTips/533) lifts the real Posts+NEW label/badge into a larger white capsule with soft shadow52–70, then restores73–88 before contact90. Blue contour begins at left curve, grows into parallel top/bottom runs, then progresses toward right arc while left clears during shrink. Native54/60/65/70/80 establish an **incomplete traveling outline**, not a static full border. Ring anticipation~68 overlaps focus peak on a separate layer. No bezel spill in this example and no whole-device zoom. Reconstruct white backing, real labels, traveling stroke and ring independently; repair original tab to avoid a duplicate label. Numerical scale/overshoot not recovered.

##574: expose an entry, then explain a result in the same shot

[Communities574](https://t.me/TelegramTips/574) uses two different real-object lifts. The newly exposed settings row starts growing247 while the underlying scroll finishes, holds roughly260–286 across both bezels, then restores287–304 before ring minimum310. A target can become discoverable during residual content motion; do not jump to the next action at its first appearance or confuse the peak focus pose with contact.

Later the actual Formula Paddock chat row lifts631–645 above the community panel and escapes both bezels. It retains avatar, sender, last message and time. Toggle660 changes that row to Alpha Lounge identity through664–680, including overlapping old/new typography; return691–707 restores its original list footprint. This is a source-linked result demonstration, **not a notification banner**. Keep the cause below and its result above concurrently readable, repair original backing, and bind the extracted row to the same camera path while allowing local enlargement. Source layer ownership remains unknown; whole1110-frame pass and native650/670/700 constrain phases without an exact scale/easing reconstruction.

Three subsequent ringless Add Chat CTA sprouts721/751/781 populate different categories while the panel expands. They omit actual adding/picker interactions and are an editorial capability montage, not an inertial list fling. Reuse that morph only when the story calls for a compressed feature demonstration; it cannot stand in for footage proving the full real workflow.

##535: enlarge one menu action while its environment stays alive

[Gift Collections535](https://t.me/TelegramTips/535), reverse-agent600-frame pass and13native anchors, lifts only Add Collection from a multirow menu. Growth79–95, large hold95–122, return123–140, contact150; anticipation128 overlaps return. White rounded backing and shadow cross right bezel, while neighboring menu rows retain base size. Manual inspected width ratio~1.5 is an estimate, not a fitted easing/pivot. Animated gifts keep moving behind the translucent menu and dialog, so a frozen full-screen backing would visibly break this scene. Root spot-check at native110 confirms bezel spill. Name entry184–205 raises later/fainter letters toward the baseline; collection result after Create240 omits actually adding its five gifts.

##575: moving icon emphasis and delivered-object group focus are distinct

[Welcome Messages575](https://t.me/TelegramTips/575),600-frame pass/20dense sheets and23native evidence entries, grows only waving purple hand icon while settings scroll128–181. Label stays normal. Eight original-pixel colored-component anchors measure width138105,155197,180237,200136,209115px;centerX~409±1px whilecenterY1141→782 follows row and then stays fixed during shrink. First138is already enlarged, not baseline. See [audited overlays](data/575-hand-color-proof.jpg) and [method/rejections](data/575-hand-color-proxy.json). Global color bbox was rejected because neighboring icons/Change Photo contaminated it. No exact easing or physical scroll release recovered. Icon crosses row-card edge but native155/180 **does not establish bezel spill**. Restoration~215 precedes contact240.

After recipient Join480 and delivery accommodation~505, message bubble, popcorn sender avatar and join-service label enlarge together511–530 and return~533–550. Physical phone and pinned header keep their size. Bubble covers composer; attached avatar visibly crosses left physical bezel at520/530. Choose the group extraction when semantic association matters, preserving separate silhouettes, shared motion and correct foreground order. A whole-device zoom would unnecessarily enlarge unrelated context; a duplicate static avatar would break the living content.

##576: held contact, lifted sharp message and defocused context

[Movie choices576](https://t.me/TelegramTips/576) compresses annulus420 then holds it compact at fixed target through449; native420/440 preserve same small material. Context response begins450, about.5s later. This visual dwell distinguishes a long press from a stuck ordinary tap; no physical touch-down timestamp recovered. During450–475 selected result lifts while header/sticker/wallpaper blur and Copy/Revert menu grows below. Ring recovers/fades only during response450–465. Sharp bezel/Dynamic Island stay fixed, selected card remains inside display. Plan held state and release separately from ordinary tap curve, and preserve selected-object sharpness above context blur. A generic whole-frame blur would obscure the very detail being explained.

##537: emphasize action and consequence with distinct real controls

[Profile Music537](https://t.me/TelegramTips/537), reverse-agent480-frame pass/14native anchors plus root135/225/365 spot-check, lifts Add to Profile123–163, then the actual resulting music banner203–244. Both cross left/right physical bezels with real icon/label and bright material sweep; restore before180/270contacts. Hand-estimated first width~610→790px (~1.3x), so local emphasis is not universally1.5x. Separate source-linked extraction, backing repair, rim/sheen, indicator and UI response. Matching title/artist and added toast192 supply proof; no separate profile-navigation click shown.

Reorder330hold→345–376travel→390rest lifts real Dance row with shadow and displaced neighbors; indicator follows moving handle. Final order changes while Swan Lake remains playing and timer advances. Preserve state and playback clock across extraction, modal transitions and drag. Reordering does not imply selecting the moved item. Untapped ending dismissal451 restores opening chat for loop; no demonstrated Stop action.

##548: sheen can attract attention without any press

[Stream vignette548](https://t.me/TelegramTips/548),180-frame pass/6dense and7native anchors, holds an already-open setup screen for3s without interaction. Start Streaming stays same size and retains sharp white text while a soft pink band passes left→right~60–120: native80bright left broad glow/rim,96bright right,107right tail. Clip material to rounded CTA, keep text above sheen, avoid a tap ring or press depression. It is autonomous affordance emphasis, not success feedback or evidence that streaming started. Exact gradient/easing unmeasured; source is a quiet feature vignette rather than a complete workflow.

##538: screen surround is different from escaping the mockup

[Sticker mini app538](https://t.me/TelegramTips/538) enlarges Open App33–48, holds48–65, returns66–83 before contact90. Blue label/button and cyan sheen move together. Root native45 confirms it covers the black screen surround while staying within physical outer bezel. Do not label every screen-mask escape as an object leaving the device; inspect full bezel context. Original65/80 constrain large/restored poses, but no numerical scale/pivot curve established.

##539–540: preserve object identity through context and articulation

[Profile tabs539](https://t.me/TelegramTips/539), reverse-agent540-frame pass/12native anchors with root225/312/325 spot-checks, holds compact ring180–210 before menu211. Sharp Gifts capsule contains actual gift miniatures over blurred context. Set as Main Tab300 returns SAME capsule left into first slot305–315 while Posts moves right and gift grid retains identity. A moving tab capsule is local emphasis/reorder proof, not a whole-phone zoom. Avatar collapse62–85 merges into fixed Island through blur/dark neck; shell remains fixed.

[Gift themes540](https://t.me/TelegramTips/540), reverse-agent540-frame pass/14native anchors plus root90/105/120 and250/260/280 checks: selected heart miniature enlarges then ARTICULATES. Closed250→lid separating260→open raised lid/cyan cavity270–280. A rigid screenshot scale cannot reproduce it. Narrow crop clipped lid; wider context corrected bounds. Keep articulated gift clock distinct from selection ring, palette and native sheet. No physical-bezel escape established.

##547: local avatar discovery and preview-to-history handoff

[Live Stories547](https://t.me/TelegramTips/547),1080-frame pass/36dense+2macro/48native anchors, grows actual Luna face/red LIVE plaque32–62 then returns63–72 while separate contact anticipation begins68, minimum90. Neighbors stay located but pale focus surround overlaps them. No particle burst or whole-phone zoom during this discovery. Later Add900 lowers sheet while matching gray Patrick message independently moves upward/left: native904 sharp over sheet controls and blurred scene;910 sharp above exiting sheet;919 same sentence/avatar/10000/crown1 joins sharp history and first leader slot. Separate local real-object path, context blur release, outgoing surface and ring at old action origin; avoid duplicate permanent preview. Flattened source leaves original implementation ownership unknown.

##541: a real object can bridge two independently transformed devices

[Upgrade Gifts541](https://t.me/TelegramTips/541), reverse-agent870-frame pass/16native anchors with root304/308/313/240/685/730/818 spot-checks. Gift an Upgrade control213–268 enlarges beyond BOTH bezels with its label/icon and cyan sheen; manual native width609→781px (~1.28), restored before300contact. This local extraction needs no global phone zoom.

After300 actual green frog lifts from sender sheet beyond physical top/right rim. Native304 shows frog in front of tilted sender while receiver enters right;308 frog remains in foreground across both oppositely tilted phone planes;313 receiving phone returns toward frontal while frog remains above its blank gift card. It lands317–325 in matching Patrick message. Plan THREE transform parents: sender device, receiver device, independent real object; transfer parent only on landing. Repair source/destination duplicates, preserve shared clock and foreground bezel occlusion. A single camera zoom or screenshot crossfade cannot reproduce the handoff. Exact3D engine, pivots/path and scale curves are unrecovered; current bundled compositor does not automatically implement this multi-plane recipe.

##544: emphasize the saved consequence after the surface has gone

[Private contact note544](https://t.me/TelegramTips/544) saves180, dismisses sheet, settles profile~195, then lifts actual notes row213–239. Native210 ordinary row;216 detached rounded white capsule with soft shadow;225 near peak crosses BOTH physical side bezels;235 returns;240 ordinary row again. All sentence/notes/privacy labels scale together while profile remains sharp and phone fixed. Separate extracted real row, repaired original slot, shadow and object transform; restore into matching origin. This is neither whole-camera zoom nor emotional particles. Saved result then rests240–337~1.62s; later338–355 unacted fade/reflow is loop reset, not Delete/Undo.
