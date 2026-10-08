"""Narration for Manim scenes: Kokoro TTS, cached, with word-level bookmarks.

Usage inside a NarratedScene:

    with self.say("We draw {dot}a dot, then {line}a line.") as seg:
        self.play(FadeIn(dot), run_time=seg.until("dot") + 0.5)
        seg.wait_until("line")
        self.play(Create(line))
    # leaving the block waits out whatever narration remains

`{name}` marks a bookmark at the next word. `[word](/ipa/)` sets a pronunciation.
"""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from manim import Scene

CACHE = Path(__file__).resolve().parent.parent / "cache" / "tts"
VOICE = "af_heart"
SPEED = 1.0
SR = 24000
GAP = 0.35  # silence after each segment

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from kokoro import KPipeline

        _pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    return _pipeline


def _parse(raw):
    """Return (tts_text, display_text, {mark: char offset in display_text})."""
    raw = re.sub(r"\s+", " ", raw).strip()
    pieces, pos = [], 0
    for m in re.finditer(r"\{(\w+)\}|\[([^\]]+)\]\((/[^)]*/)\)", raw):
        pieces.append((raw[pos : m.start()],) * 2)
        pieces.append(("MARK", m.group(1)) if m.group(1) else (m.group(2), m.group(0)))
        pos = m.end()
    pieces.append((raw[pos:],) * 2)
    tts, disp, marks, pending = "", "", {}, []
    for d, t in pieces:
        if d == "MARK":
            pending.append(t)
            continue
        if disp.endswith(" ") and d.startswith(" "):
            d, t = d[1:], t[1:]
        if pending and d.strip():
            for k in pending:
                marks[k] = len(disp) + len(d) - len(d.lstrip())
            pending = []
        disp, tts = disp + d, tts + t
    for k in pending:
        marks[k] = len(disp)
    shift = len(disp) - len(disp.lstrip())
    return tts.strip(), disp.strip(), {k: max(0, v - shift) for k, v in marks.items()}


def synth(raw):
    """Synthesize (cached). Returns dict(path, duration, marks{name: t}, sentences[(t0,t1,text)])."""
    tts_text, disp, mark_chars = _parse(raw)
    key = hashlib.sha1(f"{VOICE}|{SPEED}|{raw}".encode()).hexdigest()[:16]
    CACHE.mkdir(parents=True, exist_ok=True)
    wav, meta = CACHE / f"{key}.wav", CACHE / f"{key}.json"
    if wav.exists() and meta.exists():
        return json.loads(meta.read_text())

    import soundfile as sf

    pipe = _get_pipeline()
    audio, tok_times = [], []  # tok_times: (global char start, t_start, t_end)
    t0, search = 0.0, 0
    for r in pipe(tts_text, voice=VOICE, speed=SPEED):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        g = r.graphemes
        base = disp.find(g[: min(20, len(g))], search)
        if base < 0:
            base = search
        p = 0
        for tok in r.tokens or []:
            i = g.find(tok.text, p)
            if i < 0:
                continue
            p = i + len(tok.text)
            if tok.start_ts is not None:
                tok_times.append((base + i, t0 + tok.start_ts, t0 + (tok.end_ts or tok.start_ts)))
        search = base + len(g)
        audio.append(a)
        t0 += len(a) / SR
    audio = np.concatenate(audio) if audio else np.zeros(SR // 2)
    duration = len(audio) / SR
    sf.write(wav, audio, SR)

    def char_to_time(c):
        for cs, ts, _ in tok_times:
            if cs >= c:
                return ts
        return duration * c / max(1, len(disp))

    marks = {k: char_to_time(c) for k, c in mark_chars.items()}
    # sentence-level subtitles
    sentences = []
    for m in re.finditer(r"[^.!?]+[.!?]*\s*", disp):
        s = m.group(0).strip()
        if s:
            sentences.append([char_to_time(m.start()), s])
    subs = []
    for i, (ts, s) in enumerate(sentences):
        te = sentences[i + 1][0] if i + 1 < len(sentences) else duration
        subs.append([ts, max(te, ts + 0.5), s])
    info = dict(path=str(wav), duration=duration, marks=marks, subs=subs)
    meta.write_text(json.dumps(info))
    return info


class Segment:
    def __init__(self, scene, info):
        self.scene, self.info = scene, info
        self.start = scene.renderer.time
        self.duration = info["duration"]

    def elapsed(self):
        return self.scene.renderer.time - self.start

    def remaining(self, min_t=0.1):
        return max(min_t, self.duration - self.elapsed())

    def until(self, mark, min_t=0.1):
        """Seconds from now until the bookmark is spoken."""
        return max(min_t, self.info["marks"][mark] - self.elapsed())

    def wait_until(self, mark):
        dt = self.info["marks"][mark] - self.elapsed()
        if dt > 1e-3:
            self.scene.wait(dt)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if exc[0] is None:
            dt = self.duration - self.elapsed()
            if dt > 1e-3:
                self.scene.wait(dt)
            self.scene.wait(GAP)
        return False


class NarratedScene(Scene):
    def say(self, raw):
        info = synth(raw)
        self.add_sound(info["path"])
        for ts, te, s in info["subs"]:
            self.add_subcaption(s, duration=te - ts, offset=ts)
        return Segment(self, info)
