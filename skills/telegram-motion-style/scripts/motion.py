#!/usr/bin/env python3
"""Prepare Telegram Motion Style projects from one source-clock plan. No capture or automatic calibration."""
import argparse
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def resolve_file(root, name):
    require(isinstance(name, str) and bool(name), 'Expected a local asset path')
    p = (root / name).resolve()
    require(p.is_file(), 'Missing local asset: ' + str(p))
    return p


def digest_file(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def renderer_fingerprint():
    files = ['motion.py', 'render.py', 'vendor/compose.py', 'layers.py',
             'gestures.py', 'motion_profile.py']
    result = {name: digest_file(ROOT / 'scripts' / name) for name in files}
    for package in ('Pillow', 'numpy'):
        try:
            result[package] = version(package)
        except PackageNotFoundError:
            result[package] = None
    return result


def compile_plan(path):
    path = path.resolve()
    p = json.loads(path.read_text())
    root = path.parent
    require(p.get('version') == 1, 'plan.version must be 1')
    fps = p.get('fps', 60)
    require(isinstance(fps, int) and not isinstance(fps, bool) and fps > 0, 'Invalid fps')
    size = p.get('size', [1920, 1920])
    require(isinstance(size, list) and len(size) == 2 and all(
        isinstance(v, int) and not isinstance(v, bool) and v > 0 and v % 2 == 0 for v in size), 'Invalid even output size')
    start, end = p['trim']
    require(number(start) and number(end) and 0 <= start < end, 'Invalid source trim')

    def frame(t):
        require(number(t) and abs(t * fps - round(t * fps)) < .0001,
                'Timeline boundaries must be on the frame grid: ' + str(t))
        return round(t * fps)

    count = frame(end) - frame(start)
    texts, audio, taps, camera, layers = [], [], [], [], []
    used_ids = set()
    for group in p.get('groups', []):
        origin = group.get('origin', 0)
        require(number(origin), 'Group origin must be finite seconds')
        for event in group.get('events', []):
            event = dict(event)
            kind = event.pop('type')
            ident = event.pop('id')
            require(isinstance(ident, str) and ident and ident not in used_ids, 'Event ids must be nonempty and unique')
            used_ids.add(ident)
            at = origin + event.pop('at')
            require(number(at), 'Event time must be finite')
            if kind == 'tap':
                require(start <= at < end and all(number(event.get(k)) for k in ('x', 'y')), 'Invalid tap')
                taps.append({'time': at, 'x': event['x'], 'y': event['y']})
            elif kind == 'camera':
                require(event.get('curve', 'reference') == 'reference', 'Preserve V4 reference camera curve')
                require(number(event.get('duration')) and event['duration'] > 0, 'Camera needs positive duration')
                camera.append({**event, 'at': at, 'curve': 'reference'})
            elif kind in ('sprite', 'glint', 'swipe'):
                if kind == 'swipe':
                    require(number(event.get('duration')) and event['duration'] > 0
                            and start <= at < at + event['duration'] <= end + 1e-8,
                            'Swipe travel must be wholly inside trim')
                event.update(type=kind, start=at)
                for key in ('asset', 'repair'):
                    if key in event:
                        event[key] = str(resolve_file(root, event[key]))
                layers.append(event)
            elif kind in ('text', 'audio'):
                duration = event.pop('duration')
                require(number(duration) and duration > 0 and start <= at < at + duration <= end + 1e-8,
                        'Text/audio must be wholly inside trim: ' + ident)
                common = {'id': ident, 'from': frame(at) - frame(start), 'duration': frame(duration)}
                if kind == 'text':
                    require(event.get('space', 'composition') == 'composition', 'Only editorial composition-space text is implemented')
                    event.pop('space', None)
                    require(isinstance(event.get('text'), str), 'Text must be a string')
                    require(event.get('style', 'gentle') in ('gentle', 'emotional'), 'Invalid Gentle/Emotional style')
                    require(all(number(event.get(k)) for k in ('x', 'y', 'width')) and event['width'] > 0, 'Invalid text geometry')
                    # Catch invalid timing before browser/render startup.
                    cfg = event.get('timing', {})
                    require(isinstance(cfg, dict), 'timing must be an object')
                    for key in ('stagger', 'firstDelay', 'duration', 'pixelsPerUnit'):
                        if key in cfg:
                            require(number(cfg[key]) and (cfg[key] > 0 if key in ('duration', 'pixelsPerUnit') else cfg[key] >= 0), 'Invalid Gentle/Emotional timing')
                    texts.append({**event, **common})
                else:
                    src = resolve_file(root, event['src'])
                    trim = event.get('trimBefore', 0)
                    require(number(trim) and trim >= 0, 'Audio trimBefore must be nonnegative seconds')
                    volume = event.get('volume', 1)
                    require(number(volume) and 0 <= volume <= 1, 'Audio volume must be in 0..1')
                    audio.append({**common, '_source': str(src), 'trimBefore': frame(trim), 'volume': volume})
            else:
                raise ValueError('Unknown event type: ' + str(kind))
    taps.sort(key=lambda t: t['time'])
    require(all(a['time'] < b['time'] for a, b in zip(taps, taps[1:])), 'Duplicate tap contacts')
    camera.sort(key=lambda c: c['at'])
    require(all(a['at'] + a['duration'] <= b['at'] + 1e-8 for a, b in zip(camera, camera[1:])), 'Overlapping camera moves')
    b = dict(p['base'])
    muted = b.pop('muted', True)
    b['take'] = str((root / b['take']).resolve())
    b['bezel'] = str(resolve_file(root, b['bezel']))
    require(number(b.get('scale')) and b['scale'] > 0, 'base.scale must be actual recording pixels per point')
    if b.get('background') not in (None, 'gradient') and not b['background'].startswith('#'):
        b['background'] = str(resolve_file(root, b['background']))
    if 'backgroundVideo' in b:
        b['backgroundVideo'] = str(resolve_file(root, b['backgroundVideo']))
    rec = resolve_file(Path(b['take']), 'rec.mp4')
    fingerprints = {str(rec): digest_file(rec), b['bezel']: digest_file(Path(b['bezel']))}
    for layer in layers:
        for key in ('asset', 'repair'):
            if key in layer:
                fingerprints[layer[key]] = digest_file(Path(layer[key]))
    for key in ('background', 'backgroundVideo'):
        if key in b and Path(b[key]).is_file():
            fingerprints[b[key]] = digest_file(Path(b[key]))
    signature = hashlib.sha256(json.dumps([b, start, end, fps, size, taps, camera, layers,
                                          fingerprints, renderer_fingerprint()], sort_keys=True).encode()).hexdigest()
    return {'width': size[0], 'height': size[1], 'fps': fps, 'durationInFrames': count,
            'base': {'src': 'base.mp4', 'muted': muted}, 'texts': texts, 'audio': audio}, \
        {'config': b, 'start': start, 'end': end, 'taps': taps, 'camera': camera, 'layers': layers, 'signature': signature}


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(path)], text=True))['streams']


def prepare(plan, project, render_base=False, force_base=False):
    props, base = compile_plan(plan)
    require((project / 'package.json').is_file(), 'Initialize project first')
    generated = project / 'generated'
    generated.mkdir(exist_ok=True)
    public = project / 'public'
    public.mkdir(exist_ok=True)
    output = public / 'base.mp4'
    stamp = generated / 'base-signature.json'
    # Validate audio before starting the expensive video pass.
    audio_sources = []
    for index, audio in enumerate(props['audio']):
        src = Path(audio.pop('_source'))
        streams = [s for s in probe(src) if s['codec_type'] == 'audio']
        require(streams, 'Audio asset has no audio stream')
        needed = (audio['trimBefore'] + audio['duration']) / props['fps']
        require(float(streams[0].get('duration', 0)) + 1/props['fps'] >= needed, 'Audio asset ends before planned clip')
        name = 'audio-' + str(index) + src.suffix.lower()
        audio_sources.append((src, public / name))
        audio['src'] = name
    matches = (not force_base and output.is_file() and stamp.is_file()
               and json.loads(stamp.read_text()).get('signature') == base['signature'])
    if force_base or (render_base and not matches):
        # Use a derived take: never overwrite calibrated source taps.json.
        take = generated / 'take'
        take.mkdir(exist_ok=True)
        rec = Path(base['config']['take']) / 'rec.mp4'
        target = take / 'rec.mp4'
        if target.is_symlink():
            target.unlink()
        require(not target.exists(), 'Unexpected generated/take/rec.mp4 file')
        target.symlink_to(rec)
        (take / 'taps.json').write_text(json.dumps({'taps': base['taps']}))
        for key in ('camera', 'layers'):
            (generated / (key + '.json')).write_text(json.dumps(base[key] if key == 'camera' else {'version': 1, 'layers': base[key]}))
        b = base['config']
        pending = public / 'base.pending.mp4'
        require(not pending.exists(), 'Remove or inspect stale base.pending.mp4 before retry')
        cmd = [sys.executable, str(ROOT / 'scripts/render.py'), str(take), str(pending),
               '--bezel', b['bezel'], '--scale', str(b['scale']), '--start', str(base['start']), '--end', str(base['end']),
               '--fps', str(props['fps']), '--size', str(props['width']) + 'x' + str(props['height']),
               '--camera', str(generated / 'camera.json'), '--layers', str(generated / 'layers.json')]
        for key, flag in [('background', '--background'), ('colors', '--colors'), ('share', '--share'), ('backgroundVideo', '--background-video')]:
            if key in b:
                cmd.extend([flag, str(b[key])])
        subprocess.run(cmd, check=True)
        pending.replace(output)
        stamp.write_text(json.dumps({'signature': base['signature']}))
    elif matches:
        print('Reusing base:', output)
    require(output.is_file() and stamp.is_file(), 'Run prepare with --render-base first')
    require(json.loads(stamp.read_text())['signature'] == base['signature'], 'Base inputs changed; rerun with --render-base')
    video = next(s for s in probe(output) if s['codec_type'] == 'video')
    from fractions import Fraction
    require(int(video['width']) == props['width'] and int(video['height']) == props['height']
            and Fraction(video['r_frame_rate']) == props['fps']
            and int(video.get('nb_frames', -1)) == props['durationInFrames'], 'Base media does not match plan')
    for src, target in audio_sources:
        shutil.copy2(src, target)
    (project / 'props.json').write_text(json.dumps(props, ensure_ascii=False, indent=2))
    shutil.copy2(plan, generated / 'plan.snapshot.json')
    print('Prepared:', project, 'frames:', props['durationInFrames'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('project', type=Path)
    prep = sub.add_parser('prepare')
    prep.add_argument('plan', type=Path)
    prep.add_argument('project', type=Path)
    prep.add_argument('--render-base', action='store_true')
    prep.add_argument('--force-base', action='store_true', help='Render even when the base signature matches')
    check = sub.add_parser('check')
    check.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            require(not args.project.exists(), 'Project already exists; choose a new directory')
            shutil.copytree(ROOT / 'assets/remotion', args.project, ignore=shutil.ignore_patterns('node_modules', '.remotion', 'build'))
            shutil.copy2(ROOT / 'assets/text-motion/motion.mjs', args.project / 'src/motion.mjs')
            print('Initialized:', args.project)
        elif args.command == 'check':
            props, base = compile_plan(args.plan)
            print(json.dumps({'frames': props['durationInFrames'], 'baseSignature': base['signature'], 'textTracks': len(props['texts']), 'audioTracks': len(props['audio'])}))
        else:
            prepare(args.plan.resolve(), args.project.resolve(), args.render_base, args.force_base)
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError, StopIteration) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
