# AI generation, revision and reading rhythm

Use this entity when a demo asks AI for content, changes an existing result or fixes text. Source: [AI Text Editor, Telegram Tips561](https://t.me/TelegramTips/561),19.5s at60fps. All1170consecutive frames inspected in relevant crops; native pending, correction and decorative anchors checked. Landmarks are visible source events, generally approximate within1–2frames, not hardware touches or measured network latency. Keep the approved authoring defaults unless the current request changes them.

## Choose the response treatment by what changes

| Operation in source | What remains recognizable | Response treatment | Useful adaptation |
| --- | --- | --- | --- |
| Biblical rewrite, contactF240/4s | Result region, controls, selected style | Old text fades → local skeleton → incremental new text; panel grows with line count | A newly generated alternative needs an acknowledged wait, then readable arrival |
| Short rewrite, contactF420/7s | Same panel and task | Old result fades quickly → skeleton → incremental shorter text; panel contracts | Changing a choice should retain context while replacing the affected result |
| Emojify, contactF540/9s | Existing concise sentence | Checkbox changes, inline emojis appear with stagger, text reflows | A local modification can keep most of the result readable |
| Fix, contactF840/14s | Original preview plus existing Result | Word-local blur/deformation/substitution, neighboring reflow, persistent blue wavy underlines | Show which spans changed without retyping the whole document |

Do not apply one loading animation indiscriminately to every AI operation. Use real app behavior when capturing; these edited source treatments describe communication choices, not proof of the product's implementation.

## Keep six timing landmarks separate

1. Displayed action/acknowledgement.
2. Old-result exit, if needed.
3. Active pending state.
4. First new information.
5. Complete, settled, readable result.
6. Next consequential action.

First rewrite: compressionF240, old dark-ink proxy reaches zero246/4.1s, but faint old glyphs remain as ghosts while skeleton becomes established~255/4.25s. Last skeleton frame299, one visibly blank output frame300/5s, first new ink301/5.017s. Thus request→first ink is61frames/~1.017s; established skeleton→first ink is~.767s. Do not call frame300 the first letter or use the dark-ink threshold as the disappearance time of all visible old text.

[Native dark-ink measurements](data/561-pending-measurement.json), with [CSV](data/561-pending-ink.csv), isolate maxRGB<110 inside the output band. Dark ink is439pixels at301,2373at305,5889at310,13631at320; ten proof anchors audited. This is an onset/area proxy, not glyph count, authored alpha, service latency or unique easing. Initial Original label may contribute to the old-count baseline. Do not extrapolate the fixed crop beyond the measured frames as the sheet moves.

The long rewrite continues through~F396/6.6s. Next choice420/7s leaves only~.4s after completion. Short rewrite similarly first appears481/8.017s and finishes~522/8.7s; Emojify540/9s leaves~.3s. These are brisk source holds, not defaults for reading dense content. Count the reading hold after the required result and framing are ready; waiting and streaming do not substitute for it. For another clip, preserve meaningful processing and then allocate the requested reading time, rather than slowing glyph entry to manufacture a pause.

## Make pending active but keep it bounded

Skeleton shimmer stays in the result region. Header, selected operation and action controls remain legible; small title sparkle and local style-row deformation can continue. During Short, new text begins while pale skeleton is still fading. This overlap differs from the first rewrite's blank frame. Keep old-result exit, skeleton fade and new ink as independent tracks; a single full-panel crossfade erases these distinctions.

Panel height adapts to result line count while the phone remains approximately fixed. [15bezel anchors](data/561-bezel-measurement.json) span341–344px in540scaled source, within1–2px endpoint uncertainty. Panel expansion/contraction, composer wraps and chat insertion are local layout changes, not camera zooms or manual scrolls. Exact panel-height easing is not recovered.

## Local correction can show its own evidence

Fix changes layout aroundF842: style options leave, compact Original English preview with `more` appears above Result. By~855 both are readable. Native860shows `have` changing under blur;900shows `Monday` changing after earlier corrections already gained underlines;935shows final corrections and underlines. Corrections progress through the sentence with overlapping tails, not all words at once. Text is settled around940/15.67s; send1020/17s leaves~1.33s for comparison.

Use separate tracks for changed-span blur/deformation, insertion/substitution, adjacent reflow and retained change marking. Preserve unchanged words as reading anchors. The source does not identify a precise word-warp engine or each token's easing.

## Delivery proves more than a generated preview

First send600/10s: result lifts into a recognizable bubble while editor lowers. Editor mostly leaves608, bubble settles in chat~630/10.5s. Second send1020/17s similarly delivers corrected text by~1040/17.33s. Both outcomes remain visible before untapped grain reset1111/18.517s; particles and chat reflow overlap, grain mostly clears1150/19.17s.

Keep preview, accepted/applied output and delivered result as distinct claims. For a finite scenario, end on its actual requested result and retain the approved final hold. The source's short proof and untapped reset are loop construction; they do not establish deletion or require adding another user action.


## Incoming chat response: distinguish command, first faint text and full reading — 564

[Managed Bots](https://t.me/TelegramTips/564) presses StartF360/6s. The action first becomes a right-aligned `/start` bubble, near-settled~380/6.333s. Faint incoming letters are visible atF392/6.533s through the translucent composer, then appear above it atF393/6.55s. The [audited left-band ink proxy](data/564-reply-left-ink-measurement.json) first detects205pixels at393because its lower exclusion intentionally avoids composer contamination. Native392proves that393is not the absolute first visible content.

The reply grows upward while new soft letters resolve and wrap through four lines. Earlier message and Today label move upward as content height grows; no manual swipe, skeleton or independent waiting spinner is shown. Complete greeting is clear aroundF490/8.167s, then held about.83s to profile compression540/9s. The initial sparse inventory's7.5scompletion was too early. All720frames, eight ink-proof anchors and raw391/392/393/490checked; the left-band mask clips the reply's right side and cannot establish its completion alone.

Thus source clocks are approximately.533sfrom Start to faint reply, .2sfrom near-settled command to faint reply,1.63sof progressive reply, then.83sof full-message reading. These are different intervals. None is an independently measured network latency or a universal AI timing preset. Compare561's bounded skeleton-to-result editor with this conversation reveal before choosing another app's response treatment. Preserve the whole request/response chain when retiming; extending a readable result is different from slowing the glyph animation.


## Streamed words, wrapping and orientation changes — 568

[Threads and Streaming Text for Bots](https://t.me/TelegramTips/568), all780frames reviewed, distinguishes prompt composition from answer delivery. The first prompt enters with a soft advancing front from~F94/1.567s and wraps into two composer lines. Send compression150/2.5s changes the active topic to Travel while the previous history fades under blur. Thinking begins~182; first incoming surface/ink appears~184–185/3.07–3.08s, about.57–.58s after Send. This is source cadence, not measured service latency.

The answer visibly contains unfinished words. Width grows before each wrap; height expands and the preceding question/Today label shift upward without a manual swipe. Native185shows `Koya`,215the first line,330only `ambianc` with a faint ending. Native338has a faint final e,345a pale period,350/5.833sa dark period. The [last-glyph ink samples](data/568-last-glyph-ink.csv), [threshold limits](data/568-last-glyph-measurement.json) and [four checked overlays](data/568-last-glyph-proof.jpg) track only a fixed ending c/e/period band:0darkpixelsF330,27at338,285at339,335at345,360at350. The threshold misses earlier faint ink and is not a whole-output detector. The initial sparse4.7s completion estimate was wrong.

First reply progression therefore lasts roughly2.75s, followed by only~.167s before layout-toggle compression360/6s. Its anticipation already begins~338while the last characters resolve. Do not count streaming as a reading hold or copy this compressed source beat into a dense new result. For another demo, retain a meaningful pending phase, natural text arrival and a separate adequate hold after completion.

The topic strip then reshapes into a left rail. Its upper-left control anchors the change; width contracts, vertical items emerge, Travel plane/name/blue active mark persist. Content width narrows and answer lines temporarily show old/new positions overlapped while reflowing; native365/370/380/390checked. This is a layout transformation, not a camera zoom or an extra manual scroll.

The follow-up enters~424–455/7.07–7.58s and wraps into three lines before Send480/8s. Incoming text starts~514–515/8.57–8.58s. The shorter itinerary continues through the reverse layout change at600/10s: native600has `2 da`,610`2 day`,620`2 days`. The rail-to-strip morph601–630 widens the existing result while its final characters finish. Distinguish content progress from layout progress; neither is evidence of another request. New compression660/11s shows a new-topic invitation after the result. The untapped blur reset from721restores older context for the loop; no Fitness-tab selection is shown.


##569: progressive instructions versus local rewrite fronts

[Custom AI Styles](https://t.me/TelegramTips/569) uses different text mechanisms within one fixed phone. Long instruction starts soft~270, develops across four lines, still has a soft final word at370 and is sharp at374/6.233s. Create390 follows only.267s later. Native273/300/329/350/370/374 show crisp established text behind a soft advancing front; no keyboard/caret is visible. This is not the opening composer's compressed whole-phrase entry~31–42.

Alien contact450 changes Original to Result451 while original copy is still present. Native455 blurs leading old text,461 shows old/new words coexisting on both lines,470 retains slight first-line softness,473 is crisp. This is a local replacement wave, not a new blank message streaming from the service. Both line fronts overlap; preserve stable card/header/copy icon to isolate the change. Send510 leaves only.617s from final clarity, including anticipation~488; do not adopt this as a default reading hold.

Another Example contacts720 and810 replace Before then After with staggered overlapping fronts, preserving Theater identity and animated masks. First changed card is clear~745, second~838. Add870 leaves~.533s after second clarity, while anticipation~848 consumes most clean reading time. These example landmarks were checked in every original frame at sheet scale; exact per-glyph easing is not measured.


##571: an explicit wait followed by structured block reveal

[Rich Text Formatting](https://t.me/TelegramTips/571) sharply separates a compressed prompt appearance30–54, outgoing delivery beginning121 and visible Thinking~134→firstanswer242, about1.8s. This is visible story timing, not measured backend latency. Original-resolution110/120/122 show no large frosted contact ring; describe response121 rather than fabricate a touch-down.

Thinking and new title overlap at242; container grows through subtitle, Exam Schedule and table. Native260 clips the lower part of Exam Schedule,280 clips the body row under its table header; prepared rich blocks become visible as the surface grows. This does not prove one universal per-glyph engine. The opening prompt similarly shows multiple line fronts concurrently under the placeholder37/45 and is sharp54, with no keyboard/caret. Do not turn this compressed multi-line treatment into ordinary typing speed.

Formulas heading~300 and theorem~315 establish hierarchy; vertical traversal later shows math, questions and key. Requested code/computer-science section is not demonstrated, and first viewport readiness is not completion time for the whole offscreen answer. No decorative burst is needed to carry this text-focused scene. Distinguish captured app behavior from a planned compositing treatment; reference provenance remains unknown.
