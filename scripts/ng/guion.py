#!/usr/bin/env python3
"""Inputs and checks for the script the ES host records (see the /ng-news-guion skill).

Usage:
  uv run python scripts/ng/guion.py prepare videos/<slug>   # EN text per block + interview candidates
  uv run python scripts/ng/guion.py check   videos/<slug>   # validate guion.md, set its duration

prepare  writes data/en_script.md (EN sentences per block) and data/review/en_captions.png (the
         burned-in EN captions, the exact spelling of names). Interview candidates are sentences in
         another voice and speech Whisper skipped. A guest's webcam is not a signal: hosts narrate
         over it.
check    needs guion.md and data/interviews.json ([{"en_start", "en_end", "en", "es"}], [] if none).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import librosa
import numpy as np

from align import sentences, words
from youtube_meta import find_en_episode, mmss

WORDS_PER_SECOND = 2.7  # measured: Ricardo 2.6 (26-17), Nicolás 2.8 (26/11)
LENGTH_RANGE = (0.85, 1.05)  # ES duration vs EN speech; 0.92 on both 26-17 and 26/11
VOICE_DISTANCE = 1.3  # z-distance from the median voice of the episode
VOICE_RUN = 3  # single sentences go over by chance, a different speaker holds it
GAP_SECONDS = 2.0  # between two word starts: no sentence has a real word this long
GAP_SPEECH = 0.5  # share of the gap with sound


def voice_distances(wav: Path, sents):
    y, sr = librosa.load(wav, sr=16000)
    feats = []
    for s in sents:
        seg = y[int(s["start"] * sr) : int(s["end"] * sr)]
        if len(seg) < sr // 2:
            feats.append(None)
            continue
        m = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=20)[1:]
        f0 = librosa.yin(seg, fmin=70, fmax=350, sr=sr)
        feats.append(np.r_[m.mean(1), m.std(1), np.median(f0) / 10])
    known = np.array([f for f in feats if f is not None])
    med, sd = np.median(known, 0), known.std(0) + 1e-6
    return [float(np.sqrt((((f - med) / sd) ** 2).mean())) if f is not None else 0.0 for f in feats]


def other_voice_runs(dist):
    """Indices of the sentences in a run of VOICE_RUN or more over the threshold."""
    flagged, run = set(), []
    for i, d in enumerate([*dist, 0.0]):
        if d > VOICE_DISTANCE:
            run.append(i)
            continue
        if len(run) >= VOICE_RUN:
            flagged.update(run)
        run = []
    return flagged


def untranscribed_speech(wav: Path, ws):
    """Whisper can skip a second speaker and stretch the words around it ("and@328 she@333").
    Returns [(start, end)] where words are seconds apart but the audio is not silent."""
    y, sr = librosa.load(wav, sr=16000)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=512)[0]
    voiced = rms > np.median(rms) * 0.5
    spans = []
    for a, b in zip(ws, ws[1:]):
        if b["s"] - a["s"] < GAP_SECONDS:
            continue
        frames = voiced[int(a["s"] * sr / 512) : int(b["s"] * sr / 512)]
        if frames.size and frames.mean() >= GAP_SPEECH:
            if spans and a["s"] - spans[-1][1] < 1.0:
                spans[-1] = (spans[-1][0], b["s"])
            else:
                spans.append((a["s"], b["s"]))
    return spans


def prepare(v: Path):
    d = v / "data"
    ws = words(d / "transcript.en.json")
    en = sentences(ws)
    blocks = json.loads((d / "blocks.json").read_text())
    other = other_voice_runs(voice_distances(v / "assets/audio/en.wav", en))
    gaps = untranscribed_speech(v / "assets/audio/en.wav", ws)

    lines = [f"# EN {v.name}: {len(en)} sentences, {mmss(en[-1]['end'])}", ""]
    lines += [f"[VOZ SIN TRANSCRIBIR] {mmss(a)}-{mmss(b)}: leer en en_captions.png" for a, b in gaps] + [""]
    for b in blocks:
        lines.append(f"## block {b['id']} topic {b['topic']} {b['kind']} {mmss(b['en_start'])}-{mmss(b['en_end'])}")
        for i, s in enumerate(en):
            if b["en_start"] <= (s["start"] + s["end"]) / 2 < b["en_end"]:
                lines.append(f"{'[OTRA VOZ] ' if i in other else ''}[{mmss(s['start'])}] {s['text']}")
        lines.append("")
    (d / "en_script.md").write_text("\n".join(lines))

    review = d / "review"
    review.mkdir(exist_ok=True)
    rows = -(-int(en[-1]["end"] / 3 + 1) // 3)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(v / "assets/en/proxy.mp4"), "-vf", f"fps=1/3,crop=1560:230:90:740,scale=780:-1,tile=3x{rows}", "-frames:v", "1", str(review / "en_captions.png")],
        check=True,
    )
    print(f"data/en_script.md: {len(blocks)} blocks, {len(en)} sentences; data/review/en_captions.png")
    print(f"interview candidates: {len(other)} sentences, {len(gaps)} untranscribed spans {[f'{mmss(a)}-{mmss(b)}' for a, b in gaps]}")
    info = find_en_episode(v)
    print(f"EN episode: {info.get('title')}" if info else "EN episode metadata not found")


def check(v: Path):
    path = v / "guion.md"
    text = path.read_text()
    interviews = json.loads((v / "data/interviews.json").read_text())
    en = sentences(words(v / "data/transcript.en.json"))
    errors = []

    spoken = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith(("#", ">", "Duración estimada"))]
    n = len(" ".join(spoken).split())
    duration = n / WORDS_PER_SECOND
    host = json.loads((v / "data/episode.json").read_text()).get("host", "")
    if not host:
        errors.append('set "host" in data/episode.json: the person who records this episode')
    elif f"mi nombre es {host} y esto es NG News en español" not in spoken[0]:
        errors.append(f"the script must open with the fixed greeting for {host}")
    if "Hasta luego" not in spoken[-1]:
        errors.append("the script must end with the fixed farewell")
    markers = len(re.findall(r"^> ENTREVISTA", text, re.M))
    if markers != len(interviews):
        errors.append(f"{markers} ENTREVISTA markers in guion.md, {len(interviews)} in data/interviews.json")

    en_speech = en[-1]["end"] - en[0]["start"] - sum(i["en_end"] - i["en_start"] for i in interviews)
    ratio = duration / en_speech
    if not LENGTH_RANGE[0] <= ratio <= LENGTH_RANGE[1]:
        errors.append(f"estimated {mmss(duration)} is {ratio:.0%} of the EN speech ({mmss(en_speech)}), expected {LENGTH_RANGE[0]:.0%}-{LENGTH_RANGE[1]:.0%}")

    line = f"Duración estimada: {mmss(duration)} ({n} palabras)"
    text = re.sub(r"^Duración estimada:.*$", line, text, count=1, flags=re.M)
    if line not in text:
        errors.append("missing the 'Duración estimada:' line")
    path.write_text(text)
    for e in errors:
        print(f"ERROR: {e}")
    print(f"guion.md: {line}, {ratio:.0%} of the EN speech, {markers} interviews")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    {"prepare": prepare, "check": check}[sys.argv[1]](Path(sys.argv[2]))
