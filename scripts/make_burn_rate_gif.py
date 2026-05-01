#!/usr/bin/env python
"""
make_burn_rate_gif.py
---------------------
Reads burn_rates.txt (produced by the main analysis script) and generates
a 4-second animated GIF of the instantaneous burn-rate data points being
revealed from left (earliest time) to right (latest time).

Usage:
    python make_burn_rate_gif.py                        # uses burn_rates.txt in cwd
    python make_burn_rate_gif.py path/to/burn_rates.txt # custom input path
    python make_burn_rate_gif.py burn_rates.txt out.gif  # custom input + output
"""

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ── Config ────────────────────────────────────────────────────────────────────
GIF_DURATION_SEC = 4          # total wall-clock length of the GIF
N_FRAMES         = 80         # more frames → smoother; 80 @ 4 s = 20 fps
MOVING_AVG_WIN   = 10         # must match window used in plot_burn_rates()
OUTPUT_GIF       = "burn_rate_animation.gif"
DPI              = 120
# ─────────────────────────────────────────────────────────────────────────────


def read_burn_rates(filename: str):
    """Parse burn_rates.txt written by save_burn_rates().

    Returns (times, rates, avg_burn_avg, avg_burn_max).
    The first two lines of the file are:
        \nOverall Average Burn Rate (Avg X): ...
        Overall Average Burn Rate (Max X): ...
    then a CSV header, then data rows.
    """
    avg_burn_avg = None
    avg_burn_max = None
    times, rates = [], []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Overall Average Burn Rate (Avg X):"):
                avg_burn_avg = float(line.split(":")[1].strip())
            elif line.startswith("Overall Average Burn Rate (Max X):"):
                avg_burn_max = float(line.split(":")[1].strip())
            elif line.startswith("Time"):          # CSV header – skip
                continue
            else:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 2:
                    try:
                        times.append(float(parts[0]))
                        rates.append(float(parts[1]))
                    except ValueError:
                        continue

    if not times:
        raise RuntimeError(f"No burn-rate data found in '{filename}'.")

    return times, rates, avg_burn_avg, avg_burn_max


def moving_average(data, window):
    """Numpy convolution moving average (same length as input)."""
    w = np.ones(window) / window
    return np.convolve(data, w, mode="same")


def make_gif(input_file: str, output_file: str):
    times_raw, rates_raw, avg_avg, avg_max = read_burn_rates(input_file)

    times = np.array(times_raw)
    rates = np.array(rates_raw)
    rates_ma = moving_average(rates, MOVING_AVG_WIN)

    t_min, t_max = times.min(), times.max()
    r_min = min(rates.min(), rates_ma.min())
    r_max = max(rates.max(), rates_ma.max())
    pad = (r_max - r_min) * 0.08
    y_lo, y_hi = r_min - pad, r_max + pad

    # Pre-compute which point indices are revealed at each frame
    # Frame k reveals all points with t <= t_min + k/N_FRAMES * (t_max - t_min)
    frame_thresholds = np.linspace(t_min, t_max, N_FRAMES)

    # ── Figure setup ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#1f2937")
    for spine in ax.spines.values():
        spine.set_edgecolor("#374151")

    ax.set_xlim(t_min, t_max)
    ax.set_ylim(y_lo, y_hi)
    ax.set_xlabel("Time", color="#d1d5db")
    ax.set_ylabel("Burn Rate (dx/dt)", color="#d1d5db")
    ax.set_title("Regression (Burn) Rate Over Time", color="#f9fafb", fontsize=13, pad=10)
    ax.tick_params(colors="#9ca3af")
    ax.grid(True, color="#374151", linewidth=0.5, linestyle="--")

    # Static horizontal average lines
    if avg_avg is not None:
        ax.axhline(avg_avg, color="#4ade80", linestyle="--", linewidth=1.2,
                   label=f"Avg Burn Rate (Avg X): {avg_avg:.4f}", alpha=0.85)
    if avg_max is not None:
        ax.axhline(avg_max, color="#f87171", linestyle="--", linewidth=1.2,
                   label=f"Avg Burn Rate (Max X): {avg_max:.4f}", alpha=0.85)

    # Artists that will be updated each frame
    scatter_inst, = ax.plot([], [], "o", color="#60a5fa", markersize=3,
                            alpha=0.85, label="Instantaneous Burn Rate", linestyle="None")
    line_ma,      = ax.plot([], [], ".", color="#e2e8f0", markersize=2,
                            linestyle="-", linewidth=1.0,
                            label=f"Moving Avg (win={MOVING_AVG_WIN})")

    # Time cursor (vertical dashed line)
    cursor = ax.axvline(t_min, color="#fbbf24", linewidth=0.8, linestyle=":", alpha=0.6)

    ax.legend(loc="upper right", fontsize=8, framealpha=0.3,
              labelcolor="#d1d5db", facecolor="#1f2937", edgecolor="#374151")

    # ── Animation update ──────────────────────────────────────────────────────
    def update(frame_idx):
        threshold = frame_thresholds[frame_idx]
        mask = times <= threshold
        t_vis = times[mask]
        r_vis = rates[mask]
        ma_vis = rates_ma[mask]

        scatter_inst.set_data(t_vis, r_vis)
        line_ma.set_data(t_vis, ma_vis)
        cursor.set_xdata([threshold, threshold])
        return scatter_inst, line_ma, cursor

    # ── Build & save ──────────────────────────────────────────────────────────
    interval_ms = (GIF_DURATION_SEC * 1000) / N_FRAMES   # ms per frame

    ani = animation.FuncAnimation(
        fig, update,
        frames=N_FRAMES,
        interval=interval_ms,
        blit=True,
    )

    print(f"Saving GIF to '{output_file}' ({N_FRAMES} frames @ {1000/interval_ms:.1f} fps)…")
    ani.save(
        output_file,
        writer="pillow",
        fps=N_FRAMES / GIF_DURATION_SEC,
        dpi=DPI,
    )
    plt.close(fig)
    print("Done.")


if __name__ == "__main__":
    input_path  = sys.argv[1] if len(sys.argv) > 1 else "burn_rates.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_GIF
    make_gif(input_path, output_path)
