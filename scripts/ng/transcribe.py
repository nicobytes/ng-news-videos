#!/usr/bin/env python3
"""GPU Whisper large-v3 (faster-whisper / CTranslate2) with word timestamps.

Usage: uv run python scripts/ng/transcribe.py <audio.wav> <lang en|es> <out.json>
Output: [{"text": "word", "start": 0.0, "end": 0.4}, ...]
Audio comes from ffmpeg (16 kHz mono wav), see transcribe.sh.
"""
import json
import os
import sys
import time

# CTranslate2 needs the CUDA 12 libs shipped as pip packages (nvidia-cublas-cu12, nvidia-cudnn-cu12)
import nvidia.cublas.lib, nvidia.cudnn.lib  # noqa: E401

os.environ["LD_LIBRARY_PATH"] = ":".join(list(nvidia.cublas.lib.__path__) + list(nvidia.cudnn.lib.__path__) + [os.environ.get("LD_LIBRARY_PATH", "")])
if os.environ.get("_NG_LD") != "1":  # LD_LIBRARY_PATH is read at process start: re-exec once
    os.environ["_NG_LD"] = "1"
    os.execv(sys.executable, [sys.executable] + sys.argv)

from faster_whisper import WhisperModel

audio, lang, out = sys.argv[1:4]
t0 = time.time()
MODEL = os.path.expanduser("~/.cache/ng-news/whisper-large-v3-ct2")  # ct2-transformers-converter --model openai/whisper-large-v3 (see SETUP.md)
model = WhisperModel(MODEL if os.path.isdir(MODEL) else "large-v3", device="cuda", compute_type="float16")
# No hotwords/initial_prompt: tested, they fix a few names but invent others ("1926") and drop phrases.
segments, info = model.transcribe(audio, language=lang, word_timestamps=True, vad_filter=True, beam_size=5, condition_on_previous_text=False)
words = []
for seg in segments:
    for w in seg.words:
        t = w.word.strip()
        if t:
            words.append({"text": t, "start": round(w.start, 3), "end": round(w.end, 3)})
json.dump(words, open(out, "w"), ensure_ascii=False)
print(f"{out}: {len(words)} words, {words[-1]['end']:.1f}s audio in {time.time() - t0:.0f}s")
