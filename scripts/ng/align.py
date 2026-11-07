#!/usr/bin/env python3
"""Match the Spanish recording to the EN timeline.

Usage:
  uv run python scripts/ng/align.py prepare videos/<slug>   # sentences + data/alignment.todo.md
  uv run python scripts/ng/align.py build   videos/<slug>   # data/alignment.json -> data/cutlist.json

prepare  splits both word transcripts into sentences (data/sentences.{en,es}.json) and prints, per EN
         block, its EN sentences next to the ES sentences in the proportional time window (a hint
         only). Claude (in the session) reads it and writes data/alignment.json by MEANING:

           {"blocks": [{"block": 0, "es": [[0, 3]]},            # inclusive ES sentence-id ranges
                       {"block": 1, "es": [[4, 9], [12, 14]]}]}  # sentences 10-11 = retake, dropped

build    validates (monotonic, every block present), trims silences (> 0.6 s between sentences split
         the clip) and writes data/cutlist.json [{block, es_in, es_out}] in output order.

Interviews (data/interviews.json, from /ng-news-guion) are not recorded by the host: prepare cuts
them out of blocks.json as `interview` blocks, which take no ES ranges and keep the EN audio.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

PAD_IN, PAD_OUT, SPLIT_GAP = 0.08, 0.25, 0.6
END = re.compile(r"[.?!…]$")


def words(path: Path):
    raw = json.loads(path.read_text())
    if isinstance(raw, dict):
        raw = raw.get("words") or [w for s in raw.get("segments", []) for w in s.get("words", [])]
    return [{"t": str(w.get("text", w.get("word", ""))).strip(), "s": float(w["start"]), "e": float(w["end"])} for w in raw if str(w.get("text", w.get("word", ""))).strip()]


def sentences(ws):
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        gap = ws[i + 1]["s"] - w["e"] if i + 1 < len(ws) else 9
        if (END.search(w["t"]) and len(cur) >= 3) or gap > 0.9 or len(cur) >= 45:
            out.append({"id": len(out), "start": round(cur[0]["s"], 2), "end": round(cur[-1]["e"], 2), "text": " ".join(x["t"] for x in cur)})
            cur = []
    return out


def quiet_point(y, sr, t, window=0.35):
    """The quietest moment near t: an interview must not start or end on the host's voice."""
    hop = sr // 50
    a = max(0, int((t - window) * sr))
    seg = y[a : int((t + window) * sr)]
    n = len(seg) // hop
    energy = (seg[: n * hop].reshape(n, hop) ** 2).mean(axis=1)
    return round((a + (int(energy.argmin()) + 0.5) * hop) / sr, 3)


def burned_caption_spans(proxy: Path, a: float, b: float):
    """When each burned-in caption is on screen. Whisper often has no words for a second speaker,
    so this is the only timing the interview has."""
    w, h, fps = 182, 30, 30
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{a - 0.5:.3f}", "-t", f"{b - a + 1:.3f}", "-i", str(proxy), "-vf", f"fps={fps},crop=1454:235:146:735,scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        stdout=subprocess.PIPE, check=True,
    ).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    on = (f > 70).mean(axis=(1, 2)) > 0.004
    spans, start = [], None
    for i in range(len(f)):
        changed = i and (np.abs(f[i] - f[i - 1]) > 60).mean() > 0.01
        if start is not None and (not on[i] or changed):
            spans.append((start, i))
            start = None
        if on[i] and start is None:
            start = i
    if start is not None:
        spans.append((start, len(f)))
    spans = [(a - 0.5 + s / fps, a - 0.5 + e / fps) for s, e in spans]
    return [(max(s, a), min(e, b)) for s, e in spans if min(e, b) - max(s, a) > 0.4]


def caption_lines(v: Path, it):
    """ES caption lines of an interview, on the times of the EN burned-in captions."""
    texts = re.split(r"(?<=[.?!])\s+", it["es"].strip())
    spans = burned_caption_spans(v / "assets/en/proxy.mp4", it["en_in"], it["en_out"])
    if len(spans) != len(texts):
        print(f"WARNING: {len(spans)} burned captions for {len(texts)} ES sentences at {it['en_in']}: timing them by length")
        total, at, spans = sum(map(len, texts)), it["en_in"], []
        for t in texts:
            end = at + (it["en_out"] - it["en_in"]) * len(t) / total
            spans.append((at, end))
            at = end
    return [{"start": round(s, 3), "end": round(e, 3), "text": t} for (s, e), t in zip(spans, texts)]


def apply_interviews(v: Path):
    d = v / "data"
    path = d / "interviews.json"
    blocks = json.loads((d / "blocks.json").read_text())
    interviews = json.loads(path.read_text()) if path.exists() else []
    if not interviews or any(b["kind"] == "interview" for b in blocks):
        return
    y, sr = sf.read(v / "assets/audio/en.wav")
    for n, it in enumerate(interviews):
        # the burned-in captions change exactly when the speaker does; en_start/en_end are estimates
        starts = [s for s, _ in burned_caption_spans(v / "assets/en/proxy.mp4", it["en_start"] - 1.2, it["en_end"] + 1.2)]
        closest = lambda t: min(starts, key=lambda s: abs(s - t), default=t)
        a, z = quiet_point(y, sr, closest(it["en_start"]), 0.2), quiet_point(y, sr, closest(it["en_end"]), 0.2)
        it.update(en_in=a, en_out=z)
        it["lines"] = caption_lines(v, it)
        out, placed = [], False
        for b in blocks:
            if b["en_end"] <= a or b["en_start"] >= z:
                out.append(b)
                continue
            if b["en_start"] < a - 0.3:
                out.append({**b, "en_end": a})
            if not placed:
                out.append({"topic": b["topic"], "kind": "interview", "en_start": a, "en_end": z, "interview": n})
                placed = True
            if b["en_end"] > z + 0.3:
                out.append({**b, "en_start": z})
        blocks = out
    blocks = [{**b, "id": i} for i, b in enumerate(blocks)]
    (d / "blocks.json").write_text(json.dumps(blocks, indent=2) + "\n")
    path.write_text(json.dumps(interviews, ensure_ascii=False, indent=1))
    print(f"{len(interviews)} interviews cut out of blocks.json, blocks renumbered")


def prepare(v: Path):
    apply_interviews(v)
    d = v / "data"
    en, es = sentences(words(d / "transcript.en.json")), sentences(words(d / "transcript.es.json"))
    (d / "sentences.en.json").write_text(json.dumps(en, ensure_ascii=False, indent=1))
    (d / "sentences.es.json").write_text(json.dumps(es, ensure_ascii=False, indent=1))
    blocks = json.loads((d / "blocks.json").read_text())
    en_total, es_total = blocks[-1]["en_end"], es[-1]["end"]
    lines = [f"# alignment todo: {len(en)} EN sentences, {len(es)} ES sentences, EN {en_total:.0f}s, ES {es_total:.0f}s\n"]
    for b in blocks:
        lines.append(f"\n## block {b['id']}  topic {b['topic']}  {b['kind']}  EN {b['en_start']}-{b['en_end']}")
        if b["kind"] == "interview":
            lines.append("  ENTREVISTA: audio original, no lleva frases ES. No la pongas en alignment.json")
            continue
        for s in en:
            if b["en_start"] <= (s["start"] + s["end"]) / 2 < b["en_end"]:
                lines.append(f"  EN {s['id']:>3} [{s['start']:6.1f}] {s['text']}")
    lines.append("\n\n# ES sentences\n")
    for s in es:
        lines.append(f"  ES {s['id']:>3} [{s['start']:6.1f}-{s['end']:6.1f}] {s['text']}")
    (d / "alignment.todo.md").write_text("\n".join(lines) + "\n")
    print(f"data/alignment.todo.md written ({len(en)} EN / {len(es)} ES sentences). Now write data/alignment.json.")


def build(v: Path):
    d = v / "data"
    es = json.loads((d / "sentences.es.json").read_text())
    blocks = json.loads((d / "blocks.json").read_text())
    al = json.loads((d / "alignment.json").read_text())["blocks"]
    by_block = {a["block"]: a["es"] for a in al}
    cut, last, used = [], -1, set()
    for b in blocks:
        if b["kind"] == "interview":
            cut.append({"block": b["id"], "interview": b["interview"], "en_in": b["en_start"], "en_out": b["en_end"]})
            continue
        ranges = by_block.get(b["id"])
        if not ranges:
            sys.exit(f"block {b['id']} has no ES ranges in alignment.json")
        for a, z in ranges:
            if a > z or a <= last:
                sys.exit(f"block {b['id']}: range [{a},{z}] is not monotonic (previous end {last})")
            last = z
            seg = es[a : z + 1]
            used.update(range(a, z + 1))
            start = a
            for i in range(a, z):
                if es[i + 1]["start"] - es[i]["end"] > SPLIT_GAP:
                    cut.append(entry(b["id"], es, start, i))
                    start = i + 1
            cut.append(entry(b["id"], es, start, z))
    dropped = [s for s in es if s["id"] not in used]
    (d / "cutlist.json").write_text(json.dumps(cut, indent=1))
    total = sum(c["es_out"] - c["es_in"] for c in cut if "es_in" in c)
    print(f"cutlist.json: {len(cut)} clips, {total:.1f}s of {es[-1]['end']:.1f}s recording")
    for s in dropped:
        print(f"  dropped ES {s['id']} [{s['start']:.1f}] {s['text'][:70]}")


def entry(block, es, a, z):
    prev_end = es[a - 1]["end"] if a > 0 else 0.0
    nxt = es[z + 1]["start"] if z + 1 < len(es) else es[z]["end"] + 1
    es_in = max(es[a]["start"] - PAD_IN, (prev_end + es[a]["start"]) / 2)
    es_out = min(es[z]["end"] + PAD_OUT, (es[z]["end"] + nxt) / 2)
    return {"block": block, "es_in": round(es_in, 3), "es_out": round(es_out, 3)}


if __name__ == "__main__":
    cmd, v = sys.argv[1], Path(sys.argv[2])
    {"prepare": prepare, "build": build}[cmd](v)
