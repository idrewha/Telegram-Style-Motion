import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, mkdir, writeFile, readFile, copyFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

test('base-only export needs no browser or Remotion installation and preserves bytes', async () => {
  const root = await mkdtemp(path.join(tmpdir(), 'motion-export-'));
  try {
    await mkdir(path.join(root, 'public'));
    // No node_modules in this workspace: a browser render would fail.
    await copyFile(new URL('./render.mjs', import.meta.url), path.join(root, 'render.mjs'));
    const base = Buffer.from('already-encoded-video');
    await writeFile(path.join(root, 'public/base.mp4'), base);
    await writeFile(path.join(root, 'props.json'), JSON.stringify({base: {src: 'base.mp4', muted: true}, texts: [], audio: []}));
    const run = () => spawnSync(process.execPath, ['render.mjs', 'final.mp4'], {cwd: root, encoding: 'utf8'});
    const first = run();
    assert.equal(first.status, 0, first.stderr);
    assert.deepEqual(await readFile(path.join(root, 'final.mp4')), base);
    const second = run();
    assert.notEqual(second.status, 0);
    assert.match(second.stderr, /Output exists/);
    assert.deepEqual(await readFile(path.join(root, 'final.mp4')), base);
  } finally {
    await rm(root, {recursive: true, force: true});
  }
});
