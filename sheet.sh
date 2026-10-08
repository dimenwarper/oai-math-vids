#!/bin/bash
# sheet.sh video.mp4 [interval_s] [start_s] — 4x4 contact sheet of frames -> scratch/<name>_<start>.png
cd "$(dirname "$0")"; mkdir -p scratch
iv="${2:-8}"; ss="${3:-0}"; name="$(basename "$1" .mp4)"
ffmpeg -v error -y -ss "$ss" -i "$1" -vf "fps=1/$iv,scale=480:-1,tile=4x4" -frames:v 1 "scratch/${name}_$ss.png" && echo "scratch/${name}_$ss.png"
