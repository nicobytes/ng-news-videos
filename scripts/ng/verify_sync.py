#!/usr/bin/env python3
"""Measure caption sync on a rendered video: re-transcribe its audio and compare word times.

Usage: uv run python scripts/ng/verify_sync.py videos/<slug> <render.mp4>
Writes renders/review/sync.json. Fails (exit 1) if the median offset is over 80 ms or fewer than
90 % of the caption words are heard. Run on the render, not on the source: it catches clips placed
at the wrong offset, which the data files alone cannot show.
"""
import difflib
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

v, video = Path(sys.argv[1]), sys.argv[2]
wav = os.path.join(tempfile.mkdtemp(), "render.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
out = wav + ".json"
subprocess.run(["uv", "run", "python", "scripts/ng/transcribe.py", wav, "es", out], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
heard = json.load(open(out))
# interview lines are a translation of what is heard: only the host's words can be compared
caps = [w for g in json.loads((v / "data/timeline.json").read_text())["captions"] for w in g if not w.get("interview")]
norm = lambda t: re.sub(r"[^\w]", "", t).lower()
a, b = [norm(w["t"]) for w in caps], [norm(w["text"]) for w in heard]
pairs = [(caps[m.a + k], heard[m.b + k]) for m in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks() for k in range(m.size)]
offsets = [h["start"] - c["s"] for c, h in pairs]
med = statistics.median(offsets)
res = {
    "caption_words": len(a),
    "matched": len(offsets),
    "matched_pct": round(100 * len(offsets) / len(a), 1),
    "median_offset_ms": round(med * 1000),
    "p95_abs_offset_ms": round(sorted(abs(o) for o in offsets)[int(len(offsets) * 0.95)] * 1000),
    "worst_abs_offset_ms": round(max(abs(o) for o in offsets) * 1000),
    "worst_words": [{"word": c["t"], "at": c["s"], "offset_ms": round((h["start"] - c["s"]) * 1000)} for c, h in sorted(pairs, key=lambda p: -abs(p[1]["start"] - p[0]["s"]))[:5]],
}
(v / "renders/review/sync.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res))
sys.exit(0 if abs(med) <= 0.08 and res["matched_pct"] >= 90 else 1)
