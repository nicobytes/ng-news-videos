#!/usr/bin/env bash
# Usage: scripts/ng/transcribe.sh videos/<slug>
# faster-whisper large-v3 on the GPU, word timestamps -> data/transcript.{en,es}.json
# Finished transcripts are kept: the EN one comes from /ng-news-guion, before the ES recording exists.
set -euo pipefail
V="$1"; mkdir -p "$V/data" "$V/assets/audio"
if [ ! -f "$V/data/transcript.en.json" ]; then
  ffmpeg -y -v error -i "$V/assets/en/source.mp4" -vn -ac 1 -ar 16000 "$V/assets/audio/en.wav"
  uv run python scripts/ng/transcribe.py "$V/assets/audio/en.wav" en "$V/data/transcript.en.json" 2>&1 | tail -2
fi
if [ -e "$V/assets/es/recording.mp4" ] && [ ! -f "$V/data/transcript.es.json" ]; then
  ffmpeg -y -v error -i "$V/assets/es/recording.mp4" -vn -ac 1 -ar 16000 "$V/assets/audio/es.wav"
  uv run python scripts/ng/transcribe.py "$V/assets/audio/es.wav" es "$V/data/transcript.es.json" 2>&1 | tail -2
  uv run python scripts/ng/fix_terms.py "$V/data/transcript.es.json"
fi
