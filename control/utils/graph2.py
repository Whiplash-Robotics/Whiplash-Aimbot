#!/usr/bin/env python3
"""
Plot signed RPM log(s)
──────────────────────
• Accepts one file or an entire directory of *.txt logs produced by
  serial_rpm_logger.py.
• Supports negative values: y-axis centred on 0; dashed 0-line.
"""

import argparse, glob, os, re
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("input_path", help="file OR folder produced by logger")
    p.add_argument("-o", "--out", default="graphs", help="output folder")
    return p.parse_args()

def read_log(path):
    ts, rpm = [], []
    with open(path) as f:
        for ln in f:
            if ln.startswith("#") or not ln.strip():
                continue
            try:
                t, r = ln.split(",", 1)
                ts.append(float(t))
                rpm.append(float(r))
            except ValueError:
                # skip malformed
                continue
    return ts, rpm

def plot_one(path, out_dir):
    ts, rpm = read_log(path)
    if not ts:
        print(f"⚠ no data in {os.path.basename(path)}")
        return
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(ts, rpm, lw=1.2)
    ax.axhline(0, ls="--", c="grey", lw=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RPM (signed)")
    ax.set_title(os.path.basename(path))
    ymin, ymax = min(rpm), max(rpm)
    # Pad a little so negatives aren't flush to axis
    rng = max(abs(ymin), abs(ymax))
    ax.set_ylim(-rng*1.1, rng*1.1)
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, os.path.splitext(os.path.basename(path))[0] + ".png")
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print("✓", out_png)

def main():
    args = parse_args()
    files = []
    if os.path.isdir(args.input_path):
        files = sorted(glob.glob(os.path.join(args.input_path, "*.txt")))
    elif os.path.isfile(args.input_path):
        files = [args.input_path]
    else:
        print("Input path not found.")
        return

    if not files:
        print("No log files.")
        return

    for f in files:
        plot_one(f, args.out)

if __name__ == "__main__":
    main()
