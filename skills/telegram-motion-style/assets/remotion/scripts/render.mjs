import {readFile, access, copyFile} from 'node:fs/promises';
import {constants} from 'node:fs';
import path from 'node:path';

const outputLocation = path.resolve(process.argv[2] ?? 'final.mp4');
let exists = false;
try {await access(outputLocation); exists = true;} catch {}
if (exists) throw new Error('Output exists; choose a new filename.');
const inputProps = JSON.parse(await readFile('props.json', 'utf8'));
if (!(inputProps.texts?.length || inputProps.audio?.length)) {
  // The base already contains the camera, bezel and gestures. No browser or
  // second H.264 pass is needed when there are no editorial tracks to add.
  const source = path.resolve('public', inputProps.base.src);
  if (path.dirname(source) !== path.resolve('public')) throw new Error('Expected a prepared local base video.');
  await copyFile(source, outputLocation, constants.COPYFILE_EXCL);
} else {
  const {bundle} = await import('@remotion/bundler');
  const {selectComposition, renderMedia} = await import('@remotion/renderer');
  const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx')});
  const browserExecutable = process.env.TELEGRAM_MOTION_BROWSER || undefined;
  const composition = await selectComposition({serveUrl, id: 'TelegramMotion', inputProps, browserExecutable});
  await renderMedia({serveUrl, composition, inputProps, outputLocation,
    codec: 'h264', crf: 16, pixelFormat: 'yuv420p', audioCodec: 'aac',
    imageFormat: 'png', concurrency: 2, browserExecutable});
}
console.log(outputLocation);
