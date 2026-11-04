/** Independent renderer-neutral implementation of the documented Gentle/Emotional formulas.
 * Provenance and the adapted promo clock: references/text-motion.md.
 * Times in seconds; distances in source pixels divided by pixelsPerUnit.
 */
const NATURAL = Object.freeze({ opacity: 1, y: 0, scaleY: 1, rotation: 0, blur: 0 });
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));

export function timing(style = 'gentle', options = {}) {
  if (!['gentle', 'emotional'].includes(style)) throw new RangeError('Unknown Gentle/Emotional style');
  const preset = options.preset ?? 'promo';
  if (!['promo', 'source'].includes(preset)) throw new RangeError('Unknown timing preset');
  const source = style === 'gentle'
    ? { stagger: .015, duration: .500, firstDelay: 0 }
    : { stagger: .025, duration: .680, firstDelay: .025 };
  const base = preset === 'source' ? source : { stagger: .018, duration: .300, firstDelay: .018 };
  const stagger = options.stagger ?? base.stagger;
  const duration = options.duration ?? base.duration;
  const firstDelay = options.firstDelay ?? (preset === 'promo' ? stagger : base.firstDelay);
  const pixelsPerUnit = options.pixelsPerUnit ?? 1;
  if (![stagger, duration, firstDelay, pixelsPerUnit].every(Number.isFinite)
      || stagger < 0 || duration <= 0 || firstDelay < 0 || pixelsPerUnit <= 0) {
    throw new RangeError('Require finite nonnegative delays and positive duration/pixel scale');
  }
  return { stagger, duration, firstDelay, pixelsPerUnit };
}

// Invert Bezier X, then evaluate Y. Substituting Y(u) for Y(X^-1(time)) changes the easing.
export function gentleEase(time) {
  time = clamp(time);
  const bezier = (u, p, q) => 3 * (1-u) ** 2 * u * p + 3 * (1-u) * u*u * q + u**3;
  let lo = 0, hi = 1;
  for (let n = 0; n < 36; n++) {
    const u = (lo + hi) / 2;
    if (bezier(u, .2, .2) < time) lo = u; else hi = u;
  }
  return bezier((lo + hi)/2, .8, 1);
}

export function emotionalSelector(local, duration = .300) {
  if (!Number.isFinite(local) || !Number.isFinite(duration) || duration <= 0) {
    throw new RangeError('Invalid selector time');
  }
  if (local <= 0) return 1;
  if (local >= duration) return 0;
  const sourceTime = local * (.680 / duration);
  if (sourceTime < .180) return 1 - sourceTime / .180;
  const d = sourceTime - .180, w = 2 * Math.PI;
  return (-1 / .180) * Math.sin(d*w) / (Math.exp(10*d)*w);
}

export function sample(style, elapsed, index = 0, options = {}) {
  const cfg = timing(style, options);
  if (!Number.isFinite(elapsed) || !Number.isInteger(index) || index < 0) {
    throw new RangeError('Require finite elapsed seconds and a nonnegative unit index');
  }
  const local = elapsed - cfg.firstDelay - index * cfg.stagger;
  if (local >= cfg.duration) return { ...NATURAL };
  if (style === 'gentle') {
    const e = local <= 0 ? 0 : gentleEase(local/cfg.duration);
    return { opacity: e, y: 15*(1-e)/cfg.pixelsPerUnit, scaleY: 1, rotation: 0, blur: 0 };
  }
  const p = emotionalSelector(local, cfg.duration);
  return { opacity: clamp(1-p), y: 32*p/cfg.pixelsPerUnit,
    scaleY: 1-.22*p, rotation: 12*p, blur: 10*Math.max(p,0)/cfg.pixelsPerUnit };
}

export function totalDuration(unitCount, style = 'gentle', options = {}) {
  const c = timing(style, options);
  if (!Number.isInteger(unitCount) || unitCount < 0) throw new RangeError('Invalid unit count');
  return unitCount ? c.firstDelay + (unitCount-1)*c.stagger + c.duration : 0;
}

export function graphemes(text) {
  if (typeof text !== 'string') throw new TypeError('Expected a string');
  if (typeof Intl.Segmenter !== 'function') {
    if (/^[\x00-\x7F]*$/.test(text)) return Array.from(text);
    throw new Error('Intl.Segmenter or a grapheme polyfill is required for non-ASCII text');
  }
  return Array.from(new Intl.Segmenter(undefined, { granularity: 'grapheme' }).segment(text), x => x.segment);
}

/** Words retain trailing spaces. Explicit line breaks consume no reveal-clock slot.
 * Natural wrapping also never resets the index. Preserve the original string exactly.
 */
export function textPlan(text) {
  let index = 0;
  const parts = [];
  for (const line of text.split(/(\r\n|\r|\n)/)) {
    if (/^(\r\n|\r|\n)$/.test(line)) { parts.push({ break: line }); continue; }
    for (const word of line.match(/\S+\s*|\s+/gu) ?? []) {
      parts.push({ units: graphemes(word).map(text => ({ text, index: index++ })) });
    }
  }
  return { parts, unitCount: index };
}

/** Dense samples for WAAPI/Motion; evaluators such as Canvas/Remotion may call sample directly. */
export function keyframes(style, options = {}) {
  const cfg = timing(style, options), frames = Math.max(1, Math.ceil(cfg.duration*120));
  const localOptions = { ...options, firstDelay: 0 };
  return Array.from({ length: frames+1 }, (_, n) => {
    const offset = n/frames, p = sample(style, offset*cfg.duration, 0, localOptions);
    const frame = { offset, opacity: p.opacity,
      transform: `translateY(${p.y}px) rotate(${p.rotation}deg) scaleY(${p.scaleY})` };
    // Gentle must not animate filter/blur, including a redundant zero-blur track.
    if (style === 'emotional') frame.filter = `blur(${p.blur}px)`;
    return frame;
  });
}
