# harmonic_helix_binary_date.py
#
# 3‑D parametric helix whose ripple pattern encodes the date 2023‑08‑05 in binary
# Author: Aaron Snyder (April 2025)

import numpy as np

# ────────────────────────────────────────────────────────────────────────────────
# 1.  DATA TO ENCODE
# ────────────────────────────────────────────────────────────────────────────────
DATE_STR   = "2023-08-05"
date_int   = int(DATE_STR.replace("-", ""))        # 20230805
bin_str    = format(date_int, "b")                 # '1001101001011001010010101'
bits       = bin_str[::-1]                         # LSB → harmonic #1

# ────────────────────────────────────────────────────────────────────────────────
# 2.  HELIX & SAMPLING PARAMETERS  (feel free to tweak)
# ────────────────────────────────────────────────────────────────────────────────
RADIUS          = 100.0   # mm   – base helix radius
PITCH           = 20.0   # mm   – rise per turn
TURNS           = 5     #      – total turns
SAMPLES_TURN    = 50    #      – resolution
BASE_AMP        = 2.0    # mm   – ripple size when bit = 1
PHASE_SHIFT     = 0.0    # rad  – optional global phase tweak

# build amplitude list (harmonic i  ↔  bits[i‑1])
amplitudes = [(BASE_AMP if b == "1" else 0.0) for b in bits]
MAX_HARM   = len(amplitudes)

# ────────────────────────────────────────────────────────────────────────────────
# 3.  GENERATE THE CURVE
# ────────────────────────────────────────────────────────────────────────────────
total_samples = TURNS * SAMPLES_TURN
t = np.linspace(0.0, 2.0 * np.pi * TURNS, total_samples)

xyz = np.zeros((total_samples, 3))

for idx, tt in enumerate(t):
    radial_offset = sum(
        A * np.sin(n * tt + PHASE_SHIFT)              # n = harmonic index (1‑based)
        for n, A in enumerate(amplitudes, start=1)
    )
    r = RADIUS + radial_offset                       # instantaneous radius

    xyz[idx, 0] = r * np.cos(tt)                     # x
    xyz[idx, 1] = r * np.sin(tt)                     # y
    xyz[idx, 2] = PITCH * tt / (2.0 * np.pi)         # z (grows linearly)

# ────────────────────────────────────────────────────────────────────────────────
# 4.  SAVE → CSV  (Onshape:  “Curve from CSV”  →  Spline  →  Sweep a circle)
# ────────────────────────────────────────────────────────────────────────────────
np.savetxt("helix_points_3.csv", xyz, delimiter=",", fmt="%.5f")
print(f"🚀  {total_samples} points written to 'helix_points_3.csv'")
