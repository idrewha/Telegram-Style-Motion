import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sample, textPlan, totalDuration} from '../src/motion.mjs';

test('Cyrillic, ZWJ emoji, combining marks, spaces and continuous newline clock', () => {
  const p = textPlan('Я 👨‍👩‍👧‍👦\nе\u0301!');
  const units = p.parts.flatMap(p => p.units ?? []);
  assert.deepEqual(units.map(u => u.text), ['Я', ' ', '👨‍👩‍👧‍👦', 'е\u0301', '!']);
  assert.deepEqual(units.map(u => u.index), [0, 1, 2, 3, 4]);
});
test('seeking is deterministic and the final frame is natural', () => {
  for (const style of ['gentle', 'emotional']) {
    const before = sample(style, .09, 2);
    sample(style, 100, 2);
    assert.deepEqual(sample(style, .09, 2), before);
    assert.deepEqual(sample(style, totalDuration(3, style), 2),
      {opacity: 1, y: 0, scaleY: 1, rotation: 0, blur: 0});
  }
});
test('Gentle has no blur; Emotional has overshoot with bounded material values', () => {
  let overshoot = false;
  for (let n = 0; n < 400; n++) {
    const t = n/1000;
    assert.equal(sample('gentle', t).blur, 0);
    const v = sample('emotional', t);
    overshoot ||= v.y < 0;
    assert.ok(v.opacity >= 0 && v.opacity <= 1 && v.blur >= 0);
  }
  assert.ok(overshoot);
});
