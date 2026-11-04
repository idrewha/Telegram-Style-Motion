#!/usr/bin/env python3
"""Generate synthetic media for exercising Telegram Motion Style, not app footage or Apple artwork."""
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory', type=Path)
args = parser.parse_args()
args.directory.mkdir(parents=True, exist_ok=False)
take = args.directory / 'take'
take.mkdir()
image = Image.new('RGBA', (224, 424), '#111318')
ImageDraw.Draw(image).rectangle((12, 12, 211, 411), fill=(0, 0, 0, 0))
image.save(args.directory / 'synthetic-bezel.png')
subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
    'testsrc2=size=200x400:rate=60:duration=4', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(take / 'rec.mp4')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
    'sine=frequency=440:duration=1', str(args.directory / 'tone.wav')], check=True)
plan = {'version': 1, 'size': [480, 480], 'fps': 60, 'trim': [0, 4],
 'base': {'take': 'take', 'bezel': 'synthetic-bezel.png', 'scale': 1, 'background': '#172334'},
 'groups': [{'origin': 0, 'events': [
  {'id': 'camera', 'type': 'camera', 'at': 0, 'duration': .75, 'zoom': 1.15, 'focus': [100, 200], 'curve': 'reference'},
  {'id': 'tap', 'type': 'tap', 'at': 1.2, 'x': 100, 'y': 240},
  {'id': 'normal', 'type': 'text', 'at': 0, 'duration': 2, 'text': 'Тест Telegram Motion Style\nСлова 👋', 'style': 'normal', 'x': 16, 'y': 15, 'width': 448, 'fontSize': 30},
  {'id': 'emotional', 'type': 'text', 'at': 2, 'duration': 2, 'text': 'Emotional\nтекст ✨', 'style': 'emotional', 'x': 16, 'y': 15, 'width': 448, 'fontSize': 30},
  {'id': 'tone', 'type': 'audio', 'at': 2, 'duration': 1, 'src': 'tone.wav', 'volume': .1}
 ]}]}
(args.directory / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2))
print(args.directory / 'plan.json')
