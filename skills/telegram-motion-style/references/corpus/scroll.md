# Scrolling: content motion and attention

Source: [Passkeys, Telegram Tips 551](https://t.me/TelegramTips/551). [Native content trajectory](data/551-scroll.csv) tracks the orange Devices icon in a fixed x380:580 source band over frames 0–180 (0–3.0 s). Full-context overlays at five anchors were inspected and consecutive motion frames were reviewed. The source is 1920 square, 60 fps.

The icon moves from y≈1803 to y≈585. The first displacement greater than 2 native pixels occurs at F40 (.667 s), with a gradual early build-up before the brisk passage. Its visible content speed increases to roughly 1300 px/s near 2.3 s, then decreases: approximately 1150 at 2.4 s, 600 at 2.6 s, 220 at 2.8 s, 95 at 2.9 s and effectively zero at 3.0 s. Normalize positions/velocity by the source height when comparing to another screen. Pixel derivatives carry quantization/compression noise; these are approximate content speeds, not finger velocity or proof of a physical release/inertia coefficient.

The slow early ramp is a feature of this source; do not mistake the whole gesture for one short flick or copy it blindly into a brisk promo.

The next target's tap anticipation begins around 2.633 s, during the decelerating tail; compression is near 3.0 s as the list comes to rest. The reference couples anticipation to arrival rather than inserting another full idle beat. This works because the target is approaching a predictable readable position. An unrelated camera move or immediate new tap on a still-unreadable result can break the same sequence.

For an authored clip: retain coherent native movement through its deceleration, ensure the target is readable when compression happens, and calculate quiet/anticipation holds from actual readiness. Do not cut within a gesture or manufacture a sudden stop by dropping its tail. This measured profile is one option, not a universal scroll speed, duration or permission to shorten the user's requested reading hold. Use real native gestures when capturing another app; do not replace its scrolling behavior with a global translate just to match these numbers.

## Second measured case: arrive on a grid tile

[Gift Purchase Offers, Telegram Tips553](https://t.me/TelegramTips/553),1920square60fps, supplies another measured handoff. All660frames were inspected in relevant crops. [Third-tile trajectory](data/553-scroll.csv) tracks a green tile's upper interior at fixed native x1195:1211, avoiding the first tile's frosted tap overlay. Six full-context anchors were audited. Approximate spatial precision is2–4px; this is not a corner/finger track.

The proxy moves y1834 at.5s→1800 at1s→1636 at1.5s→956 at2s→664 at2.5s→638 at2.65s→622 at2.833s→618 at2.933–3s. Peak finite-difference speed is roughly1980nativepx/s near1.867s, about1.03source-heights/s. This case has a brisk middle and a long decelerating tail. Initial header contraction/fade belongs to native content and is not camera zoom.

Next ring anticipation starts around F158(2.633s), with only about22px of remaining tile movement. Content is nearly at rest by F176(2.933s); compression is near F180(3s). Compare with551's slower measured trajectory: both coordinate anticipation with arrival, while speed and travel differ. Do not assume a universal scroll duration from this pattern.

The alternative first-tile color mask was invalid during F160–176 because frosted indicator pixels made it switch to other runs. Tracking an unoccluded neighbor recovered a coherent tail. When calibrating a new clip, choose a stable content feature away from touch/glass/particle overlays; plausible numeric output alone is not proof of a correct track.


## Settings wave while the list is still moving — 562

[Mighty Polls](https://t.me/TelegramTips/562), all1200frames checked, is a different handoff from551/553. Settings reveal begins aroundF510/8.5s. The [native cyan-icon trajectory](data/562-settings-scroll.csv) tracks Adding Options away from the right-side glass overlays. Its top is1706px atF520,1291at530,1063at540,938at550,877at560,860at568; approximately at restF569–599. The icon enters clipped at517; this does not recover its hidden earlier path or finger release. Ten full-context proof anchors were audited; threshold uncertainty is about2–3nativepx.

First switch ring compression is nearF540/9s, when about203px of list travel remains. First green tint starts~F535, before the radius minimum. Neighboring switches follow through~F579 with overlapping local glass deformation. This is a compact wave demonstrating four settings, not four normal tap cycles on independently settled targets. Do not infer that response always begins at maximum compression, or copy this compression to a consequential choice requiring reading.

Distinguish three upward motions in this one clip: adding three form rows~F453–475 makes the form accommodate their height; settings~F510–569 and published-card reveal~F660–696 traverse content; committing Seoul~F781–794 changes card height and chat placement. A continuous global translate cannot accurately substitute for all three. Phone width stays approximately constant. Use native content behavior and keep the reason for each movement explicit.


##571: nested table travel with overlapping vertical pickup

[Rich Text Formatting for Bots](https://t.me/TelegramTips/571),900frames/30dense sheets reviewed,21raw original-resolution anchors and2proxy boards checked. The table moves horizontally inside a rich answer, initially leaving its title/formula context fixed. A coherent grid-line track spans320–425: aligned native x958at320,941at330,826at350,509.5at370,86at390,−153at420,−164.5at425. Third-divider to fourth-divider handoff at370 uses a checked498.5pxoffset. [Samples](data/571-horizontal-grid.csv), [method](data/571-horizontal-grid-measurement.json) and [proof](data/571-horizontal-grid-proof.jpg) retain identity and±2pxuncertainty.

Ten-frame average content velocity grows from−102px/s320–330 to−1392px/s370–380, then falls to−240px/s410–420. This supports clear acceleration/deceleration; it does not establish native fling physics or exact spring coefficients. Last measured425 is **still moving**, so the window endpoint is not a recovered rest time.

Vertical movement begins before the table has fully stopped. A fixed-title ink proxy has top132at330/390,123at410,112at420,105at425, with~2pxuncertainty. See [title track](data/571-title-y.csv), [limits](data/571-title-y-measurement.json) and [proof](data/571-title-y-proof.jpg). Nine-pixel rise by410 confirms meaningful overlap; tiny initial1–2pxchanges do not identify exact onset. The earlier inventory's clean1s gap between axes was incorrect.

The entire answer then travels upward through formulas, questions and answer key, gradually arriving at matching opening-end layout near870. No back-to-top jump or separate reset is demonstrated. No large click ring or physical swipe/crown log establishes gesture delivery. Retrieve this as nested movement/axis handoff evidence, not a reason to add simultaneous diagonal motion everywhere. In production preserve separate table and message coordinate spaces and keep header/composer fixed; source-linked overlays need the correct parent transform.

##546: near-linear travel followed by explicit rebound and reading hold

[Bugs and Suggestions546](https://t.me/TelegramTips/546),630-frame full pass/17original anchors plus audited measurement proof, scrolls content under fixed soft-edge Back/menu chrome. Same Show100morecomments label row-profile proxy moves native y1688at420→1346at430→1167at435→988at440→810at445; near final crossing448–449; minimum702at454;734at465;750at480;752at485/500/515. Translation936px and50px overshoot (~5.34%travel,~2pxboundary uncertainty). [Samples](data/546-scroll-label-proxy.csv), [method](data/546-scroll-label-method.json), [audited label identity](data/546-scroll-label-proof.jpg). It is a16-band white-ink NCC proxy, not recovered transform/finger data.

Middle430–445 is nearly linear (~179px per5frames), then travel decelerates into one overshoot and returns through a long tail. Do not label the entire path exponential inertia or infer physical release; source gesture is unindicated. Ready comments hold~485–544 about1s before reverse scroll545–575; no immediate tap on still-moving comments. Keep travel, turn, settling and reading separate. This is an optional empirical replay profile, not a new universal scroll preset. Preserve actual native footage behavior in production; do not globally translate fixed chrome with content. Phone stays held throughout.
