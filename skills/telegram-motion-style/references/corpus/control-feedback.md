# Continuous controls and action-to-status continuity

Source: [Gift Auctions, Telegram Tips550](https://t.me/TelegramTips/550),1080 square at60fps. Whole900-frame pass inspected in relevant crops; native slider anchors checked. Landmarks are visible source phases, generally±1–2frames, not physical touch timestamps. Exact material or spring coefficients were not recovered.

## Continuous gesture: attach feedback to changing meaning

Thumb press becomes visible around F302(5.033s). During one continuous movement, amount changes from5000 to5100(near F306), toward6200(around F325), then7200(near F345,5.75s). Amount digits change independently rather than instantly substituting one label. Bubble tilts during motion and settles afterward. Track/bubble pass from purple through muted neutral near F330 to green around F338. Projected rank312→212→21 trails the amount, reaching21 near F356(5.933s).

The scene is not ready just because the thumb or amount stops: downstream feedback still explains the consequence. Give the settled value, state color and consequence time to read before commit; in this source commit is F420(7s), approximately1s after remaining settlement. Keep the frame stable so the viewer can follow this causal chain.

For a new app, use the actual control's behavior. If reconstructing editorial feedback, separate thumb/path, label anchor, label tilt/settlement, digit replacement, color blend and dependent result. A bubble body centroid is not its pointer tip or the thumb center; screen-edge constraints and rotation can offset the body. An exploratory color-mask centroid was rejected because it included the drag indicator and clipped part of the tilted bubble. Do not use that track as an original motion curve or guess damping/stiffness from it.

## The action surface can become its own status

Commit compression is near F420. At F421(7.017s), the green button starts widening beyond the display and across the bezel. Its label blurs, material changes toward dark translucent, and success text becomes readable around F435(7.25s). The gavel icon continues moving during the stable readable state.

Exit begins around F521(8.683s): success text blurs away, the wide bar becomes green and contracts toward button geometry. OK is clear around F534(8.9s), just as the countdown resolves. This is a continuous action→status→next-state transformation, not merely a separate toast placed on top of a stationary button.

Use when a compact action and its confirmation can share a clear semantic origin. Animate geometry, material, old-label disappearance and new-label clarity on separate tracks, preserving recognizable continuity. Do not invent a morph if the real app supplies a different response; retain its native behavior unless editorial reconstruction is explicitly within scope.

## Countdown and celebration have narrative jobs

After commit, the countdown visibly explains why the scene waits. Outcome transition starts around F556(9.267s); confetti begins near F557 while the incoming result is still blurred. Gift proof is readable by roughly F573(9.55s). Particle density decays, becoming nearly empty around12s, while the gift stays readable until14s. The rotating small illustration keeps the hold alive after particles disappear.

An automatic/editorial outcome transition is shown without an OK tap. At F841(14.017s), the gift disperses into dust while chat repositions toward the starting state; the loop is almost restored near F894(14.9s). Neither action proves a user pressed OK or deleted the gift. Retrieve this as a deliberate loop-ending example, not ordinary interaction evidence.

For a finite demo, wait on visible progress when processing matters, then keep durable proof after the celebration tail. Let particles introduce the success beat and recede so they do not permanently cover the result. A long hold with active countdown, a readable proof hold and a decorative idle hold serve different purposes and should not be timed as one category.


## Rolling confirmation: translation, width and glyph curvature differ — 563

[Live and Motion Photos563](https://t.me/TelegramTips/563) selects Live atF300/5s. A tiny gray confirmation is already visible atF301, while the old menu starts collapsing around302. The toast drops toward the open sky area while widening; its text initially looks wrapped around a short cylinder, with compressed/stretched outer glyphs. Round ends and the Live icon resolve as copy becomes flat. Main phrase mostly reads by~F335/5.583s; near-rest geometry byF344/5.733s. Raw301/302/310/320/335and12mask-proof anchors were audited.

[Native dark-body bounds](data/563-toast-bounds.csv) and [method/limits](data/563-toast-measurement.json) distinguish the phases. Width spans32px atF302,113at305,287at310,393at315,550at320,600at325,612at330,624at335 and620at344. Relative to late620px,10/50/90%width is reached303/311/321. Body height peaks162px nearF309, then falls to126px byF344while width is still growing. Its center also drops; a uniformly scaled pill cannot reproduce this envelope. The4px width peak-to-rest difference is too small against threshold/warping uncertainty to prove a spring overshoot. The36px height difference is clear. Measurement follows connected gray fill, excluding white warped glyphs/rim; it does not recover actual typography or alpha.

A reconstruction should separate downward travel, widening, temporary height, end curvature, glyph deformation, icon resolution and reading hold. The pixels support a cylindrical appearance, not a specific original3D engine or shader. Keep the operation's changed mode visible in its original control too: the top label returns as Live nearF315while the confirmation is still resolving.

The toast stays readable over moving coastal footage through SendF420/7s. It does not exit at6.1s as the initial inventory suggested. Send response begins aroundF424, so maximum ring compression and first geometry change differ by~4frames. The toast then fades with editor controls while the same photo becomes a chat bubble. Follow the actual action's response clock rather than forcing confirmation, indicator minimum and surface exit to one timestamp.


##570: recording, preview and sent proof are distinct states

[Watch Apps](https://t.me/TelegramTips/570),810original60fps frames/27dense sheets reviewed. Voice Message contact510/8.5s opens an already-recording screen under blur; no separate Record tap is shown. First native waveform525/8.75s appears while prior ring tail fades. Keep blue vertical playhead fixed; add new bars next to it and translate existing history left, leaving a white future baseline to the right. Do not uniformly scale a completed waveform to fake recording.

Five checked raw/threshold anchors show bright-history left edge407at525→350at550→305at570→237at600→170at630 in a native crop, about−135.4px/s. The [samples](data/570-waveform-history.csv), [method/limits](data/570-waveform-history-measurement.json) and [mask proof](data/570-waveform-history-proof.jpg) measure near-white ink, exclude the blue playhead and future baseline, and miss faint antialiasing. Approximate edge uncertainty±2px; not an audio amplitude or synchronization track. Sent duration0:03 differs from shown~1.75s waveform interval; no unedited real-time capture is established.

Stop compression630/10.5s freezes the take and changes red square to white Play at the same bottom-center origin. Native634 shows old/new icon overlap; header simultaneously blurs from Voice Message/back to Cancel X and Send. Preview is crisp by645/10.75s. Send690/11.5s follows without a demonstrated preview-play tap. Ready-to-contact interval.75s includes anticipation~668; clean reading only~.383s. Preserve the meaning of each state rather than making Stop send immediately.

Send response begins691 with blur; blue outgoing audio bubble is visible but blurred~695–700 and clear by native707/11.783s. The ring stays at its old upper-right origin during return. Hold the new bubble as consequence; source retains it through750, then unmarked clock reset751–770 closes the loop. A finite promo should give its own adequate result hold. Audio was level-measured, not listened to.


##528: sustained drag indication and editable voice selection

[Voice trimming](https://t.me/TelegramTips/528) was reviewed by the reverse-study agent:540frames/18dense sheets,macro and17original-resolution anchors. A microphone press~40 becomes a sustained upward lock gesture53–84. Later trim handles move under a compressed indicator: left grip240→300 reduces42→32s; right330→360 reduces32→26s. Unlike separate taps, the sustained indicator follows its active source grip. Its release grows/fades afterward; a new independent ring may start while the preceding tail remains. Do not force sustained drags into a fixed-anchor discrete-tap envelope.

Discarded waveform dims while retained boundaries move; duration/play pill follows the kept selection's center. Right boundary stays fixed during left trim and left stays fixed during right trim. Final ready selection~380 toSend420 leaves~.67s including anticipation398. This is continuous semantic feedback, not uniform waveform scaling. No preview Play tap was demonstrated.

Pause180 morphs large green control/surface into waveform editor: broad green geometry spreads~184, waveform clear~196–200, secondary trash only~213. Preserve these separate arrival clocks. Native here means original-resolution evidence; flat video does not establish runtime implementation. For a new production, plan this as recorded UI when already captured, or explicitly authorized compositing of real UI assets; do not presume it belongs in app code.

Displayed timer10at90,20at120,30at150,40at180 advances20x relative to output time. It is a compressed demonstration, not real waiting. Send420 lifts26s draft into matching sent bubble, readable~438/settled450, held to520; unmarked downward reset521–537 restores opening. Chat insertion accommodation is not proof of a swipe, and reset is not deletion. Exact gesture/easing/material and implementation origin remain unknown.


##530: remote completion is a coordinated proof beat

[Collaborative checklists](https://t.me/TelegramTips/530) shows five remote results331/361/391/421/451, each.5s apart, **without local taps**. Each combines a purple check transition, participant avatar, name unfolding, rolling count and service message; row/service accommodation shifts chat beneath fixed chrome. Title/task emoji continue animating during later reading. Keep these clocks separate; a lone checkmark loses the collaboration proof. No new confetti burst follows all-complete. Final proof ready~465, held through540~1.25s; grain reset541 is editorial.

Form creation also overlaps fields: progressive Surprise Party title124–155 continues while first Cake task begins142. Later task words arrive as soft whole-word silhouettes with stagger153/163/173/183, final Music clear~198 and geometry settled~210 beforeSend240. No keyboard/caret or independent per-key timing is established. Future authoring should distinguish recorded form behavior from optional text/emoji overlays and keep existing animated emoji alive through useful holds.


##572: local error, retry release and staged success

[AI admins](https://t.me/TelegramTips/572),660-frame pass/22dense sheets and13original-resolution anchors, retains the question and all choices after wrong MOV contact240. Red first~244, right cross visible246, fully readable~254; strong red still present315. During retry anticipation308–330, old red/cross already fade: native325 nearly neutral,329 neutral, before WAV contact330; green/check clear334. Do not time old-error disappearance, retry contact and new feedback as one instantaneous cut. No physical input log was recovered. The warning line is clipped in native crop; exact bounds/exit cannot be inferred from it.

Success is a local page change351–420: old content slides/fades left while the badge enters from right. A check is **already present** at360, not proven stroke drawing. Badge centers~370, faint headline375, clear text390; next-action material faint395, clear405–410, near-rest420. Small notes/stars and overlapping lobed badge contours continue during hold. These separately staged tracks preserve hierarchy: symbol, explicit result, next action. Full success420→Continue480 allows~1s including ring anticipation458. Preserve useful reading time for a new task rather than automatically copying this short cadence. See [native phase limits](data/572-native-phase-notes.json).

Dismiss481–494 restores chat, with admission service~488, approval toast~489 and musical hand sticker; accommodation lifts conversation, not a demonstrated swipe. Durable status remains readable under active sticker through630. Untapped restoration631–650 is an editorial loop, not Leave Group or deletion. Outer bezel appears fixed; mini-app/base-chat recession is not camera zoom.


##534: retain count causality even when a reference compresses it

[Story albums534](https://t.me/TelegramTips/534) selects three images at contact proxies390/410/420 with overlapping indicator tails. Original-resolution418/420 still show only two blue checks, while CTA already says Add3Stories; third blue check starts423, full428. Record this reference inconsistency as a limit, not an authoring recipe. For a new promo, visible selected count, checks and submitted objects must agree. Add450 returns matching three thumbnails, settled480 and held to524~.73s. Subsequent profile expansion525–560 is internal UI; untapped tab/image reset581–595 is editorial, not a demonstrated deletion.

##547: slider channels update at different phases

[Live Stories547](https://t.me/TelegramTips/547) drags751–836. Native750 purple10/white thumb;770 cyan bubble leans with rolling digits while active thumb becomes glassy capsule;800 gold250→500 glyphs overlap vertically;818 red top bubble10000 while preview remains2000 and CTA rolls10000;836gray/preview10000/crown1,850settled. Bubble tracks thumb, changes width with digit count and relaxes tilt after release. Perks1m/60/1→1h/400/20 and preview rank/color have their own phases. Fine glints already live around control. Separate value path, thumb material, bubble placement/tilt/size, per-digit rolling, palette, perks, preview and CTA clocks; synchronized instant substitution loses observed detail. No exact original physics/renderer recovered.
