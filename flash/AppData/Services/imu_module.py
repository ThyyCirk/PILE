import math
import time
from M5 import Imu

# ─── CONFIGURATION ────────────────────────────────────────
SHAKE_THRESHOLD  = 2.5       # total accel magnitude change (in g) to trigger shake
SHAKE_COOLDOWN   = 500       # ms to ignore after a shake event

TILT_THRESHOLD   = 20        # degrees — how far from level to consider "tilted"
RETURN_THRESHOLD = 5         # degrees — how close to original to consider "returned"

# ─── INTERNAL STATE ───────────────────────────────────────
_last_shake_time = 0
_initial_angles  = None      # (pitch, roll) saved when "start tracking" is called
_was_tilted      = False     # whether we've already reported the tilt event
_tilted_axis     = None

# ─── EVENT FLAGS (set by tick(), read by main loop) ──────
shake_detected   = False     # True for one cycle after a shake
tilted_this_frame = None     # dict or None — set when tilt first occurs
returned_this_frame = False  # True for one cycle after returning to home

# ─── HELPERS ───────────────────────────────────────────────

def _read_accel():
    """Returns (ax, ay, az) in g units."""
    accel = Imu.getAccel()
    return (accel[0], accel[1], accel[2])

def _accel_magnitude(ax, ay, az):
    return math.sqrt(ax*ax + ay*ay + az*az)

def _angles_from_accel(ax, ay, az):
    """Returns (pitch, roll) in degrees."""
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))
    roll  = math.degrees(math.atan2(ay, az))
    return (pitch, roll)

# ─── PUBLIC API ───────────────────────────────────────────

def reset():
    """Call once in setup() to initialise."""
    global _initial_angles
    ax, ay, az = _read_accel()
    _initial_angles = _angles_from_accel(ax, ay, az)

def set_initial_position():
    """Save the current orientation as the 'home' position."""
    global _initial_angles
    ax, ay, az = _read_accel()
    _initial_angles = _angles_from_accel(ax, ay, az)

def get_accel():
    return _read_accel()

def get_angles():
    ax, ay, az = _read_accel()
    return _angles_from_accel(ax, ay, az)

def tick():
    """
    Call this every frame from the main loop.
    It updates the event flags: shake_detected, tilted_this_frame, returned_this_frame.
    """
    global _last_shake_time, _was_tilted, _tilted_axis
    global shake_detected, tilted_this_frame, returned_this_frame

    # Reset frame flags at the start of every tick
    shake_detected   = False
    tilted_this_frame = None
    returned_this_frame = False

    ax, ay, az = _read_accel()
    mag = _accel_magnitude(ax, ay, az)
    pitch, roll = _angles_from_accel(ax, ay, az)

    # ─── 1. Shake detection ──────────────────────────────
    now = time.ticks_ms()
    if abs(mag - 1.0) > SHAKE_THRESHOLD and (now - _last_shake_time) > SHAKE_COOLDOWN:
        shake_detected = True
        _last_shake_time = now

    # ─── 2. Tilt detection ───────────────────────────────
    # Determine dominant axis of tilt
    tilt_result = None
    if abs(pitch) > abs(roll) and abs(pitch) > TILT_THRESHOLD:
        tilt_result = {'axis': 'x', 'pitch': pitch, 'roll': roll}
    elif abs(roll) > TILT_THRESHOLD:
        tilt_result = {'axis': 'y', 'pitch': pitch, 'roll': roll}

    # Edge: level → tilted  (fires ONCE)
    if tilt_result and not _was_tilted:
        _was_tilted = True
        _tilted_axis = tilt_result['axis']
        tilted_this_frame = tilt_result

    # Edge: tilted → level (reset for next tilt)
    if not tilt_result:
        _was_tilted = False
        _tilted_axis = None

    # ─── 3. Return detection ─────────────────────────────
    if _was_tilted and _initial_angles is not None:
        p0, r0 = _initial_angles
        if abs(pitch - p0) < RETURN_THRESHOLD and abs(roll - r0) < RETURN_THRESHOLD:
            returned_this_frame = True
            _was_tilted = False   # reset
            _tilted_axis = None