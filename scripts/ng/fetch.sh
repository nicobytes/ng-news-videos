#!/usr/bin/env bash
# Usage: scripts/ng/fetch.sh videos/<slug> [en-file.mp4 | youtube-url]
# Links the local sources and derives the media the pipeline uses:
#   assets/en/source.mp4   -> assets/ng-news-<slug>-en.mp4 (original)
#   assets/es/recording.mp4 -> assets/ng-news-<slug>-es.mp4 (original)
#   assets/en/hq.mp4       4K30 H.264 base layer (the source is usually AV1 60 fps), once the ES exists
#   assets/en/proxy.mp4    1080p, analysis only, never on screen
# A YouTube URL is a last resort: it can lose quality.
set -euo pipefail
V="$1"; SRC="${2:-}"; SLUG="$(basename "$V")"
mkdir -p "$V/assets/en" "$V/assets/es" "$V/data"
EN="$V/assets/ng-news-$SLUG-en.mp4"; ES="$V/assets/ng-news-$SLUG-es.mp4"
[ -e "$ES" ] && ln -sfn "../ng-news-$SLUG-es.mp4" "$V/assets/es/recording.mp4"
if [ -e "$EN" ]; then
  ln -sfn "../ng-news-$SLUG-en.mp4" "$V/assets/en/source.mp4"
elif [ -f "$SRC" ]; then
  ln -sfn "$(realpath "$SRC")" "$V/assets/en/source.mp4"
elif [ -n "$SRC" ] && [ ! -e "$V/assets/en/source.mp4" ]; then
  uv run yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b" --merge-output-format mp4 \
    --no-progress --write-info-json -o "$V/assets/en/source.%(ext)s" "$SRC"
  mv "$V/assets/en/source.info.json" "$V/data/en.info.json" 2>/dev/null || true
fi
[ -e "$V/assets/en/source.mp4" ] || { echo "fetch: no EN source, expected $EN" >&2; exit 1; }
# hq.mp4 takes minutes and only the edit needs it: it waits for the ES recording
if [ -e "$V/assets/es/recording.mp4" ] && [ ! -f "$V/assets/en/hq.mp4" ]; then
  ffmpeg -y -v error -i "$V/assets/en/source.mp4" -an -vf "fps=30,format=yuv420p" \
    -c:v libx264 -crf 14 -preset veryfast -g 30 "$V/assets/en/hq.mp4"
fi
if [ ! -f "$V/assets/en/proxy.mp4" ]; then
  ffmpeg -y -v error -i "$V/assets/en/source.mp4" -vf "scale=1920:1080,fps=30" \
    -c:v libx264 -crf 20 -preset veryfast -c:a aac "$V/assets/en/proxy.mp4"
fi
echo "fetch ok: $V/assets/en/"
