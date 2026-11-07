#!/usr/bin/env bash
# Usage: scripts/ng/review.sh videos/<slug> [render.mp4]
# Review material for the critique loop (see SKILL.md), in <slug>/renders/review/:
#   draft.mp4        1080p draft render (skipped if a render.mp4 is given)
#   contact.png      one frame every 4 s
#   phone.png        360 px test, one frame every 8 s
#   clips.png        one full frame per clip
#   captions.png     the caption bar once per caption, to proofread every line
#   strips/cut-NN.png  12 frames around each cut
#   checks.json, sync.json  automatic checks (see verify_sync.py)
set -euo pipefail
V="$1"; R="$V/renders/review"; mkdir -p "$R/strips"
rm -f "$R"/strips/*.png
export HYPERFRAMES_EXTRACT_CACHE_DIR="${HYPERFRAMES_EXTRACT_CACHE_DIR:-$HOME/.cache/hf-extract}"
mkdir -p "$HYPERFRAMES_EXTRACT_CACHE_DIR"
D="${2:-$R/draft.mp4}"
if [ -z "${2:-}" ]; then
  ( cd "$V" && pnpm exec hyperframes render -q draft -o renders/review/draft.mp4 ) >"$R/render.log" 2>&1 || { tail -20 "$R/render.log"; exit 1; }
fi

uv run python - "$V" "$D" <<'PY'
import json, math, subprocess, sys
v, d = sys.argv[1:3]; R = f"{v}/renders/review"
tl = json.load(open(f"{v}/data/timeline.json"))
def ff(*a): subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
def sheet(times, vf, cols, out):
    """one frame per timestamp, tiled (select by frame number at 30 fps)"""
    sel = "+".join(f"eq(n\\,{int(t * 30)})" for t in times)
    ff("-i", d, "-vf", f"select='{sel}',{vf},tile={cols}x{math.ceil(len(times) / cols)}", "-fps_mode", "vfr", "-frames:v", "1", out)
total = tl["total"]
sheet([t + 2 for t in range(0, int(total) - 2, 4)], "scale=320:-1", 6, f"{R}/contact.png")
sheet([t + 2 for t in range(0, int(total) - 2, 8)], "scale=360:-1", 5, f"{R}/phone.png")
sheet([e["start"] + e["dur"] / 2 for e in tl["entries"]], "scale=640:-1", 4, f"{R}/clips.png")
sheet([g[-1]["s"] + 0.1 for g in tl["captions"]], "scale=1920:1080,crop=1560:230:90:740,scale=780:-1", 3, f"{R}/captions.png")
for i, e in enumerate(tl["entries"][1:], 1):
    ff("-ss", f"{max(0, e['start'] - 0.2):.2f}", "-i", d, "-vf", "fps=30,scale=320:-1,tile=12x1", "-frames:v", "1", f"{R}/strips/cut-{i:02d}.png")
PY

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$D")
EXPECT=$(python3 -c "import json;print(json.load(open('$V/data/timeline.json'))['total'])")
BLACK=$(ffmpeg -v info -i "$D" -vf "blackdetect=d=0.1:pix_th=0.02" -an -f null - 2>&1 | grep -c black_start || true)
SILENCE=$(ffmpeg -v info -i "$D" -af "silencedetect=n=-45dB:d=0.7" -vn -f null - 2>&1 | grep -c silence_start || true)
LUFS=$(ffmpeg -nostats -i "$D" -vn -af ebur128=framelog=quiet -f null - 2>&1 | awk '/ I:/{v=$2} END{print v}')
printf '{"duration":%s,"expected":%s,"black_segments":%s,"silence_gaps_0.7s":%s,"lufs":%s}\n' "$DUR" "$EXPECT" "$BLACK" "$SILENCE" "$LUFS" | tee "$R/checks.json"
uv run python scripts/ng/verify_sync.py "$V" "$D" || echo "SYNC CHECK FAILED"
echo "review material in $R: read contact, phone, clips, captions and strips/"
