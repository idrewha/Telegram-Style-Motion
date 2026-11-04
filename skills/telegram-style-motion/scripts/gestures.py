"""Frame-driven moving touch indicator; material is shared with the tap renderer."""
import math
from bisect import bisect_right
from motion_profile import tap_state, cubic_in_out, cubic_out


def path_point(track, local):
    points = track.get('path')
    if points:
        times = [p[0] for p in points]
        i = bisect_right(times, local)
        if i == 0:
            return tuple(points[0][1:])
        if i == len(points):
            return tuple(points[-1][1:])
        a, b = points[i-1], points[i]
        p = (local-a[0])/(b[0]-a[0])
        return a[1]+(b[1]-a[1])*p, a[2]+(b[2]-a[2])*p
    progress = min(1, max(0, local/track['duration']))
    return (track['from'][0] + (track['to'][0]-track['from'][0])*progress,
            track['from'][1] + (track['to'][1]-track['from'][1])*progress)


def swipe_state(track, time):
    local = time - track['start']
    duration = track['duration']
    anticipation = track.get('anticipation', .22)
    release = track.get('release', .28)
    if local < -anticipation or local >= duration + release:
        return None
    if track.get('steady', bool(track.get('path'))):
        # Position follows the measured source clock, including any stationary
        # frames and the lift fade. Fade only; never pulse size during a drag.
        radius, hole = track.get('heldRadius', .64), .60
        if local < 0:
            alpha = cubic_in_out((local+anticipation)/anticipation)
        elif local <= duration:
            alpha = 1.0
        else:
            alpha = 1-cubic_in_out((local-duration)/release)
        x, y = path_point(track, max(0, local))
        return x, y, radius, alpha, hole
    if local < 0:
        radius, alpha, hole = tap_state(local * .37 / anticipation)
        progress = 0
    elif local <= duration:
        progress = local / duration
        radius = .50 + .14 * cubic_out(min(1, local / .10))
        alpha, hole = 1.0, .60
    else:
        progress = 1
        p = (local-duration) / release
        radius = .64 + .10*cubic_out(p)
        alpha, hole = 1-cubic_in_out(p), .60+.20*cubic_in_out(p)
    x = track['from'][0] + (track['to'][0]-track['from'][0])*progress
    y = track['from'][1] + (track['to'][1]-track['from'][1])*progress
    return x, y, radius, alpha, hole
