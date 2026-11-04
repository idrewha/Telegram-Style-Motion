import { keyframes, textPlan, timing } from './motion.mjs';
const active = new WeakMap();

/** One-shot reveal of a text-only host. Existing typography/color stay on the host.
 * Returns {finished, cancel}; finished resolves to {cancelled:boolean} without double waiting.
 */
export function revealText(host, { style = 'normal', ...options } = {}) {
  active.get(host)?.cancel();
  if (Array.from(host.childNodes).some(n => n.nodeType !== 3)) {
    throw new TypeError('Use a text-only host; preserve rich markup in a host-specific adapter');
  }
  const cfg = timing(style, options), plan = textPlan(host.textContent);
  const whiteSpace = host.ownerDocument.defaultView?.getComputedStyle(host).whiteSpace;
  if (whiteSpace && !['pre', 'pre-wrap', 'break-spaces'].includes(whiteSpace)
      && /[\r\n\t]| {2,}/.test(host.textContent)) {
    throw new TypeError('Whitespace would change: use a pre-wrap text host or a host-specific layout adapter');
  }
  if (!plan.unitCount || globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
    return { finished: Promise.resolve({ cancelled: false }), cancel() {} };
  }
  const doc = host.ownerDocument, original = Array.from(host.childNodes), visual = doc.createElement('span');
  visual.setAttribute('aria-hidden', 'true');
  const readable = doc.createElement('span');
  readable.textContent = host.textContent;
  Object.assign(readable.style, { position:'absolute', width:'1px', height:'1px', padding:'0',
    margin:'-1px', overflow:'hidden', clip:'rect(0, 0, 0, 0)', whiteSpace:'nowrap', border:'0' });
  const units = [];
  for (const part of plan.parts) {
    if ('break' in part) { visual.append(doc.createElement('br')); continue; }
    const word = doc.createElement('span');
    Object.assign(word.style, { display:'inline-block', whiteSpace:'nowrap' });
    for (const unit of part.units) {
      const span = doc.createElement('span'); span.textContent = unit.text;
      Object.assign(span.style, { display:'inline-block', whiteSpace:'pre', transformOrigin:'50% 55%' });
      word.append(span); units.push({ span, index:unit.index });
    }
    visual.append(word);
  }
  const frames = keyframes(style, options);
  host.replaceChildren(visual, readable);
  const animations = [];
  let settled = false, resolve;
  const finished = new Promise(r => { resolve = r; });
  const restore = cancelled => {
    if (settled) return;
    settled = true;
    // Do not overwrite text that the host application replaced while this reveal ran.
    if (visual.parentNode === host && readable.parentNode === host) host.replaceChildren(...original);
    animations.forEach(a => a.cancel());
    if (active.get(host) === controller) active.delete(host);
    resolve({ cancelled });
  };
  const controller = { finished, cancel: () => restore(true) };
  active.set(host, controller);
  try {
    for (const {span,index} of units) {
      animations.push(span.animate(frames, { duration:cfg.duration*1000,
        delay:(cfg.firstDelay+index*cfg.stagger)*1000, easing:'linear', fill:'both' }));
    }
    Promise.all(animations.map(a => a.finished)).then(() => restore(false), () => restore(true));
  } catch (error) { restore(true); throw error; }
  return controller;
}
