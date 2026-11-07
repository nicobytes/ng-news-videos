#!/usr/bin/env python3
"""Split the EN episode into blocks (shots) and classify the left panel.

Usage: uv run python scripts/ng/segment_en.py videos/<slug> [--fps 4]

Reads  assets/en/proxy.mp4 (1920x1080)
Writes data/blocks.json  [{id, topic, kind, en_start, en_end}]
       data/review/segment_sheet.png  (one thumbnail per block, for visual confirmation)

topic = run of the right panel with the same title/bullets (pixel-diff on the right rect)
kind  = "presenter" if the left panel looks like the host webcam (closest to the dominant
        left-panel appearance), else "screen". Blocks split on topic change OR kind change.
Thresholds are constants below; confirm the sheet by eye (see SKILL.md step 4).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

# Geometry @1920x1080 (shared/brand/FRAME.md)
LEFT = (110, 174, 750, 422)
RIGHT = (940, 90, 910, 560)

RIGHT_PX = (228, 140)  # downscaled right rect (w, h)
LEFT_PX = (48, 27)
CUT_FPS = 30  # proxy frame rate
CUT_WINDOW = 0.75  # seconds around a sampled boundary to look for the real cut
MIN_BLOCK = 1.5  # seconds; shorter runs merge into the previous block
RIGHT_CHANGE = 0.012  # fraction of right-rect pixels that flip -> topic change
PRESENTER_DIST = 45.0  # mean |diff| vs the host reference frame (0-255)


def frames(video: Path, rect, size, fps, pix_fmt):
    x, y, w, h = rect
    vf = f"fps={fps},crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=area"
    ch = 3 if pix_fmt == "rgb24" else 1
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(video), "-vf", vf, "-f", "rawvideo", "-pix_fmt", pix_fmt, "-"],
        stdout=subprocess.PIPE,
    )
    n = size[0] * size[1] * ch
    out = []
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        out.append(np.frombuffer(buf, np.uint8).reshape(size[1], size[0], ch).astype(np.float32))
    p.wait()
    return np.stack(out)


def exact_cut(video: Path, near: float) -> float:
    """Time of the hard cut closest to `near`: the biggest frame-to-frame jump in both panels."""
    t0 = max(0.0, near - CUT_WINDOW)
    w, h = 96, 54
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{2 * CUT_WINDOW:.3f}", "-i", str(video), "-vf", f"fps={CUT_FPS},crop=1780:600:70:70,scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        stdout=subprocess.PIPE,
        check=True,
    )
    f = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
    jump = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))
    return round(t0 + (int(jump.argmax()) + 1) / CUT_FPS, 3)


def main():
    v = Path(sys.argv[1])
    fps = float(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 4.0
    proxy = v / "assets/en/proxy.mp4"

    right = frames(proxy, RIGHT, RIGHT_PX, fps, "gray")[..., 0]
    left = frames(proxy, LEFT, LEFT_PX, fps, "rgb24")
    n = min(len(right), len(left))
    right, left = right[:n], left[:n]

    # topic runs: right panel text changed between consecutive samples (sustained 2 samples)
    topic = np.zeros(n, int)
    for i in range(1, n):
        flipped = (np.abs(right[i] - right[i - 1]) > 60).mean()
        topic[i] = topic[i - 1] + (1 if flipped > RIGHT_CHANGE else 0)

    # presenter = host webcam. Face found (OpenCV Haar) AND background close to the dominant
    # face-frame appearance. A guest's webcam also has a face but a different background -> screen.
    import cv2

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    big = frames(proxy, LEFT, (LEFT[2] // 2, LEFT[3] // 2), fps, "gray")[:n, ..., 0].astype(np.uint8)
    has_face = np.array([len(cascade.detectMultiScale(f, 1.1, 5, minSize=(48, 48))) > 0 for f in big])
    flat = left.reshape(n, -1)
    cand = np.where(has_face)[0]
    kind = np.array(["screen"] * n, dtype=object)
    if len(cand):
        sample = flat[cand[:: max(1, len(cand) // 120)]]
        d = np.abs(sample[:, None, :] - sample[None, :, :]).mean(axis=2)
        ref = sample[(d < PRESENTER_DIST).sum(axis=1).argmax()]
        dist = np.abs(flat - ref).mean(axis=1)
        kind[has_face & (dist < PRESENTER_DIST)] = "presenter"

    # runs of (topic, kind)
    runs = []
    for i in range(n):
        key = (int(topic[i]), str(kind[i]))
        if runs and runs[-1]["key"] == key:
            runs[-1]["end"] = i + 1
        else:
            runs.append({"key": key, "start": i, "end": i + 1})
    # merge too-short runs into the previous one
    merged = []
    for r in runs:
        if merged and (r["end"] - r["start"]) / fps < MIN_BLOCK:
            merged[-1]["end"] = r["end"]
        else:
            merged.append(r)
    # adjacent runs with the same key after merging
    blocks = []
    for r in merged:
        if blocks and blocks[-1]["key"] == r["key"]:
            blocks[-1]["end"] = r["end"]
        else:
            blocks.append(dict(r))

    out = [
        {"id": i, "topic": b["key"][0], "kind": b["key"][1], "en_start": round(b["start"] / fps, 2), "en_end": round(b["end"] / fps, 2)}
        for i, b in enumerate(blocks)
    ]
    out[-1]["en_end"] = round(n / fps, 2)

    # Sampling at 4 fps leaves a boundary up to 0.25 s off, and the EN host then flashes for a few
    # frames at the cut. The EN uses hard cuts: snap each boundary to the real one, frame-accurate.
    for a, b in zip(out, out[1:]):
        cut = exact_cut(proxy, b["en_start"])
        a["en_end"] = cut
        b["en_start"] = round(cut + 1 / CUT_FPS, 3)

    # a host shot shorter than MIN_BLOCK was merged away: it would stay visible on a screen block
    for b in out:
        if b["kind"] == "screen":
            i0, i1 = int(b["en_start"] * fps) + 1, int(b["en_end"] * fps) - 1
            hits = int((kind[i0:i1] == "presenter").sum())
            if hits:
                print(f"  WARNING block {b['id']}: EN host in {hits / fps:.2f}s of a screen block, check it")

    (v / "data").mkdir(exist_ok=True)
    (v / "data/blocks.json").write_text(json.dumps(out, indent=2) + "\n")

    # visual confirmation sheet: mid-frame of every block
    rev = v / "data/review"
    rev.mkdir(parents=True, exist_ok=True)
    sel = "+".join(f"eq(n\\,{int(round((b['en_start'] + b['en_end']) / 2 * 30))})" for b in out)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(proxy), "-vf", f"select='{sel}',scale=384:-1,tile=5x{(len(out) + 4) // 5}", "-vsync", "vfr", "-frames:v", "1", str(rev / "segment_sheet.png")],
        check=False,
    )
    topics = len({b["topic"] for b in out})
    print(f"{len(out)} blocks, {topics} topics -> data/blocks.json; check data/review/segment_sheet.png")
    for b in out:
        print(f"  #{b['id']:>2} topic {b['topic']:>2} {b['kind']:<9} {b['en_start']:7.2f}-{b['en_end']:7.2f}")


if __name__ == "__main__":
    main()
