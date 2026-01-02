#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: python3 stop_stream.py <stream_key>")
    sys.exit(1)

STREAM_KEY = sys.argv[1]

try:
    result = subprocess.run(["pgrep", "-fa", "ffmpeg"], capture_output=True, text=True)
    processes = result.stdout.strip().split("\n")

    for process in processes:
        if STREAM_KEY in process:
            parts = process.split()
            pid = parts[0]

            # Get the parent PID
            ppid_result = subprocess.run(["ps", "-o", "ppid=", "-p", pid], capture_output=True, text=True)
            ppid = ppid_result.stdout.strip()

            print(f"Killing FFmpeg process PID: {pid}, PPID: {ppid}")
            subprocess.run(["kill", "-9", pid], check=False)
            if ppid:
                subprocess.run(["kill", "-9", ppid], check=False)

except Exception as e:
    print(f"Error stopping stream: {e}")
