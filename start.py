#!/usr/bin/env python3

import subprocess
import time
import sys

if len(sys.argv) != 3:
    print("Usage: python3 start_stream.py <stream_key> <video_file>")
    sys.exit(1)

STREAM_KEY = sys.argv[1]
VIDEO_FILE = sys.argv[2]
STREAM_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

command = [
    "ffmpeg",
    "-re",
    "-stream_loop", "-1",
    "-i", VIDEO_FILE,
    "-c:v", "copy",
    "-c:a", "copy",
    "-f", "flv", STREAM_URL
]

while True:
    try:
        print(f"Starting stream with {VIDEO_FILE} and stream key {STREAM_KEY}...")
        subprocess.run(command, check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e.stderr}")
        print("Restarting stream in 10 seconds...")
        time.sleep(10)
