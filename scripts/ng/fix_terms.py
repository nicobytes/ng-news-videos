#!/usr/bin/env python3
"""Fix ASR errors in a word transcript using references/glossary.json (asr_fixes + canonical case).

Usage: uv run python scripts/ng/fix_terms.py data/transcript.es.json
Multi-word phrases are replaced on the first word's slot; the other words are removed (timing kept
from the first/last word). Idempotent.
"""
import json
import re
import sys
from pathlib import Path

G = json.loads((Path(__file__).parents[2] / ".agents/skills/ng-news-es/references/glossary.json").read_text())
path = Path(sys.argv[1])
words = json.loads(path.read_text())
norm = lambda t: re.sub(r"[^\w]", "", t, flags=re.U).lower()
trail = lambda t: re.search(r"[^\w]*$", t).group(0)

fixes = [(k.split(), v) for k, v in {**G["asr_fixes"], **{t: t for t in G["keep_english"] if " " in t}}.items()]
out, i, n = [], 0, 0
while i < len(words):
    hit = None
    for ph, rep in fixes:
        seg = words[i : i + len(ph)]
        if len(seg) == len(ph) and all(norm(w["text"]) == norm(p) for w, p in zip(seg, ph)):
            hit = (len(ph), rep)
            break
    if hit:
        k, rep = hit
        last = words[i + k - 1]
        out.append({"text": rep + trail(last["text"]), "start": words[i]["start"], "end": last["end"]})
        n += rep != " ".join(w["text"] for w in words[i : i + k])
        i += k
    else:
        out.append(words[i])
        i += 1
canon = {norm(t): t for t in G["keep_english"] if " " not in t}
for w in out:
    c = canon.get(norm(w["text"]))
    if c and w["text"].strip(".,;:!?¿¡") != c:
        w["text"] = re.sub(r"^[^\w]*", lambda m: m.group(0), w["text"]).replace(w["text"].strip(".,;:!?¿¡"), c)
        n += 1
path.write_text(json.dumps(out, ensure_ascii=False))
print(f"{path}: {n} term fixes")
