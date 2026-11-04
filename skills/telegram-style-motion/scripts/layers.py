"""Optional recorded-object extraction and restrained glints on the edited footage clock."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


class LayerPlan:
    def __init__(self, path, pixels_per_point, screen_size):
        self.tracks = []
        self.scale = pixels_per_point
        self.screen_size = screen_size
        path = Path(path)
        data = json.loads(path.read_text())
        if data.get('version') != 1 or not isinstance(data.get('layers'), list):
            raise ValueError('layers.json requires version:1 and layers:[]')
        for original in data['layers']:
            track = dict(original)
            if track.get('type') not in ('sprite', 'glint', 'swipe'):
                raise ValueError('Layer type must be sprite, glint or swipe')
            required = ['start', 'enter', 'hold', 'exit', 'scale'] if track['type'] == 'sprite' else ['start', 'duration', 'radius']
            if any(not finite(track.get(key)) for key in required):
                raise ValueError('Layer times/scales must be finite')
            if track['start'] < 0:
                raise ValueError('Layer start must be nonnegative')
            if track['type'] == 'sprite':
                if min(track['enter'], track['exit'], track['scale']) <= 0 or track['hold'] < 0:
                    raise ValueError('Sprite requires positive travel/scaling and nonnegative hold')
                rect = track.get('screenRect')
                if not isinstance(rect, list) or len(rect) != 4 or not all(finite(x) for x in rect):
                    raise ValueError('Sprite screenRect must be [x,y,width,height] in window points')
                x, y, w, h = rect
                if min(x, y) < 0 or min(w, h) <= 0 or (x+w)*self.scale > screen_size[0]+1 or (y+h)*self.scale > screen_size[1]+1:
                    raise ValueError('Sprite source rect outside recorded screen')
                for field in ['asset', 'repair']:
                    asset_path = path.parent / track[field]
                    source = Image.open(asset_path)
                    if source.mode != 'RGBA':
                        raise ValueError('Sprite and repair require RGBA PNG artwork/masks')
                    track[field] = source.copy()
                if track.get('exitCurve', 'smooth') not in ('smooth', 'settle'):
                    raise ValueError('Sprite exitCurve must be smooth or settle')
                sheen = track.get('sheen')
                if sheen is not None:
                    if not isinstance(sheen, dict) or not all(finite(sheen.get(k)) for k in ('start', 'duration', 'strength')):
                        raise ValueError('Sheen requires finite start, duration and strength')
                    if sheen['start'] < 0 or sheen['duration'] <= 0 or not 0 <= sheen['strength'] <= 1:
                        raise ValueError('Invalid sheen timing/strength')
                track['offset'] = track.get('offset', [0, 0])
                if len(track['offset']) != 2 or not all(finite(x) for x in track['offset']):
                    raise ValueError('Sprite offset must be two composition-frame fractions')
                if not finite(track.get('dim', 0)) or not 0 <= track.get('dim', 0) <= 1:
                    raise ValueError('Sprite dim must be in0..1')
            elif track['type'] == 'glint':
                anchor = track.get('anchor')
                if not isinstance(anchor, list) or len(anchor) != 2 or not all(finite(x) for x in anchor):
                    raise ValueError('Glint anchor must be two window points')
                if track['duration'] <= 0 or track['radius'] <= 0:
                    raise ValueError('Glint duration/radius must be positive')
            else:
                if track['duration'] <= 0 or track['radius'] <= 0:
                    raise ValueError('Swipe duration/radius must be positive')
                for name in ('from', 'to'):
                    point = track.get(name)
                    if not isinstance(point, list) or len(point) != 2 or not all(finite(x) for x in point):
                        raise ValueError('Swipe endpoints must be window-point pairs')
                    if not (0 <= point[0]*self.scale <= screen_size[0] and 0 <= point[1]*self.scale <= screen_size[1]):
                        raise ValueError('Swipe endpoint outside recorded screen')
                for key, default in [('anticipation', .22), ('release', .28)]:
                    if not finite(track.get(key, default)) or track.get(key, default) <= 0:
                        raise ValueError('Swipe envelopes must be finite and positive')
                if track['from'] == track['to']:
                    raise ValueError('Swipe must travel; use a tap for stationary contact')
                if 'path' in track:
                    points = track['path']
                    if not isinstance(points, list) or len(points) < 2:
                        raise ValueError('Swipe path needs at least two [seconds,x,y] samples')
                    previous = -1
                    for point in points:
                        if not isinstance(point, list) or len(point) != 3 or not all(finite(x) for x in point):
                            raise ValueError('Swipe path samples must be finite [seconds,x,y]')
                        if point[0] <= previous or point[0] < 0:
                            raise ValueError('Swipe path times must increase strictly')
                        if not (0 <= point[1]*self.scale <= screen_size[0] and 0 <= point[2]*self.scale <= screen_size[1]):
                            raise ValueError('Swipe path point outside recorded screen')
                        previous = point[0]
                    if abs(points[0][0]) > 1e-7 or points[-1][0] < track['duration']-1e-7:
                        raise ValueError('Swipe path must cover contact and travel')
                    held = track.get('heldRadius', .64)
                    if not finite(held) or held <= 0:
                        raise ValueError('Swipe heldRadius must be positive')
            self.tracks.append(track)

    @staticmethod
    def progress(track, time):
        local = time - track['start']
        a, b, c = track['enter'], track['hold'], track['exit']
        if local < 0 or local > a+b+c:
            return None
        if local < a:
            u = local/a
            return 1-(1-u)**3
        if local <= a+b:
            return 1.0
        u = (local-a-b)/c
        if track.get('exitCurve') == 'settle':
            # One small scale undershoot, then exact restoration. Position stays anchored.
            value = (1 + 8*u) * math.exp(-8*u) * math.cos(5*u)
            tail = min(1, max(0, (u-.75)/.25))
            return value * (1-tail*tail*(3-2*tail))
        return 1-u*u*(3-2*u)

    def prepare_screen(self, screen, time):
        active = [(t, self.progress(t, time)) for t in self.tracks if t['type']=='sprite']
        active = [(t, p) for t, p in active if p is not None]
        if not active:
            return screen
        result = screen.convert('RGBA')
        for track, p in active:
            x,y,w,h = track['screenRect']
            size = (round(w*self.scale),round(h*self.scale))
            repair = track['repair'].resize(size,Image.Resampling.LANCZOS)
            result.alpha_composite(repair,(round(x*self.scale),round(y*self.scale)))
            dim = track.get('dim',0)*max(0,p)
            if dim:
                shade=Image.new('RGBA',result.size,(0,0,0,round(255*dim)))
                result=Image.alpha_composite(result,shade)
        return result.convert('RGB')

    def draw(self, frame, time, project, output_pixels_per_point):
        for track in self.tracks:
            if track['type']=='sprite':
                p=self.progress(track,time)
                if p is None:continue
                x,y,w,h=track['screenRect']
                cx,cy=project(x+w/2,y+h/2)
                cx+=track['offset'][0]*frame.width*p
                cy+=track['offset'][1]*frame.height*p
                grow=1+(track['scale']-1)*p
                size=(max(1,round(w*output_pixels_per_point*grow)),max(1,round(h*output_pixels_per_point*grow)))
                sprite=track['asset'].resize(size,Image.Resampling.LANCZOS)
                sheen = track.get('sheen')
                if sheen:
                    phase=(time-track['start']-sheen['start'])/sheen['duration']
                    if 0 < phase < 1:
                        # Soft diagonal band, clipped to the real object's alpha.
                        import numpy as np
                        yy,xx=np.mgrid[0:size[1],0:size[0]]
                        position=(xx+yy*.3)/max(1,size[0]+size[1]*.3)
                        band=np.exp(-((position-(-.2+1.4*phase))/.16)**2)
                        band*=math.sin(math.pi*phase)*255*sheen['strength']
                        mask=Image.fromarray(band.astype('uint8'))
                        mask=ImageChops.multiply(mask,sprite.getchannel('A'))
                        light=Image.new('RGBA',size,(255,247,222,0));light.putalpha(mask)
                        sprite=Image.alpha_composite(sprite,light)
                left,top=round(cx-size[0]/2),round(cy-size[1]/2)
                if p>0:
                    shadow=Image.new('RGBA',(size[0]+80,size[1]+80))
                    shadow.paste((0,0,0,round(45*p)),(40,46),sprite.getchannel('A'))
                    shadow=shadow.filter(ImageFilter.GaussianBlur(10*p))
                    frame.alpha_composite(shadow,(left-40,top-40))
                frame.alpha_composite(sprite,(left,top))
            elif track['type'] == 'glint':
                phase=(time-track['start'])/track['duration']
                if not 0<phase<1:continue
                envelope=math.sin(math.pi*phase)
                cx,cy=project(*track['anchor'])
                radius=track['radius']*output_pixels_per_point*envelope
                local=Image.new('RGBA',frame.size)
                d=ImageDraw.Draw(local)
                points=[(cx,cy-radius),(cx+radius*.23,cy-radius*.23),(cx+radius,cy),(cx+radius*.23,cy+radius*.23),(cx,cy+radius),(cx-radius*.23,cy+radius*.23),(cx-radius,cy),(cx-radius*.23,cy-radius*.23)]
                d.polygon(points,fill=(255,249,231,round(210*envelope)))
                glow=local.filter(ImageFilter.GaussianBlur(max(1,radius*.25)))
                frame.alpha_composite(glow);frame.alpha_composite(local)
            else:
                from gestures import swipe_state
                from vendor.compose import ring
                state = swipe_state(track, time)
                if state is None:
                    continue
                x, y, share, alpha, hole = state
                cx, cy = project(x, y)
                ring(frame, cx, cy, track['radius']*output_pixels_per_point*share,
                     alpha, 'telegram', hole)
