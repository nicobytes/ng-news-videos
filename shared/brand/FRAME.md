# NG News frame (1920×1080 coordinates)

Measured from the EN episode (`ref/en-presenter.png`). The composition is authored at 1920×1080 and rendered at 4K with `--resolution 4k`.

The frame, the NEWS logo and the right panel are **not rebuilt**: they are the original pixels of the EN base layer. These rects are the only ones the composition needs:

| Element | Rect (x, y, w, h) | Notes |
|---|---|---|
| **Left panel** | 110, 174, 750×422 | 16:9, ES host on `presenter` blocks, EN pixels on `screen` blocks |
| **Right panel** | 940, 90, 910×560 | EN pixels, stays in English; used by `segment_en.py` to detect topics |
| **`#capbar`** | 72, 700, 1610×308 | Black cover over the burned-in EN captions. Stops before the logo (x ≥ 1686) |
| **ES captions** | 146, 735, 1454×235 | Centered, vertical center y≈853 |

## Left-panel kinds

- `presenter`: webcam of the EN host, replaced by the ES host.
- `screen`: screen recording, web page, repo, image, logo or guest webcam. Kept.

## ES recording

Host on a blurred room background, 3:2 content centered in a 4096×2160 frame with black side bars (content x≈427…3670). Default crop in `compose.mjs`: `{x:559, y:333, w:2594}`, override with `es_crop` in `data/episode.json`.

## Caption palette

White text on black, dim `#8b8b99` before a word is spoken, sweep `#f433de` → `#ef1452` (sampled from the frame gradient), emphasis `#ff4f9e`.
