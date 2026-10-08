# Making more videos

The catalogue has 372 result families and 40 have videos. This guide covers how the existing ones were made and how to add more, by hand or with parallel AI coding agents.

## Picking a result

The best candidates are both important and visual. Before starting one:

- **Check the Lean status.** `repo/lean/docs/NNN.md` says exactly which statement is formalized, if any. Prefer formalized results, or be prepared to say clearly what isn't verified.
- **Check that nobody has made one already.** Two results already have independent videos: 158 ([the-plane-needs-six](https://github.com/Th1nhNg0/the-plane-needs-six)) and 268 ([haldane-gap-explainer](https://github.com/yuxuanwang2009/haldane-gap-explainer)).
- **Find the family's papers.** Its entry in `repo/CONTENTS.md` lists them (search for `**NNN.`).

## Anatomy of a video

Each video is one file, `videos/vNN_slug.py`, containing `class Video(NarratedScene)`:

```python
with self.say("We draw {dot}a dot, then {line}a line.") as s:
    self.play(FadeIn(dot), run_time=s.until("dot") + 0.5)
    s.wait_until("line")
    self.play(Create(line))
# leaving the block waits out whatever narration remains
```

- `self.say(...)` synthesizes the narration with Kokoro, a free local text-to-speech model. Results are cached in `cache/tts/`, and subtitles are added automatically.
- `{name}` places a bookmark at the next spoken word, so animations can be timed to it.
- `[Name](/ipa/)` sets a pronunciation, for example `[Erdős](/ˈɛɹdəʃ/)`.
- `common/style.py` holds the palette, `title_card()` and `status_card()`. Every video ends with a status card that states the claim and its Lean status.
- Heavy numerics go in `videos/data/make_vNN.py`, which writes `videos/data/vNN.npz`. Prefer real computed data over decorative pictures.

The usual structure, about 550–750 narrated words (3.5–5 minutes):

1. Title.
2. A hook that shows the problem visually.
3. History, and why it matters.
4. The theorem.
5. The paper's actual proof idea, honestly simplified.
6. The status card.

## The loop

```bash
./render.sh videos/vNN_slug.py low      # ~1 min draft at 480p; errors land in logs/vNN_slug.low.log
./sheet.sh media/vNN_slug/videos/vNN_slug/480p15/vNN_slug.mp4 6 0    # 4x4 contact sheet of frames -> scratch/
./sheet.sh media/vNN_slug/videos/vNN_slug/480p15/vNN_slug.mp4 6 96
./render.sh videos/vNN_slug.py high     # final 1080p30 -> out/vNN_slug.mp4 + .srt
```

Read the contact sheets, fix overlaps, off-screen text and wrong visuals, and re-render until clean. `render.sh` runs at most `MAX_RENDERS` (default 3) renders at a time across the whole machine, and extra calls wait for a free slot. That makes it safe to call from many agents at once. On a 16 GB machine, keep the limit at 3.

## Making videos with parallel agents

Videos v11–v40 were made by six Claude Code subagents working in parallel, five videos each, with a human-in-the-loop session reviewing everything they produced. The full brief each agent received is below. Paste it into your agent of choice and replace the last section with your assignments. Group related topics per agent so background reading is shared.

What it cost for 30 videos (Claude Opus 5.5, October 2026):

| | |
|---|---|
| Tokens | about 2.6M in total (about 87k per video) |
| Wall-clock | about 70 minutes with 6 agents |
| Rendering | local, about 1 minute per video at 1080p |
| Narration | free (local text-to-speech) |

The review step is not optional. In this batch:

- **Unfinished work:** one agent handed back three videos unrendered.
- **Crashes:** two of those three crashed when they were finally rendered.
- **Unchecked claims:** a few historical claims needed checking against the paper.

For each finished batch, check every `formalized=True` card against `repo/lean/docs/NNN.md`, look at frames from every video, and spot-check the most surprising claims in the papers.

### The agent brief

````text
You are making 3Blue1Brown-style explainer videos (Manim CE, narrated) for results in OpenAI's math
catalogue (github.com/openai/math). A working pipeline and finished videos already exist in this repo.
Make the videos assigned at the bottom, end-to-end, matching the existing ones in quality and style.
Work autonomously; don't ask questions.

PROJECT (repo root):
- README.md and docs/making-more.md: pipeline overview. Read them first.
- common/vo.py: NarratedScene + self.say(): Kokoro TTS (cached), {mark} bookmarks, [word](/ipa/) pronunciations.
- common/style.py: palette (BLUE_3B, YELLOW_3B, TEAL_3B, RED_3B, GREEN_3B, ORANGE_3B, PURPLE_3B, GREY_3B),
  title_card(), status_card(), caption_box().
- videos/v08_thompson_f.py and videos/v04_plane_coloring.py: finished examples. Read one fully and copy its
  structure and idioms (title card, then sections each wrapped in `with self.say(...) as s:`, then status card).
- repo/: local clone of openai/math. repo/CONTENTS.md (family -> manuscripts + abstracts),
  repo/preprints/<dir>/*.pdf, repo/lean/docs/NNN.md (exact scope of the Lean formalization; may not exist).
- Read PDFs: `.venv/bin/python pdftxt.py <pdf> <first_page> <last_page> 2>&1 | LC_ALL=C tr -d '\000' | grep -v '^ *$'`
  (0-indexed pages; abstract, intro and proof overview are usually in the first ~6 pages).

PER VIDEO:
1. Research: the family's entry in repo/CONTENTS.md (grep '**NNN.'), the main paper's abstract/intro/proof
   overview, and repo/lean/docs/NNN.md if present. Understand the history, why it matters, the precise
   theorem, and the paper's actual key proof idea.
2. Script (~550-750 narrated words, 3.5-5 min): title -> hook that shows the problem visually -> history /
   why it matters -> the theorem -> the genuine proof idea from the paper (its core mechanism, honestly
   simplified, not generic filler) -> closing status card.
3. ACCURACY IS THE TOP PRIORITY. Every name, date, number and attribution must come from the paper or be
   standard, well-established fact; if unsure, leave it out. Present results as claims from manuscripts
   produced by an OpenAI model, not yet peer reviewed. status_card(lines, formalized, paper): formalized=True
   only if repo/lean/docs/NNN.md covers the main theorem. If it covers only part, or there is no doc, use
   False and say precisely in the narration what is and isn't formalized. Don't claim "first ever" /
   "open since X" unless the paper says so.
4. Code: videos/vNN_slug.py with `class Video(NarratedScene)`. Precompute numerics in
   videos/data/make_vNN.py -> videos/data/vNN.npz (numpy, mpmath, sympy, scipy are installed). Prefer real
   computed visuals (actual curves, actual data) over decorative ones.
5. Draft render: `./render.sh videos/vNN_slug.py low` prints `rc=... <mp4 path> <duration>s`; errors are in
   logs/vNN_slug.low.log. Renders are capped machine-wide and the script waits for a free slot
   automatically. That's expected; don't kill it.
6. Visual QA: `./sheet.sh <mp4 path> 6 0`, then `... 6 96`, `... 6 192` (4x4 contact sheets of frames 6 s
   apart, written to scratch/). Read each PNG. Fix overlapping text/objects, anything off-screen (keep within
   x in [-6.8,6.8], y in [-3.8,3.8]), awkwardly wrapped Tex (wrap long lines in \mbox{...} or split them),
   and any visual that is mathematically wrong. Re-render low and re-check until clean.
7. Final: `./render.sh videos/vNN_slug.py high` copies the result to out/vNN_slug.mp4 (+ .srt).
   Do not hand back until every final render exists in out/.

KNOWN GOTCHAS:
- Inside construct(), never assign local names that shadow Manim rate functions (smooth, linear,
  there_and_back, ...). It causes UnboundLocalError.
- Point clouds (PMobject) can't go in a VGroup (use Group), and always_redraw breaks if the number of points
  changes between frames (swap the submobject in an updater instead).
- Year axes: decimal_number_config={"group_with_commas": False, "num_decimal_places": 0}.
- Every s.wait_until("x") / s.until("x") needs {x} in that segment's text. The `with self.say(...)` block
  auto-waits for leftover audio.
- TTS: write numbers/symbols as words where pronunciation matters ("seven eighths", "n log n", "pi"). Avoid
  abbreviations like "e.g.". For names the voice may mangle, use misaki IPA [Name](/ipa/)
  (A=eɪ, O=oʊ, I=aɪ, W=aʊ, Y=ɔɪ; e.g. [Erdős](/ˈɛɹdəʃ/)).
- Keep font sizes ~28-44 and reuse title_card / status_card for consistency.
- Only create/edit your own files (your videos/vNN_*.py, videos/data/*vNN* files, and their outputs). Do NOT
  modify common/, render.sh, sheet.sh, README.md, other videos, or repo/. Don't install packages, commit,
  push, or publish anything.

REPORT when done (under ~300 words): for each video, give the file, duration, formalized status as shown on
the card, one line on the proof idea presented, and any claim you were unsure about or left out. Mention
unresolved problems.

YOUR VIDEOS:
- vNN_slug.py: family NNN, <title>. <Lean doc or not>. <Any prior-work caveat or visual idea.>
````

## Ideas not yet done

These suit the format: visual, with a crisp statement, and mostly with Lean docs. "Lean doc" means `repo/lean/docs/NNN.md` exists; check its exact scope before writing the status card.

| Family | Result | Lean doc |
|---|---|---|
| 160 | Superexponential van der Waerden numbers | yes |
| 172 | Classification of finite Euclidean Ramsey configurations | yes |
| 173 | Seymour's second-neighborhood conjecture | yes |
| 179 | The circulant Hadamard and Barker-sequence conjectures | yes |
| 181 | The Erdős–Gallai cycle-decomposition conjecture | yes |
| 096 | The Gaussian propeller conjecture | yes |
| 097 | The Euclidean Steinitz–Bergström bound | yes |
| 039 | Nagata's conjecture | yes |
| 266 | Exactly three mutually unbiased bases in dimension six | yes |
| 293 | Hyperinvariant subspaces | yes |
| 354 | The isoperimetric profile of the cubic three-torus | yes |
| 345 | Infinitely many closed geodesics on spheres | no |
| 375 | De Giorgi's conjecture in dimension eight | no |
