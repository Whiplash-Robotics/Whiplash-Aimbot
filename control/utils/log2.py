#!/usr/bin/env python3
"""
Serial RPM logger
──────────────────
• Creates a log automatically on the *first* line that parses as “RPM”.
• Stops (and closes the file) on KeyboardInterrupt / SIGINT.
• Expected serial payload: any line containing a floating-point number preceded
  by the token “RPM” (case-insensitive), e.g.  `RPM = -123.45`.
  If your micro prints something else, tweak the REGEX below.
"""

import argparse, datetime as dt, os, re, signal, sys, time
import serial

RPM_REGEX = re.compile(r"rpm\s*[:=]\s*([-+]?\d*\.?\d+)", re.IGNORECASE)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("out_dir", nargs="?", default="logs", help="folder for .txt logs")
    p.add_argument("port",    nargs="?", default="COM3")
    p.add_argument("baud",    nargs="?", type=int, default=115200)
    return p.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    print(f"Opening {args.port} @ {args.baud} …")
    ser = serial.Serial(args.port, args.baud, timeout=None)
    time.sleep(2)                    # allow board reset
    ser.flushInput()

    log_f = None                     # file handle
    start_time = None

    def graceful_exit(signum, _frame):
        print("\nStopping, closing log …")
        try:
            ser.cancel_read()     # ⬅ break the blocking read right now
        except (serial.SerialException, AttributeError):
            pass                  # old PySerial versions don’t have it

        if log_f:
            log_f.write(f"# Stopped {dt.datetime.now()}\n")
            log_f.close()
        ser.close()
        sys.exit(0)

    # Handle Ctrl-C and kill nicely
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    print("Waiting for first RPM line …")

    while True:
        line_raw = ser.readline()
        if not line_raw:
            continue
        line = line_raw.decode(errors="ignore").strip()
        m = RPM_REGEX.search(line)
        if m:
            if not log_f:            # first ever reading → open file
                ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(args.out_dir, f"rpm_{ts}.txt")
                log_f = open(path, "w")
                start_time = time.perf_counter()
                log_f.write(f"# Started {dt.datetime.now()}\n")
                print(f"▶ Logging to {path}")
            elapsed = time.perf_counter() - start_time
            log_f.write(f"{elapsed:.6f},{m.group(1)}\n")  # "seconds,rpm"
            log_f.flush()                                 # minimal risk loss
            print(f"{elapsed:8.3f}s  {m.group(1)} RPM")
        else:
            # ignore non-RPM chatter; optionally print it
            pass

if __name__ == "__main__":
    try:
        main()
    except serial.SerialException as e:
        print("Serial error:", e)
