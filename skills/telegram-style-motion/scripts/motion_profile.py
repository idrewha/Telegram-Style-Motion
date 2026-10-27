#!/usr/bin/env python3
"""Portable owner-approved V4 curves; no compositor, UI or third-party dependencies."""
import json
import math
from pathlib import Path

PRESET = json.loads((Path(__file__).resolve().parents[1] / 'assets/motion-presets/approved-v4.json').read_text())


def cubic_in_out(value):
    t = min(max(value, 0.0), 1.0)
    return 4*t*t*t if t < .5 else 1-(-2*t+2)**3/2


def cubic_out(value):
    t = min(max(value, 0.0), 1.0)
    return 1-(1-t)**3


def camera_progress(elapsed, duration=PRESET['camera']['durationSeconds']):
    """Dimensionless displacement, including overshoot. Scale/translation share it.

    Duration scales the complete shape, including its settlement. Reject invalid
    timings; constrain endpoints exactly so the camera stops rather than drifts.
    """
    if not math.isfinite(duration) or duration <= 0 or not math.isfinite(elapsed):
        raise ValueError('Camera timing must be finite and duration must be positive')
    if elapsed <= 0:
        return 0.0
    if elapsed >= duration:
        return 1.0
    c = PRESET['camera']
    t = elapsed/duration*c['durationSeconds']
    a,b = c['decayPerSecond'],c['angularFrequencyPerSecond']
    value = 1-math.exp(-a*t)*(math.cos(b*t)+(a/b)*math.sin(b*t))
    blend = cubic_in_out((t-c['terminalBlendStartSeconds']) /
                         (c['terminalBlendEndSeconds']-c['terminalBlendStartSeconds']))
    return value*(1-blend)+blend


def tap_state(relative):
    """Return outer radius / max, relative opacity, and inner / outer radius."""
    if not math.isfinite(relative):
        raise ValueError('Tap time must be finite')
    c = PRESET['tap']
    hole = c['initialInnerOuterRatio']
    if relative < c['appearanceSeconds'] or relative > c['endSeconds']:
        return 0.0,0.0,hole
    if relative < c['peakSeconds']:
        p = (relative-c['appearanceSeconds'])/(c['peakSeconds']-c['appearanceSeconds'])
        radius = c['initialRadiusFraction']+(1-c['initialRadiusFraction'])*cubic_out(p)
        return radius,cubic_in_out(p/c['opacityGrowthFraction']),hole
    if relative < 0:
        p = (relative-c['peakSeconds'])/(-c['peakSeconds'])
        return 1-(1-c['contactRadiusFraction'])*cubic_in_out(p),1.0,hole
    p = relative/c['endSeconds']
    radius = c['contactRadiusFraction']+(c['recoveryRadiusFraction']-c['contactRadiusFraction'])*cubic_out(p)
    return radius,1-cubic_in_out(p),hole+(c['finalInnerOuterRatio']-hole)*cubic_in_out(p)


if __name__ == '__main__':
    print(json.dumps({'preset':PRESET['id'],
                      'camera':[{'seconds':t,'progress':camera_progress(t)} for t in (0,.1,.2,.3,.4,.6,.75)],
                      'tap':[{'seconds':t,'state':tap_state(t)} for t in (-.37,-.17,0,.14,.28)]},indent=2))
