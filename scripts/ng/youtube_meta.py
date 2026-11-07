#!/usr/bin/env python3
"""YouTube metadata for an edited episode (see the /ng-news-youtube skill).

Usage:
  uv run python scripts/ng/youtube_meta.py prepare videos/<slug>   # inputs for writing the copy
  uv run python scripts/ng/youtube_meta.py build   videos/<slug>   # validate + write youtube.md

prepare  writes data/final_transcript.md: the corrected captions with the timestamps of the EDITED
         video (the ES recording has other times, chapters from it would be wrong). It also looks
         up the EN episode on @ng-news for its links (metadata only, no video download) and saves
         them in data/en.links.txt.
build    reads data/youtube.json, fails on any broken rule and writes youtube.md:
           {"titles": ["...", "...", "..."], "description": "...", "tags": ["..."],
            "chapters": [{"time": "00:00", "title": "..."}], "links": ["https://..."]}
"""
import json
import re
import subprocess
import sys
from pathlib import Path

MAX_CHAPTERS = 10
MIN_CHAPTERS = 3  # YouTube ignores chapters below this
MIN_CHAPTER_GAP = 10  # seconds, YouTube requirement
TITLE_TARGET = 70
TITLE_MAX = 100  # YouTube hard limit
EMOJI = re.compile("[\U0001f300-\U0001faff☀-➿]")


def mmss(s: float) -> str:
    return f"{int(s) // 60:02d}:{int(s) % 60:02d}"


def seconds(t: str) -> int:
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def episode(v: Path) -> str:
    """videos/26-17 -> 26/17"""
    return v.name.replace("-", "/")


def find_en_episode(v: Path):
    """Looks the episode up by number on @ng-news. Failure is not fatal: links stay empty."""
    info = v / "data/en.info.json"
    if info.exists():
        return json.loads(info.read_text())
    ytdlp = ["uv", "run", "yt-dlp", "--no-warnings", "--skip-download"]
    try:
        listing = subprocess.run(
            [*ytdlp, "--flat-playlist", "--playlist-end", "40", "--print", "%(id)s\t%(title)s", "https://www.youtube.com/@ng-news/videos"],
            capture_output=True, text=True, timeout=120, check=True,
        ).stdout
        hit = next((line.split("\t")[0] for line in listing.splitlines() if episode(v) in line), None)
        if not hit:
            return None
        url = f"https://www.youtube.com/watch?v={hit}"
        raw = subprocess.run([*ytdlp, "-J", url], capture_output=True, text=True, timeout=120, check=True).stdout
    except (subprocess.SubprocessError, OSError) as e:
        print(f"WARNING: could not read the EN episode ({type(e).__name__}); add links by hand")
        return None
    d = json.loads(raw)
    keep = {k: d.get(k) for k in ("title", "description", "webpage_url", "tags")}
    info.write_text(json.dumps(keep, ensure_ascii=False, indent=1))
    return keep


def prepare(v: Path):
    d = v / "data"
    tl = json.loads((d / "timeline.json").read_text())
    final = v / f"renders/ng-news-{v.name}-es.mp4"
    if not final.exists():
        print(f"WARNING: {final} does not exist, run this after the final render")
    elif final.stat().st_mtime < (d / "timeline.json").stat().st_mtime:
        print("WARNING: timeline.json is newer than the final render, timestamps may not match it")

    topic_starts = {}
    for e in tl["entries"]:
        topic_starts.setdefault(e["topic"], e["start"])
    marks = sorted(topic_starts.values())[1:]
    lines = [f"# Transcripción final {episode(v)} ({mmss(tl['total'])})", ""]
    for g in tl["captions"]:
        while marks and g[0]["s"] >= marks[0] - 0.5:
            lines.append("--- el panel derecho cambia de tema ---")
            marks.pop(0)
        said = "(entrevista) " if g[0].get("interview") else ""
        lines.append(f"[{mmss(g[0]['s'])}] {said}" + " ".join(w["t"] for w in g).replace("\u00a0", " "))
    (d / "final_transcript.md").write_text("\n".join(lines) + "\n")
    print(f"data/final_transcript.md: {len(tl['captions'])} lines, {mmss(tl['total'])}")

    en = find_en_episode(v)
    links = []
    if en:
        links = list(dict.fromkeys(u.rstrip(".,)") for u in re.findall(r"https?://\S+", en.get("description") or "")))
        print(f"EN episode: {en.get('title')} {en.get('webpage_url')}")
    else:
        print("EN episode not found on @ng-news")
    (d / "en.links.txt").write_text("\n".join(links) + ("\n" if links else ""))
    print(f"data/en.links.txt: {len(links)} links, keep only the news sources")


def build(v: Path):
    y = json.loads((v / "data/youtube.json").read_text())
    tl = json.loads((v / "data/timeline.json").read_text())
    errors, warnings = [], []

    prefix = f"Ng-News en español {episode(v)}: "
    if len(y["titles"]) != 3:
        errors.append(f"expected 3 title options, got {len(y['titles'])}")
    for t in y["titles"]:
        if not t.startswith(prefix) or len(t) == len(prefix):
            errors.append(f'title must start with "{prefix}": {t}')
        if len(t) > TITLE_MAX:
            errors.append(f"title over {TITLE_MAX} chars: {t}")
        elif len(t) > TITLE_TARGET:
            warnings.append(f"title has {len(t)} chars (aim for {TITLE_TARGET}): {t}")
        if EMOJI.search(t):
            errors.append(f"emoji in title: {t}")
        if "  " in t:
            errors.append(f"double space in title: {t}")

    desc = y["description"].strip()
    if not 200 <= len(desc) <= 500:
        errors.append(f"description has {len(desc)} chars, expected 200-500")
    if re.search(r"[*_`#]|\]\(", desc):
        errors.append("description must be plain text, no markdown")

    if not 5 <= len(y["tags"]) <= 10:
        errors.append(f"expected 5-10 tags, got {len(y['tags'])}")

    ch = y["chapters"]
    if not MIN_CHAPTERS <= len(ch) <= MAX_CHAPTERS:
        errors.append(f"expected {MIN_CHAPTERS}-{MAX_CHAPTERS} chapters, got {len(ch)}")
    if not all(re.fullmatch(r"\d{2}:\d{2}", c["time"]) and c["title"].strip() for c in ch):
        errors.append("every chapter needs a MM:SS time and a title")
    else:
        if ch and ch[0]["time"] != "00:00":
            errors.append("first chapter must be 00:00")
        times = [seconds(c["time"]) for c in ch]
        for a, b, c in zip(times, times[1:], ch[1:]):
            if b - a < MIN_CHAPTER_GAP:
                errors.append(f"chapter {c['time']} is under {MIN_CHAPTER_GAP} s after the previous one")
        if times and tl["total"] - times[-1] < MIN_CHAPTER_GAP:
            errors.append(f"last chapter {ch[-1]['time']} lasts under {MIN_CHAPTER_GAP} s (video ends at {mmss(tl['total'])})")
        starts = [g[0]["s"] for g in tl["captions"]]
        for c, t in zip(ch[1:], times[1:]):
            if min(abs(s - t) for s in starts) > 1.5:
                warnings.append(f"chapter {c['time']} does not start on a caption line")

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    text = [desc, "", *[f"{c['time']} {c['title']}" for c in ch]]
    if y.get("links"):
        text += ["", "Links:", *y["links"]]
    body = "\n".join(text)
    md = ["# Títulos", "", *[f"{i}. {t}" for i, t in enumerate(y["titles"], 1)], "", "# Descripción", "", "```text", body, "```", "", "# Tags", "", "```text", ", ".join(y["tags"]), "```", ""]
    (v / "youtube.md").write_text("\n".join(md))
    print(f"youtube.md: 3 titles, {len(desc)} char description, {len(ch)} chapters, {len(y['tags'])} tags, {len(y.get('links', []))} links")


if __name__ == "__main__":
    {"prepare": prepare, "build": build}[sys.argv[1]](Path(sys.argv[2]))
