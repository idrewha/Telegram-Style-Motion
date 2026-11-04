import {bundle} from '@remotion/bundler';
import {selectComposition, renderMedia} from '@remotion/renderer';
import {readFile, access} from 'node:fs/promises';
import path from 'node:path';

const outputLocation = path.resolve(process.argv[2] ?? 'final.mp4');
let exists = false;
try {await access(outputLocation); exists = true;} catch {}
if (exists) throw new Error('Output exists; choose a new filename.');
const inputProps = JSON.parse(await readFile('props.json', 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx')});
const browserExecutable = process.env.TG_UP_BROWSER || undefined;
const composition = await selectComposition({serveUrl, id: 'TGUp', inputProps, browserExecutable});
await renderMedia({serveUrl, composition, inputProps, outputLocation,
  codec: 'h264', crf: 16, pixelFormat: 'yuv420p', audioCodec: 'aac',
  imageFormat: 'png', concurrency: 2, browserExecutable});
console.log(outputLocation);
