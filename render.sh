#!/bin/bash
# render.sh videos/vNN_name.py [low|high] — renders class Video to out/vNN_name.mp4
# Each video gets its own media dir (no shared LaTeX cache races). At most $MAX_RENDERS
# (default 3) renders run at once across all callers; extra calls wait for a free slot.
cd "$(dirname "$0")"
export PATH="$PATH:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.TinyTeX/bin/x86_64-linux"
export PYTHONPATH="$PWD/common:$PYTHONPATH"
f="$1"; q="${2:-high}"; name="$(basename "$f" .py)"
if [ "$q" = low ]; then flags="-ql"; sub=480p15; else flags="-r 1920,1080 --fps 30"; sub=1080p30; fi
mkdir -p locks logs
slot=""
while [ -z "$slot" ]; do
  for i in $(seq 1 "${MAX_RENDERS:-3}"); do
    d="locks/slot$i"
    if mkdir "$d" 2>/dev/null; then echo $$ > "$d/pid"; slot="$d"; break; fi
    # reclaim slots left behind by killed renders
    p=$(cat "$d/pid" 2>/dev/null); [ -n "$p" ] && ! kill -0 "$p" 2>/dev/null && rm -rf "$d"
  done
  [ -z "$slot" ] && sleep 5
done
trap 'rm -rf "$slot"' EXIT
.venv/bin/manim $flags --media_dir "media/$name" -o "$name" "$f" Video > "logs/$name.$q.log" 2>&1
rc=$?
grep -E 'Error|Traceback|Exception|File "/Users.*videos/' "logs/$name.$q.log" | tail -15
src="media/$name/videos/$name/$sub/$name.mp4"
if [ $rc -eq 0 ] && [ "$q" = high ]; then mkdir -p out; cp "$src" "out/$name.mp4"; cp "${src%.mp4}.srt" "out/$name.srt" 2>/dev/null; fi
echo "rc=$rc $src $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src" 2>/dev/null)s"
