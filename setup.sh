#!/bin/bash
# One-time setup: Python env, LaTeX (TinyTeX, no sudo), and the source papers.
# Needs: uv (https://docs.astral.sh/uv/), ffmpeg, git, curl. Tested on macOS (Apple silicon).
set -e
cd "$(dirname "$0")"

echo "== Python environment"
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt

echo "== LaTeX (TinyTeX in ~/Library/TinyTeX or ~/.TinyTeX; skipped if latex is found)"
if ! command -v latex >/dev/null && [ ! -d "$HOME/Library/TinyTeX" ] && [ ! -d "$HOME/.TinyTeX" ]; then
  curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
fi
export PATH="$PATH:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.TinyTeX/bin/x86_64-linux"
tlmgr install standalone preview doublestroke ms everysel rsfs setspace tipa wasy wasysym xcolor \
  jknapltx relsize ragged2e fundus-calligra microtype physics dvisvgm babel-english mathtools cancel || true

echo "== Source papers (shallow clone of openai/math into repo/)"
[ -d repo ] || git clone --depth 1 https://github.com/openai/math.git repo

echo "Done. Try: ./render.sh videos/v08_thompson_f.py low"
